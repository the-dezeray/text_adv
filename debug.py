import argparse

from main import main

parser = argparse.ArgumentParser()
parser.add_argument('-c', "--chatper")
args = parser.parse_args()
chapter = args.chatper 


main(chapter_id=chapter)
 
