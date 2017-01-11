#!/usr/bin/env python

import sys, os, subprocess
import StringIO
import argparse

CORENLP = '/Users/noji/Dropbox/tmp/stanford-corenlp-full-2015-12-09'
# MODEL = 'edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger'
MODEL = 'edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger'

# Can read both conllx and genia formatted files.
def listify_tab_separated_file(input):
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

def run_tagger(raw_sentences, corenlp, model):
    if not corenlp:
        corenlp = CORENLP
    if corenlp[-1] == '/':
        corenlp = corenlp[:-1]
    corenlp = corenlp + '/*'

    if not model:
        model = MODEL

    cmd = 'java -cp %s edu.stanford.nlp.tagger.maxent.MaxentTagger -model %s -outputFormat tsv -sentenceDelimiter newline -tokenize false' % (corenlp, model)

    p = subprocess.Popen(cmd.split(' '),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # sentences = de_penn_tokenize(raw_sentences)
    stdout, stderr = p.communicate(input='\n'.join(raw_sentences))

    return stdout

def read_conllx(input):
    return listify_tab_separated_file(input)

def conll_to_raw(sentences):
    def raw(sentence):
        return ' '.join([t[1] for t in sentence])
    return [raw(sentence) for sentence in sentences]

def modify_tags(sentences, tagger_output):
    tagger_sentences = listify_tab_separated_file(StringIO.StringIO(tagger_output))
    assert len(sentences) == len(tagger_sentences)

    def mod_sentence(sentence, tagger_sentence):
        def mod_tag(t, tag_t):
            guess = tag_t[1]

            u = t[:]
            u[4] = guess
            return u
        return [mod_tag(t, tag_t) for (t, tag_t) in zip(sentence, tagger_sentence)]

    return [mod_sentence(s, tagger_s)
            for (s, tagger_s) in zip(sentences, tagger_sentences)]

def run(input, corenlp=None, model=None):
    sentences = read_conllx(input)
    raw_sentences = conll_to_raw(sentences)

    tagger_output = run_tagger(raw_sentences, corenlp, model)
    mod_sentences = modify_tags(sentences, tagger_output)

    return mod_sentences

def write_conllx(sentences, output):
    for sentence in sentences:
        for token in sentence:
            output.write('\t'.join(token) + '\n')
        output.write('\n')
    output.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run stanford tagger on CoNLL input.')
    parser.add_argument('--corenlp', default=CORENLP, help='Path to corenlp directory')
    parser.add_argument('--model', default=MODEL, help='Model name')

    args = parser.parse_args()

    sentences = run(sys.stdin, args.corenlp, args.model)
    write_conllx(sentences, sys.stdout)
