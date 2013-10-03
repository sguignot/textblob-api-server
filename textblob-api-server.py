from text.blob import TextBlob
from text.blob import Blobber
from text.sentiments import NaiveBayesAnalyzer
from text.np_extractors import ConllExtractor
from text.taggers import NLTKTagger
from textblob_aptagger import PerceptronTagger
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect
import os, psutil

DEV_ENV = bool(os.environ.get('DEV_ENV', False))

class TextBlobFactory:
    def __init__(self):
        # create custom components
        self.naive_bayes_analyzer = NaiveBayesAnalyzer()
        self.conll_extractor = ConllExtractor()
        self.nltk_tagger = NLTKTagger()
        self.perceptron_tagger = PerceptronTagger()
        if DEV_ENV:
            return
        # train all components (default and custom)
        text = 'TextBlob blobs great!'
        default_blob = TextBlob(text)
        default_blob.sentiment
        default_blob.noun_phrases
        default_blob.pos_tags
        custom_blob = TextBlob(text, analyzer=self.naive_bayes_analyzer, np_extractor=self.conll_extractor, pos_tagger=self.nltk_tagger)
        custom_blob.sentiment
        custom_blob.noun_phrases
        custom_blob.pos_tags
        custom2_blob = TextBlob(text, pos_tagger=self.perceptron_tagger)
        custom2_blob.pos_tags

    def create_blob(self, request_json):
        options = {}
        if request_json.get('analyzer') == 'NaiveBayesAnalyzer':
            options['analyzer'] = self.naive_bayes_analyzer
        if request_json.get('np_extractor') == 'ConllExtractor':
            options['np_extractor'] = self.conll_extractor
        if request_json.get('pos_tagger') == 'NLTKTagger':
            options['pos_tagger'] = self.nltk_tagger
        elif request_json.get('pos_tagger') == 'PerceptronTagger':
            options['pos_tagger'] = self.perceptron_tagger
        return TextBlob(request_json['text'], **options)

# human size
def hs(bytes):
    for x in ['bytes','KB','MB','GB']:
        if bytes < 1024.0:
            return "%3.1f%s" % (bytes, x)
        bytes /= 1024.0
    return "%3.1f%s" % (bytes, 'TB')


tb_factory = TextBlobFactory()
app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/textblob/api/sentiment', methods = ['POST'])
def get_sentiment():
    if not request.json or not 'text' in request.json:
        abort(400)
    blob = tb_factory.create_blob(request.json)
    if isinstance(blob.analyzer, NaiveBayesAnalyzer):
        classification, pos_probability, neg_probability = blob.sentiment
        return jsonify( { 'classification': classification, 'pos_probability': pos_probability, 'neg_probability': neg_probability } ), 200
    polarity, subjectivity = blob.sentiment
    return jsonify( { 'polarity': polarity, 'subjectivity': subjectivity } ), 200        

@app.route('/textblob/api/pos_tags', methods = ['POST'])
def get_pos_tags():
    if not request.json or not 'text' in request.json:
        abort(400)
    blob = tb_factory.create_blob(request.json)
    pos_tags = blob.pos_tags
    return jsonify( { 'pos_tags': pos_tags } ), 200

@app.route('/textblob/api/noun_phrases', methods = ['POST'])
def get_noun_phrases():
    if not request.json or not 'text' in request.json:
        abort(400)
    blob = tb_factory.create_blob(request.json)
    noun_phrases = blob.noun_phrases
    return jsonify( { 'noun_phrases': noun_phrases } ), 200

@app.route('/monitor/meminfo', methods = ['GET'])
def get_meminfo():
    process = psutil.Process(os.getpid())
    appmem = process.get_memory_info()
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    meminfo = {
        'app': {
            'percent': "%.1f%%" % process.get_memory_percent(),
            'rss': hs(appmem[0]),
            'vms': hs(appmem[1])
        },
        'vmem': {
            'total': hs(vmem[0]),
            'available': hs(vmem[1]),
            'percent': "{percent}%".format(percent=vmem[2]),
            'used': hs(vmem[3]),
            'free': hs(vmem[4]),
            'active': hs(vmem[5]),
            'inactive': hs(vmem[6]),
            'buffers': hs(vmem[7]),
            'cached': hs(vmem[8])
        },
        'swap': {
            'total': hs(swap[0]),
            'used': hs(swap[1]),
            'free': hs(swap[2]),
            'percent': "{percent}%".format(percent=swap[3]),
            'sin': hs(swap[4]),
            'sout': hs(swap[5])
        }
    }
    return jsonify( { 'meminfo': meminfo } ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEV_ENV)
