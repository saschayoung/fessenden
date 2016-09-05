#!/usr/bin/env python3

import random
import string
import time

from inference_engine import InferenceEngine

ie = InferenceEngine()

random.seed(42)

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

facts = {}

for i in range(5000):
    key = random_word(random.randint(10, 15))
    value = random_word(random.randint(10, 15))
    facts[key] = value

ie.add_facts(facts)
print("Added the facts")

def function_factory(key, value):
    def rule(args):
        if args[key] == value:
            args[key+'_t'] = value  + '_t'
    return rule

i = 1
for key, value in facts.items():
    ie.add_rule("rule_{0}".format(i), function_factory(key, value))
    i += 1

print("Evaluating the rules")
t0 = time.process_time()
ie.evaluate_rules()
t1 = time.process_time()
print("Done evaluation, elapsed time = {} seconds".format(t1-t0))



# for key, value in ie.facts.items():
#     print("{0} : {1}".format(key, value))