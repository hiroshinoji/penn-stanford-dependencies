#!/usr/bin/env python

import sys

def read_conllx(input):
    sentences = []
    sentence = []

    for line in input:
        line = line.strip()
        if line:
            sentence.append(line.split('\t'))
        elif sentence:
            sentences.append(sentence)
            sentence = []
    if sentence:
        sentences.append(sentence)
    return sentences

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "Usage: %s <gold.conll> <guess.conll>" % (sys.argv[0])
        exit(1)

    gold = [line for line in open(sys.argv[1])]
    guess = [line for line in open(sys.argv[2])]

    assert len(gold) == len(guess)

    correct = 0
    total = 0
    for t1, t2 in zip(gold, guess):
        if t1.strip():
            if t1.split('\t')[4] == t2.split('\t')[4]:
                correct += 1
            total += 1
    print "accuracy: %s" % (float(correct) / total)
