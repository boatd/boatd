import serial
import time

from boatd import BasePlugin
import boatd.coreplugins.mavlink_common as mv


class MavlinkPlugin(BasePlugin):

    def send_heartbeat(self):
        self.ml.heartbeat_send(
            mv.MAV_TYPE_SURFACE_BOAT,
            mv.MAV_AUTOPILOT_GENERIC,
            mv.MAV_MODE_FLAG_GUIDED_ENABLED,
            0,
            mv.MAV_STATE_ACTIVE,
            3
        )

    def send_position(self, lat, lon):
        self.ml.global_position_int_send(
            int(time.time()),
            int(lat * 1e7),
            int(lon * 1e7),
            25000,
            25000,
            1,1,1,180*100)

        self.ml.gps_raw_int_send(
            int(time.time()*100),
            3,
            int(lat * 1e7),
            int(lon * 1e7),
            25000,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            5
        )

    def send_heading(self, heading):
        heading = heading % 360
        if heading > 180:
            heading = heading - 360

        self.ml.vfr_hud_send(
            0,  # airspeed
            10,  # groundspeed
            heading,  # heading
            100,  # throttle
            0,  # alt
            0  # climb
        )

    def send_param(self, name, value, index):
        self.ml.param_value_send(
            name,
            value,
            mv.MAV_PARAM_TYPE_REAL32,
            len(self.params),
            index
        )

    def send_params(self):
        for param in self.params:
            name, value = param
            self.send_param(name, value, 0)

    def main(self):
        device = self.config.get('device', '/dev/ttyUSB0')
        baud = self.config.get('baud', 115200)

        # FIXME: make serial port name and baud rate configurable
        self.ser = serial.Serial(device, baud, timeout=0.1)
        self.ml = mv.MAVLink(self.ser)

        self.params = [(b'RUDDER', 0.5)]

        i = 0

        while self.running:
            lat, lon = self.boatd.boat.position()
            heading = self.boatd.boat.heading()

            self.send_heartbeat()
            self.send_position(lat, lon)
            self.send_heading(int(heading))

            buf = self.ser.read(18)
            messages = self.ml.parse_buffer(buf)
            if messages:
                for message in messages:
                    name = message.get_type()
                    print(name)
                    if name == 'PARAM_REQUEST_LIST':
                        self.send_params()

            time.sleep(0.01) 


plugin = MavlinkPlugin
