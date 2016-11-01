import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3

def start():
	print("Starting up Database")
	sql = sqlite3.connect('unit_database.db')
	cur = sql.cursor()
	print("Creating database if it doesn't exist")
	cur.execute('CREATE TABLE IF NOT EXISTS units (main_weapon varchar NOT NULL, main_ammo varchar NOT NULL, secondary_weapon varchar NOT NULL, secondary_ammo varchar NOT NULL, sidearm_weapon varchar NOT NULL, sidearm_ammo varchar NOT NULL, unit_name varchar NOP NULL, unit_side varchar NOT NULL)')
	sql.commit()
	generateGUI(cur,sql)

def generateGUI(cur,sql):
	root = tk.Tk()
	root.title("Framework Generator")

	#Main Weapon
	label1 = Label(root, text = "Main Weapon")
	label1.grid(row=0, sticky=W)
	e1 = tk.Entry(root)
	e1.grid(row=0, column=1)

	#Main Weapon Ammo
	label2 = Label(root, text = "Main Ammo")
	label2.grid(row=1, sticky=W)
	e2 = tk.Entry(root)
	e2.grid(row=1, column=1)

	#Secondary Weapon
	label3 = Label(root, text = "Secondary Weapon")
	label3.grid(row=2, sticky=W)
	e3 = tk.Entry(root)
	e3.grid(row=2, column=1)

	#Secondary Weapon Ammo
	label4 = Label(root, text = "Secondary Ammo")
	label4.grid(row=3, sticky=W)
	e4 = tk.Entry(root)
	e4.grid(row=3, column=1)

	#Sidearm Weapon 
	label5 = Label(root, text = "Sidearm")
	label5.grid(row=4, sticky=W)
	e5 = tk.Entry(root)
	e5.grid(row=4, column=1)

	#Sidearm Ammo
	label6 = Label(root, text = "Sidearm Ammo")
	label6.grid(row=5, sticky=W)
	e6 = tk.Entry(root)
	e6.grid(row=5, column=1)

	#Unit name
	label7 = Label(root, text = "Unit name (r,ar,etc)")
	label7.grid(row=6, sticky=W)
	e7 = tk.Entry(root)
	e7.grid(row=6, column=1)

	#Unit side
	label8 = Label(root, text = "Unit side (blu/red/ind/civ)")
	label8.grid(row=7, sticky=W)
	e8 = tk.Entry(root)
	e8.grid(row=7, column=1)

	#Uniform
	label9 = Label(root, text = "Uniform(s)")
	label9.grid(row=0, column=3, sticky=W)
	e9 = tk.Entry(root)
	e9.grid(row=0, column=4)

	#Vest
	label10 = Label(root, text = "Vest(s)")
	label10.grid(row=1, column=3, sticky=W)
	e10 = tk.Entry(root)
	e10.grid(row=1, column=4)

	#Backpacks
	label11 = Label(root, text = "Backpack(s)")	
	label11.grid(row=2, column=3, sticky=W)
	e11 = tk.Entry(root)
	e11.grid(row=2, column=4)

	#HeadGear (Helmets)
	label12 = Label(root, text = "HeadGear (Helmets)")	
	label12.grid(row=3, column=3, sticky=W)
	e12 = tk.Entry(root)
	e12.grid(row=3, column=4)

	#HeadGear (Glasses)
	label13 = Label(root, text = "HeadGear (Glasses)")	
	label13.grid(row=4, column=3, sticky=W)
	e13 = tk.Entry(root)
	e13.grid(row=4, column=4)


	submitButton = tk.Button(root,text="Submit Gear",command=lambda: submitGear(e9,e10,e11,e12,e13))
	submitButton.grid(row=5, column=4, sticky=W)

	submitButton = tk.Button(root,text="Submit Weapons",command=lambda: submitWeapons(cur,sql,e1,e2,e3,e4,e5,e6,e7,e8))
	submitButton.grid(row=8, column=1, sticky=W)

	clearAll = tk.Button(root,text="Clear All Boxes",command=lambda: clearboxes(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11))
	clearAll.grid(row=9, column=1, sticky=W)

	generateGearScript = tk.Button(root,text="Generate Gear Script",command=lambda: gearScriptSetUp(cur))
	generateGearScript.grid(row=10, column=1, sticky=W)

	root.mainloop()


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
    sql.commit()
    #messagebox.showinfo("Notice", "Weapons Inserted Successfully!")

def submitGear(e9,e10,e11,e12,e13):
	print()

def clearboxes(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11):
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
	#messagebox.showinfo("Notice", "Cleared Boxes.")

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

		file.write('_typeofUnit = toLower (_this select 0);\n')
		file.write('_unit = _this select 1;	\n')
		file.write('_isMan = _unit isKindOf "CAManBase";\n\n')
		file.write('if (_isMan) then {\n')
		file.write('removeBackpack _unit;\nremoveAllWeapons _unit;\nremoveAllItemsWithMagazines _unit;\nremoveAllAssignedItems _unit;\n')
		file.write('#include "f_assignGear_clothes.sqf";\n\n')
		file.write('_unit addItem "FirstAidKit";\n')
		
		if(includeMap == "y"):
			file.write('_unit linkItem "ItemMap";\n')
		if(includeNVG == "y"):
			file.write('_unit linkItem "";\n')
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
		file.write('switch (_typeofUnit) do \n{\n')
		file.write('_backpack = {\n_typeofBackPack = _this select 0;\n_loadout = f_param_backpacks;\nif (count _this > 1) then {_loadout = _this select 1};\nswitch (_typeofBackPack) do\n{\n')
		if(unitSide == "aaf"):
			file.write('#include "f_assignGear_aaf_b.sqf";\n')
		elif(unitSide == "fia"):
			file.write('#include "f_assignGear_fia_b.sqf";\n')
		elif(unitSide == "csat"):
			file.write('#include "f_assignGear_csat_b.sqf";\n')
		elif(unitSide == "red"):
			file.write('#include "f_assignGear_csat_b.sqf";\n')
		else:
			file.write('#include "f_assignGear_nato_b.sqf";\n')
		file.write('};\n};\n\n')

		for row in cur.execute("SELECT * FROM units"):
			main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side = (row)
			if(unit_side == unitSide):	
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

				#adding one last set of 6 mags for main gun just incase 4 isn't enough
				file.write('_unit addmagazines ["' + main_ammo + '",6];\n')
				file.write('["' + unit_name +'"] call _backpack;')
				file.write('};\n\n')
		
		#end closing bracket
		file.write('};\n')

if __name__ == "__main__":
	start()

