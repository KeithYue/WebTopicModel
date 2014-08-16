# coding=utf-8
from pymongo import MongoClient

HOST = '183.57.42.116'
PORT = 27017

def connect_db():
    client = MongoClient(HOST, PORT)
    return client['pingan']

