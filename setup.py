#importing necessary modules/packages
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import mysql.connector as sqlcon
import pickle
import matplotlib.pyplot as plt
import numpy as np

#Extracting Host and MySQL Password from temp.dat file
with open('temp.dat', 'rb') as file:
    file_data = pickle.load(file)
    try:
        for i in file_data:
            sqlPass = file_data['pass']
            host = file_data['host']
    except EOFError:
        print("Data copied!")

#Houses and Positions available
housedisp = 'gandhi'
housesearch = "gandhi"
houses = ['gandhi', 'nehru', 'vivekanand', 'tagore']
position = ['_captain', '_vicecaptain', 'jr_captain', 'jr_vicecaptain']

#Connecting to MySQL database
conn = sqlcon.connect(
    host=host,
    password=sqlPass,
    user='root',
    database='MySQLVotingServer'
)


#Finding missing post(s) from houses
def tableCheck():
    global conn
    cursor = conn.cursor()
    cmd = "SHOW TABLES"
    cursor.execute(cmd)
    tableLst = cursor.fetchall()
    data = []
    for j in tableLst:
        data.append(j[0])
    print(data)
    missing = []
    for house in houses:
        for post in position:
            if f"{house}{post}" not in data:
                missing.append(f"{house}{post}")
    print(missing)
    for missingTable in missing:
        cmd = f'CREATE TABLE {missingTable}(name VARCHAR(50),votes INT DEFAULT 0)'
        print(cmd)
        cursor.execute(cmd)
        conn.commit()


tableCheck()


#Getting the names of students for the respective posts
def getData():
    poslist = ["", "", "", ""]

    for k in range(len(position)):
        cmd = f"SELECT * FROM {housedisp}{position[k]}"
        print(cmd)
        cursor = conn.cursor()
        cursor.execute(cmd)
        names = cursor.fetchall()
        for j in range(len(names)):
            poslist[k] += names[j][0]+"\n"
    houseOptionsDisp.set(housedisp.capitalize())
    capText.configure(text=poslist[0])
    vcapText.configure(text=poslist[1])
    capjrText.configure(text=poslist[2])
    vcapjrText.configure(text=poslist[3])


#Getting the data of selected house
def houseSelectedDisp(choice):
    global housedisp

    if choice != "Select House":
        housedisp = choice
        getData()
    return choice


#Setting appearance
set_appearance_mode("dark")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("")
app.geometry("1280x600")

#Forming the inner frame
inpFrame = CTkFrame(master=app, width=360, height=720, fg_color="#ffffff",)
inpFrame.pack_propagate()
inpFrame.pack(expand=True, side="right")

#Forming the outer frame
dispFrame = CTkFrame(master=app, width=860, height=720, fg_color="#ffffff",)
dispFrame.pack_propagate()
dispFrame.pack(expand=True, side="left")

pos = "_captain"


#Adding name of representative
def addRep():
    if repName.get() == '':
        CTkMessagebox(title="Error", message="Please enter a name.", icon="cancel")
    else:
        cmd = f"INSERT INTO {housesearch}{pos}(name) VALUES('{repName.get().title()}')"
        print(cmd)
        cursor = conn.cursor()
        cursor.execute(cmd)
        conn.commit()
        global housedisp
        housedisp = housesearch
        getData()


#Removing name of representative
def delRep():
    if repName.get() == '':
        CTkMessagebox(title="Error", message="Please enter a name.", icon="cancel")
    else:
        data = f"SELECT NAME FROM {housesearch}{pos}"
        cursor = conn.cursor()
        cursor.execute(data)
        rep_names = cursor.fetchall()
        print("REPNAMES: ",rep_names)
        for i in rep_names:
            if repName.get().title() == i[0]:
                msg = CTkMessagebox(title="Warning Message!", message="Are you sure?",
                                    icon="warning", option_1="Cancel", option_2="Proceed")

                if msg.get() == "Proceed":
                    cmd = f"DELETE FROM {housesearch}{pos} WHERE name='{repName.get().title()}'"
                    print(cmd)
                    cursor = conn.cursor()
                    cursor.execute(cmd)
                    conn.commit()
                    global housedisp
                    housedisp = housesearch
                    getData()
                    break
        else:
            CTkMessagebox(title="Error", message="Please ensure name is correct.", icon="warning")



