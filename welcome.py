#!/usr/bin/env python3

import time

def welcome_msg():
	print("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|")
	print("|~~~ Welcome to floyd-merge.py! ~~~|")
	print("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|")
	time.sleep(1)
	print("This script will merge elan projects.")
	print("Projects must have the same tier structure and tier dependencies.")
	print("The script doesn't compare tier structures or tier dependencies.")
	print("You have to do that yourself.")
	print("Your media should also have the same parameters: stero/mono, bit rate/depth, etc.")
	print("The script doesn't compare media file parameters.")
	print("You have to do that yourself.")
	print("Using this script on projects that don't meet the above conditions will yeild unpredictable results.")
	time.sleep(1)

def main():
	welcome_msg()
if __name__ == '__main__':
	main()
