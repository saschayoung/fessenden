#!/usr/bin/env python


class KnowledgeBase(object):
    def __init__(self):
        self.current_location = 0
        self.duration = []


    def get_state(self):
        """
        Get current state of knowledge base.
        
        Returns
        -------
        out : dict
            Dictionary containing names and values of all data currently in
            database.
        """
        return {'current_location' : self.current_location,}



if __name__=='__main__':
    kb = KnowledgeBase()
    state = kb.get_state()
    print state


    
