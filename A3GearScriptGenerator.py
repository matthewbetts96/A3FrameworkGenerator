import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

#Start function
def start():
    print("Starting up Database")
    sql = sqlite3.connect('unit_database.db')
    cur = sql.cursor()
    print("Creating database if it doesn't exist")
    cur.execute('CREATE TABLE IF NOT EXISTS units (main_weapon varchar NOT NULL, main_ammo varchar NOT NULL, secondary_weapon varchar NOT NULL, secondary_ammo varchar NOT NULL, sidearm_weapon varchar NOT NULL, sidearm_ammo varchar NOT NULL, unit_name varchar NOT NULL, unit_side varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS uniforms (uniform varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS vests (vest varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS backpacks (backpack varchar NOT NULL, gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS helmets (helmet varchar NOT NULL,gearSide varchar NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS glasses (glasses varchar NOT NULL, gearSide varchar NOT NULL)')
    sql.commit()
    clearFiles()
    generateGUI(cur,sql)

#Generates the UI
def generateGUI(cur,sql):
    root = tk.Tk()
    root.title("Framework Generator")
 

    #Main Weapon
    label1 = Label(root, text = "Main Weapon")
    label1.grid(row=1, column=1, sticky=W)
    e1 = tk.Entry(root)
    e1.grid(row=1, column=2)
 
    #Main Weapon Ammo
    label2 = Label(root, text = "Main Ammo")
    label2.grid(row=2, column=1, sticky=W)
    e2 = tk.Entry(root)
    e2.grid(row=2, column=2)
 
    #Secondary Weapon
    label3 = Label(root, text = "Secondary Weapon")
    label3.grid(row=3, column=1, sticky=W)
    e3 = tk.Entry(root)
    e3.grid(row=3, column=2)
 
    #Secondary Weapon Ammo
    label4 = Label(root, text = "Secondary Ammo")
    label4.grid(row=4, column=1, sticky=W)
    e4 = tk.Entry(root)
    e4.grid(row=4, column=2)
 
    #Sidearm Weapon
    label5 = Label(root, text = "Sidearm")
    label5.grid(row=5, column=1, sticky=W)
    e5 = tk.Entry(root)
    e5.grid(row=5, column=2)
 
    #Sidearm Ammo
    label6 = Label(root, text = "Sidearm Ammo")
    label6.grid(row=6, column=1, sticky=W)
    e6 = tk.Entry(root)
    e6.grid(row=6, column=2)
 
    #Unit name
    label7 = Label(root, text = "Unit name (r/ar etc)")
    label7.grid(row=7, column=1, sticky=W)
    e7 = tk.Entry(root)
    e7.grid(row=7, column=2)

    #Unit side
    label8 = Label(root, text = "Unit side (MUST BE FILLED)")
    label8.grid(row=0, sticky=W)
    e8 = tk.Entry(root)
    e8.grid(row=0, column=1)
 
    #Uniform
    label9 = Label(root, text = "Uniform")
    label9.grid(row=0, column=5, sticky=W)
    e9 = tk.Entry(root)
    e9.grid(row=0, column=6)
 
    #Vest
    label10 = Label(root, text = "Vest")
    label10.grid(row=1, column=5, sticky=W)
    e10 = tk.Entry(root)
    e10.grid(row=1, column=6)
 
    #Backpacks
    label11 = Label(root, text = "Backpack")
    label11.grid(row=2, column=5, sticky=W)
    e11 = tk.Entry(root)
    e11.grid(row=2, column=6)
 
    #HeadGear (Helmets)
    label12 = Label(root, text = "HeadGear (Helmets)") 
    label12.grid(row=3, column=5, sticky=W)
    e12 = tk.Entry(root)
    e12.grid(row=3, column=6)
 
    #HeadGear (Glasses)
    label13 = Label(root, text = "HeadGear (Glasses)") 
    label13.grid(row=4, column=5, sticky=W)
    e13 = tk.Entry(root)
    e13.grid(row=4, column=6)
   
 
 
    submitButton = tk.Button(root,text="Submit Gear",command=lambda: submitGear(e7,e9,e10,e11,e12,e13,cur,sql))
    submitButton.grid(row=6, column=6, sticky=W)
 
    submitButton = tk.Button(root,text="Submit Weapons",command=lambda: submitWeapons(cur,sql,e1,e2,e3,e4,e5,e6,e7,e8))
    submitButton.grid(row=8, column=1, sticky=W)
 
    clearAll = tk.Button(root,text="Clear All Boxes",command=lambda: clearboxes(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13))
    clearAll.grid(row=9, column=1, sticky=W)
 
    generateGearScript = tk.Button(root,text="Generate Gear Script",command=lambda: gearScriptSetUp(cur))
    generateGearScript.grid(row=10, column=1, sticky=W)
 
    root.mainloop()
 
