import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

def main():
	print("Starting up Database")
	sql = sqlite3.connect('unit_database.db')
	cur = sql.cursor()
	print("Creating database if it doesn't exist")
	cur.execute('CREATE TABLE IF NOT EXISTS units (faction varchar NOT NULL, unitRole varchar NOT NULL, arsenalPasteCode varchar NOT NULL, genericClothes varchar NOT NULL, isSpecialist varchar NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS uniforms (uniform varchar NOT NULL, gearSide varchar NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS vests (vest varchar NOT NULL, gearSide varchar NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS backpacks (backpack varchar NOT NULL, gearSide varchar NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS helmets (helmet varchar NOT NULL,gearSide varchar NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS glasses (glasses varchar NOT NULL, gearSide varchar NOT NULL)')
	sql.commit()
	factionstring = "Enter Faction here"
	clearFiles()
	chooseSide(cur,sql,factionstring)
	
def chooseSide(cur,sql,factionstring):
	sideWindow = tk.Tk()
	sideWindow.title("Framework Generator")
	sideWindow.minsize(height=200, width=275)
	sideWindow.maxsize(height=200, width=275)
	
	#Initalise Checkbox Variables
	unitAssociationToSide = IntVar()
	unitAssociationToSide.set(0)

	aboutLabel = Message(sideWindow, text = "GearScript Generator written by Matthew Betts with special thanks and contributions by _name_. Enter a faction side and hit 'Submit' to begin.", fg="red")
	aboutLabel.place(relx=0.5, rely=0)

	unitSideLabel = Label(sideWindow, text = "Faction:")
	unitSideLabel.place(relx=0, rely=0)
	unitSideEntry = tk.Entry(sideWindow)
	unitSideEntry.place(relx=0, rely=0.1)
	unitSideEntry.insert(0, factionstring)

	unitSideLabel = Label(sideWindow, text = "Unit is associated with:")
	unitSideLabel.place(relx=0, rely=0.2)
	
	unitSideRadio = Radiobutton(sideWindow, variable=unitAssociationToSide, value = 0, text= "BLUFOR")
	unitSideRadio.place(relx=0, rely=0.32)
	unitSideRadio = Radiobutton(sideWindow, variable=unitAssociationToSide, value = 1, text= "OPFOR")
	unitSideRadio.place(relx=0, rely=0.42)
	unitSideRadio = Radiobutton(sideWindow, variable=unitAssociationToSide, value = 2, text= "INDFOR")
	unitSideRadio.place(relx=0, rely=0.52)

	#Progress to next stage
	chooseSideButton = tk.Button(sideWindow,text="Submit",command=lambda: closeSideWindow(sideWindow,cur,sql,unitSideEntry,unitAssociationToSide))
	chooseSideButton.place(relx=0.05, rely=0.7)

	sideWindow.mainloop()
	
def closeSideWindow(sideWindow,cur,sql,unitSideEntry,unitAssociationToSide):
	#get the side of the unit
	unit_side = unitSideEntry.get()

	_factionstring = ""
	_factionstring = unitSideEntry.get()

	#checks for if it's empty or contains spaces, if so returns to chooseSide()
	if(unit_side == ""):
		messagebox.showinfo("Notice", "Faction name is empty. Please fill and resubmit.")
		sideWindow.destroy()
		chooseSide(cur,sql,_factionstring)
	elif (" " in unit_side or "." in unit_side):
		messagebox.showinfo("Notice", "Faction name contains space. Please remove space and resubmit.")
		sideWindow.destroy()
		chooseSide(cur,sql,_factionstring)
	else:
		#if no problems arise, continue to enterData()
		sideWindow.destroy()
		unitAssociationToSideString = ""
		if(unitAssociationToSide.get() == 0):
			unitAssociationToSideString = "West"
		if(unitAssociationToSide.get() == 1):
			unitAssociationToSideString = "East"
		if(unitAssociationToSide.get() == 2):
		   unitAssociationToSideString = "Independant"
		enterData(cur,sql,unit_side,unitAssociationToSideString)
		
