from tempfile import NamedTemporaryFile
import shutil
import serial
import time
import csv
import sys

class Student:

    def __init__(self,uid_):
        with open('attendancesys.csv', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:
                if uid_ == row[0]:
                    self.uid = row[0]
                    self.roll = row[1]
                    self.attendance = row[2]
                    
    def __str__(self):
        print("Details of the student in Library")
        print("UID:",self.uid)
        print("Roll Number:",self.roll)
        print("Attendance count:",self.attendance)
        return ""
    
    def increment(self):
        self.attendance = str(int(self.attendance) + 1)
        self.update_csv()

    def update_csv(self):
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open('attendancesys.csv',newline='') as csv_file, tempfile:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(tempfile, delimiter=',')
            for row in csv_reader:
                if self.uid == row[0]:
                    data = [self.uid,self.roll,self.attendance]
                    csv_writer.writerow(data)
                else:
                    csv_writer.writerow(row)
        
        shutil.move(tempfile.name, 'attendancesys.csv')
        remove_empty_lines()

def remove_empty_lines():
    with open('attendancesys.csv') as filehandle:
        lines = filehandle.readlines()

    with open('attendancesys.csv', 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)   

def main():
    comPort = 'COM6'
    baudRate = 9600
    myserial = serial.Serial(comPort,baudRate)

    uids = []
    with open('attendancesys.csv') as csv_file:
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

                        print("Attendance Manager, what do you want to do?")
                        print('Increase attendance? Enter 1')
                        print('To accept another card, Enter any other key.')

                        choice = input()

                        if choice == "1":
                            student.increment()
                        
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