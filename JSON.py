import requests, json, sys, calendar, string
from difflib import SequenceMatcher

# Pull age from JSON
def age(remark):
  numStrings = ["zero", "one","two","three","four","five","six","seven","eight","nine"]
  if "age" in remark.lower():
    remarkList = remark.lower().split("age")[1].split(" ")
    ageString = "" 
    if len(remarkList) > 1:
      for c in remarkList[1]:
        if c.isdigit():
          ageString = ageString + c
      if ageString == "":
        i = 0
        for numString in numStrings:
          if remarkList[1] == numString:
            ageString = str(i)
          i += 1
      if len(remarkList)>=3:
       if "months" in remarkList[2] or "mths" in remarkList[2] or "mnths" in remarkList[2]:
           return str(round(int(ageString)/12,2))
    return ageString
  return ''

# Pull any meaningful data from the remarks
def arrivedWith(remark):
  separators = ["with", "and", "&amp;", "also"]
  for separator in separators:
    if separator in remark.lower():
      return "with " + remark.lower().split(separator)[1].strip()
  return ''

# Check if the remark refers to death in particular
def died(remark):
  if "died" in remark.lower():
    return remark.lower()
  else:
    return ''

people = json.load(open("arrivals.json.1",'r'))

date = ""
location = ""
year = ""
ship = ""
name = ""
data = {}
ship_occurences = {}
sys.stdout = open("json", "w")

# Put each person into the correct ship, year, date, location
for id in people:
  
  date = ""
  location = ""
  year = ""
  ship = ""
  name = ""  

  for attr in people[id]:
    for val in  people[id][attr]:
      if(attr == 'NI_ARRIVAL_DATE'):
        dateArray = val.split(" ")
        dateArray[0] = dateArray[0].zfill(2)
        if len(dateArray[1]) == 3:
          dateArray[1] = str(list(calendar.month_abbr).index(dateArray[1])).zfill(2)
        else:
          dateArray[1] = str(list(calendar.month_name).index(dateArray[1])).zfill(2)
        date = dateArray[2] + "-" + dateArray[1] + "-" + dateArray[0]  
      if(attr == 'NI_DEPARTURE_PORT'):
        location = val.replace("&amp;","&")
        location = location.split("via")[0]
        location = string.capwords(location.lower())
      if(attr == 'NI_YEAR'):
        year = val        
      if(attr == 'NI_SHIP'):
        ship = val.replace("&amp;","&")
        ship = string.capwords(ship.lower())
        ship_occurences.setdefault(ship, 0)
        ship_occurences[ship] = ship_occurences[ship] + 1

  # Organise Data by ship, year, arrival data and departure location
  if(ship not in data):
    data[ship] = {}
  if(year not in data[ship]):
    data[ship][year] = {}
  if(date not in data[ship][year]):
    data[ship][year][date] = {}
  if(location not in data[ship][year][date]):
    data[ship][year][date][location] = {}

  data[ship][year][date][location][id] = people[id]

unique_names = []
# Sort and output relevant data
shipListFile = open("shipsNew2","r")
shipList = []
for line in shipListFile:
  shipList.append(line.strip().lower())
badShipFile = open("badShips","w")
# Iterate through each ship and print the data in a readable form,
# ignoring ships with small, potentially outlying datasets
for x in sorted(data):
  if x.lower() not in shipList:
    score = 0
    bestmatch = ""

    # Create a file with each ship's closest match to the HTML table from https://libraries.tas.gov.au/archive-heritage/guides-records/Pages/Immigrant-ships.aspx
    for ship in shipList:
      seq = SequenceMatcher(None, x.lower(), ship)
      ratio = seq.ratio()
      if(ratio > score and ratio > 0.5):
        bestmatch = ship
        score = ratio
    if(x != ""):
      # Ignore the ships with few people
      if(ship_occurences[x] < 10):
        continue
      badShipFile.write(x + " : " + str(ship_occurences[x]) + "\n")

  print("Ship: ", x)
  for y in sorted(data[x]):
    print("    Year: ", y)
    for z in sorted(data[x][y]):
      print("        Date: ", z)
      for l in sorted(data[x][y][z]):
        print("            Departure: ", l)
        for m in data[x][y][z][l]:
          person = data[x][y][z][l][m]
          personAge = ""
          name = ""
          personWith = ""
          personDied = ""
          #With or died
          if "NI_REMARKS" in person:
            if arrivedWith(person['NI_REMARKS'][0]):
              personWith = ", " + arrivedWith(person['NI_REMARKS'][0]).replace("&amp;","&")
            if died(person['NI_REMARKS'][0]):
              personDied = ", " + died(person['NI_REMARKS'][0]).replace("&amp","&")
          # Age
          if 'NI_AGE' in person:
            personAge = ", " + person['NI_AGE'][0]
          elif 'NI_REMARKS' in person:
            personAge = age(person['NI_REMARKS'][0])
            if personAge:
              personAge = ", " + personAge
          # Name with title
          if 'NI_NAME_FACET' in person:
            if "NI_NAME_TITLE" in person:
              title = person['NI_NAME_TITLE'][0].strip() 
              title = title.replace("&amp;","&")
              name = ", " + title + " " + name.replace("&amp;","&")
            else:
              name = ", "
            nameArray = person['NI_NAME_FACET'][0].split(',')
            if len(nameArray) <= 1 or nameArray[1].strip() == "Given Name Not Recorded":
              name += nameArray[0].strip()
            else:
              name += nameArray[1].strip() + " " + nameArray[0].strip()
          name = string.capwords(name.lower())
          print("                People: ", m + name + personAge + personWith + personDied)
          if(name not in unique_names):
            unique_names.append(name)

# Write a file containing each unique name found (does not consider children with parents names as unique entities)
names_file = open("unique_names","w")
print ("Unique Entries: ", len(unique_names))
for name in unique_names:
  names_file.write(name + "\n")

