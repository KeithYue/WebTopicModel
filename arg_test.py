# coding=utf-8
import argparse

parser = argparse.ArgumentParser(description='''
        the argparse module test
''')

parser.add_argument('-l', '--list', help='a list', nargs='*', default=[])
args = parser.parse_args()

print(args.list)