def enterData(cur,sql,unit_side,unitAssociationToSideString):
	dataWindow = tk.Tk()
	dataWindow.title("Framework Generator")

	dataWindow.minsize(height=500, width=700)
	dataWindow.maxsize(height=500, width=700)

	#Initalise Checkbox Variables
	isGeneric = IntVar()
	isGeneric.set(0)
	
	isSpecialist = IntVar()
	isSpecialist.set(0)
	
	#Show what the side is that they entered in the previous window
	unitsideLabel = Label(dataWindow, text = 'Faction = ' + unit_side, fg="blue",relief=RIDGE)
	unitsideLabel.place(relx=0, rely=0)

	unitsideLabel1 = Label(dataWindow, text = 'Associated with = ' + unitAssociationToSideString, fg="blue",relief=RIDGE)
	unitsideLabel1.place(relx=0, rely=0.05)

	#Change Faction
	factionChangeButton = tk.Button(dataWindow,text="Change Faction", fg="red", command=lambda: UnitToFaction(cur,sql,dataWindow,unit_side))
	factionChangeButton.place(relx=0, rely=0.10)
	
	#Go to insert clothes screen
	enterGearButton = tk.Button(dataWindow, text="Insert Clothes", fg="red", command=lambda: enterGear(unit_side,cur,sql,dataWindow,unitAssociationToSideString))
	enterGearButton.place(relx=0, rely=0.16)

	#Generate Markers
	platoonGenButt = tk.Button(dataWindow,text="Generate Markers", fg="red",command=lambda: platoonGenStart(unit_side,unitAssociationToSideString,dataWindow))
	platoonGenButt.place(relx=0, rely=0.22)
	
	pasteArsenalLabel = Label(dataWindow, text = 'Paste Arsenal Code Here: ', fg="red")
	pasteArsenalLabel.place(relx=0.25, rely=0.05)
	
	#Entry box for arsenal
	textbox = Text(dataWindow, width = 60, height = 10, wrap = WORD)
	textbox.place(relx=0.25, rely=0.1)

	aboutLabel = Message(dataWindow, text = "Note: 'Generic clothes' are a set of vests/uniforms etc that are randomly selected from the ones that you can manually enter. \
		\nIf the box is ticked when a unit is submitted, generic clothes are given to it. This overwrites the clothes that are already given to it.\
		\nTo insert Generic Clothes, press the 'Insert Clothes' button to the left.", fg="red")
	aboutLabel.place(relx=0.65, rely=0.45)

	#Unit role
	unitRoleLabel = Label(dataWindow, text = "Unit Role (r/ar etc):")
	unitRoleLabel.place(relx=0.25, rely=0.45)
	unitRoleEnt = tk.Entry(dataWindow)
	unitRoleEnt.place(relx=0.25, rely=0.5)
	
	isSpecialistLabel = Label(dataWindow, text = "Has own marker in squad?:")
	isSpecialistLabel.place(relx=0.25, rely=0.55)
	isSpecialistRadio = Radiobutton(dataWindow, variable=isSpecialist, value = 1, text= "Yes")
	isSpecialistRadio.place(relx=0.25, rely=0.6)
	isSpecialistRadio = Radiobutton(dataWindow, variable=isSpecialist, value = 0, text= "No")
	isSpecialistRadio.place(relx=0.25, rely=0.65)

	#Enable popups?
	enablePopups = IntVar()
	enablePopups.set(1)
	enablePopupsCheckbox1 = Checkbutton(dataWindow, variable=enablePopups, onvalue = 1, offvalue = 0, text= "Enable Popups?")
	enablePopupsCheckbox1.place(relx=0.25, rely=0.75)

	#Check if unit is using generic clothes for faction
	isGenericClothes = Checkbutton(dataWindow, variable=isGeneric, onvalue = 1, offvalue = 0, text= "Generic Clothes?")
	isGenericClothes.place(relx=0.65, rely=0.77)

	submitArsenalButton = tk.Button(dataWindow,text="Submit Arsenal",command=lambda: submitArsenal(cur,sql,textbox,unit_side,unitRoleEnt,isGeneric,isSpecialist,enablePopups))
	submitArsenalButton.place(relx=0.4, rely=0.9)

	createGSButton = tk.Button(dataWindow,text="Generate GearScript", fg="red",command=lambda: generateGS(cur,sql,unit_side,unitAssociationToSideString,dataWindow))
	createGSButton.place(relx=0, rely=0.28)

