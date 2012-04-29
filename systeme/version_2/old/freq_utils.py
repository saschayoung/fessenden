#!/usr/bin/env python
"""
RFM22 frequency calculations

Routines in this module:

fb_select(freq, DEBUG=False)
carrier_freq(freq, DEBUG=False)

"""

__all__ = ['fb_select', 'carrier_freq']


def fb_select(freq, DEBUG=False):
    """
    Determine the Frequency Band and High Band or Low Band.

    Determine the frequency band `fb` and High Band (`hbsel` = 1)
    or Low Band (`hbsel` = 0), as determined by [RFM22] 

    Parameters
    ----------
    freq : float
        Transmit frequency: 240.0e6 <= freq <= 930.0e6.
    DEBUG : bool, optional
        Flag to turn on debug message printing .

    Returns
    -------
    hbsel : int
        High Band (`hbsel` = 1) or Low Band (`hbsel` = 0). 
    fb : int
        Frequncy band, 0 <= `fb` <=23. 

    Raises
    ------
    ValueError
        If `freq` is not: 240.0e6 <= `freq` <= 930.0e6.

    Examples
    --------
    >>> fb_select(434e6)
    (0, 19)

    References
    ----------
    .. [RFM22] Table 12, pg 23, RFM22 Data sheet.

    """

    if freq < 240.0e6 or freq > 930.0e6:
        if DEBUG:
            print "\nError: frequency %f out of range" %(freq,)
            print "240.0e6 <= freq <= 930.0e6\n" 
        raise ValueError

    elif freq >= 240.0e6 and freq <= 479.9e6:
        hbsel = 0

        if freq >= 240.0e6 and freq <= 249.9e6:
            fb = 0

        elif freq >= 250.0e6 and freq <= 259.9e6:
            fb = 1

        elif freq >= 260.0e6 and freq <= 269.9e6:
            fb = 2

        elif freq >= 270.0e6 and freq <= 279.9e6:
            fb = 3

        elif freq >= 280.0e6 and freq <= 289.9e6:
            fb = 4

        elif freq >= 290.0e6 and freq <= 299.9e6:
            fb = 5

        elif freq >= 300.0e6 and freq <= 309.9e6:
            fb = 6

        elif freq >= 310.0e6 and freq <= 319.9e6:
            fb = 7

        elif freq >= 320.0e6 and freq <= 329.9e6:
            fb = 8

        elif freq >= 330.0e6 and freq <= 339.9e6:
            fb = 9

        elif freq >= 340.0e6 and freq <= 349.9e6:
            fb = 10

        elif freq >= 350.0e6 and freq <= 359.9e6:
            fb = 11

        elif freq >= 360.0e6 and freq <= 369.9e6:
            fb = 12

        elif freq >= 370.0e6 and freq <= 379.9e6:
            fb = 13

        elif freq >= 380.0e6 and freq <= 389.9e6:
            fb = 14

        elif freq >= 390.0e6 and freq <= 399.9e6:
            fb = 15

        elif freq >= 400.0e6 and freq <= 409.9e6:
            fb = 16

        elif freq >= 410.0e6 and freq <= 419.9e6:
            fb = 17

        elif freq >= 420.0e6 and freq <= 429.9e6:
            fb = 18

        elif freq >= 430.0e6 and freq <= 439.9e6:
            fb = 19

        elif freq >= 440.0e6 and freq <= 449.9e6:
            fb = 20

        elif freq >= 450.0e6 and freq <= 459.9e6:
            fb = 21

        elif freq >= 460.0e6 and freq <= 469.9e6:
            fb = 22

        else:  # freq >= 470.0e6 and freq <= 479.9e6
            fb = 23

    else:  # freq >= 480.0e6 and freq <= 930.0e6
        hbsel = 1
        
        if freq >= 480.0e6 and freq <= 499.9e6:
            fb = 0

        elif freq >= 500.0e6 and freq <= 519.9e6:
            fb = 1
    
        elif freq >= 520.0e6 and freq <= 539.9e6:
            fb = 2
    
        elif freq >= 540.0e6 and freq <= 559.9e6:
            fb = 3
    
        elif freq >= 560.0e6 and freq <= 579.9e6:
            fb = 4
    
        elif freq >= 580.0e6 and freq <= 599.9e6:
            fb = 5
    
        elif freq >= 600.0e6 and freq <= 619.9e6:
            fb = 6
    
        elif freq >= 620.0e6 and freq <= 639.9e6:
            fb = 7
    
        elif freq >= 640.0e6 and freq <= 659.9e6:
            fb = 8
    
        elif freq >= 660.0e6 and freq <= 679.9e6:
            fb = 9
    
        elif freq >= 680.0e6 and freq <= 699.9e6:
            fb = 10
    
        elif freq >= 700.0e6 and freq <= 719.9e6:
            fb = 11
    
        elif freq >= 720.0e6 and freq <= 739.9e6:
            fb = 12
    
        elif freq >= 740.0e6 and freq <= 759.9e6:
            fb = 13
    
        elif freq >= 760.0e6 and freq <= 779.9e6:
            fb = 14
    
        elif freq >= 780.0e6 and freq <= 799.9e6:
            fb = 15
    
        elif freq >= 800.0e6 and freq <= 819.9e6:
            fb = 16
    
        elif freq >= 820.0e6 and freq <= 839.9e6:
            fb = 17
    
        elif freq >= 840.0e6 and freq <= 859.9e6:
            fb = 18
    
        elif freq >= 860.0e6 and freq <= 879.9e6:
            fb = 19
        
        elif freq >= 880.0e6 and freq <= 899.9e6:
            fb = 20
    
        elif freq >= 900.0e6 and freq <= 919.9e6:
            fb = 21
    
        else:  # freq >= 920.0e6 and freq <= 930e6
            fb = 22
    
    return hbsel, fb




def carrier_freq(freq, DEBUG=False):
    """
    Determine the carrier frequency. 

    Determine the carrier frequency register value `fc` corresponding to the
    desired transmit frequency `freq`. See [RFM22]

    Parameters
    ----------
    freq : float
        Transmit frequency, should be 240.0e6 <= freq <= 930.0e6.
        NB: Does this mean that it should be exceptions/errors should
        be handled here too?

    DEBUG : bool, optional
        Flag to turn on debug message printing .

    Returns
    -------
    fc : int
        Carrier frequency register value used in registers 0x76 (fc[15:8])
        and 0x77 (fc[7:0])
    hbsel : int
        High Band (`hbsel` = 1) or Low Band (`hbsel` = 0). 
    fb : int
        Frequncy band, 0 <= `fb` <=23.

    Examples
    --------
    >>> carrier_freq(434e6, DEBUG=False)
    (25600, 0, 19)

    References
    ----------
    .. [RFM22] RFM22 Data sheet, pg 22.

    """
   
    hbsel, fb = fb_select(freq)

    fc = int(round(((freq / (10e6 *(hbsel+1))) - fb - 24) * 64000.0))
    
    if DEBUG:
        print "hbsel: 0x%s" %('{0:02x}'.format(hbsel),)
        print "fb: 0x%s" %('{0:02x}'.format(fb),)
        print "fc: 0x%s" %('{0:04x}'.format(fc),)

    return fc, hbsel, fb



if __name__ == '__main__':

    import doctest
    doctest.testmod()

    # freq = 434e6
    # fc, hbsel, fb = carrier_freq(freq)

    
