from tempfile import NamedTemporaryFile
import shutil
import serial
import time
import csv

import sys

class Student:

    def __init__(self,uid_):
        self.book = []
        with open('librarysys.csv', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:
                if uid_ == row[0]:
                    self.uid = uid_
                    self.roll = row[1]
                    self.count = row[2]
                    for j in range(3,7):
                        self.book.append(row[j])

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

    def issue(self,book_,id_):
        self.count = str(int(self.count) - 1)
        self.book[int(id_)-1] = book_
        self.update_csv()

    def update_csv(self):
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open('librarysys.csv',newline='') as csv_file, tempfile:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(tempfile, delimiter=',')
            for row in csv_reader:
                if self.uid == row[0]:
                    data = [self.uid,self.roll,self.count,self.book[0],self.book[1],self.book[2],self.book[3]]
                    csv_writer.writerow(data)
                else:
                    csv_writer.writerow(row)
        
        shutil.move(tempfile.name, 'librarysys.csv')
        remove_empty_lines()

def remove_empty_lines():
    with open('librarysys.csv') as filehandle:
        lines = filehandle.readlines()

    with open('librarysys.csv', 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines) 

def main():
    comPort = 'COM6'
    baudRate = 9600
    myserial = serial.Serial(comPort,baudRate)

    uids = []
    with open('librarysys.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            uids.append(row[0])

    try:
        while True:
            if (myserial.inWaiting()):
                mydata = (myserial.readline()).decode('utf-8').rstrip()

                if mydata == '' or len(mydata) == 4:
                    pass
                elif len(mydata) > 4:
                    if mydata in uids:
                        student = Student(mydata)
                        print(student)

                        print("Library Manager, what do you want to do?")
                        print('Return the book? Enter 1')
                        print('Issue a book? Enter 2')
                        print('To accept another card, Enter any other key.')

                        choice = input()
                        if choice == '1':
                            if student.count == '4':
                                print("You don't need to return any more books.")
                            else:
                                print('Enter which book to return')
                                book_i = input()
                                student.deissue(book_i)

                        elif choice == '2':
                            if student.count == '0':
                                print("You cannot issue any more books!")
                            else:
                                print('Enter book and card')
                                book_ = input()
                                id_ = input()
                                student.issue(book_,id_)

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