#To check selected house
def houseSelected(choice):
    global housesearch
    housesearch = choice


#To check selected position
def positionSelected(choice):
    global pos
    if choice == "Captian":
        choice = "_captain"
    elif choice == "Vice-Captain":
        choice = "_vicecaptain"
    elif choice == "Captain Jr":
        choice = "jr_captain"
    elif choice == "Vice-Captain Jr":
        choice = "jr_vicecaptain"
    pos = choice

def results():
    fig, ax = plt.subplots()

    cursor = conn.cursor()
    cmd = f"SELECT * FROM {housesearch}{pos}"
    cursor.execute(cmd)
    data = cursor.fetchall()
    people = []
    votes = []
    for i in data:
        people.append(i[0])
        votes.append(i[2])
    y_pos = np.arange(len(people))
    error = np.random.rand(len(people))

    bars = ax.barh(y_pos, votes)
    ax.bar_label(bars)
    ax.set_yticks(y_pos, labels=people)
    ax.invert_yaxis()
    ax.set_xlabel('Votes Obtained')
    ax.set_title('')

    plt.show()



#Forming label for Input Menu
CTkLabel(master=inpFrame,
         text="INPUT MENU",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 24)).pack(anchor="w", pady=(25, 2), padx=(25, 0))

#Forming label asking to choose house
CTkLabel(master=inpFrame,
         text="Choose House: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(25, 0))

#Making a dropdown menu to select house
houseOptions = CTkOptionMenu(master=inpFrame,
                             values=["Gandhi", "Nehru", "Tagore", "Vivekanand"],
                             command=houseSelected,
                             width=225)
houseOptions.pack(anchor="w", padx=(25, 0), pady=(0, 2))

#Forming a label asking to choose position
CTkLabel(master=inpFrame,
         text="Choose Position: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(25, 0))

#Making a dropdown menu to select position
positionOptions = CTkOptionMenu(master=inpFrame,
                                values=["Captian", "Vice-Captain", "Captain Jr", "Vice-Captain Jr"],
                                command=positionSelected,
                                width=225)
positionOptions.pack(anchor="w", padx=(25, 0), pady=(0, 15))

resultsBtn = CTkButton(master=inpFrame,
                      text="View Results",
                      fg_color="#601E88",
                      hover_color="#E44982",
                      font=("Arial Bold", 12),
                      text_color="#ffffff",
                      width=225,
                      command=results)
resultsBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


CTkLabel(master=inpFrame,
         text="Want to add or remove a candidate?",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(25,5))

#Forming a label asking for name of representative
CTkLabel(master=inpFrame,
         text="Representative Name: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(0, 2), padx=(25, 0))

#Making an entry box to enter name of representative
repName = CTkEntry(master=inpFrame,
                   width=225,
                   fg_color="#EEEEEE",
                   border_color="#601E88",
                   border_width=1,
                   text_color="#000000")
repName.pack(anchor="w", padx=(25, 0))

#Forming a button to add name of representative
addBtn = CTkButton(master=inpFrame,
                   text="Add",
                   fg_color="#601E88",
                   hover_color="#E44982",
                   font=("Arial Bold", 12),
                   text_color="#ffffff",
                   width=225,
                   command=addRep)
addBtn.pack(anchor="w", pady=(15, 5), padx=(25, 25))

#Forming a button to remove name of representative
removeBtn = CTkButton(master=inpFrame,
                      text="Remove",
                      fg_color="#601E88",
                      hover_color="#E44982",
                      font=("Arial Bold", 12),
                      text_color="#ffffff",
                      width=225,
                      command=delRep)
removeBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))

#Forming a warning label for removing a candidate
CTkLabel(master=inpFrame,
         text="**Removing a candidate will permanently"
              "\n   remove his name from the list"
              "\n   All the votes given to him will be removed."
              "\n   Remove a candidate with caution",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(5, 25))
"""
CTkLabel(master=inpFrame,
         text="RESULTS",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))
"""

#Forming a label displaying set up for voting
CTkLabel(master=dispFrame,
         text="VOTING SETUP",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 24)).pack(anchor="w", pady=(50, 2), padx=(25, 0))

