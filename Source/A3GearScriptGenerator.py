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
    cur.execute('CREATE TABLE IF NOT EXISTS units (main_weapon varchar NOT NULL, main_ammo varchar NOT NULL, main_sight varchar NOT NULL, main_barrel varchar NOT NULL, main_bipod varchar NOT NULL, main_other varchar NOT NULL, sec_weapon varchar NOT NULL, sec_ammo varchar NOT NULL, sec_sight varchar NOT NULL, side_weapon varchar NOT NULL, side_ammo varchar NOT NULL, side_sight varchar NOT NULL, side_barrel varchar NOT NULL, unit_name varchar NOT NULL, unit_side varchar NOT NULL, unit_command varchar NOT NULL, unit_medic varchar NOT NULL)')
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

    #Initalise tkinter window
    root = tk.Tk()
    root.title("Framework Generator")

    #Initalise Variables
    isMedic = IntVar()
    isMedic.set(0)

    isCommander = IntVar()
    isCommander.set(0)

    hasMap = IntVar()
    hasMap.set(0)

    hasNVG = IntVar()
    hasNVG.set(0)

    hasRadio = IntVar()
    hasRadio.set(0)

    hasCompass = IntVar()
    hasCompass.set(0)

    hasWatch = IntVar()
    hasWatch.set(0)

    hasGPS = IntVar()
    hasGPS.set(0)

    #Unit side
    unitSideLabel = Label(root, text = "Unit side")
    unitSideLabel.grid(row=0, column=0, sticky=W)
    unitSideEntry = tk.Entry(root)
    unitSideEntry.grid(row=0, column=1)

    #Unit name
    unitNameLabel = Label(root, text = "Unit name (r/ar etc)")
    unitNameLabel.grid(row=1, column=0, sticky=W)
    unitNameEntry = tk.Entry(root)
    unitNameEntry.grid(row=1, column=1)

    #Check if unit is going to get more medical suppiles 
    isMedicCheckbox = Checkbutton(root, variable=isMedic, onvalue = 1, offvalue = 0, text= "Is Medic?")
    isMedicCheckbox.grid(row=2, column=1)

    #Check if unit is going to get LR radio
    #Commenting this out for now, will include at a later date
    isCommanderCheckbox = Checkbutton(root, variable=isCommander, onvalue = 1, offvalue = 0, text= "Is Commander?")
    #isCommanderCheckbox.grid(row=3, column=1)

    #Main Weapon
    mainWepLabel = Label(root, text = "Main Weapon")
    mainWepLabel.grid(row=4, column=0)
    mainWepEntry = tk.Entry(root)
    mainWepEntry.grid(row=4, column=1)
 
    #Main Weapon Ammo
    mainAmmoLabel = Label(root, text = "Main Ammo")
    mainAmmoLabel.grid(row=5, column=0)
    mainAmmoEntry = tk.Entry(root)
    mainAmmoEntry.grid(row=5, column=1)
 
    #It doesn't actually matter if they have the wrong attachment in the slots, it's all added the same in sqf
    #Main Weapon Sight
    mainWepSight = Label(root, text = "Sight")
    mainWepSight.grid(row=6, column=0)
    mainWepSightEnt = tk.Entry(root)
    mainWepSightEnt.grid(row=6, column=1)

    #Main Weapon Barrel 
    mainWepBar = Label(root, text = "Barrel")
    mainWepBar.grid(row=7, column=0)
    mainWepBarEnt = tk.Entry(root)
    mainWepBarEnt.grid(row=7, column=1)

    #Main Weapon Bipod 
    mainWepBip = Label(root, text = "Bipod")
    mainWepBip.grid(row=8, column=0)
    mainWepBipEnt = tk.Entry(root)
    mainWepBipEnt.grid(row=8, column=1)

    #Any other attachments 
    mainWepOther = Label(root, text = "Other attachments")
    mainWepOther.grid(row=9, column=0)
    mainWepOtherEnt = tk.Entry(root)
    mainWepOtherEnt.grid(row=9, column=1)

    #Secondary Weapon
    secWepLabel = Label(root, text = "Secondary Weapon")
    secWepLabel.grid(row=4, column=2)
    secWepEntry = tk.Entry(root)
    secWepEntry.grid(row=4, column=3)
 
    #Secondary Weapon Ammo
    secAmmoLabel = Label(root, text = "Secondary Ammo")
    secAmmoLabel.grid(row=5, column=2)
    secAmmoEntry = tk.Entry(root)
    secAmmoEntry.grid(row=5, column=3)
   
    #Secondary Weapon Sight
    secWepSight = Label(root, text = "Sight")
    #secWepSight.grid(row=6, column=2) #Commenting this out for now, will include at a later date
    secWepSightEnt = tk.Entry(root)
    #secWepSightEnt.grid(row=6, column=3)

    #Sidearm Weapon
    sideWepLabel = Label(root, text = "Sidearm")
    sideWepLabel.grid(row=4, column=4)
    sideWepEntry = tk.Entry(root)
    sideWepEntry.grid(row=4, column=5)
 
    #Sidearm Ammo
    sideAmmoLabel = Label(root, text = "Sidearm Ammo")
    sideAmmoLabel.grid(row=5, column=4)
    sideAmmoEntry = tk.Entry(root)
    sideAmmoEntry.grid(row=5, column=5)

    #Sidearm Weapon Sight
    sideWepSight = Label(root, text = "Sight")
    sideWepSight.grid(row=6, column=4)
    sideWepSightEnt = tk.Entry(root)
    sideWepSightEnt.grid(row=6, column=5)

    #Sidearm Weapon Barrel 
    sideWepBar = Label(root, text = "Barrel")
    sideWepBar.grid(row=7, column=4)
    sideWepBarEnt = tk.Entry(root)
    sideWepBarEnt.grid(row=7, column=5)

    #Submit Unit button
    submitUnitButton = tk.Button(root,text="Submit Unit",command=lambda: submitUnit(unitSideEntry,unitNameEntry,mainWepEntry,mainAmmoEntry,mainWepSightEnt,mainWepBarEnt,mainWepBipEnt,mainWepOtherEnt,secWepEntry,secAmmoEntry,secWepSightEnt,sideWepEntry,sideAmmoEntry,sideWepSightEnt,sideWepBarEnt,isCommander,isMedic,cur,sql))
    submitUnitButton.grid(row=10, column=2, sticky=W)

    #Blank gap
    Blank = Label(root, text = "")
    Blank.grid(row=11, column=0)
 
    #Uniform
    uniformLabel = Label(root, text = "Uniform")
    uniformLabel.grid(row=12, column=0)
    uniformEntry = tk.Entry(root)
    uniformEntry.grid(row=12, column=1)
 
    #Vest
    vestLabel = Label(root, text = "Vest")
    vestLabel.grid(row=13, column=0)
    vestEntry = tk.Entry(root)
    vestEntry.grid(row=13, column=1)
 
    #Backpacks
    backpackLabel = Label(root, text = "Backpack")
    backpackLabel.grid(row=14, column=0)
    backpackEntry = tk.Entry(root)
    backpackEntry.grid(row=14, column=1)
 
    #HeadGear (Helmets)
    helmetLabel = Label(root, text = "HeadGear (Helmets)") 
    helmetLabel.grid(row=15, column=0)
    helmetEntry = tk.Entry(root)
    helmetEntry.grid(row=15, column=1)
 
    #HeadGear (Glasses)
    glassesLabel = Label(root, text = "HeadGear (Glasses)") 
    glassesLabel.grid(row=16, column=0)
    glassesEntry = tk.Entry(root)
    glassesEntry.grid(row=16, column=1)
    
    #Submit Gear Button
    submitGearButton = tk.Button(root,text="Submit Gear",command=lambda: submitGear(unitSideEntry,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,cur,sql))
    submitGearButton.grid(row=17, column=2, sticky=W)

    #Clear all boxes Button
    clearAllButton = tk.Button(root,text="Clear All Boxes",command=lambda: clearAllBoxes(unitNameEntry,unitSideEntry,mainWepEntry,mainAmmoEntry,mainWepSightEnt,mainWepBarEnt,mainWepBipEnt,mainWepOtherEnt,secWepEntry,secAmmoEntry,secWepSightEnt,sideWepEntry,sideAmmoEntry,sideWepSightEnt,sideWepBarEnt,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry))
    clearAllButton.grid(row=0, column=3, sticky=W)

    #Blank gap
    Blank = Label(root, text = "")
    Blank.grid(row=18, column=0)

    hasMapCheckbox = Checkbutton(root, variable=hasMap, onvalue = 1, offvalue = 0, text= "Map?")
    hasMapCheckbox.grid(row=11, column=4, sticky=W)

    hasNVGCheckbox = Checkbutton(root, variable=hasNVG, onvalue = 1, offvalue = 0, text= "NVG?")
    hasNVGCheckbox.grid(row=12, column=4, sticky=W)

    hasRadioCheckbox = Checkbutton(root, variable=hasRadio, onvalue = 1, offvalue = 0, text= "Radio?")
    hasRadioCheckbox.grid(row=13, column=4, sticky=W)

    hasCompassCheckbox = Checkbutton(root, variable=hasCompass, onvalue = 1, offvalue = 0, text= "Compass?")
    hasCompassCheckbox.grid(row=14, column=4, sticky=W)

    hasWatchCheckbox = Checkbutton(root, variable=hasWatch, onvalue = 1, offvalue = 0, text= "Watch?")
    hasWatchCheckbox.grid(row=15, column=4, sticky=W)

    hasGPSCheckbox = Checkbutton(root, variable=hasGPS, onvalue = 1, offvalue = 0, text= "GPS?")
    hasGPSCheckbox.grid(row=16, column=4, sticky=W)

    #Takes you to final generation page
    generateGearScriptButton = tk.Button(root,text="Generate Gear Script",command=lambda: GenerateGearScript(cur,hasMap,hasNVG,hasRadio,hasCompass,hasWatch,hasGPS,unitSideEntry))
    generateGearScriptButton.grid(row=17, column=4, sticky=W)
 
    root.mainloop()
 
