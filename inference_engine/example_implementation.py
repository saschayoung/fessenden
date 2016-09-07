#!/usr/bin/env pypy

import sys

from inference_engine import InferenceEngine

ie = InferenceEngine()


def blah():
    print("This is the function `blah`")


ie.add_function('blah', blah)
    
facts = {'Bobby': 'green',
         'town': 'Konigsberg',
         'baby': 'Agnes'}
ie.add_facts(facts)


def rule_1(args):
    if args['Bobby'] == 'green':
        args['Bobby'] = 'frog'
ie.add_rule('rule_1', rule_1, 100)


def rule_2(args):
    if args['Bobby'] == 'frog':
        args['Bobby'] = 'croaks'
ie.add_rule('rule_2', rule_2, 200)


def rule_3(args):
    if args['town'] == 'Konigsberg':
        args['bridges'] = 7
ie.add_rule('rule_3', rule_3)


def rule_4(args):
    if args['baby'] == 'Agnes':
        args['reaction'] = 'Awwwwww'
ie.add_rule('rule_4', rule_4)


def rule_5(args, functions):
    if args['baby'] == 'Agnes':
        args['mood'] = 'really crabby'
    functions['blah']()
ie.add_rule('rule_5', rule_5)


def rule_6(args, functions):
    if args['coffee'] == 'black':
        args['daddy'] = 'happy'
    functions['blah']()
ie.add_rule('rule_6', rule_6)


ie.evaluate_rules()


if sys.version_info[0] > 2.7:
    for key, value in ie.facts.items():
        print("{0} : {1}".format(key, value))
else:
    for key, value in ie.facts.iteritems():
        ie.facts[key] = value
