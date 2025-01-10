import os
import sys

scanner = input("Please enter source path:")
source_letter= scanner
scanner = input("Please enter a destination path:")
destination_letter = scanner
source_path = source_letter+":\ "
destination_path=destination_letter + ":\ "


flags = "/h/e/r/k/y/j"

if source_letter == destination_letter:
    exit(0)
else:
    print("Beginnig Copy...")

command = "xcopy" + " "+ source_path+ " "+ destination_path+" "+flags


print(command)
#os.system(command)
