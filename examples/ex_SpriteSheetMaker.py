#!/usr/bin/python3.9

from pathlib import Path
from sys import argv

from personal_gamedev_asset_tools import ssm_ffmpeg

# Example code for creating sprite sheets
# Provide all paths to the files as arguments, the order of the files matter
# All provided images must have the exact same dimensions

def main():
	files_list_raw=argv[1:]
	if len(files_list_raw)<2:
		print("Not enough paths")
		return

	files_list=[]
	for f in files_list_raw:
		ff=Path(f)
		if not ff.exists():
			continue
		if not ff.is_file():
			continue
		files_list.append(ff)

	if len(files_list)<2:
		print("Not enough files")
		return

	fname="sprite-sheet-made-with-SSM"
	issues=util_ssm_ffmpeg(".",fname,files_list)

	print("\nRESULTS\ntotal_files:",len(files_list),"; errors/wanings:",issues)
	print("The filename starts with \""+fname+"\"")

main()
