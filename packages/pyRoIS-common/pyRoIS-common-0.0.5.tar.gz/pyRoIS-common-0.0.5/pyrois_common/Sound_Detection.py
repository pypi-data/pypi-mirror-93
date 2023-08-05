# Sound_Detection.py
#
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Sound_Detection
"""

import sys
import queue
import time
from datetime import datetime
import threading

from pyrois import RoIS_Common, RoIS_HRI

import socketserver
import xmlrpc.server

class ThreadingXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    """ThreadingXMLRPCServer
    """
    pass


class Command(RoIS_Common.Command):
    """Command
    """
    def __init__(self, c):
        self._component = c

    def start(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def stop(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def suspend(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def resume(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status


class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, c):
        self._component = c

    def component_status(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        c_status = self.c_status
        return (status, c_status)


class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()

    def poll_event(self):
        """poll_event
        """
        msg = self.event_queue.get()
        return msg

    def sound_detected(self, timestamp, number):
        """sound_detected
        """
        msg = xmlrpc.client.dumps((timestamp, number), 'sound_detected')
        self.event_queue.put(msg)


class Sound_Detection(Event, Command, Query):
    """Sound_Detection
    """
    def __init__(self, c):
        super().__init__(c)
        self._component = c
        self.c_status = RoIS_Common.Component_Status.READY.value


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(sd):
    """event_dispatch
    """
    sd.sound_detected(datetime.now().isoformat(), 1)
    time.sleep(0.1)
    sd.sound_detected(datetime.now().isoformat(), 1)


def example_sd(port):
    """example_sd
    """
    c = component()
    sd = Sound_Detection(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(sd,))
    t.start()

    # start the XML-RPC server
    server = ThreadingXMLRPCServer(("0.0.0.0", port), logRequests=False)
    server.register_instance(sd)
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.serve_forever()


if __name__ == '__main__':
    example_sd(8007)
