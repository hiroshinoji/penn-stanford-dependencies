#!/usr/bin/env python

import os, sys, tempfile, subprocess

class_path = '"/Users/noji/Dropbox/tmp/stanford-corenlp-full-2015-12-09/*"'
input_dir = '/Users/noji/Dropbox/data/penn3/PARSED/MRG/WSJ/'
output_dir = os.path.dirname(os.path.abspath( __file__ )) + '/../section/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_corenlp(tree_dir_path, out_path):
    tmp = tempfile.NamedTemporaryFile()
    subprocess.check_call('cat %s/* > %s' % (tree_dir_path, tmp.name), shell=True)
    tmp.seek(0)
    
    subprocess.check_call('java -cp %s edu.stanford.nlp.trees.EnglishGrammaticalStructure \
    -treeFile %s -conllx -basic -originalDependencies > %s' % (class_path, tmp.name, out_path), shell=True)

dirs = os.listdir(input_dir)
for dir_num in dirs:
    if (len(dir_num) == 2):
        print 'processing %s...' % dir_num 
        run_corenlp(os.path.join(input_dir, dir_num), os.path.join(output_dir, dir_num))
        print 'done.'
        