def enterGear(unit_side,cur,sql,dataWindow,unitAssociationToSideString):
	dataWindow.destroy()
	gearWindow = tk.Tk()
	gearWindow.title("Framework Generator")
	unitsideLabel = Label(gearWindow, text = 'Faction = ' + unit_side, fg="red",relief=RIDGE)
	unitsideLabel.grid(row=0, column=0)
	unitsideLabel = Label(gearWindow, text = 'Associated with = ' + unitAssociationToSideString, fg="red",relief=RIDGE)
	unitsideLabel.grid(row=1, column=0)

	#Uniform
	uniformLabel = Label(gearWindow, text = "Uniform")
	uniformLabel.grid(row=2, column=0)
	uniformEntry = tk.Entry(gearWindow)
	uniformEntry.grid(row=2, column=1)

	#Vest
	vestLabel = Label(gearWindow, text = "Vest")
	vestLabel.grid(row=3, column=0)
	vestEntry = tk.Entry(gearWindow)
	vestEntry.grid(row=3, column=1)

	#Backpacks
	backpackLabel = Label(gearWindow, text = "Backpack")
	backpackLabel.grid(row=4, column=0)
	backpackEntry = tk.Entry(gearWindow)
	backpackEntry.grid(row=4, column=1)

	#HeadGear (Helmets)
	helmetLabel = Label(gearWindow, text = "HeadGear (Helmets)") 
	helmetLabel.grid(row=5, column=0)
	helmetEntry = tk.Entry(gearWindow)
	helmetEntry.grid(row=5, column=1)

	#HeadGear (Glasses)
	glassesLabel = Label(gearWindow, text = "HeadGear (Glasses)") 
	glassesLabel.grid(row=6, column=0)
	glassesEntry = tk.Entry(gearWindow)
	glassesEntry.grid(row=6, column=1)

	#Enable popups?
	enablePopups = IntVar()
	enablePopups.set(1)
	enablePopupsCheckbox1 = Checkbutton(gearWindow, variable=enablePopups, onvalue = 1, offvalue = 0, text= "Enable Popups?")
	enablePopupsCheckbox1.grid(row=3, column=3)

	#Submit Gear Button
	submitGearButton = tk.Button(gearWindow,text="Submit Clothes",command=lambda: submitGear(unit_side,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,\
		cur,sql,enablePopups))
	submitGearButton.grid(row=6, column=2, sticky=W)

	#Change Faction
	factionChangeButton = tk.Button(gearWindow,text="Change Faction", fg="red", command=lambda: gearToFaction(cur,sql,gearWindow))
	factionChangeButton.grid(row=0, column=3, sticky=W)
	#Change to guns window
	gunChangeButton = tk.Button(gearWindow,text="Change to Guns", fg="red", command=lambda: gearToUnit(cur,sql,unit_side,unitAssociationToSideString,gearWindow))
	gunChangeButton.grid(row=1, column=3, sticky=W)

	clearBoxesButton2 = tk.Button(gearWindow,text="Clear All Boxes",command=lambda: clearVests(uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,enablePopups))
	clearBoxesButton2.grid(row=2, column=3, sticky=W)

