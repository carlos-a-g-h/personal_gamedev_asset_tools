#!/usr/bin/python3.9

# Example for recovering a single asset from a GMS2 project
# For this example, provide the path to the asset directory (sprite or sound) as an argument

from personal_gamedev_asset_tools import yyz_recover_single
from sys import argv

def main():
	p=argv[1]
	res=yyz_recover_single(".",p)
	print("\nRecovery results:",res)

main()
