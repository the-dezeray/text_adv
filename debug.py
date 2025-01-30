import argparse

from main import main

parser = argparse.ArgumentParser()
parser.add_argument('-c', "--chatper", help="Chapter to start from" )
parser.add_argument('-s', "--subchapter", help="a sub chapter to start from" )
args = parser.parse_args()
chapter = args.chatper 

main(chapter_id=chapter)
 
