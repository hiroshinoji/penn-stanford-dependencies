
CORENLP = /Users/noji/Dropbox/tmp/stanford-corenlp-full-2015-12-09
TAGGER_MODEL = edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger
WSJ = /Users/noji/Dropbox/data/penn3/PARSED/MRG/WSJ

SECTIONS_DIR = ./sections

# replace with 1 2 ... 23 if seq is not available
SECTIONS = $(shell seq -w 1 24)
TRAIN = $(shell seq -w 2 21)
DEVEL = 22
TEST = 23

all: gold stanford_tagged no_punc

gold: sections gold/train.conll gold/devel.conll gold/test.conll

define make_collection
	@mkdir -p $1
	cat $2 > $3
endef

## gold data
gold/train.conll: $(TRAIN:%=$(SECTIONS_DIR)/%)
	$(call make_collection, gold, $^, $@)
gold/devel.conll: $(SECTIONS_DIR)/$(DEVEL)
	$(call make_collection, gold, $^, $@)
gold/test.conll: $(SECTIONS_DIR)/$(TEST)
	$(call make_collection, gold, $^, $@)

sections: $(SECTIONS:%=$(SECTIONS_DIR)/%)

$(SECTIONS_DIR)/%:
	@mkdir -p $(SECTIONS_DIR)
	cat $(WSJ)/$*/* > tmp_section_$*.mrg
	java -cp "$(CORENLP)/*" edu.stanford.nlp.trees.GrammaticalStructure \
	-treeFile tmp_section_$*.mrg -conllx -basic -originalDependencies > $@
	rm tmp_section_$*.mrg

## Stanford tagged data
stanford_tagged: \
  stanford_tagged/train.conll stanford_tagged/devel.conll stanford_tagged/test.conll

stanford_tagged/%.conll: gold/%.conll
	mkdir -p stanford_tagged
	python ./script/run_stanford_tagger.py --corenlp $(CORENLP) \
	  --model $(TAGGER_MODEL) < $^ > $@

## No punctuation data
no_punc: $(SECTIONS:%=no_punc/%) \
  no_punc/no_punc_train.conll \
  no_punc/no_punc_devel.conll \
  no_punc/no_punc_test.conll

no_punc/%:
	@mkdir -p no_punc
	python ./script/remove_puncs.py < $(SECTIONS_DIR)/$* > $@

no_punc/no_punc_train.conll: $(TRAIN:%=no_punc/%)
	$(call make_collection, no_punc, $^, $@)
no_punc/no_punc_devel.conll: no_punc/$(DEVEL)
	$(call make_collection, no_punc, $^, $@)
no_punc/no_punc_test.conll: no_punc/$(TEST)
	$(call make_collection, no_punc, $^, $@)

