import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3

def start():
	print("Starting up Database")
	sql = sqlite3.connect('unit_database.db')
	cur = sql.cursor()
	print("Creating database if it doesn't exist")
	cur.execute('CREATE TABLE IF NOT EXISTS posts (main_weapon varchar NOT NULL, main_ammo varchar NOT NULL, secondary_weapon varchar NOT NULL, secondary_ammo varchar NOT NULL, sidearm_weapon varchar NOT NULL, sidearm_ammo varchar NOT NULL, unit_name varchar NOP NULL, unit_side varchar NOT NULL)')
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
	label8 = Label(root, text = "Unit side (blu/red/gren/civ)")
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

	submitButton = tk.Button(root,text="Submit Weapons",command=lambda: submit(cur,sql,e1,e2,e3,e4,e5,e6,e7,e8))
	submitButton.grid(row=8, column=1, sticky=W)

	clearAll = tk.Button(root,text="Clear All Boxes",command=lambda: clearboxes(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11))
	clearAll.grid(row=9, column=1, sticky=W)

	generateGearScript = tk.Button(root,text="Generate Gear Script",command=lambda: submit(cur,sql,e1,e2,e3,e4,e5,e6,e7))
	generateGearScript.grid(row=10, column=1, sticky=W)

	root.mainloop()


def submit(cur,sql,e1,e2,e3,e4,e5,e6,e7,e8):
    main_weapon = e1.get()
    main_ammo = e2.get()
    secondary_weapon = e3.get()
    secondary_ammo = e4.get()
    sidearm_weapon = e5.get()
    sidearm_ammo = e6.get()
    unit_name = e7.get()
    unit_side = e8.get()
    cur.execute('INSERT INTO posts(main_weapon, main_ammo, secondary_weapon, secondary_ammo, sidearm_weapon, sidearm_ammo, unit_name, unit_side) VALUES (?,?,?,?,?,?,?,?)',(str(main_weapon),str(main_ammo),str(secondary_weapon),str(secondary_ammo),str(sidearm_weapon),str(sidearm_ammo),str(unit_name),str(unit_side)))
    sql.commit()
    messagebox.showinfo("Notice", "Weapons Inserted Successfully!")

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


if __name__ == "__main__":
	start()