def submitArsenal(cur,sql,textbox,unit_side,unitRoleEnt,isGeneric,isSpecialist,enablePopups):
	_unit_side = unit_side
	_unit_role = unitRoleEnt.get()
	_genericClothes = isGeneric.get()
	_isSpecialist = isSpecialist.get()
	_enablePopups = enablePopups.get()
	_arsenal = textbox.get("1.0",'end-1c')
	if(_unit_role != ""):
		cur.execute('INSERT INTO units(faction, unitRole, arsenalPasteCode,genericClothes,isSpecialist) VALUES (?,?,?,?,?)',(str(_unit_side),str(_unit_role),str(_arsenal),str(_genericClothes),_isSpecialist))
		sql.commit()
		textbox.delete('1.0', END)
		unitRoleEnt.delete(0, END)
		if(_enablePopups == True):
			messagebox.showinfo("Notice", "Arsenal Inserted Successfully!")
	else:
		messagebox.showinfo("Notice", "Unit Role is empty.")	
		
def submitGear(unit_side,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,cur,sql,enablePopups):
	_uniform = uniformEntry.get()
	_vests = vestEntry.get()
	_backpacks = backpackEntry.get()
	_helmets = helmetEntry.get()
	_glasses = glassesEntry.get()
	_enablePopups = enablePopups.get()
	if(_uniform != ""):
		cur.execute('INSERT INTO uniforms(uniform,gearSide) VALUES (?,?)', (str(_uniform),str(unit_side)))
		sql.commit()
	if(_vests != ""):
		cur.execute('INSERT INTO vests(vest,gearSide) VALUES (?,?)', (str(_vests),str(unit_side)))
		sql.commit()
	if(_backpacks != ""):
		cur.execute('INSERT INTO backpacks(backpack,gearSide) VALUES (?,?)', (str(_backpacks),str(unit_side))),
		sql.commit()   
	if(_helmets != ""):
		cur.execute('INSERT INTO helmets(helmet,gearSide) VALUES (?,?)', (str(_helmets),str(unit_side)))
		sql.commit()
	if(_glasses != ""):
		cur.execute('INSERT INTO glasses(glasses,gearSide) VALUES (?,?)', (str(_glasses),str(unit_side)))
		sql.commit()
	if(_enablePopups == True):
		messagebox.showinfo("Notice", "Gear Inserted Successfully!")

