import os.path
import requests
import sys
import logging
from bs4 import BeautifulSoup
from datetime import date

logging.basicConfig(filename='Data.log', level=logging.DEBUG)


def FileRead():
    # It first check if the file is existing if not it will generate the file "record.txt"
    path = './record.txt'
    check_file = os.path.isfile(path)
    if not check_file:
        logging.warning('No record.txt found in the file path. Will Generating')
        f = open("record.txt", "w")
        f.write("5396")


    else:
        if os.stat("record.txt").st_size == 0:
            with open("record.txt", 'w') as f:
                f.write("5396")
        else:
            logging.debug(f'./record.txt exist in the file path')
            return True


def downloader(url, number):
    logging.info(f'Downloading {url}')
    downloadUrl = f'https://links.sgx.com/1.0.0/derivatives-historical/{number}/{url}'
    req = requests.get(downloadUrl)
    filename = str(date.today()) + "_" + str(number) + "_" + downloadUrl.split('/')[-1]
    logging.debug('File Overwrite the same file name')
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
            else:
                logging.critical("chunk_size is not enough")


def FileWrite(UpdateNumber):
    '''
    Write on record.txt the current number available.
    '''
    logging.info("New File Download")
    with open("record.txt", "r") as f:
        contents = f.readlines()
    contents.insert(0, str(UpdateNumber) + ' \n')
    with open("record.txt", "w") as f:
        contents = "".join(contents)
        f.write(contents)
        f.close()


def ErrorChecker(number):
    # check if the download URL exist
    try:
        logging.info("No new Update Available")
        Url = f'https://links.sgx.com/1.0.0/derivatives-historical/{number}/WEBPXTICK_DT.zip'
        result = requests.get(Url)
        doc = BeautifulSoup(result.text, "html.parser")
        tag = doc.title.string.strip()
        if tag == "Error":
            return False
        else:
            return True
    except:
        logging.info("New Update Available")
        return True


FileRead()

'''

'''
DataList = ['WEBPXTICK_DT.zip', 'TickData_structure.dat', 'TC.txt', 'TC_structure.dat']
current = 0

logging.info("read current record")
with open("record.txt") as file:
    record = str(file.readline(4))
    current = int(record)


def Main():
    loop = False
    newCurrent = current
    UpdateNumber = newCurrent + 1
    while not loop:
        ErrorCheck = ErrorChecker(UpdateNumber)
        if not ErrorCheck:
            loop = True
            i = 1
            for i in range(0, len(DataList)):
                downloader(DataList[i], current)
            while i < 5:
                ErrorCheck = ErrorChecker(UpdateNumber + i)
                if ErrorCheck:
                    logging.debug("A file is missiSng from the website")
                    UpdateNumber = UpdateNumber + i
                    for i in range(0, len(DataList)):
                        downloader(DataList[i], UpdateNumber)
                    FileWrite(UpdateNumber)
                    break
                if i == 4:
                    logging.debug("No New Update")
                    logging.warning("File Overwrite right now")
                    print("No New Update")

                i += 1

        elif ErrorCheck:
            logging.debug('Link existing, Downloading Links')
            FileWrite(UpdateNumber)
            for i in range(0, len(DataList)):
                downloader(DataList[i], UpdateNumber)
            UpdateNumber += 1


