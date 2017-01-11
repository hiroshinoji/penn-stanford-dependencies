#!/usr/bin/env python

import os, sys, tempfile, subprocess

def read_sentences(input):
    sentences = []
    sentence = []

    for line in input:
        line = line.strip()
        if line == '':
            sentences.append(sentence)
            sentence = []
        else:
            sentence.append(line.split('\t'))
    if sentence:
        sentences.append(sentence)
    return sentences

def remove_puncs(sentence):
    puncs = set([',', '.', ':', '``', '\'\'', '(', ')', '[', ']', '{', '}', '-LRB-', '-RRB-', '-LSB-', '-RSB-', '-LCB-', '-RCB-', '$', '#'])
    i = 0
    while i < len(sentence):
        l = sentence[i]
        pos = l[3]
        if pos in puncs:
            parent = int(l[6])
            if (parent == i + 1): # NOTE that head index is 1-based, while loop is 0-based.
                print l # meaning head = dep; this should never be happen
            sentence = sentence[:i] + sentence[i+1:]
            for j, m in enumerate(sentence):
                d = int(m[6])
                if d == i + 1:
                    d = parent
                    m[6] = str(d)
                assert(d != i + 1)
                if d > i + 1:
                    m[6] = str(int(m[6]) - 1)
                if j >= i:
                    m[0] = str(int(m[0]) - 1)
            i -= 1
        i += 1
    return sentence

def print_sentences(sentences, out):
    for sentence in sentences:
        for line in sentence:
            out.write('\t'.join(line)+'\n')
        out.write('\n')

if __name__ == '__main__':
    sentences = read_sentences(sys.stdin)
    removed = [remove_puncs(s) for s in sentences]
    print_sentences(removed, sys.stdout)
