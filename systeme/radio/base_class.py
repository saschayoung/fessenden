#!/usr/bin/env python

"""
Base classes/templates.

"""


class RadioBaseClass(object):
    """
    Radio base class.

    """

    def __init__(self):
        """
        RadioBaseClass constructor.

        This function should be overridden in a subclas.

        Raises
        ------
        NotImplementedError
            If not overridden in subclass.

        """
        
        raise NotImplementedError("RadioBaseClass.__init__() must be overridden")

    
    
