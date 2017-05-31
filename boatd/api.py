# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from six.moves.socketserver import ThreadingMixIn

import json

import tornado.ioloop
import tornado.web

from . import exceptions

# reported api version
VERSION = 1.3

log = logging.getLogger(__name__)


def get_wind_dict(boat):
    try:
        speed = boat.wind_speed()
    except (AttributeError, TypeError):
        speed = -1

    try:
        return {'apparent': boat.wind_apparent(),
                'absolute': boat.wind_absolute(),
                'speed': speed}
    except AttributeError:
        log.exception('Error when attempting to read wind direction')
        raise


class BoatdHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'boatd': {'version': VERSION}}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = {}
        if data.get('quit'):
            # FIXME: doesn't actually quit the server
            self.running = False
            response['quit'] = True

        self.write(response)


class BoatHandler(tornado.web.RequestHandler):
    def initialize(self, boat):
        self.boat = boat

    def get(self):
        response = {
            'heading': self.boat.heading(),
            'wind': get_wind_dict(self.boat),
            'position': self.boat.position(),
            'active': self.boat.active,
            'rudder_angle': self.boat.target_rudder_angle,
            'sail_angle': self.boat.target_sail_angle,
        }
        self.write(response)


class BehaviourHandler(tornado.web.RequestHandler):
    def initialize(self, behaviour_manager):
        self.behaviour_manager = behaviour_manager

    def behaviours(self):
        b = {
                behaviour.name: {
                    'running': behaviour.running,
                    'filename': behaviour.filename
                }
                for behaviour in
                self.behaviour_manager.behaviours
        }

        response = {
            'behaviours': b,
            'active': self.behaviour_manager.active_behaviour
        }
        return response

    def get(self):
        self.write(self.behaviours())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        if 'active' in data:
            behaviour = data.get('active')
            self.behaviour_manager.stop()
            if behaviour is not None:
                self.behaviour_manager.start_behaviour_by_name(behaviour)

        self.write(self.behaviours())


class RudderHandler(tornado.web.RequestHandler):
    def initialize(self, boat):
        self.boat = boat

    def get(self):
        response = {'value': self.boat.target_rudder_angle}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        value = data.get('value')
        if value:
            self.boat.rudder(value)

        self.write({'value': value})


class SailHandler(tornado.web.RequestHandler):
    def initialize(self, boat):
        self.boat = boat

    def get(self):
        response = {'value': self.boat.target_sail_angle}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        value = data.get('value')
        if value:
            self.boat.sail(value)

        self.write({'value': value})


class WindHandler(tornado.web.RequestHandler):
    def initialize(self, boat):
        self.boat = boat

    def get(self):
        response = get_wind_dict(self.boat)
        self.write(response)


class BoatdAPI(object):
    def __init__(self, boat, behaviour_manager, waypoint_manager,
                 server_address):
        log.info('boatd api listening on %s:%s', *server_address)

        self.boat = boat
        self.behaviour_manager = behaviour_manager
        self.waypoint_manager = waypoint_manager
        self.running = True

        self.app = tornado.web.Application([
            (r'/', BoatdHandler),

            (r'/boat', BoatHandler,
                {'boat': self.boat}),

            (r'/rudder', RudderHandler,
                {'boat': self.boat}),

            (r'/sail', SailHandler,
                {'boat': self.boat}),

            (r'/wind', WindHandler,
                {'boat': self.boat}),

            (r'/behaviours', BehaviourHandler,
                {'behaviour_manager': self.behaviour_manager}),
        ])

    def run(self):
        self.app.listen(2222)
        tornado.ioloop.IOLoop.instance().start()


def get_deep_attr(obj, path):
    if len(path) > 1:
        attr, path = path[0], path[1:]
        return get_deep_attr(getattr(obj, attr), path)
    else:
        return getattr(obj, path[0])


