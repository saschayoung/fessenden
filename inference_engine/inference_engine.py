#!/usr/bin/env python

import logging
from operator import itemgetter
import sys
import time


class InferenceEngine(object):
    """
    A forward-chaining rule based inference engine.

    """

    def __init__(self, logfile='rule_engine.log'):
        """
        Initialize members and methods.

        Parameters
        ----------
        logfile : str
            Name of log file for recording logging data/

        Attributes
        ----------
        logfile : str (opt)
            Name of log file.

        Returns
        -------
        None

        Raises
        ------
        None

        """
        logging.basicConfig(filename=logfile, filemode='a', level=logging.DEBUG)
        self.logger = logging.getLogger('InferenceEngine')
        s = "\n\n\n\n\nStart logging: {0}\n---------------------------------------".format(time.asctime())
        self.logger.info(s)
        self.facts = {}
        self.functions = {}
        self.rules = []

    def add_rule(self, name, rule, weight=0):
        """
        Add rule to inference engine.

        This function adds a rule to the inference engine's rule
        set. A rule is a function of the type:

        def rule(args):
            if <test>:
                <result>

        Where `args` is a dictionary that contains the inference engines's
        fact set, accessed via `args['parameter']`; <test> is the logical
        expression to be evaluated; and <result> is the result to be asserted.

        Rules may also implement the `functions` parameter, as in:

        def rule(args, functions):
            if <test>:
                <result>
        
        Where `functions` is a dictionary that contains the inference engine's
        helper functions, any function that will be used during the evaluation
        of a rule, and is accessed via `functions['function_name']()`.

        Paramters
        ---------
        name : str
            Name used to identify rule.
        rule : function
            The rule that is to be added to the inference engine's rule set.
        weight : number
            Value by which to sort the rule set. Lower values are evaluated
            first.

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> ie = InferenceEngine()
        >>> def rule_1(args):
        ...     if args['value1'] == 'spam':
        ...             args['value2'] = 'eggs'
        ...
        >>> ie.add_rule('test_rule', rule_1, 100)
        >>>

        """
        self.rules.append((name, rule, weight))

    def add_function(self, name, function):
        """
        Add function to inference engine.

        This function adds a helper function to the inference engine's function
        set. A helper function is a function used by the rules to get some type of
        information or caluclate some intermediate result.

        Parameters
        ---------
        name : str
            Name used to identify function.
        function : function
            The helper function that is to be added to the inference engine's function
            set.

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> ie = InferenceEngine()
        >>> def fib(n):
        ...     a,b = 1,1
        ...     for i in range(n-1):
        ...         a,b = b,a+b
        ...     return a
        ...
        >>> ie.add_function('fib', fib)

        """
        self.functions[name] = function

    def add_facts(self, facts):
        """
        Add fact to the inference engine

        This function adds facts to the inference engine's
        fact set.

        Parameters
        ----------
        facts : dict
            Dictionary of key value pairs where the key is the fact name
            and the value is any Python-valid object.

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> ie = InferenceEngine()
        >>> facts = {'value1' : 'spam', 'town' : 'Konigsberg'}
        >>> ie.add_facts(facts)
        >>>

        """
        if sys.version_info[0] > 2.7:
            for key, value in facts.items():
                self.facts[key] = value
        else:
            for key, value in facts.iteritems():
                self.facts[key] = value

    def evaluate_rules(self):
        """
        Run inference engine.

        This function evaluates the rules in the inference engine's rule
        set, using the facts in the inference engine's fact set.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> ie = InferenceEngine()
        >>> ie.evaluate_rules()
        >>>

        """
        for (name, rule, _) in sorted(self.rules, key=itemgetter(2)):
            try:
                if rule.func_code.co_argcount == 1:
                    rule(self.facts)
                elif rule.func_code.co_argcount == 2:
                    rule(self.facts, self.functions)
                else:
                    pass
                self.logger.info("Executed rule {0}".format(name))
            except Exception as e:
                self.logger.error("Failed to execute rule {0}".format(name))
                self.logger.error("Exception occurred: {0}".format(e))
            finally:
                self.logger.info("Facts: {0}".format(self.facts))
                

if __name__ == "__main__":
    import doctest
    doctest.testmod()
