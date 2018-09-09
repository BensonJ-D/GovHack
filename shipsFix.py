# Script used to convert dates to readable YYYY-MM-DD for easier processing (commented out)
# Split text at commas and only output ship name (current iteration)

#!/bin/python3
import calendar

inFile = open("ships",'r')
outFile = open("shipsNew",'w')

for line in inFile:
  lineArray = line.split(",")
  
  #dateArray = lineArray[0].split(" ")
  #dateArray[0] = dateArray[0][:4]
  #if len(dateArray[1]) > 0 and dateArray[1][0].isalpha(): 
  #  dateArray[1] = str(list(calendar.month_abbr).index(dateArray[1][:3])).zfill(2)
  #dateArray[2] = dateArray[2].zfill(2)
  #outFile.write(dateArray[0] + "-" + dateArray[1] + "-" + dateArray[2])
  
  outFile.write(lineArray[1])

  outFile.write("\n")