class BoatdHTTPServer(ThreadingMixIn, HTTPServer):
    '''
    The main REST server for boatd. Listens for requests on port server_address
    and handles each request with RequestHandlerClass.
    '''
    def __init__(self, boat, behaviour_manager, waypoint_manager,
                 server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass,
                            bind_and_activate)
        log.info('boatd api listening on %s:%s', *server_address)

        self.boat = boat
        self.behaviour_manager = behaviour_manager
        self.waypoint_manager = waypoint_manager
        self.running = True

        # set API endpoints for GETs
        self.handles = {
            '/': self.boatd_info,
            '/boat': self.boat_attr,
            '/wind': self.wind,
            '/active': self.boat_active,
            '/behaviours': self.behaviours,
            '/waypoints': self.waypoints,
        }

        # set API endpoints for POSTs
        self.post_handles = {
            '/': self.boatd_post,
            '/behaviours': self.behaviours_post,
            '/waypoints': self.waypoints_post,
        }

    def waypoints(self):
        return {
            'waypoints': self.waypoint_manager.waypoints,
            'home': self.waypoint_manager.home_position,
            'current': self.waypoint_manager.current,
        }

    def waypoints_post(self, content):
        waypoints = content.get('waypoints', None)

        try:
            self.waypoint_manager.add_waypoints(waypoints)
        except exceptions.WaypointMalformedError:
            return {'error': 'bad waypoint values'}

        return self.waypoints()

    def behaviours(self):
        b = {
                behaviour.name: {
                    'running': behaviour.running,
                    'filename': behaviour.filename
                }
                for behaviour in
                self.behaviour_manager.behaviours
        }

        return {
            'behaviours': b,
            'active': self.behaviour_manager.active_behaviour
        }



    def boat_active(self):
        return {'value': self.boat.active}

    def boatd_post(self, content):
        # posting only supports shutting down the server and quitting boatd
        response = {}
        if 'quit' in content:
            if content.get('quit'):
                self.running = False
                response['quit'] = True

        return response

    def boat_post_function(self, name, content):
        f = self.post_handles.get(name)
        if f is not None:
            return f(content)
        else:
            return self.driver_function(name, args=[content['value']])

    def boat_function(self, function_string):
        '''Return the encoded json response from an endpoint string.'''
        json_content = self.handles.get(function_string)()
        return json_content

    def driver_function(self, function_string, args=None):
        '''
        Return the json response from the string describing the path to the
        attribute.
        '''
        if args is None:
            args = []

        obj_path = [p for p in function_string.split('/') if p]
        attr = get_deep_attr(self.boat, obj_path)
        if callable(attr):
            json_content = {"result": attr(*args)}
        else:
            raise AttributeError
        return json_content


class BoatdRequestHandler(BaseHTTPRequestHandler):
    '''
    Handle a single HTTP request. Returns JSON content using data from the rest
    of boatd.
    '''
    server_version = 'boatd/{}'.format(VERSION)

    def send_json(self, content, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content.encode())

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server.'''
        if self.path in self.server.handles:
            # get the function that self.server.handles maps to this path
            handler_func = self.server.boat_function
        else:
            # try handling by poking the driver with a stick
            handler_func = self.server.driver_function

        try:
            func_response = handler_func(self.path)
            code = 200
        except AttributeError:
            log.exception('could not find attribute')
            func_response = "404 - attribute not found"
            code = 404

        if func_response is not None:
            self.send_json(json.dumps(func_response), code)
        else:
            # if the handler runs, but doesn't return anything, 404
            self.send_json("404", code)

    def do_POST(self):
        '''Handle a POST request to the server.'''
        length = int(self.headers.get('content-length'))
        post_body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(post_body)
        except ValueError:
            log.error('Can\'t decode {}'.format(post_body))
            self.send_json("400 - bad json syntax", 400)
        else:
            response_data = self.server.boat_post_function(self.path, data)
            self.send_json(json.dumps(response_data))

    def log_request(self, code='-', size='-'):
        '''Log the request stdout.'''
        log.debug('{} requested'.format(self.path))