#Forming a label asking to choose house
CTkLabel(master=dispFrame,
         text="Choose House: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(25, 0))

#Making a dropdown menu to select house
houseOptionsDisp = CTkOptionMenu(master=dispFrame,
                                 values=["Select House", "Gandhi", "Nehru", "Tagore", "Vivekanand"],
                                 width=225, command=houseSelectedDisp)
houseOptionsDisp.pack(anchor="w", padx=(25, 0), pady=(5, 15))

#Making a frame for candidates for the post of senior captain
capFrame = CTkFrame(master=dispFrame, width=200, height=300, fg_color="#E44982")
capFrame.pack_propagate(False)
capFrame.pack(expand=True, side="left", padx=(25, 10), pady=(0, 50))

#Forming a label asking to select a senior captain
CTkLabel(master=capFrame,
         text="Sr Captain:",
         text_color="#ffffff",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(20, 0))

capText = CTkLabel(master=capFrame,
                   text="",
                   text_color="#ffffff",
                   anchor="w",
                   justify="center",
                   font=("Helvetica", 16))
capText.pack(anchor="w", pady=(5, 2), padx=(20, 0))

#Making a frame for candidates for the post of senior vice captain
vcapFrame = CTkFrame(master=dispFrame, width=200, height=300, fg_color="#E44982")
vcapFrame.pack_propagate(False)
vcapFrame.pack(expand=True, side="left", padx=(0, 10), pady=(0, 50))

#Forming a label asking to select a senior vice captain
CTkLabel(master=vcapFrame,
         text="Sr Vice-Captain:",
         text_color="#ffffff",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(20, 5))

vcapText = CTkLabel(master=vcapFrame,
                    text="",
                    text_color="#ffffff",
                    anchor="w",
                    justify="center",
                    font=("Helvetica", 16))
vcapText.pack(anchor="w", pady=(5, 2), padx=(20, 0))

#Making a frame for candidates for the post of junior captain
capJrFrame = CTkFrame(master=dispFrame, width=200, height=300, fg_color="#E44982")
capJrFrame.pack_propagate(False)
capJrFrame.pack(expand=True, side="left", padx=(0, 10), pady=(0, 50))

#Forming a label asking to select a junior captain
CTkLabel(master=capJrFrame,
         text="Jr Captain:",
         text_color="#ffffff",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(20, 5))

capjrText = CTkLabel(master=capJrFrame,
                     text="",
                     text_color="#ffffff",
                     anchor="w",
                     justify="center",
                     font=("Helvetica", 16))
capjrText.pack(anchor="w", pady=(5, 2), padx=(20, 0))

#Making a frame for candidates for the post of junior vice captain
vcapJrFrame = CTkFrame(master=dispFrame, width=200, height=300, fg_color="#E44982")
vcapJrFrame.pack_propagate(False)
vcapJrFrame.pack(expand=True, side="left", padx=(0, 25), pady=(0, 50))

#Forming a label asking to select a junior vice captain
CTkLabel(master=vcapJrFrame,
         text="Jr Vice-Captain:",
         text_color="#ffffff",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(20, 5))

vcapjrText = CTkLabel(master=vcapJrFrame,
                      text="",
                      text_color="#ffffff",
                      anchor="w",
                      justify="center",
                      font=("Helvetica", 16))
vcapjrText.pack(anchor="w", pady=(5, 2), padx=(20, 0))


app.mainloop()
