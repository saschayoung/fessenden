#!/usr/bin/env python



def get_barcode(dev = "/dev/hidraw0"):
    """
    Get barcode.

    This function reads an hidraw data stream from a barcode scanner
    returns the numeric value of the barcode scnned.

    Parameters
    ----------
    dev : str, optional
        Full path hidraw device from which to read hidraw data stream.
        Default path is `/dev/hidraw0`.

    Returns
    -------
    barcode : str
        String representation of numerical value of scanned barcode.

    """
    hiddev = open(dev, "rb")
 
    barcode = ''

    continue_looping = True

    k = 0

    while continue_looping:
        report = hiddev.read(8)

        # print "k value: ", k
        k += 1

        for i in report:
            j = ord(i)
            # # print j
            if j == 0:
                # print "j = ", j
                continue

            if j == 0x1E:
                barcode += '1'
                # print "j = ", j
                continue
            elif j == 0x1F:
                barcode += '2'
                # print "j = ", j
                continue
            elif j == 0x20:
                barcode += '3'
                # print "j = ", j
                continue
            elif j == 0x21:
                barcode += '4'
                # print "j = ", j
                continue
            elif j == 0x22:
                barcode += '5'
                # print "j = ", j
                continue
            elif j == 0x23:
                barcode += '6'
                # print "j = ", j
                continue
            elif j == 0x24:
                barcode += '7'
                # print "j = ", j
                continue
            elif j == 0x25:
                barcode += '8'
                # print "j = ", j
                continue
            elif j == 0x26:
                barcode += '9'
                # print "j = ", j
                continue
            elif j == 0x27:
                barcode += '0'
                # print "j = ", j
                continue
            elif j == 0x28:
                # print "j = ", j
                # print barcode
                hiddev.close()
                continue_looping = False
                break
            else:
                pass
                # print "+++ Melon melon melon +++"
                # print "j = ", j
                # hiddev.close()
                # continue_looping = False
                # break

    return barcode
