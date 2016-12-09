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
    cur.execute('CREATE TABLE IF NOT EXISTS units (faction varchar NOT NULL, unitRole varchar NOT NULL, arsenalPasteCode varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS uniforms (uniform varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS vests (vest varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS backpacks (backpack varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS helmets (helmet varchar NOT NULL,gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS glasses (glasses varchar NOT NULL, gearSide varchar NOT NULL)')
    sql.commit()
    clearFiles()
    chooseSide(cur,sql)
    
def chooseSide(cur,sql):
    sideWindow = tk.Tk()
    sideWindow.title("Framework Generator")
    sideWindow.minsize(140, 180)
    
    #Initalise Checkbox Variables
    unitAssociationToSide = IntVar()
    unitAssociationToSide.set(0)

    aboutLabel = Message(sideWindow, text = "GearScript Generator \nwritten by Matthew Betts with special thanks and contributions by . \n\nEnter a faction side \nand hit 'Submit' to begin.", fg="red")
    aboutLabel.grid(row=0, column=0)

    unitSideLabel = Label(sideWindow, text = "Enter Faction Name")
    unitSideLabel.grid(row=1, column=0)
    unitSideEntry = tk.Entry(sideWindow)
    unitSideEntry.grid(row=2, column=0)
    
    unitSideLabel = Label(sideWindow, text = "Unit is associated with:")
    unitSideLabel.grid(row=3, column=0)
    
    unitSideRadio =Radiobutton(sideWindow, variable=unitAssociationToSide, value = 0, text= "BLUFOR")
    unitSideRadio.grid(row=4, column=0)
    unitSideRadio =Radiobutton(sideWindow, variable=unitAssociationToSide, value = 1, text= "OPFOR")
    unitSideRadio.grid(row=5, column=0)
    unitSideRadio =Radiobutton(sideWindow, variable=unitAssociationToSide, value = 2, text= "INDFOR")
    unitSideRadio.grid(row=6, column=0)

    chooseSideButton = tk.Button(sideWindow,text="Submit",command=lambda: closeSideWindow(sideWindow,cur,sql,unitSideEntry,unitAssociationToSide))
    chooseSideButton.grid(row=7, column=0)

    blankLabel = Label(sideWindow, text = "                  ")
    blankLabel.grid(row=8, column=0)

    sideWindow.mainloop()
    
def closeSideWindow(sideWindow,cur,sql,unitSideEntry,unitAssociationToSide):
    #get the side of the unit
    unit_side = unitSideEntry.get()

    #checks for if it's empty or contains spaces, if so returns to chooseSide()
    if(unit_side == ""):
        messagebox.showinfo("Notice", "Faction name is empty. Please fill and resubmit.")
        sideWindow.destroy()
        chooseSide(cur,sql)
    elif (" " in unit_side or "." in unit_side):
        messagebox.showinfo("Notice", "Faction name contains space. Please remove space and resubmit.")
        sideWindow.destroy()
        chooseSide(cur,sql)
    else:
        #if no problems arise, continue to enterData()
        sideWindow.destroy()
        unitAssociationToSideString = ""
        if(unitAssociationToSide.get() == 0):
            unitAssociationToSideString = "BLUFOR"
        if(unitAssociationToSide.get() == 1):
            unitAssociationToSideString = "OPFOR"
        if(unitAssociationToSide.get() == 2):
           unitAssociationToSideString = "INDFOR"
        enterData(cur,sql,unit_side,unitAssociationToSideString)
        
def enterData(cur,sql,unit_side,unitAssociationToSideString):
    dataWindow = tk.Tk()
    dataWindow.title("Framework Generator")
    
    #Initalise Checkbox Variables
    isGeneric = IntVar()
    isGeneric.set(0)
    
    #Show what the side is that they entered in the previous window
    unitsideLabel = Label(dataWindow, text = 'Faction = ' + unit_side, fg="red",relief=RIDGE)
    unitsideLabel.grid(row=0, column=0)
    unitsideLabel = Label(dataWindow, text = 'Associated with = ' + unitAssociationToSideString, fg="red",relief=RIDGE)
    unitsideLabel.grid(row=1, column=0)

    #Unit role
    unitRoleLabel = Label(dataWindow, text = "Unit Role (r/ar etc)")
    unitRoleLabel.grid(row=3, column=0)
    unitRoleEnt = tk.Entry(dataWindow)
    unitRoleEnt.grid(row=3, column=1)
    
    #Check if unit is using generic clothes for faction
    isGenericClothes = Checkbutton(dataWindow, variable=isGeneric, onvalue = 1, offvalue = 0, text= "Generic Clothes?")
    isGenericClothes.grid(row=4, column=0)

    enterGearButton = tk.Button(dataWindow, text="Insert Clothes", fg="red", command=lambda: enterGear(unit_side,cur,sql,dataWindow,unitAssociationToSideString))
    enterGearButton.grid(row=5, column=0)

    aboutLabel = Message(dataWindow, text = "Note: 'Generic clothes' are a set of vests/uniforms etc that are randomly selected from the ones that you can manually enter. If the box is ticked when a unit is submitted, generic clothes are given to it. This overwrites the clothes that are already given to it.", fg="red")
    aboutLabel.grid(row=6, column=0)
    
    pasteArsenalLabel = Label(dataWindow, text = 'Paste Arsenal Code Here: ', fg="red")
    pasteArsenalLabel.grid(row=5, column=2)
    
    textbox = Text(dataWindow, width = 75, height = 10, wrap = WORD)
    textbox.grid(row=6, column=2, columnspan=1, sticky=W)

    #Change Faction
    factionChangeButton = tk.Button(dataWindow,text="Change Faction", fg="red", command=lambda: UnitToFaction(cur,sql,dataWindow))
    factionChangeButton.grid(row=0, column=1)

    submitArsenalButton = tk.Button(dataWindow,text="Submit Arsenal",command=lambda: submitArsenal(cur,sql,textbox,unit_side,unitRoleEnt))
    submitArsenalButton.grid(row=7, column=2, sticky=W)

    createGSButton = tk.Button(dataWindow,text="Generate GearScript",command=lambda: generateGS(cur,sql,unit_side,unitAssociationToSideString))
    createGSButton.grid(row = 8, column = 2)

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
    submitGearButton = tk.Button(gearWindow,text="Submit Clothes",command=lambda: submitGear(unit_side,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,cur,sql,enablePopups))
    submitGearButton.grid(row=6, column=2, sticky=W)

    #Change Faction
    factionChangeButton = tk.Button(gearWindow,text="Change Faction", fg="red", command=lambda: gearToFaction(cur,sql,gearWindow))
    factionChangeButton.grid(row=0, column=3, sticky=W)
    #Change to guns window
    gunChangeButton = tk.Button(gearWindow,text="Change to Guns", fg="red", command=lambda: gearToUnit(cur,sql,unit_side,unitAssociationToSideString,gearWindow))
    gunChangeButton.grid(row=1, column=3, sticky=W)

    clearBoxesButton2 = tk.Button(gearWindow,text="Clear All Boxes",command=lambda: clearVests(uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,enablePopups))
    clearBoxesButton2.grid(row=2, column=3, sticky=W)

