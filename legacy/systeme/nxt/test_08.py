#!/usr/bin/env python


import time

from barcode_server import BarcodeServer



class ThreadedTest(object):
    def __init__(self):
        self.scanner = BarcodeServer(self.callback)


    def callback(self, barcode):
        print "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "\n current location: ", barcode
        print "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"

    def run(self):
        self.scanner.start()
        while True:
            print time.time()
            time.sleep(1)



    def shutdown(self):
        self.scanner.join()
        


if __name__=='__main__':
    main = ThreadedTest()
    try:
        main.run()
    except KeyboardInterrupt:
        main.shutdown()
