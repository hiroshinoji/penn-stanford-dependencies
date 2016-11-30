#!/usr/bin/env python

import os, sys, tempfile, subprocess

def read_sentences(input):
    if os.path.isdir(input):
        files = [os.path.join(input, f) for f in os.listdir(input)]
    else:
        files = [input]

    sentences = []
    sentence = []
    
    for f in files:
        with open(f) as fin:
            for line in fin:
                line = line.strip()
                if line == '':
                    sentences.append(sentence)
                    sentence = []
                else:
                    sentence.append(line.split('\t'))
    return sentences

def print_sentences(sentences, output):
    with open(output,'w') as out:
        for sentence in sentences:
            for line in sentence:
                out.write('\t'.join(line)+'\n')
            out.write('\n')

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

input_dir = os.path.dirname(os.path.abspath( __file__ )) + '/../section/'
output_dir = os.path.dirname(os.path.abspath( __file__ )) + '/../no_punc/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
for fn in os.listdir(input_dir):
    sentences = read_sentences(os.path.join(input_dir, fn))
    removed = [remove_puncs(s) for s in sentences]
    print_sentences(removed, os.path.join(output_dir, fn))
