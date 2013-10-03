#!/bin/sh
export TEXTBLOB_VERSION=0.7.1
cd /tmp && git clone https://github.com/sloria/TextBlob.git && cd /tmp/TextBlob && git checkout $TEXTBLOB_VERSION && python download_corpora.py && rm -rf /tmp/TextBlob && find $HOME/nltk_data -name '*.zip' | xargs rm
