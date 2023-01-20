#!/usr/bin/python3.9

# Example for recovering a single sprite from a GMS2 project
# For this example, provide the path to the sprite directory as an argument

from personal_gamedev_asset_tools import yy_recover_single
from sys import argv

def main():
	sprite_dir=argv[1]
	res=yy_recover_single(".",sprite_dir)
	print("\nRecovery results:",res)

main()