def generateGS(cur,sql,unit_side,unitAssociationToSideString,dataWindow):

	#initialises/resets values 
	#can't be in an __init__ due to needing to be run everytime a new set of sqf files is made
	_unit_side = unit_side
	varA = 0
	varB = 0
	varC = 0
	varD = 0
	varE = 0
	varF = 0

	with open('gearScript.sqf', 'w') as file:
		#clothes assignments
		#Uniforms
		file.write('_uniforms = ["')
		for row in cur.execute("SELECT * FROM uniforms"):
			value, gearSide = (row)
			if(gearSide == _unit_side):
				#will only trigger for first value
				if(varA == 0):
					varA = varA + 1 
					file.write(value)
				else:
					file.write('","')
					file.write(value)
		file.write('"];\n\n')  
		   
		#Vests
		file.write('_vests = ["')
		for row in cur.execute("SELECT * FROM vests"):
			value, gearSide = (row)
			if(gearSide == _unit_side):
				#will only trigger for first value
				if(varB == 0):
					varB = varB + 1 
					file.write(value)
				else:
					file.write('","')
					file.write(value)
		file.write('"];\n\n')  
		   
		#Helmets
		file.write('_helmets = ["')
		for row in cur.execute("SELECT * FROM helmets"):
			value, gearSide = (row)
			if(gearSide == _unit_side):
				#will only trigger for first alue
				if(varC == 0):
					varC = varC + 1 
					file.write(value)
				else:
					file.write('","')
					file.write(value)
		file.write('"];\n\n')  
		   
		#Glasses
		file.write('_goggles = ["')
		for row in cur.execute("SELECT * FROM glasses"):
			value, gearSide = (row)
			if(gearSide == _unit_side):
				#will only trigger for first value
				if(varD == 0):
					varD = varD + 1 
					file.write(value)
				else:
					file.write('","')
					file.write(value)
		file.write('"];\n\n')  
			
		#Backpacks
		file.write('_backpacks = ["')
		for row in cur.execute("SELECT * FROM backpacks"):
			value, gearSide = (row)
			if(gearSide == _unit_side):
				#will only trigger for first value
				if(varE == 0):
					varE = varE + 1 
					file.write(str(value))
				else:
					file.write('","')                       
					file.write(str(value))
		file.write('"];\n\n') 

		#Creates list for units that want to use generic clothes
		file.write('_genericUnits = ["')
		for row in cur.execute("SELECT * FROM units"):
			faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
			if(faction == _unit_side):
				if(genericClothes == "1"):
					#will only trigger for first value
					if(varF == 0):
						varF = varF + 1 
						file.write(str(unitRole))
					else:
						file.write('","')                       
						file.write(str(unitRole))
		file.write('"];\n\n') 

		file.write('_typesofUnit = toLower (_this select 0);\n')
		file.write('_unit = _this select 1; \n')
		file.write('removeBackpack _unit;\nremoveAllWeapons _unit;\nremoveAllItemsWithMagazines _unit;\nremoveAllAssignedItems _unit;\n')

		file.write('switch (_typeofUnit) do \n{\n')

		actualUnitSide = _unit_side
		for row in cur.execute("SELECT * FROM units"):
			faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
			if(faction == _unit_side):
				file.write('case "' + unitRole + '": {\n')
				file.write(arsenalPasteCode)
				print("Created unit: '" + unitRole + "' on '" + faction +"'")
				file.write('};\n\n')


		#default
		file.write('default {\n_unit addmagazines ["30Rnd_65x39_caseless_mag",7];\n_unit addweapon "arifle_MX_pointer_F";\n_unit selectweapon primaryweapon _unit;\n')
		file.write('if (true) exitwith {player globalchat format ["DEBUG: Unit = %1. Gear template %2 does not exist, used Rifleman instead.",_unit,_typeofunit]};\n};\n')
		
		#end closing bracket for switch statement
		file.write('};\n')

		#Add generic clothes in the sqf code
		file.write('if(_typeofUnit in _genericunits) then {\n_backpackItems = backpackItems _unit;\nremoveBackpack _unit;\n_unit addBackpack selectrandom _backpacks;\
			\n{_unit addItemToBackpack _x;} forEach _backpackItems;\n\n_vestitems = vestItems _unit;\nremoveVest _unit;\n_unit addvest selectRandom _vests;\
			\n{_unit addItemToVest _x;} forEach _vestitems;\n\n_uniformitems = uniformItems _unit;\nremoveUniform _unit;\n_unit forceAddUniform selectRandom \
			_uniforms;\n{_unit addItemToUniform _x;} forEach _uniformitems;\n\nremoveGoggles _unit;\n_unit addGoggles selectRandom _goggles;\n\nremoveHeadgear \
			_unit;\n_unit addHeadgear selectRandom _helmets;\n\n};')
		 
		file.close()
		replaceThis()
		renameFiles(actualUnitSide)
		generateFn_AssignGear(cur,sql,dataWindow,_unit_side,unitAssociationToSideString)

def generateFn_AssignGear(cur,sql,dataWindow,_unit_side,unitAssociationToSideString):
	createdSides = []

	with open('fn_assignGear.sqf', 'w') as file:
		file.write('private ["_faction","_typeofUnit","_unit"];\n\n')
		file.write('_typeofUnit = toLower (_this select 0);\n_unit = _this select 1;\n\n')
		file.write('_faction = toLower (faction _unit);\nif(count _this > 2) then\n{\n_faction = toLower (_this select 2);\n};')

		#Insignia setup 
		#WARNING -not even sure if this works, no guarantees 
		file.write('[_unit,_typeofUnit] spawn {\n#include "f_assignInsignia.sqf"\n};\n')
		
		file.write('if !(local _unit) exitWith {};\n')
		file.write('_unit setVariable ["f_var_assignGear",_typeofUnit,true];\n')
		factionList = []
		for row in cur.execute("SELECT * FROM units"):
			faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
			if faction not in factionList:
				factionList.append(faction)
				file.write('if (_faction == "' + faction + '") then {\n')
				file.write('#include "f_assignGear_' + faction + '.sqf"\n};\n')
		file.write('_unit setVariable ["f_var_assignGear_done",false,true];\n')
		file.close()
	
