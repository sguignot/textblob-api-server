#!/bin/sh
export TEXTBLOB_VERSION=0.5.2
cd /tmp && git clone https://github.com/sloria/TextBlob.git && cd /tmp/TextBlob && git checkout $TEXTBLOB_VERSION && python download_corpora.py && rm -rf /tmp/TextBlob
