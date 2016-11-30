#!/bin/sh

for i in `seq -w 2 21`; do cat no_punc/$i; done >| no_punc.train
cp no_punc/22 no_punc.devel
