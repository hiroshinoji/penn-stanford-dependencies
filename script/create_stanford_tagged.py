#!/usr/bin/env python

INPUT = '/Users/noji/Dropbox/data/penn3/dep/stanford/gold/'
OUTPUT = '/Users/noji/Dropbox/data/penn3/dep/stanford/stanford-tagged/'

import os, sys
import subprocess
import run_stanford_tagger

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

for x in ['train', 'test', 'dev']:
    gold_path = INPUT + '%s.conll' % (x)
    output_path = OUTPUT + '%s.conll' % (x)

    with open(gold_path) as g:
        sys.stderr.write("Tagging %s ...\n" % gold_path)
        sentences = run_stanford_tagger.run(g)

        with open(output_path, 'w') as o:
            run_stanford_tagger.write_conllx(sentences, o)
