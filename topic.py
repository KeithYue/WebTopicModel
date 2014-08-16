# coding=utf-8
from db_helper import connect_db
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LsiModel
from datetime import datetime, timedelta
from itertools import tee
from utils import timeit, append_or_extend
import math
import logging
import argparse
import os
import glob

#  config the
parser = argparse.ArgumentParser(description='''
        extract topic from specific documents
''')
parser.add_argument('-d', '--days', help="how many days of documents  before today you want to analyse", type=int, default=1)
parser.add_argument('-s', '--source', help="The source of the doucments, could be blog, news, magazines, support multi sources",  nargs='*', default=['news'])
parser.add_argument('-k', '--keys', help="The keywords you want the documents contain, support multisources", default=[], nargs='*')

# parse the command line
args = parser.parse_args()

class NoDocumentsError(ValueError):
    pass
class NoDictError(ValueError):
    pass

class Dict():
    '''
    the dictionary of the corpus
    '''
    def __init__(self, s_time, e_time, source):
        pass

    @staticmethod
    def build_dict(docs):
        dictionay = Dictionary.from_documents(docs)
        return dictionay

    @staticmethod
    def save_dict(d):
        d.save_as_text('./dict.txt')
        return d

    @staticmethod
    def load_dict():
        return Dictionary.load_from_text('./dict.txt')

    @staticmethod
    def merge(d1, d2):
        return d1.merge_with(d2)


class Documents():
    '''
    the iterator for reading documents from database
    '''
    def __init__(self, s_time, e_time, source_type, keywords, num=-1):
        '''
        s_time: start time
        e_time: end time
        source_type: list of sources
        '''
        db = connect_db()
        if keywords == []:
            self.cursors = [ db[t].find({'timestamp': {'$gte': s_time, '$lte': e_time}}, timeout=True) for t in source_type]
        else:
            self.cursors = [ db[t].find({'timestamp': {'$gte': s_time, '$lte': e_time}, 'tokens': {
                '$all': keywords}}, timeout=True) for t in source_type]

        self.limit = num
        return

    def __iter__(self):
        self.index=0
        return self

    def __next__(self):
        # check whether go out of range
        if self.limit > 0 and self.index >= self.limit:
            for c in self.cursors:
                c.close()
            else:
                raise StopIteration

        for c in self.cursors:
            if c.alive:
                self.index += 1
                return next(c)['tokens'] # each document is represented by tokens

        raise StopIteration

    def __def__(self):
        '''
        close all the cursor
        '''
        for c in self.cursors:
            c.close()

    def count(self):
        '''
        the count of the documents
        '''
        count = 0
        for c in self.cursors:
            count += c.count()
        else:
            return count

def get_corpus(dictionary):
    '''
    given the dictionary, return the corpus format
    '''
    for d in get_document():
        yield dictionary.doc2bow(d)

def update_dict():
    '''
    update the dictionay based on the modified time
    '''
    if 'dict.txt' in glob.glob('dict.txt'):
        # just update the dict
        last_modified_time = datetime.fromtimestamp(os.stat('./dict.txt').st_mtime)
        d = Dict.load_dict()
        d.add_documents(Documents(last_modified_time, datetime.today(), ['blog', 'news'], []))
        return Dict.save_dict(d)
    else:
        logging.error('No dictionary has found, exit...')
        return None

def save_model(model):
    '''
    Given a model, save it to the database
    '''
    db = connect_db()
    for t in model.show_topics(model.num_topics, num_words=100, formatted=False):
        topic = {}
        topic['words'] = []
        topic['period'] ={
                'start_time':START_TIME,
                'end_time': END_TIME
                }
        topic['keys'] = KEYS
        topic['sources'] = SOURCES
        for i in t:
            topic['words'].append({'contribution': i[0], 'token': i[1]})

        db['topics'].insert(topic)
    logging.info('have saved the topics into the database')
    return

def get_topic_number(doc_num):
    '''
    return the topic number based on the doc number
    '''
    a = int(math.sqrt(doc_num))
    if a > 500:
        return 500
    else:
        return a


def build_lsi(docs):
    '''
    build lsi model from beginning
    the documents that needs to extract topics
    '''
    doc_num = docs.count()
    if doc_num == 0:
        raise NoDocumentsError('There is no document to analyse')

    logging.info('There are {} documents'.format(doc_num))

    # copy the iterator
    # build the dictionary
    logging.info('Building the dictionary...')
    dictionary = update_dict()
    if dictionary is None:
        raise NoDictError('There is no dictionary to load')

    logging.info('There are {} unique words in dictionary'.format(len(dictionary.items())))
    corpus = [i for i in get_corpus(dictionary)] # freeze all the corpus
    logging.info('number of corpus {}'.format(len(corpus)))
    logging.info('Construction Completed.')

    # build the tfidf model
    logging.info('Building the tfidf model...')
    tfidf_model = TfidfModel(corpus, normalize=True)
    corpus_tfidf = tfidf_model[corpus]


    logging.info('Construction Completed.')

    # build the lsi model
    logging.info('Building the LSI model...')
    logging.info('Topic number is {}'.format(get_topic_number(doc_num)))
    lsi_model = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=get_topic_number(doc_num))
    corpus_lsi = lsi_model[corpus_tfidf]
    logging.info('Construction Complete.')
    # save the model
    save_model(lsi_model)
    return


def get_document():
    '''
    The factory of document class
    read the config file and return the related Document class
    '''
    return Documents(START_TIME, END_TIME, SOURCES, KEYS, NUM)

@timeit
def test():
    docs = get_document()
    try:
        build_lsi(docs)
    except NoDocumentsError as e:
        logging.error(e)
    except NoDictError as e:
        logging.error(e)
    pass

# assign the command line args to the config
END_TIME =  datetime.today()
START_TIME = END_TIME - timedelta(days=args.days)
SOURCES = args.source
KEYS = args.keys
NUM = 1000000


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('command line:' + repr(args))
    logging.info('start:' + repr(START_TIME))
    logging.info('end:' + repr(END_TIME))
    test()
