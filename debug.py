"""heheheh"""

import argparse
from main import main

parser = argparse.ArgumentParser()
parser.add_argument(
    "-r", "--return", help="enable return to previous node funtionality "
)
parser.add_argument(
    "-d",
    "--dev",
    help="run in dev therefore constant reloading of config files and story files ",
)
parser.add_argument("-c", "--chatper", help="Chapter to start from")
parser.add_argument("-p", "--place", help="Chapter to start from")
parser.add_argument("-e", "--event", help="load event from a file")
parser.add_argument("-m", "--mute", help="mute sound")
parser.add_argument("-tank", "--tank", help="create player as a tank")
parser.add_argument("-sub", "--subchapter", help="a sub chapter to start from")
parser.add_argument("-s", "--story", help="path to the story")
parser.add_argument('--menu', dest='menu', action='store_true', help="show menu")
parser.add_argument('--no-menu', dest='menu', action='store_false', help="hide menu")
parser.set_defaults(menu=False)  # or False if you prefer hidden by default
args = parser.parse_args()
chapter = args.chatper
main(chapter_id= int(chapter),menu=args.menu)
