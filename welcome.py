#!/usr/bin/env python3

import time

def welcome_msg():
	print("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|")
	print("|~~~ Welcome to floyd-merge.py! ~~~|")
	print("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|")
	time.sleep(2)
	print("~~~This script will merge elan projects.~~~")
	print("Projects MUST have the same tier structure and tier dependencies.")
	print("The script doesn't compare tier structures or tier dependencies.")
	print("You have to do that yourself.")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("")
	time.sleep(2)
	print("Your MEDIA should also have the SAME PARAMETERS: stero/mono, bit rate/depth, etc.")
	print("The script doesn't compare media file parameters.")
	print("You have to do that yourself.")
	print("Using this script on projects that don't meet the above conditions will yeild unpredictable results.")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("")
	time.sleep(2)
	print("You can disable this message by commenting out line 143 in ELAN_floyd-merge.py")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("")
	time.sleep(1)

def main():
	welcome_msg()
if __name__ == '__main__':
	main()
