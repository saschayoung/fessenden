#!/usr/bin/env python

"""
Module: motion_subsystem

Threaded AV motion subsystem
"""

import threading
import time

class MotionSubsystem(threading.Thread):
    """
    Threaded AV motion subsystem.

    Enables threaded operation of motion.

    """

    def __init__(self, knowledge_base, lock, callback):
        """
        Extend threading class.

        Parameters
        ----------
        knowledge_base : object
            Handle to shared knoweldge base.
        lock : object
            File lock for concurrent access to knowledge base.
        callback : object
            Callback to parent (calling) function.

        """

        threading.Thread.__init__(self)

        self.kb = knowledge_base
        self.lock = lock
        self.controller_callback = callback

    def run(self):
        """
        Run the motion subsystem.

        Start the threaded motion subsystem using `MotionSubsystem.start()`.

        """
        i
