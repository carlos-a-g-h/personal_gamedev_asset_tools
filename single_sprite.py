#!/usr/bin/python3.9

# Example for recovering a single sprite
# For this example, provide the path to the sprite directory as an argument

from gms2_asset_recovery import recover_single
from sys import argv

def main():
	sprite_dir=argv[1]
	res=recover_single(".",sprite_dir)
	print("Recovery results:",res)

main()
