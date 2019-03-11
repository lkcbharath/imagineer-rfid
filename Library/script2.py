from tempfile import NamedTemporaryFile
import shutil
import serial
import time
import csv
import sys
import pandas as pd

class Student:

    def __init__(self,uid_):
        self.book = []
        df = pd.read_csv('librarysys.1.csv')
        for i in range(len(df.index)):
            if df.iloc[i,0] == int(uid_):
                self.uid = uid_
                self.roll = df.iloc[i,1]
                self.count = df.iloc[i,2]
                for j in range(3,7):
                    self.book.append(df.iloc[i,j])

    def __str__(self):
        print("Details of the student in Library")
        print("UID:",self.uid)
        print("Roll Number:",self.roll)
        print("Book count remaining:",self.count)
        print("Book 1:",self.book[0])
        print("Book 2:",self.book[1])
        print("Book 3:",self.book[2])
        print("Book 4:",self.book[3])
        return ""

    def deissue(self,id_):
        self.count = str(int(self.count) + 1)
        self.book[int(id_)-1] = '0'
        self.update_csv()

    def issue(self,book_):
        self.count = str(int(self.count) - 1)
        self.book[3-int(self.count)] = book_
        self.update_csv()

    def update_csv(self):
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        df = pd.read_csv('librarysys.1.csv')
        for i in range(len(df.index)):
            if df.iloc[i,0] == self.uid:
                df.iloc[i] = [self.uid,self.roll,self.count,self.book[0],self.book[1],self.book[2],self.book[3]]
        
        df.to_csv('librarysys.1.csv')

def main():
    comPort = 'COM6'
    baudRate = 9600
    myserial = serial.Serial(comPort,baudRate)

    uids = []

    df = pd.read_csv('librarysys.1.csv')

    for i in range(len(df.index)):
        uids.append(df.iloc[i,0])

    try:
        while True:
            if (myserial.inWaiting()):
                mydata = (myserial.readline()).decode('utf-8').rstrip()

                if mydata == '' or len(mydata) == 4:
                    pass
                elif len(mydata) > 4:
                    if int(mydata) in uids:
                        student = Student(mydata)
                        print(student)

                        print("Library Manager, what do you want to do?")
                        print('Return the book? Enter 1')
                        print('Issue a book? Enter 2')
                        print('To accept another card, Enter any other key.')

                        choice = int(input())

                        if choice == 1:
                            if student.count == 4:
                                print("You don't need to return any more books.")
                            else:
                                print('Enter which book to return')
                                book_i = int(input())
                                student.deissue(book_i)
                                print("Done!")

                        elif choice == 2:
                            if student.count == 0:
                                print("You cannot issue any more books!")
                            else:
                                print('Enter book')
                                book_ = input()
                                student.issue(book_)
                                print("Done!")
                    else:
                        print(uids,mydata)
                        print("Unauthorized user")
                else:
                    print("Oops! Something went wrong.",mydata)
    except:
        print(sys.exc_info())

if __name__ == '__main__':
    main()