#Collects the weapon and stores in db for later use
def submitWeapons(cur,sql,e1,e2,e3,e4,e5,e6,e7,e8):
    main_weapon = e1.get()
    main_ammo = e2.get()
    secondary_weapon = e3.get()
    secondary_ammo = e4.get()
    sidearm_weapon = e5.get()
    sidearm_ammo = e6.get()
    unit_name = e7.get()
    unit_side = e8.get()
    cur.execute('INSERT INTO units(main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side) VALUES (?,?,?,?,?,?,?,?)',(str(main_weapon),str(main_ammo),str(secondary_weapon),str(secondary_ammo),str(sidearm_weapon),str(sidearm_ammo),str(unit_name),str(unit_side)))
    print('Inserted unit ' + unit_name + ' on ' + unit_side + ' side.')
    sql.commit()
    #messagebox.showinfo("Notice", "Weapons Inserted Successfully!")
 
#Collects all the clothes gear and stores them in the db for later use
#Due to not all fields being entered at once it only executes when entry box is not empty
def submitGear(e7,e9,e10,e11,e12,e13,cur,sql):
    m_uniform = e9.get()
    m_vests = e10.get()
    m_backpacks = e11.get()
    m_helmets = e12.get()
    m_glasses = e13.get()
    gearSide = e7.get()
    if(m_uniform != ""):
        cur.execute('INSERT INTO uniforms(uniform,gearSide) VALUES (?,?)', (str(m_uniform),str(gearSide)))
        sql.commit()
    if(m_vests != ""):
        cur.execute('INSERT INTO vests(vest,gearSide) VALUES (?,?)', (str(m_vests),str(gearSide)))
        sql.commit()
    if(m_backpacks != ""):
        cur.execute('INSERT INTO backpacks(backpack,gearSide) VALUES (?,?)', (str(m_backpacks),str(gearSide))),
        sql.commit()   
    if(m_helmets != ""):
        cur.execute('INSERT INTO helmets(helmet,gearSide) VALUES (?,?)', (str(m_helmets),str(gearSide)))
        sql.commit()
    if(m_glasses != ""):
        cur.execute('INSERT INTO glasses(glasses,gearSide) VALUES (?,?)', (str(m_glasses),str(gearSide)))
        sql.commit()
   
 
