import sys, argparse


from twisted.python import log
from twisted.internet.endpoints import serverFromString
# from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import CallOptions, RegisterOptions

class MyPubsubWampSession(ApplicationSession):
    """
    An application component that publishes an event every second.
    """
    def __init__(self, realm = "realm1"):
        ApplicationSession.__init__(self)
        self._realm = realm

    def onConnect(self):
        self.join(self._realm)

    @inlineCallbacks
    def onJoin(self, details):
        counter = 0
        while True:
            self.publish('com.myapp.topic1', counter)
            counter += 1
            yield sleep(1)




class MyRpcWampSession(ApplicationSession):
    """
    Application component that produces progressive results.
    """

    def __init__(self, realm = "realm1"):
        ApplicationSession.__init__(self)
        self._realm = realm


    def onConnect(self):
        self.join(self._realm)


    def onJoin(self, details):

        @inlineCallbacks
        def longop(n, details = None):
            if details.progress:
                for i in range(n):
                    details.progress(i)
                    yield sleep(1)
            else:
                yield sleep(1 * n)
            returnValue(n)

        self.register(longop, 'com.myapp.longop', RegisterOptions(details_arg = 'details'))


parser = argparse.ArgumentParser()

parser.add_argument("-d", "--debug", action="store_true",
                    help = "Enable debug output.")
parser.add_argument("--websocket", type = str, default="tcp:8080",
                    help = 'WebSocket server Twisted endpoint descriptor, e.g. "tcp:8080" or "unix:/tmp/mywebsocket".')
parser.add_argument("--wsurl", type=str, default="ws://localhost:8080/ws",
                    help = 'WebSocket URL (must suit the endpoint), e.g. "ws://localhost:8080/ws".')

parser.add_argument("--session_type", type=str, default="pubsub")

args = parser.parse_args()
if args.debug:
    log.startLogging(sys.stdout)


from autobahn.twisted.choosereactor import install_reactor
reactor = install_reactor()
if args.debug:
    print("Running on reactor{0}".format(reactor))


## create a WAMP router factory
##
from autobahn.wamp.router import RouterFactory
router_factory = RouterFactory()

## create a WAMP router session factory
##
from autobahn.twisted.wamp import RouterSessionFactory
session_factory = RouterSessionFactory(router_factory)

# create and add a WAMP application session to run next to the router
if args.session_type == 'pubsub':
    session_factory.add(MyPubsubWampSession())
elif args.session_type == 'rpc':
    session_factory.add(MyRpcWampSession())
else:
    raise ValueError("Bad Session Type")

## create a WAMP-over-WebSocket transport server factory
##
from autobahn.twisted.websocket import WampWebSocketServerFactory
transport_factory = WampWebSocketServerFactory(session_factory, args.wsurl, debug=args.debug)
transport_factory.setProtocolOptions(failByDrop=False)

## start the WebSocket server from an endpoint
##
server = serverFromString(reactor, args.websocket)
server.listen(transport_factory)


## now enter the Twisted reactor loop
##
reactor.run()
