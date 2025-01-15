import os
import time


def gui():
    return


def options():
    local = "local"
    network = "network"
    reply = input("Will this copy be local or via network connection?")
    if reply == local:
        xcopy()
    elif reply == network:
        robocopy()
    else:
        print("Please check the available options and try again!")
        exit(0)


def xcopy():
    scanner = input("Please enter source path:")
    source_path = str(scanner)
    scanner = input("Please enter a destination path:")
    destination_path = str(scanner)
    flags = "/h/e/r/k/y/j"
    if source_path.lower() == destination_path.lower():
        print("Please check entered values and try again!")
        exit(0)
    else:
        print("Starting Copy...")
    command = "xcopy" + " " + source_path + " " + destination_path + " " + flags
    print(command)
    os.system(command)
    w = open("history.txt", "a")
    w.write(str(time.ctime()) + " " + command + "\n")


def robocopy():
    start = "Robocopy"
    flags = "/E /XC /XN /XO"
    user = str(input("Please enter the source path:")).lower()
    source_path = user.lower()
    user = str(input("Please enter the destination path:")).lower()
    destination_path = user
    if source_path.lower() == destination_path.lower():
        print("Please check entered values and try again")
        exit(0)
    else:
        print("Starting Copy...")
    command = start + " " + source_path + " " + destination_path + " " + flags
    os.system(command)
    print(command)
    w = open("history.txt", "a")
    w.write(str(time.ctime()) + " " + command + "\n")


if __name__ == '__main__':
    options()