def clearboxes(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
    e8.delete(0, END)
    e9.delete(0, END)
    e10.delete(0, END)
    e11.delete(0, END)
    e12.delete(0, END)
    e13.delete(0, END)
    print("Cleared Boxes.")
    messagebox.showinfo("Notice", "Cleared Boxes.")
 
def gearScriptSetUp(cur):
    gearScriptWindow = tk.Tk()
    gearScriptWindow.title("Framework Generator")
 
    label1 = Label(gearScriptWindow, text = "Side (blu/red etc)")
    label1.grid(row=0, sticky=W)
    f1 = tk.Entry(gearScriptWindow)
    f1.grid(row=0, column=1)
 
    #Map? (y/n)
    label2 = Label(gearScriptWindow, text = "Map? (y/n)")
    label2.grid(row=1, sticky=W)
    f2 = tk.Entry(gearScriptWindow)
    f2.grid(row=1, column=1)
 
    #NVG's? (y/n)
    label3 = Label(gearScriptWindow, text = "NVG's? (y/n)")
    label3.grid(row=2, sticky=W)
    f3 = tk.Entry(gearScriptWindow)
    f3.grid(row=2, column=1)
 
    #Radio? (y/n)
    label4 = Label(gearScriptWindow, text = "Radio? (y/n)")
    label4.grid(row=3, sticky=W)
    f4 = tk.Entry(gearScriptWindow)
    f4.grid(row=3, column=1)
 
    #Compass
    label5 = Label(gearScriptWindow, text = "Compass? (y/n)")
    label5.grid(row=4, sticky=W)
    f5 = tk.Entry(gearScriptWindow)
    f5.grid(row=4, column=1)
 
    #Watch? (y/n)
    label6 = Label(gearScriptWindow, text = "Watch? (y/n)")
    label6.grid(row=5, sticky=W)
    f6 = tk.Entry(gearScriptWindow)
    f6.grid(row=5, column=1)
 
    #GPS? (y/n)
    label7 = Label(gearScriptWindow, text = "GPS? (y/n)")
    label7.grid(row=6, sticky=W)
    f7 = tk.Entry(gearScriptWindow)
    f7.grid(row=6, column=1)
 
    generateGearScript = tk.Button(gearScriptWindow,text="Generate Gear Script",command=lambda: GenerateGearScript(cur,f1,f2,f3,f4,f5,f6,f7))
    generateGearScript.grid(row=10, column=1, sticky=W)
 
 
def GenerateGearScript(cur,f1,f2,f3,f4,f5,f6,f7):
    unitSide = f1.get()
    includeMap = f2.get()
    includeNVG = f3.get()
    includeRadio = f4.get()
    includeCompass = f5.get()
    includeWatch = f6.get()
    includeGPS = f7.get()

    #initialises/resets values 
    varA = 0
    varB = 0
    varC = 0
    varD = 0
    varE = 0
 
    with open('gearScript.sqf', 'w') as file:
 
        #TFR radio backpack
        file.write('if(f_var_radios == 2) then {\n')
        file.write('_bagradio =')
 
        #if they aren't red/csat/aaf or ind give them a blufor radio
        if(unitSide == "aaf"):
            file.write('TF_defaultGuerBackpack;\n')
        elif(unitSide == "ind"):
            file.write('TF_defaultGuerBackpack;\n')
        elif(unitSide == "csat"):
            file.write('TF_defaultEastBackpack;\n')
        elif(unitSide == "red"):
            file.write('TF_defaultEastBackpack;\n')
        else:
            file.write('TF_defaultWestBackpack;\n')
 
        file.write('f_radios_settings_tfr_backpackRadios = ["co","dc"];\n')
        file.write('if(_typeOfUnit in f_radios_settings_tfr_backpackRadios) then {\n_bagsmall = _bagradio;\n_bagmedium = _bagradio;\n_baglarge = _bagradio;\n};\n};\n\n')
       
        #clothes assignments
        #Uniforms
        file.write('_baseUniform = ["')
        for row in cur.execute("SELECT * FROM uniforms"):
            insertValue, gearSide = (row)
            if(gearSide == unitSide):
            	#will only trigger for first value
                if(varA == 0):
                    varA = varA + 1 
                    file.write(str(insertValue))
                else:
                    file.write('","')
                    file.write(str(insertValue))
        file.write('"];\n\n')  
       
       	#Vests
        file.write('_mediumRig = ["')
        for row in cur.execute("SELECT * FROM vests"):
            insertValue, gearSide = (row)
            if(gearSide == unitSide):
            	#will only trigger for first value
                if(varB == 0):
                    varB = varB + 1 
                    file.write(str(insertValue))
                else:
                    file.write('","')
                    file.write(str(insertValue))
        file.write('"];\n\n')  
       
        #Helmets
        file.write('_baseHelmet = ["')
        for row in cur.execute("SELECT * FROM helmets"):
            insertValue, gearSide = (row)
            if(gearSide == unitSide):
            	#will only trigger for first value
                if(varC == 0):
                    varC = varC + 1 
                    file.write(str(insertValue))
                else:
                    file.write('","')
                    file.write(str(insertValue))
        file.write('"];\n\n')  
       
        #Glasses
        file.write('_baseGlasses = ["')
        for row in cur.execute("SELECT * FROM glasses"):
            insertValue, gearSide = (row)
            if(gearSide == unitSide):
            	#will only trigger for first value
                if(varD == 0):
                    varD = varD + 1 
                    file.write(str(insertValue))
                else:
                    file.write('","')
                    file.write(str(insertValue))
        file.write('"];\n\n')  
        
        #Backpacks
        file.write('_backpacks = ["')
        for row in cur.execute("SELECT * FROM backpacks"):
            insertValue, gearSide = (row)
            if(gearSide == unitSide):
            	#will only trigger for first value
                if(varE == 0):
                    varE = varD + 1 
                    file.write(str(insertValue))
                else:
                    file.write('","')
                    file.write(str(insertValue))
        file.write('"];\n\n') 
       
        file.write('_typesofUnit = toLower (_this select 0);\n')
        file.write('_unit = _this select 1; \n')
        file.write('_isMan = _unit isKindOf "CAManBase";\n\n')
        file.write('if (_isMan) then {\n')
        file.write('removeBackpack _unit;\nremoveAllWeapons _unit;\nremoveAllItemsWithMagazines _unit;\nremoveAllAssignedItems _unit;\n')
        file.write('#include "f_assignGear_clothes.sqf";\n\n')
        file.write('_unit addItem "FirstAidKit";\n')
       
        if(includeMap == "y"):
            file.write('_unit linkItem "ItemMap";\n')
        if(includeNVG == "y"):
            file.write('_unit linkItem "NVGoggles";\n')
        if(includeRadio == "y"):
            file.write('_unit linkItem "ItemRadio";\n')
        if(includeCompass == "y"):
            file.write('_unit linkItem "ItemCompass";\n')
        if(includeWatch == "y"):
            file.write('_unit linkItem "ItemWatch";\n')
        if(includeGPS == "y"):
            file.write('_unit linkItem "ItemGPS"; \n')
        file.write('};\n\n')
 
        #backpack setup for each faction
        file.write('_backpack = {\n_typeofBackPack = _this select 0;\n_loadout = f_param_backpacks;\nif (count _this > 1) then {_loadout = _this select 1};\nswitch (_typeofBackPack) do\n{\n')
        file.write('#include "f_assignGear_' + unitSide +'_b.sqf";\n')
        file.write('};\n};\n\n')

        file.write('switch (_typeofUnit) do \n{\n')
        
        #need to define it before use
        actualUnitSide = "default"

        #Build switch statements for unit weapons
        for row in cur.execute("SELECT * FROM units"):
            main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side = (row)
            if(unit_side == unitSide): 

                #Fix for when it was overriding unitside on the last pass
                actualUnitSide = unitSide
                file.write('case "' + unit_name + '": {\n')
 
                #add main weapon + ammo
                file.write('_unit addmagazines ["' + main_ammo + '",4];\n')
                file.write('_unit addweapon "' + main_weapon + '";\n')
 
                #add secondary weapon + ammo
                file.write('_unit addmagazines ["' + secondary_ammo + '",2];\n')
                file.write('_unit addweapon "' + secondary_weapon + '";\n')
 
                #add sidearm + ammo
                file.write('_unit addmagazines ["' + sidearm_ammo + '",5];\n')
                file.write('_unit addweapon "' + sidearm_weapon + '";\n')
 
                #add other items
                file.write('_unit addmagazines ["HandGrenade",2];\n')
                file.write('_unit addmagazines ["ACE_M84",2];\n')
                file.write('_unit addmagazines ["SmokeShell",4];\n')
                file.write('_unit addmagazines ["FirstAidKit",4];\n')

                file.write('["' + unit_name +'"] call _backpack;')
                file.write('};\n\n')
                print('Created unit ' + unit_name + ' on ' + actualUnitSide + ' side.')
       
        #default
        file.write('default {\n_unit addmagazines ["30Rnd_65x39_caseless_mag",7];\n_unit addweapon "arifle_MX_pointer_F";\n_unit selectweapon primaryweapon _unit;\n')
        file.write('if (true) exitwith {player globalchat format ["DEBUG: Unit = %1. Gear template %2 does not exist, used Rifleman instead.",_unit,_typeofunit]};\n};\n')
        #end closing bracket
        file.write('};\n')
        file.close()
        GenerateBackpackScript(cur,actualUnitSide)

#Generates Backpack sqf file
def GenerateBackpackScript(cur,actualUnitSide):
	with open('gearScript_b.sqf', 'w') as file:  
		for row in cur.execute("SELECT * FROM units"):
			main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side = (row)
			if(unit_side == actualUnitSide): 
				file.write('m_backpack = (_backpacks call BIS_fnc_selectRandom);')
				file.write('case "' + unit_name + '": {\n')
				file.write('_unit addBackpack m_backpack;\n')
				file.write('clearMagazineCargoGlobal (unitBackpack _unit);\n')
				file.write('(unitBackpack _unit) addItemCargoGlobal ["HandGrenade",2];\n(unitBackpack _unit) addMagazineCargoGlobal ["SmokeShell", 2];\n(unitBackpack _unit) addItemCargoGlobal ["FirstAidKit", 4];\n')
				file.write('(unitBackpack _unit) addMagazineCargoGlobal ["' + main_ammo + '", 6];')
				file.write('};')
	file.close()
	generateFn_AssignGear(cur)
	renameFiles(actualUnitSide)

#remanmes files dependant on the side
def renameFiles(actualUnitSide):
	os.rename('gearScript.sqf','f_assignGear_' + actualUnitSide +'.sqf')
	os.rename('gearScript_b.sqf','f_assignGear_' + actualUnitSide +'_b.sqf')


def generateFn_AssignGear(cur):
    #Creates
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
        file.write('private ["_attach1","_attach2","_silencer1","_silencer2","_scope1","_scope2","_scope3","_bipod1","_bipod2","_attachments","_silencer","_hg_silencer1","_hg_scope1","_hg_attachments",')
        file.write('"_typeofUnit","_unit","_isMan","_backpack","_typeofBackPack","_loadout","_typeofunit"];\n')
        for row in cur.execute("SELECT * FROM units"):
            main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side = (row)
            file.write('if (_faction == "' + unit_side + '") then {\n')
            file.write('#include "f_assignGear_' + unit_side + '.sqf"\n};\n')

        file.write('_unit setVariable ["f_var_assignGear_done",false,true];\n')

#Removes default files
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

if __name__ == "__main__":
    start()
