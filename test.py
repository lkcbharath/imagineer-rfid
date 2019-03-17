from tempfile import NamedTemporaryFile
import shutil
import serial
import time
import csv

import sys

def main():
    comPort = 'COM6'
    baudRate = 9600
    myserial = serial.Serial(comPort,baudRate)

    while True:
        if (myserial.inWaiting()):
            mydata = (myserial.readline()).decode('utf-8').rstrip()
            print(mydata)

    
if __name__ == '__main__':
    main()