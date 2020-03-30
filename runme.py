import argparse
from composition import composer

#Define the parser and all its arguments
parser = argparse.ArgumentParser(description="Created a new composed image")

parser.add_argument("-s", "--source",
                    help="Image source")

parser.add_argument("-f", "--folder",
                    help="Component Image Folder")

parser.add_argument("--size", type=int,
                    help="Size of a pixel")

args = parser.parse_args()

resizevalue = 20
if args.size:
	resizevalue = args.size

#Execute the different tasks according to the parameters

if args.source and args.folder:
	composer(args.source,args.folder,resizevalue)
else:
	print("Must add a source and a component image folder")