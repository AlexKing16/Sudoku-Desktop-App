import os
import csv
import random
import sys
import time

pipe="pipe.txt"
input="input.csv"
output="output.csv"

while 1:
    time.sleep(1)
    f=open(os.path.join(sys.path[0],"pipe.txt"),"r+")
    r1=f.read()
    if r1.isdigit() and int(r1)in range(0,9):
        print("running")
        lvl= int (r1)
        numbers = (range(0,9))
        sudoku_grid = []
        with open('input.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    sudoku_grid.append(row)
        print ("processing....\n")
        for i in range(len(sudoku_grid)):
            randNum= random.sample(numbers, lvl)
            for k in randNum:
                n=random.randint(0,8)
                sudoku_grid[i][k] = 0
        print("Done....Sending Data\n")
        with open("output.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(sudoku_grid)
        
        f.seek(0)
        f.truncate()
        f.close()
    elif r1=="stop":
        f.seek(0)
        f.truncate()
        f.close() 
        break
