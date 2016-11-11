#!/usr/bin/env python
"""
GPIO creation and control 

Routines in this module

gpio_reset(port)


TODO: handle errors if file is already open or doesn't exist upon closing...


"""

import subprocess


def gpio_reset(port):
    """
    Reset a GPIO port.

    This function resets a GPIO port by using sysfs to unexport it.

    Parameters
    ----------
    port : int
        GPIO port to reset/unexport.

    Examples
    --------
    >>> gpio_reset(138)

    """
    s = "echo " + str(port) + " > /sys/class/gpio/unexport"
    result = subprocess.call(s, shell=True)



class gpio(object):
    """
    Create and manage gpio devices.

    Parameters
    ----------
    obj : class instance
        Default Python class object.

    """

    def __init__(self, port, direction="in", DEBUG=False):
        """
        GPIO class constructor.
       
        This function instantiatea and initialize a GPIO object. GPIO
        access is enabled by sysfs, and controlled using file-like
        interfaces. A GPIO port is enabled with the following
        userspace command:

        ``echo $PORT > /sys/class/gpio/export``

        Parameters
        ----------
        port : int
            GPIO port to be intialized. 
        direction: str, optional
            Direction of GPIO port, either ``in`` (default) or ``out``.
        DEBUG : bool, optional
            Flag to turn on debug message printing .

        Raises
        ------
        ValueError
            If the direction is not either ``in`` (default) or ``out``.

        Examples
        --------
        >>> nint = gpio(157)
        >>> nint.close()
        
        """
        self.DEBUG = DEBUG
        self.port = port
        if direction in ["in", "out"]:
            self.direction = direction
        else:
            if self.DEBUG:
                print "direction needs to be one of ``in`` (default) or ``out``."
                print "current value: ", direction
            raise ValueError

        s = "echo " + str(self.port) + " > /sys/class/gpio/export"
        result = subprocess.call(s, shell=True)
        
        s = "echo " + self.direction + " > /sys/class/gpio/gpio" + str(self.port) + "/direction"
        result = subprocess.call(s, shell=True)
        


    def read(self):
        """
        Read a GPIO value.

        This function reads the value of a GPIO port. This value is accessed via:

        ``/sys/class/gpio$PORT/value``
        
        Returns
        -------
        out : int
            Value of GPIO port. 

        Examples
        --------
        >>> nint = gpio(157)
        >>> i = nint.read()
        >>> nint.close()


        """

        # NB: this has problems, see note above in __init__
        # val = self.f.read()
        # return int(val.strip('\n'))

        s = "cat /sys/class/gpio/gpio" + str(self.port) + "/value"
        result = subprocess.check_output(s, shell=True)
        return int(result.strip('\n'))


    def write(self, value):
        """
        Write a GPIO value.

        This function writes a value to a GPIO port for output. 
        
        Parameters
        ----------
        value : int
            The value to write to the GPIO port for output, either ``0`` or ``1``.

        Raises
        ------
        ValueError
            If the value is not either ``0`` or ``1``.

        Examples
        --------
        >>> tx = gpio(138, "out")
        >>> tx.write(1)
        >>> tx.read()
        1
        >>> tx.write(0)
        >>> tx.read()
        0
        >>> tx.close()

        """

        if value in [0, 1]:
            s = "echo " + str(value) + " > /sys/class/gpio/gpio" + str(self.port) + "/value"
            result = subprocess.call(s, shell=True)
            if self.DEBUG:
                print "result: ", result
            # NB: this has problems, see note above in __init__
            # self.f.write(value)
            # self.f.flush()
        else:
            if self.DEBUG:
                print "value needs to be either ``0`` or ``1``."
                print "current value: ", direction
            raise ValueError








    def close(self):
        """
        Close GPIO port.

        The function closes a GPIO port and performs cleanup: close
        `f`, the file object associated with
        ``/sys/class/gpio$PORT/value``, and unexport the GPIO port
        number in sysfs.
        
        """

        s = "echo " + str(self.port) + " > /sys/class/gpio/unexport"
        result = subprocess.call(s, shell=True)








if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    gpio_reset(138)
    gpio_reset(157)










