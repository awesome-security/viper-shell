from rdpy.protocol.rdp import rdp

class MyRDPFactory(rdp.ServerFactory):

    def buildObserver(self, controller, addr):

        class MyObserver(rdp.RDPServerObserver):

            def onReady(self):
                """
                @summary: Call when server is ready
                to send and receive messages
                """

            def onKeyEventScancode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in scan code format
                @param code: scan code of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventScancode
                """

            def onKeyEventUnicode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in unicode format
                @param code: unicode of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventUnicode
                """

            def onPointerEvent(self, x, y, button, isPressed):
                """
                @summary: Event call on mouse event
                @param x: x position
                @param y: y position
                @param button: 1, 2 or 3 button
                @param isPressed: True if mouse button is pressed
                @see: rdp.RDPServerObserver.onPointerEvent
                """

            def onClose(self):
                """
                @summary: Call when human client close connection
                @see: rdp.RDPServerObserver.onClose
                """

        return MyObserver(controller)

from twisted.internet import reactor
reactor.listenTCP(8083, MyRDPFactory())
reactor.run()
