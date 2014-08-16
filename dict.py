# coding=utf-8
from db_helper import connect_db
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LsiModel
from datetime import datetime
from itertools import tee
import logging

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

class Documents():
    '''
    the iterator for reading documents from database
    '''
    def __init__(self, s_time, e_time, source_type, num=-1):
        '''
        s_time: start time
        e_time: end time
        source_type: list of sources
        '''
        db = connect_db()
        self.cursors = [ db[t].find({'timestamp': {'$gte': s_time, '$lte': e_time}}) for t in source_type]
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
                return next(c)['tokens']

        raise StopIteration

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
    for d in Documents(START_TIME, END_TIME, SOURCES, NUM):
        yield dictionary.doc2bow(d)

def build_lsi(docs):
    '''
    build lsi model from beginning
    the documents that needs to extract topics
    '''
    logging.info('There are {} documents'.format(docs.count()))
    # copy the iterator
    # build the dictionary
    logging.info('Building the dictionary...')
    dictionary = Dict.build_dict(docs)
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
    lsi_model = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
    corpus_lsi = lsi_model[corpus_tfidf]
    logging.info('Construction Complete.')

    lsi_model.show_topics()
    return

def test():
    docs = Documents(START_TIME, END_TIME, SOURCES, NUM)
    build_lsi(docs)

# the config part
START_TIME = datetime(2014,7,1)
END_TIME =  datetime(2014,7,15)
SOURCES = ['news']
NUM = 1000000


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    test()