def replaceThis():
	f = open('gearScript.sqf','r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("this","_unit")
	f = open('gearScript.sqf','w')
	f.write(newdata)
	f.close()

	#Edge case(s)file edit for the one time you do want a 'this'
	f = open('gearScript.sqf','r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("_unit = __unit select 1; ","_unit = _this select 1; ")
	newerdata = filedata.replace("_typesofUnit = toLower (__unit select 0);","_typesofUnit = toLower (_this select 0);")
	f = open('gearScript.sqf','w')
	f.write(newdata)
	f.write(newerdata)
	f.close()

def renameFiles(actualUnitSide):
	try: 
		os.rename('gearScript.sqf','f_fnc_assignGear_' + actualUnitSide +'.sqf')
	except Exception as e:
	   print("An error occured in the file re-naming. File(s) probably already exist.")

def clearFiles():
	print("Removing old files...")	
	try:
		os.remove('gearScript.sqf')
	except OSError:
		pass

def clearVests(uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,enablePopups):
	uniformEntry.delete(0, END)
	vestEntry.delete(0, END)
	backpackEntry.delete(0, END)
	helmetEntry.delete(0, END)
	glassesEntry.delete(0, END)
	if(enablePopups.get() == 1):
		messagebox.showinfo("Notice", "Cleared Boxes.")

def gearToFaction(cur,sql,gearWindow):
	gearWindow.destroy()
	chooseSide(cur,sql)

def gearToUnit(cur,sql,unit_side,unitAssociationToSide,gearWindow):
	gearWindow.destroy()
	enterData(cur,sql,unit_side,unitAssociationToSide)

def UnitToFaction(cur,sql,dataWindow,unit_side):
	dataWindow.destroy()
	chooseSide(cur,sql,unit_side)

def platoonToFaction(cur,sql,platoonGenWindow,_unit_side):
	platoonGenWindow.destroy()
	chooseSide(cur,sql,_unit_side)

def platoonToGuns(platoonGenWindow,cur,sql,_unit_side,unitAssociationToSideString):
	platoonGenWindow.destroy()
	enterData(cur,sql,_unit_side,unitAssociationToSideString)

def closeGunWindow(dataWindow):
	dataWindow.destroy()

#Start of platoon Generator
def platoonGenStart(_unit_side,unitAssociationToSideString,dataWindow):
	closeGunWindow(dataWindow)
	sql = sqlite3.connect('unit_database.db')
	cur = sql.cursor()	
	platoonGenWindow = tk.Tk()
	platoonGenWindow.title("Framework Generator - Platoon Generator")
	platoonGenWindow.minsize(height=500, width=1000)
	platoonGenWindow.maxsize(height=500, width=1000)
	
	#Show what the side is that they entered in the start window
	unitsideLabel = Label(platoonGenWindow, text = 'Faction = ' + _unit_side, fg="blue",relief=RIDGE)
	unitsideLabel.place(relx=0, rely=0)

	unitsideLabel1 = Label(platoonGenWindow, text = 'Associated with = ' + unitAssociationToSideString, fg="blue",relief=RIDGE)
	unitsideLabel1.place(relx=0, rely=0.05)

	#Change Faction
	factionChangeButton = tk.Button(platoonGenWindow,text="Change Faction", fg="red", command=lambda: platoonToFaction(cur,sql,platoonGenWindow,_unit_side))
	factionChangeButton.place(relx=0, rely=0.10)
	
	#Change to guns window
	gunChangeButton = tk.Button(platoonGenWindow,text="Change to Guns", fg="red", command=lambda: platoonToGuns(platoonGenWindow,cur,sql,_unit_side,unitAssociationToSideString))
	gunChangeButton.place(relx=0, rely=0.15)
	
	#Get a list of all unique units in this faction
	listOfUnits = []
	for row in cur.execute("SELECT * FROM units"):
		faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
		if(faction ==_unit_side):
			if(unitRole not in listOfUnits):
				listOfUnits.append(unitRole)
	unitsideLabel1 = Label(platoonGenWindow, text = 'Units in this faction are:', fg="green",relief=RIDGE)
	unitsideLabel1.place(relx=0.85, rely=0.05)
	listOfUnitsLabel = Label(platoonGenWindow)
	listOfUnitsLabel.place(relx=0.9, rely=0.1)
	for val in listOfUnits:
		text = listOfUnitsLabel.cget("text") + val + '\n'
		listOfUnitsLabel.configure(text=text)

	coloursLabel1 = Label(platoonGenWindow, text = 'Colours:',relief=RIDGE)
	coloursLabel1.place(relx=0, rely=0.25)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorRed', fg="red")
	coloursLabel1.place(relx=0, rely=0.3)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorBlue', fg="blue")
	coloursLabel1.place(relx=0, rely=0.35)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorGreen', fg="Green")
	coloursLabel1.place(relx=0, rely=0.40)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorBlack', fg="black")
	coloursLabel1.place(relx=0, rely=0.45)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorGrey', fg="grey")
	coloursLabel1.place(relx=0, rely=0.50)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorBrown', fg="brown")
	coloursLabel1.place(relx=0, rely=0.55)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorOrange', fg="orange")
	coloursLabel1.place(relx=0, rely=0.6)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorYellow', fg="yellow", bg = "grey")
	coloursLabel1.place(relx=0, rely=0.65)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorKhaki', fg="khaki", bg = "grey")
	coloursLabel1.place(relx=0, rely=0.7)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorPink', fg="pink", bg = "grey")
	coloursLabel1.place(relx=0, rely=0.75)
	coloursLabel1 = Label(platoonGenWindow, text = 'ColorWhite', fg="white", bg = "grey")
	coloursLabel1.place(relx=0, rely=0.8)
	
	coloursLabel1 = Label(platoonGenWindow, text = 'Markers:',relief=RIDGE)
	coloursLabel1.place(relx=0.1, rely=0.25)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_hq = Headquarters')
	coloursLabel1.place(relx=0.1, rely=0.3)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_support = Support units (MMG,HMG)')
	coloursLabel1.place(relx=0.1, rely=0.35)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_motor_inf = Launchers (MAT, HAT)')
	coloursLabel1.place(relx=0.1, rely=0.4)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_mortar = Mortars')
	coloursLabel1.place(relx=0.1, rely=0.45)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_maint = Engineers')
	coloursLabel1.place(relx=0.1, rely=0.5)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_mech_inf = IFVs & APCs')
	coloursLabel1.place(relx=0.1, rely=0.55)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_armor = Tanks')
	coloursLabel1.place(relx=0.1, rely=0.6)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_recon = Recon')
	coloursLabel1.place(relx=0.1, rely=0.65)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_air = Helicopters')
	coloursLabel1.place(relx=0.1, rely=0.7)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_plane = Planes')
	coloursLabel1.place(relx=0.1, rely=0.75)
	coloursLabel1 = Label(platoonGenWindow, text = 'b_art = Artillery')
	coloursLabel1.place(relx=0.1, rely=0.8)

	
	squadLabel = Label(platoonGenWindow, text = "In the text box below, please define how you want your platoon to be set out.\n Init lines and marker files will automatically be generated for you. \n\n\
Rules for defining.\n\n All variables must be seperated by a comma (,). The end (and subsiquent start) of a new squad, is denoted by a colon (:). \nThe first variable in each squad is it's name (ASL/A1/A2 etc) \
The next is it's marker type, then followed by it's colour. \nValid inputs of these are listed to the left. After that, you define the units in the squad (again seperated by a comma)\n with the starting unit \
being the leader of the squad to which the marker will be attached too.\n\nExample input: ASL,b_hq,ColorYellow,sl,m:A1,b_hq,ColorBlue,ftl,m,r,r,r,ar,aar")
	squadLabel.place(relx=0.17, rely=0)
	textbox = Text(platoonGenWindow, width = 60, height = 15, wrap = WORD)
	textbox.place(relx=0.35, rely=0.35)
	passString = tk.Button(platoonGenWindow,text="Parse Platoon String", fg="red", command=lambda: parseSquadString(textbox,_unit_side,unitAssociationToSideString))
	passString.place(relx=0.6, rely=0.9, anchor=CENTER)

def parseSquadString(textbox,_unit_side,unitAssociationToSideString):
	sql = sqlite3.connect('unit_database.db')
	cur = sql.cursor()
	#Test input
	#ASL,b_hq,ColorYellow,sl,m:A1,b_hq,ColorBlue,ftl,m,r,r,r,ar,aar
	with open('unitsInit.txt', 'w') as file:
		inputText = textbox.get("1.0",'end-1c')
		squadList = inputText.split(":")
			
		#Converts the inputted string
		#Trust me this works, somehow...
		for squadString in squadList:
			squadString.split(",")
			indivdualSquads = squadString.split(",")
			squadName = indivdualSquads[0]
			indivdualSquads = indivdualSquads[3:]
			file.write("----------------------" + squadName + "----------------------\n")
			for member in indivdualSquads:
				file.write(_unit_side + "_" + squadName + '= group this; ["' + member + '",this,"' + _unit_side + '"] call fn_fnc_assignGear; ')
						
				#Opens DB
				for row in cur.execute("SELECT * FROM units"):
					faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
					if(faction ==_unit_side):
						if(unitRole == member):
							if(isSpecialist == "1"):
								file.write('missionNamespace setvariable ["' + _unit_side + '_' + squadName + '_' + unitRole + '",this,true]')
				file.write("\n")
	try: 
		os.rename('unitsInit.sqf',_unit_side + unitAssociationToSideString + '_Init.txt')
	except Exception as e:
	   print("An error occured in the file re-naming. File probably already exist. Overwriting...")

	with open('groupmarkers.txt', 'w') as file:	
		for squadString in squadList:
			squadString.split(",")
			indivdualSquads = squadString.split(",")
			squadName = indivdualSquads[0]
			markerType = indivdualSquads[1]
			markerColour = indivdualSquads[2]
			squadLeader = indivdualSquads[3]
			file.write('["' + _unit_side + '_' + squadName + '","' + markerType +'","' + squadName + squadLeader + '","'+  markerColour + '"] spawn f_fnc_localGroupMarker;\n')
			
		for squadString in squadList:
			squadString.split(",")
			indivdualSquads = squadString.split(",")
			squadName = indivdualSquads[0]
			indivdualSquads = indivdualSquads[3:]
			for member in indivdualSquads:						
				for row in cur.execute("SELECT * FROM units"):
					faction, unitRole, arsenalPasteCode, genericClothes, isSpecialist = (row)
					if(faction == _unit_side):
						if(unitRole == member):
							if(isSpecialist == "1"):
								file.write('["' + _unit_side + '_' + squadName + '_' + unitRole + '","' + markerType + '","' + squadName + unitRole + '","'+  markerColour + '"] spawn f_fnc_localSpecialistMarker;\n')
	try: 
		os.rename('groupmarkers.txt','f_setLocalGroupMarkers_'+unitAssociationToSideString +'.sqf')
	except Exception as e:
	   print("An error occured in the file re-naming. File probably already exists. Overwriting...")
if __name__ == "__main__":
	main()