#Collects the weapon and stores in db for later use
def submitUnit(unitSideEntry,unitNameEntry,mainWepEntry,mainAmmoEntry,mainWepSightEnt,mainWepBarEnt,mainWepBipEnt,mainWepOtherEnt,secWepEntry,secAmmoEntry,secWepSightEnt,sideWepEntry,sideAmmoEntry,sideWepSightEnt,sideWepBarEnt,isCommander,isMedic,cur,sql):
    main_weapon = mainWepEntry.get()
    main_ammo = mainAmmoEntry.get()
    main_sight = mainWepSightEnt.get()
    main_barrel = mainWepBarEnt.get()
    main_bipod = mainWepBipEnt.get()
    main_other = mainWepOtherEnt.get()

    sec_weapon = secWepEntry.get()
    sec_ammo = secAmmoEntry.get()
    sec_sight = secWepSightEnt.get()

    side_weapon = sideWepEntry.get()
    side_ammo = sideAmmoEntry.get()
    side_sight = sideWepSightEnt.get()
    side_barrel = sideWepBarEnt.get()

    unit_name = unitNameEntry.get()
    unit_side = unitSideEntry.get()

    unit_command = isCommander.get()
    unit_medic = isMedic.get()

    if(unit_side == ""):
        messagebox.showinfo("Notice", "Unit side is empty. Please fill and resubmit.")
    elif(unit_name == ""):
        messagebox.showinfo("Notice", "Unit name is empty. Please fill and resubmit.")
    else:
        cur.execute('INSERT INTO units(main_weapon, main_ammo, main_sight, main_barrel, main_bipod, main_other, sec_weapon, sec_ammo, sec_sight, side_weapon, side_ammo, side_sight, side_barrel, unit_name, unit_side, unit_command, unit_medic) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(str(main_weapon),str(main_ammo),str(main_sight),str(main_barrel),str(main_bipod),str(main_other),str(sec_weapon),str(sec_ammo),str(sec_sight),str(side_weapon),str(side_ammo),str(side_sight),str(side_barrel),str(unit_name),str(unit_side),int(unit_command),int(unit_medic)))
        print('Inserted unit ' + unit_name + ' on ' + unit_side + ' side.')
        sql.commit()
        messagebox.showinfo("Notice", "Weapons Inserted Successfully!")
 
#Collects all the clothes gear and stores them in the db for later use
#Due to not all fields being entered at once it only executes when entry box is not empty
def submitGear(unitSideEntry,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry,cur,sql):
    m_uniform = uniformEntry.get()
    m_vests = vestEntry.get()
    m_backpacks = backpackEntry.get()
    m_helmets = helmetEntry.get()
    m_glasses = glassesEntry.get()
    m_gearSide = unitSideEntry.get()
    if(m_gearSide == ""):
        messagebox.showinfo("Notice", "Unit side is empty. Please fill and resubmit.")
    else:
        if(m_uniform != ""):
            cur.execute('INSERT INTO uniforms(uniform,gearSide) VALUES (?,?)', (str(m_uniform),str(m_gearSide)))
            sql.commit()
        if(m_vests != ""):
            cur.execute('INSERT INTO vests(vest,gearSide) VALUES (?,?)', (str(m_vests),str(m_gearSide)))
            sql.commit()
        if(m_backpacks != ""):
            cur.execute('INSERT INTO backpacks(backpack,gearSide) VALUES (?,?)', (str(m_backpacks),str(m_gearSide))),
            sql.commit()   
        if(m_helmets != ""):
            cur.execute('INSERT INTO helmets(helmet,gearSide) VALUES (?,?)', (str(m_helmets),str(m_gearSide)))
            sql.commit()
        if(m_glasses != ""):
            cur.execute('INSERT INTO glasses(glasses,gearSide) VALUES (?,?)', (str(m_glasses),str(m_gearSide)))
            sql.commit()
        messagebox.showinfo("Notice", "Gear Inserted Successfully!")
 
def clearAllBoxes(unitNameEntry,unitSideEntry,mainWepEntry,mainAmmoEntry,mainWepSightEnt,mainWepBarEnt,mainWepBipEnt,mainWepOtherEnt,secWepEntry,secAmmoEntry,secWepSightEnt,sideWepEntry,sideAmmoEntry,sideWepSightEnt,sideWepBarEnt,uniformEntry,vestEntry,backpackEntry,helmetEntry,glassesEntry):
    unitSideEntry.delete(0, END)
    unitNameEntry.delete(0, END)
    mainWepEntry.delete(0, END)
    mainAmmoEntry.delete(0, END)
    mainWepSightEnt.delete(0, END)
    mainWepBarEnt.delete(0, END)
    mainWepBipEnt.delete(0, END)
    mainWepOtherEnt.delete(0, END)
    secWepEntry.delete(0, END)
    secAmmoEntry.delete(0, END)
    secWepSightEnt.delete(0, END)
    sideWepEntry.delete(0, END)
    sideAmmoEntry.delete(0, END)
    sideWepSightEnt.delete(0, END)
    sideWepBarEnt.delete(0, END)
    uniformEntry.delete(0, END)
    vestEntry.delete(0, END)
    backpackEntry.delete(0, END)
    helmetEntry.delete(0, END)
    glassesEntry.delete(0, END)
    print("Cleared Boxes.")
    messagebox.showinfo("Notice", "Cleared Boxes.")
  
def GenerateGearScript(cur,hasMap,hasNVG,hasRadio,hasCompass,hasWatch,hasGPS,unitSideEntry):
   
    #Get passed in values
    unitSide = unitSideEntry.get()
    includeMap = hasMap.get()
    includeNVG = hasNVG.get()
    includeRadio = hasRadio.get()
    includeCompass = hasCompass.get()
    includeWatch = hasWatch.get()
    includeGPS = hasGPS.get()

    if(unitSide == ""):
        messagebox.showinfo("Notice", "Unit side is empty. Select a side to generate.")
    else:
        #initialises/resets values 
        #can't be in an __init__ due to needing to be run everytime a new set of sqf files is made
        varA = 0
        varB = 0
        varC = 0
        varD = 0
        varE = 0
        createdSides = []
     
        with open('gearScript.sqf', 'w') as file:
           
            #clothes assignments
            #Uniforms
            file.write('_uniform = ["')
            for row in cur.execute("SELECT * FROM uniforms"):
                insertValue, gearSide = (row)
                if(gearSide == unitSide):
                	#will only trigger for first value
                    if(varA == 0):
                        varA = varA + 1 
                        file.write(insertValue)
                    else:
                        file.write('","')
                        file.write(insertValue)
            file.write('"];\n\n')  
           
           	#Vests
            file.write('_rig = ["')
            for row in cur.execute("SELECT * FROM vests"):
                insertValue, gearSide = (row)
                if(gearSide == unitSide):
                	#will only trigger for first value
                    if(varB == 0):
                        varB = varB + 1 
                        file.write(insertValue)
                    else:
                        file.write('","')
                        file.write(insertValue)
            file.write('"];\n\n')  
           
            #Helmets
            file.write('_helmet = ["')
            for row in cur.execute("SELECT * FROM helmets"):
                insertValue, gearSide = (row)
                if(gearSide == unitSide):
                	#will only trigger for first alue
                    if(varC == 0):
                        varC = varC + 1 
                        file.write(insertValue)
                    else:
                        file.write('","')
                        file.write(insertValue)
            file.write('"];\n\n')  
           
            #Glasses
            file.write('_glasses = ["')
            for row in cur.execute("SELECT * FROM glasses"):
                insertValue, gearSide = (row)
                if(gearSide == unitSide):
                	#will only trigger for first value
                    if(varD == 0):
                        varD = varD + 1 
                        file.write(insertValue)
                    else:
                        file.write('","')
                        file.write(insertValue)
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

            #add uniforms
            file.write('_unit setVariable ["BIS_enableRandomization", false];\n')
            file.write('removeUniform _unit;removeHeadgear _unit;removeVest _unit;')
            file.write('if(count _uniform > 0) then {\n_unit forceAddUniform (_uniform call BIS_fnc_selectRandom);\n};\n\n')
            file.write('if(count _helmet > 0) then {\n_unit addHeadgear (_helmet call BIS_fnc_selectRandom);\n};\n\n')
            file.write('if(count _glasses > 0) then {\n_unit addGoggles (_glasses call BIS_fnc_selectRandom);\n};\n\n')
            file.write('if(count _rig > 0) then {\n_unit addVest (_rig call BIS_fnc_selectRandom);\n};\n\n')
            if(includeMap == 1):
                file.write('_unit linkItem "ItemMap";\n')
            if(includeNVG == 1):
                file.write('_unit linkItem "NVGoggles";\n')
            if(includeRadio == 1):
                file.write('_unit linkItem "ItemRadio";\n')
            if(includeCompass == 1):
                file.write('_unit linkItem "ItemCompass";\n')
            if(includeWatch == 1):
                file.write('_unit linkItem "ItemWatch";\n')
            if(includeGPS == 1):
                file.write('_unit linkItem "ItemGPS"; \n')
            file.write('};\n\n')
     
            #backpack setup for each faction
            file.write('_backpack = {\n_typeofBackPack = _this select 0;\n_loadout = f_param_backpacks;\nif (count _this > 1) then {_loadout = _this select 1};\nswitch (_typeofBackPack) do\n{\n')
            file.write('#include "f_assignGear_' + unitSide +'_b.sqf";\n')
            file.write('};\n};\n\n')

            file.write('_attachments = [];')
            file.write('_hg_attachments = [];')

            file.write('switch (_typeofUnit) do \n{\n')
            
            #need to define it before use
            actualUnitSide = "default"

            #Build switch statements for unit weapons
            for row in cur.execute("SELECT * FROM units"):
                main_weapon,main_ammo,main_sight,main_barrel,main_bipod,main_other,sec_weapon,sec_ammo,sec_sight,side_weapon,side_ammo,side_sight,side_barrel,unit_name,unit_side,unit_command,unit_medic = (row)
                if(unit_side == unitSide): 

                    #Fix for when it was overriding unitside on the last pass
                    actualUnitSide = unitSide

                    file.write('case "' + unit_name + '": {\n')
     
                    #add main weapon + ammo
                    if(main_ammo != ""):
                        file.write('_unit addmagazines ["' + main_ammo + '",4];\n')
                    if(main_weapon != ""):
                        file.write('_unit addweapon "' + main_weapon + '";\n')
     
                    #add secondary weapon + ammo
                    if(sec_ammo != ""):
                        file.write('_unit addmagazines ["' + sec_ammo + '",1];\n')
                    if(sec_weapon != ""):
                        file.write('_unit addweapon "' + sec_weapon + '";\n')
     
                    #add sidearm + ammo
                    if(side_ammo != ""):
                        file.write('_unit addmagazines ["' + side_ammo + '",5];\n')
                    if(side_weapon != ""):
                        file.write('_unit addweapon "' + side_weapon + '";\n')
     
                    #Add more medical if unit is medic
                    if(unit_medic == "1"):
                        file.write('{_unit addItemToVest "FirstAidKit";} foreach [1,2,3,4,5,6,7,8,9,10];\n')
                        file.write('{_unit addItemToVest "ACE_epinephrine";} foreach [1,2,3,4,5,6,7,8,9,10];\n')
                        file.write('{_unit addItemToVest "ACE_bloodIV";} foreach [1,2,3,4,5];\n')
                    else:
                        file.write('{_unit addItemToVest "FirstAidKit";} foreach [1,2,3,4,5];\n')

                    #start of code for scopes
                    file.write('_attachments = ["')
                    attachmentsList = []
                    v = 0
                    if(main_sight != ""):
                        attachmentsList.append(main_sight)
                    if(main_barrel != ""):
                        attachmentsList.append(main_barrel)
                    if(main_bipod != ""):
                        attachmentsList.append(main_bipod)
                    if(main_other != ""):
                        attachmentsList.append(main_other)
                    for i in attachmentsList:
                        if(v == 0):
                            firstItem = attachmentsList[0]
                            v =  v + 1
                            file.write(firstItem)
                        else:
                            file.write('","')
                            file.write(attachmentsList[v])
                            v =  v + 1
                    file.write('"];\n')

                    file.write('_hg_attachments = ["')
                    hg_attachmentsList = []
                    v = 0
                    if(side_sight != ""):
                        hg_attachmentsList.append(side_sight)
                    if(side_barrel != ""):
                        hg_attachmentsList.append(side_barrel)
                    for i in hg_attachmentsList:
                        if(v == 0):
                            firstItem = hg_attachmentsList[0]
                            v =  v + 1
                            file.write(firstItem)
                        else:
                            file.write('","')
                            file.write(hg_attachmentsList[v])
                            v =  v + 1
                    file.write('"];\n')

                    file.write('["' + unit_name +'"] call _backpack;\n')
                    file.write('};\n\n')
                    print('Created unit ' + unit_name + ' on ' + actualUnitSide + ' side.')
           
            #default
            file.write('default {\n_unit addmagazines ["30Rnd_65x39_caseless_mag",7];\n_unit addweapon "arifle_MX_pointer_F";\n_unit selectweapon primaryweapon _unit;\n')
            file.write('if (true) exitwith {player globalchat format ["DEBUG: Unit = %1. Gear template %2 does not exist, used Rifleman instead.",_unit,_typeofunit]};\n};\n')
            #end closing bracket
            file.write('};\n')

            #Add attachments
            file.write('_unit selectweapon primaryweapon _unit;')
            file.write('removeAllPrimaryWeaponItems _unit;\n{\n_unit addPrimaryWeaponItem _x;\n} \nforeach _attachments;\n\n')
            file.write('removeAllHandgunItems _unit;\n{\n_unit addHandgunItem _x;\n} \nforeach _hg_attachments;\n\n')

            file.close()
            GenerateBackpackScript(cur,actualUnitSide,createdSides)

#Generates Backpack sqf file
def GenerateBackpackScript(cur,actualUnitSide,createdSides):
	with open('gearScript_b.sqf', 'w') as file:  
		for row in cur.execute("SELECT * FROM units"):
			main_weapon,main_ammo,main_sight,main_barrel,main_bipod,main_other,sec_weapon,sec_ammo,sec_sight,side_weapon,side_ammo,side_sight,side_barrel,unit_name,unit_side,unit_command,unit_medic = (row)
			if(unit_side == actualUnitSide): 
				file.write('m_backpack = (_backpacks call BIS_fnc_selectRandom);')
				file.write('case "' + unit_name + '": {\n')
				file.write('_unit addBackpack m_backpack;\n')
				file.write('clearMagazineCargoGlobal (unitBackpack _unit);\n')
				file.write('(unitBackpack _unit) addItemCargoGlobal ["HandGrenade",2];\n(unitBackpack _unit) addMagazineCargoGlobal ["SmokeShell", 2];\n(unitBackpack _unit) addItemCargoGlobal ["FirstAidKit", 4];\n')
				file.write('(unitBackpack _unit) addMagazineCargoGlobal ["' + main_ammo + '", 6];')
				file.write('};')
	file.close()
	generateFn_AssignGear(cur,createdSides)
	renameFiles(actualUnitSide)

def generateFn_AssignGear(cur,createdSides):
    #Creates a list of sides that have already been written, limits it to one #include f_assignGear_FACTION_NAME.sqf.sqf line per faction

    with open('fn_assignGear.sqf', 'w') as file:
        file.write('private ["_faction","_typeofUnit","_unit"];\n\n')
        file.write('_typeofUnit = toLower (_this select 0);\n_unit = _this select 1;\n\n')
        file.write('_faction = toLower (faction _unit);\nif(count _this > 2) then\n{\n_faction = toLower (_this select 2);\n};')

        file.write('if !(local _unit) exitWith {};\n')
        file.write('_unit setVariable ["f_var_assignGear",_typeofUnit,true];\n')
        for row in cur.execute("SELECT * FROM units"):
            main_weapon,main_ammo,main_sight,main_barrel,main_bipod,main_other,sec_weapon,sec_ammo,sec_sight,side_weapon,side_ammo,side_sight,side_barrel,unit_name,unit_side,unit_command,unit_medic = (row)
            if(unit_side not in createdSides):
            	createdSides.append(unit_side)
            	file.write('if (_faction == "' + unit_side + '") then {\n')
            	file.write('#include "f_assignGear_' + unit_side + '.sqf"\n};\n')

        file.write('_unit setVariable ["f_var_assignGear_done",false,true];\n')

#renames files dependant on the side
def renameFiles(actualUnitSide):
    os.rename('gearScript.sqf','f_assignGear_' + actualUnitSide +'.sqf')
    os.rename('gearScript_b.sqf','f_assignGear_' + actualUnitSide +'_b.sqf')

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
