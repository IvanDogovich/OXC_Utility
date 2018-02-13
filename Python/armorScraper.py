# Created by bbbbb (BBallin- on discord)

#dictionaries with keys armors have recipe of items and quantities.
#This combines them
def combineDict(aDict,bDict):
	cDict = {}
	for k in aDict:
		if k in bDict:
			cDict[k] = addDict(aDict,bDict)[k]
		else:
			cDict[k] = aDict[k]
	for k in bDict:
		if k not in cDict:
			cDict[k] = bDict[k]
	return cDict

# {'a':1,'b':2,'c':3} + {'a':1,'b':5,'d':8} = {'a':2,'b':7,'c':3,'d':8}
def addDict(aDict,bDict):
	cDict = {}
	for k in aDict:
		if k in bDict:
			cDict[k] = aDict[k] + bDict[k]
		else:
			cDict[k] = aDict[k]
	for k in bDict:
		if k not in cDict:
			cDict[k] = bDict[k]
	return cDict


infile = open('Piratez.rul')
outfile = open('Piratez.rul2','w')

data = infile.read()
# get the manufacturing data
    # gets the data from the beginning of 'manufacture' to the beginning of
    # starting base
data= data[data.index('manufacture:'):data.index('startingBase:')]
# get each entry
dataList = data.split('  - name: ')[1:]
#this holds armor recipes
armorList = {}

#for each entry, add it to the armor list, if it's an armor
for someEntry in dataList:
	lineList = someEntry.split('\n')
	if len(lineList) > 1:
		if 'STR_PERSONAL_ARMOR_CAT' in lineList[1]:
			armorShit = lineList[0].strip()
			armorList[armorShit] = {}
			itemIndex = -1
			for i in range(0,len(lineList)):
				if 'requiredItems' in lineList[i]:
					itemIndex = i
				elif itemIndex > 0:
					if '      ' not in lineList[i]:
						endIndex = i
						break
			if itemIndex != -1:
				itemList = lineList[itemIndex+1:endIndex]
				for item in itemList:
					if len(item.split(':')) > 1:
						a,b = item.split(':')
						a = a.strip()
						b = b.strip()
						# print item
						armorList[armorShit][a] = int(b)
#keys
    #extracts just the keys (armor names) from the list
armorOnly = [k for k in armorList]
#our updated recipe list

# Lets try printing out just the armor list here
# print armorOnly
newList = {k:armorList[k] for k in armorList}
print newList

#for each armor, if its in a recipe, replace that recipe with components instead
# set the next loop to run until doneYet = True
doneYet = False
while not doneYet:
    # match armors in the armors key list
    for armors in armorOnly:
		for k in newList:
			if armors in newList[k]:
				index = newList[k][armors]
				addTo = {}
				while index > 0:
					addTo = addDict(addTo,newList[armors])
					index = index - 1
				newList[k] = combineDict(newList[k],addTo)
				del newList[k][armors]
    for armors in armorOnly:
		for k in newList:
			if armors in k:
				doneYet = False
				break
    doneYet = True
#write the modified info
outfile.write('manufacture:\n')
for anEntry in dataList:
	lineList = anEntry.split('\n')

	if len(lineList) > 1:
		if 'STR_PERSONAL_ARMOR_CAT' in lineList[1]:
			outfile.write('  - name: '+lineList[0].strip()+'\n')
			armorShit = lineList[0].strip()
			itemIndex = -1
			for i in range(0,len(lineList)):
				if 'requiredItems' in lineList[i]:
					itemIndex = i
				elif itemIndex > 0:
					if '      ' not in lineList[i]:
						endIndex = i
						break
			if itemIndex == -1:
				for line in lineList[1:]:
					outfile.write(line+'\n')
			else:
				for line in lineList[1:itemIndex]:
					outfile.write(line +'\n')
				outfile.write('    requiredItems:' +'\n')
				#print newList
				for k in newList[armorShit]:
					outfile.write('      ' + k + ': ' + str(newList[armorShit][k]) +'\n')
				if len(lineList) > endIndex:
					for line in lineList[endIndex:-1]:
						outfile.write(line +'\n')
					outfile.write(lineList[-1])
		else:
			outfile.write('  - name: '+lineList[0].strip()+'\n')
			for line in lineList[1:-1]:
				outfile.write(line +'\n')
			outfile.write(lineList[-1])


