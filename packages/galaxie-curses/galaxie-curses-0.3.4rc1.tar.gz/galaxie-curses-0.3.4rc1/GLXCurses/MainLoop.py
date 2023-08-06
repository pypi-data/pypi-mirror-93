#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import sys
import GLXCurses
import logging

import threading

lock = threading.Lock()


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class EventList(object):
    def __init__(self):
        self.__buffer = None
        self.buffer = None

        self.debug = True

    @property
    def buffer(self):
        """
        Return the event_buffer list attribute, it lis can be edited or modify as you need

        :return: event buffer
        :rtype: list()
        """
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'buffer' property value must be list type or None")
        if value != self.buffer:
            self.__buffer = value

    def add(self, signal, args):
        """
        Emit a signal, it consist to add the signal structure inside a global event list

        .. code-block:: python

           args = dict(
               'uuid': Widget().get_widget_id()
               'key1': value1
               'key2': value2
           )
           structure = list(
               detailed_signal,
               args
           )

        :param signal: a string containing the signal name
        :param args: additional parameters arg1, arg2
        """

        if self.debug:
            logging.debug(signal + " " + str(args))

        self.buffer.insert(0, [signal, args])

    def pop(self):
        # noinspection PyBroadException
        try:
            if self.buffer:
                return self.buffer.pop()

        except Exception as the_error:
            logging.error(self.__class__.__name__ + ": Error %s" % str(the_error))


# https://developer.gnome.org/glib/stable/glib-The-Main-Event-Loop.html
class MainLoop(object, metaclass=Singleton):
    """
    :Description:

    The MainLoop is something close to a infinity loop with a start() and stop() method
     . Refresh the Application for the first time
     . Start the Loop
     . Wait for a Curses events then dispatch events and signals over Application Children's
     . Refresh the Application if a event or a signal have been detect
     . If MainLoop is stop the Application will close and should be follow by a sys.exit()

    Attributes:
        event_buffer       -- A List, Default Value: list()
        started            -- A Boolean, Default Value: False

    Methods:
        get_event_buffer() -- get the event_buffer attribute
        get_started()      -- get the started attribute
        start()            -- start the mainloop
        stop()             -- stop the mainloop
        emit()             -- emit a signal

    .. warning:: you have to start the mainloop from you application via MainLoop().start()
    """

    def __init__(self, application=None):
        """
        Creates a new MainLoop structure.
        """
        self.__application = None
        self.__event_list = None
        self.__running = None
        self.__glxcurses_support = None

        # First init
        self.application = application
        self.event_list = None
        self.glxcurses_support = None

        self.running = None

        self.debug = True
        self.debug_level = 0

    @property
    def application(self):
        return self.__application

    @application.setter
    def application(self, value):
        if value is None:
            value = GLXCurses.Application()
        if value != self.application:
            self.__application = value

    @property
    def event_list(self):
        return self.__event_list

    @event_list.setter
    def event_list(self, value):
        if value is None:
            value = EventList()
        if value != self.event_list:
            self.__event_list = value

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        """
        Set the is_running attribute

        :param value: False or True
        :type value: Boolean
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'running' property value must be bool type or None")
        if self.running != value:
            self.__running = value

    @property
    def glxcurses_support(self):
        return self.__glxcurses_support

    @glxcurses_support.setter
    def glxcurses_support(self, value):
        """
        Set the glxcurses_support attribute

        :param value: If ``True`` the support for GLXCurses is enable
        :type value: Boolean
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'glxcurses_support' property value must be bool type or None")
        if self.glxcurses_support != value:
            self.__glxcurses_support = value

    def start(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        if self.debug:
            logging.info("Starting " + self.__class__.__name__)
        self.running = True

        # Normally it the first refresh of the application, it can be considered as the first stdscr display.
        # Consider a chance to crash before the start of the loop
        try:
            if hasattr(self.application, "evloop_cmd"):
                self.application.evloop_cmd()
        except Exception:
            self.stop()
            sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
            sys.stdout.flush()
            raise

        # A bit light for notify about we are up and running, but we are really inside the main while(1) loop
        logging.debug(self.__class__.__name__ + ": Started")
        # The loop
        while self.running:
            # Parse user input into a Statement object
            # Start timer
            # Call loop_precmd method
            # Add statement to History
            # Call loop_cmd method
            # Call loop_postcmd method
            # Stop timer and display the elapsed time
            # In Case of Exit
            #   Call methods loop_finalization
            try:
                # Parse input event
                if hasattr(self.application, "evloop_input_event"):
                    self.handle_event(self.application.evloop_input_event())

                if hasattr(self.application, "evloop_precmd"):
                    self.application.evloop_precmd()

                if hasattr(self.application, "evloop_cmd"):
                    self.application.evloop_cmd()

                if hasattr(self.application, "loop_postcmd"):
                    self.application.evloop_postcmd()

            except KeyboardInterrupt:
                # Check is the focused widget is a Editable, because Ctrl + c,  is a Copy to Clipboard action
                if (
                        isinstance(self.application.has_focus, GLXCurses.ChildElement) and
                        isinstance(self.application.has_focus.widget, GLXCurses.Editable)
                ):
                    # Consider as Ctrl + c
                    self.event_list.add("CURSES", 3)
                else:
                    # The user have manually stop operations
                    self.stop()
                    sys.stdout.write("{0}: {1}\n".format("KeyboardInterrupt", sys.exc_info()[2]))
                    sys.stdout.flush()

            except Exception:
                self.stop()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        # Here self.get_started() == False , then the GLXCurse.Mainloop() should be close
        self.stop()

    def stop(self):
        """
        Stops a MainLoop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A MainLoop quit() call will certainly cause the end of you programme
        """
        if self.debug:
            logging.debug(self.__class__.__name__ + ": Stopping")

        self.running = False

        if hasattr(self.application, "evloop_finalization"):
            self.application.evloop_finalization()

    def handle_event(self, event=None):
        # In case that ise ncurses
        if event != -1:
            if event == 409:
                if (
                        hasattr(self.application, "screen") and
                        hasattr(self.application.screen, "get_mouse")
                ):
                    self.event_list.add("MOUSE_EVENT", self.application.screen.get_mouse())
            else:
                self.event_list.add("CURSES", event)

        # Do something with event
        event = self.event_list.pop()
        try:

            if event:
                while event:
                    # If it have event dispatch it
                    if self.debug:
                        logging.debug("{0}: Dispatch {1}: {2} to self.application".format(
                            self.__class__.__name__, event[0], event[1]))

                    # Dispatch to the application
                    if hasattr(self.application, "events_dispatch"):
                        self.application.events_dispatch(event[0], event[1])

                    # Delete the last event inside teh event list
                    event = self.event_list.pop()

        except KeyError as the_error:
            # # Mouse Wheel bug ?
            logging.error(
                "{0}._handle_event(): KeyError:{1} event:{2}".format(
                    self.__class__.__name__, the_error, event
                )
            )
