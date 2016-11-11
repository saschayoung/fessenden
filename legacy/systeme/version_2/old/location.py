#!/usr/bin/env python

import threading

class Location(threading.Thread):
    """
    Threaded location module.

    """

    def __init__(self, knowledge_base, lock, dev="/dev/hidraw0"):
        """
        Extend thread class for location module.

        Parameters
        ----------
        knowledge_base : object
            Handle to shared knoweldge base.
        lock : object
            File lock for concurrent access to knowledge base.
        dev : str
            Full path of raw device used to read barcodes.

        """
        threading.Thread.__init__(self)

        self.kb = knowledge_base
        self.lock = lock
        self.dev = dev
        
        self.stop_event = threading.Event()

    def _get_location(self):
        """
        Get location.

        This function reads an hidraw data stream from a barcode scanner
        returns the numeric value of the barcode scanned.

        """
        self.hiddev = open(self.dev, "rb")
        barcode = ''
        continue_looping = True
        k = 0

        while continue_looping:
            report = self.hiddev.read(8)
            k += 1
            for i in report:
                j = ord(i)
                if j == 0:
                    continue
                if j == 0x1E:
                    barcode += '1'
                    continue
                elif j == 0x1F:
                    barcode += '2'
                    continue
                elif j == 0x20:
                    barcode += '3'
                    continue
                elif j == 0x21:
                    barcode += '4'
                    continue
                elif j == 0x22:
                    barcode += '5'
                    continue
                elif j == 0x23:
                    barcode += '6'
                    continue
                elif j == 0x24:
                    barcode += '7'
                    continue
                elif j == 0x25:
                    barcode += '8'
                    continue
                elif j == 0x26:
                    barcode += '9'
                    continue
                elif j == 0x27:
                    barcode += '0'
                    continue
                elif j == 0x28:
                    self.hiddev.close()
                    continue_looping = False
                    break
                else:
                    pass
        return int(barcode)
        

    def run(self):
        """
        Run location module.

        """
        while not self.stop_event.isSet():
            location = self._get_location()
            self.lock.acquire()
            # this try/finally may be overkill?
            try: 
                self.kb.current_location = location
            finally:
                self.lock.release()



    def join(self):
        """
        Stop threaded location module.

        """
        self.stop_event.set()
        try:
            self.hiddev.close()
        except Exception as e:
            print e
        threading.Thread.join(self, timeout)
        