def submitArsenal(cur,sql,textbox,unit_side,unitRoleEnt):
    _unit_side = unit_side
    _unit_role = unitRoleEnt.get()
    _arsenal = textbox.get("1.0",'end-1c')
    if(_unit_role != ""):
        cur.execute('INSERT INTO units(faction, unitRole, arsenalPasteCode) VALUES (?,?,?)',(str(_unit_side),str(_unit_role),str(_arsenal)))
        sql.commit()
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

def generateGS(cur,sql,unit_side,unitAssociationToSideString):

    #initialises/resets values 
    #can't be in an __init__ due to needing to be run everytime a new set of sqf files is made
    _unit_side = unit_side
    varA = 0
    varB = 0
    varC = 0
    varD = 0
    varE = 0

    with open('gearScript.sqf', 'w') as file:
        #clothes assignments
        #Uniforms
        file.write('_uniform = ["')
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
        file.write('_rig = ["')
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
        file.write('_helmet = ["')
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
        file.write('_glasses = ["')
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
                    varE = varD + 1 
                    file.write(str(value))
                else:
                    file.write('","')                       
                    file.write(str(value))
        file.write('"];\n\n') 
        file.write('_typesofUnit = toLower (_this select 0);\n')
        file.write('_unit = _this select 1; \n')
        file.write('removeBackpack _unit;\nremoveAllWeapons _unit;\nremoveAllItemsWithMagazines _unit;\nremoveAllAssignedItems _unit;\n')

        file.write('switch (_typeofUnit) do \n{\n')

        for row in cur.execute("SELECT * FROM units"):
            faction, unitRole, arsenalPasteCode = (row)
            if(faction == _unit_side):
                actualUnitSide = faction
                file.write('case "' + unitRole + '": {\n')
                file.write(arsenalPasteCode)
                print("Created unit: '" + unitRole + "' on '" + faction +"'")
                file.write('};\n\n')

        #default
        file.write('default {\n_unit addmagazines ["30Rnd_65x39_caseless_mag",7];\n_unit addweapon "arifle_MX_pointer_F";\n_unit selectweapon primaryweapon _unit;\n')
        file.write('if (true) exitwith {player globalchat format ["DEBUG: Unit = %1. Gear template %2 does not exist, used Rifleman instead.",_unit,_typeofunit]};\n};\n')
        #end closing bracket
        file.write('};\n')
        file.close()
        replaceThis()
        renameFiles(actualUnitSide)
        generateFn_AssignGear(cur)

def generateFn_AssignGear(cur):
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
        for row in cur.execute("SELECT * FROM units"):
            faction, unitRole, arsenalPasteCode = (row)
            file.write('if (_faction == "' + faction + '") then {\n')
            file.write('#include "f_assignGear_' + faction + '.sqf"\n};\n')
        file.write('_unit setVariable ["f_var_assignGear_done",false,true];\n')
		
def replaceThis():
    f = open('gearScript.sqf','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("this","_unit")
    f = open('gearScript.sqf','w')
    f.write(newdata)
    f.close()

def renameFiles(actualUnitSide):
    try: 
        os.rename('gearScript.sqf','f_assignGear_' + actualUnitSide +'.sqf')
    except Exception as e:
       print("An error occured in the file re-naming. Files probably already exist.")

def clearFiles():
 	print("Removing old files...")
 	try:
 		os.remove('default.sqf')
 	except OSError:
 		pass
 
 	try:
 		os.remove('default_b.sqf')
 	except OSError:
 		pass
 	
 	try:
 		os.remove('gearScript.sqf')
 	except OSError:
 		pass
 
 	try:
 		os.remove('gearScript_b.sqf')
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

def UnitToFaction(cur,sql,dataWindow):
    dataWindow.destroy()
    chooseSide(cur,sql)

if __name__ == "__main__":
    main()

           