if len(sys.argv) > 1:

    arg1 = (sys.argv[1]).lower()
    if arg1 == '-h' or arg1 == '--help':
        FileRead()
        logging.warning("Command To follow")
        print("Expected 2 argument, (Type Of Data) (Number Update)")
        print('Ex. Downloader.py Tick_Data_Structure 300')
        print(
            f'Available Type of Data: Tick, Tick_Data_Structure, Trade_Cancellation, Trade_Cancellation_Data_Structure')
        print(f'Available Number of Updates : {current}')
    elif arg1 == "tick":
        FileRead()
        arg2 = sys.argv[2].isdigit()
        if arg2:
            if int(sys.argv[2]) < current:
                downloader(DataList[0], int(sys.argv[2]))
            else:
                logging.debug(f'{sys.argv[2]} is out of range')
                print(f'{sys.argv[2]} is out of range')
        else:

            logging.error(f'{sys.argv[2]} is not accepted')
            print("Invalid Input")
    elif arg1 == "tick_data_structure":
        FileRead()
        arg2 = sys.argv[2].isdigit()
        if arg2:
            if int(sys.argv[2]) < current:
                downloader(DataList[1], int(sys.argv[2]))
            else:
                logging.debug(f'{sys.argv[2]} is out of range')
                print(f'{sys.argv[2]} is out of range')
        else:
            logging.error(f'{sys.argv[2]} is not accepted')
            print("Invalid Input")

    elif arg1 == "trade_cancellation":
        FileRead()
        arg2 = sys.argv[2].isdigit()
        if arg2:
            if int(sys.argv[2]) < current:
                downloader(DataList[2], int(sys.argv[2]))
            else:
                logging.debug(f'{sys.argv[2]} is out of range')
                print(f'{sys.argv[2]} is out of range')
        else:
            logging.error(f'{sys.argv[2]} is not accepted')
            print("Invalid Input")
    elif arg1 == "trade_cancellation_data_structure":
        FileRead()
        arg2 = sys.argv[2].isdigit()
        if arg2:
            if int(sys.argv[2]) < current:
                downloader(DataList[3], int(sys.argv[2]))
            else:
                logging.debug(f'{sys.argv[2]} is out of range')
                print(f'{sys.argv[2]} is out of range')
        else:
            logging.error(f'{sys.argv[2]} is not accepted')
            print("Invalid Input")
    else:
        print("invalid ")
        logging.error("Input Invalid")


else:

    inp = input("Update or Modified: ").lower()
    if inp == "update":
        Main()
    elif inp == "modified":
        FileRead()
        print("Tick, Tick Data Structure, Trade Cancellation, Trade Cancellation Data Structure:")
        inp2 = input("Input: ").lower()
        if inp2 == "tick":
            print(f"Available File:{current}")
            inp3 = input("Count of Update before: ")
            if not inp3.isdigit():
                print("Invalid Input")
                logging.error("Input is not Valid")
            else:
                if int(inp3) < current:
                    downloader("WEBPXTICK_DT.zip", current - int(inp3))
                else:
                    print(f'{inp3} is out of range')
                    logging.error(f'{inp3} is out of range')


        elif inp2 == "tick data structure":
            print(f"Available File:{current}")
            inp3 = input("Count of Update before: ")
            if not inp3.isdigit():
                print("Invalid Input")
                logging.error("Input is not Valid")
            else:
                if int(inp3) < current:
                    downloader("TickData_structure.dat", current - int(inp3))
                else:
                    print(f'{inp3} is out of range')
                    logging.error(f'{inp3} is out of range')

        elif inp2 == "trade cancellation":
            print(f"Available File:{current}")
            inp3 = input("Count of Update before: ")
            if not inp3.isdigit():
                print("Invalid Input")
                logging.error("Input is not Valid")
            else:
                if int(inp3) < current:
                    downloader("TC.txt", current - int(inp3))
                else:
                    print(f'{inp3} is out of range')
                    logging.error(f'{inp3} is out of range')

        elif inp2 == "trade cancellation data structure":
            print(f"Available File:{current}")
            inp3 = input("Count of Update before: ")
            if not inp3.isdigit():
                print("Invalid Input")
                logging.error("Input is not Valid")
            else:
                if int(inp3) < current:
                    downloader("TC_structure.dat", current - int(inp3))
                else:
                    print(f'{inp3} is out of range')
                    logging.error(f'{inp3} is out of range')

        else:
            print("input Invalid")
            logging.error("User Input is invalid for modified download")

    elif inp == "recover" or inp == "repair":

        logging.info("New File Download")
        with open("record.txt", "r") as f:
            contents = f.readlines()
        contents.insert(0, '5390' + ' \n')
        with open("record.txt", "w") as f:
            contents = "".join(contents)
            f.write(contents)
            f.close()
        Main()




    else:
        logging.error('Input is Invalid Only "Update" and "Modified"')
        print('"Modified" and "Update" only')

