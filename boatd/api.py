from twisted.web.server import Site
from twisted.web.resource import Resource

class Root(Resource):
    def render_GET(self, request):
        return 'sup, boat'

class Boatd(Resource):
    def getChild(self, name, request):
        uri = request.uri
        print uri
        return Root()

root = Boatd()
factory = Site(root)

if __name__ == '__main__':
    from twisted.internet import reactor
    print 'starting on port 6969'

    reactor.listenTCP(6969, factory)
    reactor.run()
