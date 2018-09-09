# Remove unexpected data (non-alphabet characters) from ship names and save in an updated file for comparison
import re

shipListFile = open("shipsNew","r")
updateShipFile = open("shipsNew2","w")
ships = []

for line in shipListFile:
	s = re.sub("[^a-zA-Z]+", " ", line)
	s = s.strip()
	if (s not in ships):
		ships.append(s)

for s in ships:	
	updateShipFile.write(s+"\n")