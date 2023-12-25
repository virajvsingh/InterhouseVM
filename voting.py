#importing necessary modules/packages
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import mysql.connector as sqlcon
import pickle
import smtplib
from email.message import EmailMessage

#Extracting Host and MySQL Password from temp.dat file
with open('temp.dat', 'rb') as file:
    file_data = pickle.load(file)
    try:
        for i in file_data:
            sqlPass = file_data['pass']
            host = file_data['host']
    except EOFError:
        print("Data copied!")

#Connecting to MySQL database and creating voting data table (if it doesn't exist)
conn = sqlcon.connect(
    host=host,
    password=sqlPass,
    user='root',
    database='MySQLVotingServer'
)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS voting_data('
               'AdmNo INT PRIMARY KEY,'
               'Name VARCHAR(50),'
               'Class INT,'
               'EmailID VARCHAR(100),'
               'House VARCHAR(50),'
               'Cap VARCHAR(50),'
               'VCap VARCHAR(50))')
conn.commit()

#Setting Appearance
set_appearance_mode("dark")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Interhouse Voting Machine - Vote")
app.geometry("350x780")

#Forming the frame
frame = CTkFrame(master=app, width=275, height=600, fg_color="#ffffff")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

#Making all the required variables
vClass = ""
vHouse = ""
cap = ""
viceCap = ""
tag1, tag2 = "", ""
classListDisp = ['IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
actualClassList = [4, 5, 6, 7, 8, 9, 10, 11]


#Checking eligibility of selected class for either junior or senior post

def getData():
    cursor = conn.cursor()
    cmd = f"SELECT * FROM {vHouse}{tag1}"
    cursor.execute(cmd)
    data = cursor.fetchall()
    capName = []
    for name in data:
        capName.append(name[0])
    captainRep.configure(values=capName)
    cmd = f"SELECT * FROM {vHouse}{tag2}"
    cursor.execute(cmd)
    data = cursor.fetchall()
    vCapName = []
    for name in data:
        vCapName.append(name[0])
    vcaptainRep.configure(values=vCapName)


def classSelected(choice):
    global tag1
    global tag2
    global vClass
    if vHouse != "":
        if choice != "Select your class":
            index = classListDisp.index(choice)
            vClass = actualClassList[index]
            if vClass > 5:
                tag1 = "_captain"
                tag2 = "_vicecaptain"
            elif vClass <= 5:
                tag1 = "jr_captain"
                tag2 = "jr_vicecaptain"
            getData()
    else:
        index = classListDisp.index(choice)
        vClass = actualClassList[index]
        if vClass > 5:
            tag1 = "_captain"
            tag2 = "_vicecaptain"
        elif vClass <= 5:
            tag1 = "jr_captain"
            tag2 = "jr_vicecaptain"

#Extracting the names of candidates from selected house
def houseSelected(choice):
    global vHouse
    if choice != 'Select your house':
        vHouse = choice.lower()
        getData()


#Choosing Captain
def capSelected(choice):
    if choice != "Select your captain":
        global cap
        cap = choice


#Choosing Vice-Captain
def vcapSelected(choice):
    if choice != "Select your vice-captain":
        global viceCap
        viceCap = choice


#Entering necessary details (name, Admno. etc.) to cast vote
def vote():
    if voterName.get() != "":
        if voterEmail.get() != "":
            if voterAdmno.get() != "":
                if voterAdmno.get().isdigit():
                    if vClass != "" and vHouse != "" and cap != "" and viceCap != "":
                        global tag1
                        global tag2
                        try:
                            cursor = conn.cursor()
                            cmd = (f"INSERT INTO voting_data "
                                   f"VALUES({int(voterAdmno.get())},'{voterName.get()}',"
                                   f"{vClass},'{voterEmail.get()}','{vHouse}','{cap}','{viceCap}')")
                            cursor.execute(cmd)
                            conn.commit()
                            cmd = f"UPDATE {vHouse}{tag1} SET votes = votes+1 WHERE name ='{cap}'"
                            cursor.execute(cmd)
                            conn.commit()
                            cmd = f"UPDATE {vHouse}{tag2} SET votes = votes+1 WHERE name ='{viceCap}'"
                            cursor.execute(cmd)
                            conn.commit()
                            CTkMessagebox(title="Voted", message='Voted successfully!!!')

                            message = f"""Dear {voterName.get()},
    I hope this email finds you well. 
    I am delighted to inform you that your commitment to 
    the democratic process has paid off, 
    and I am thrilled to extend my heartfelt congratulations on your 
    successful election as the Interhouse Representative.       
    
    You have voted for {cap} as your Captain,
    and {viceCap} as your Vice-Captain.
    
    Warm Regards,
    Salwan Public School
    Mayur Vihar
                            """

                            msg = EmailMessage()
                            msg.set_content(message)

                            msg['Subject'] = 'Congratulations on Your Successful Voting'
                            msg['From'] = "voting.spsmayurvihar@gmail.com"
                            msg['To'] = voterEmail.get()

                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.login("voting.spsmayurvihar@gmail.com", "vcpk mdov donv lqjg")
                            server.send_message(msg)
                            server.quit()


                            voterName.delete(0, END)
                            voterEmail.delete(0, END)
                            voterAdmno.delete(0, END)
                            voterClass.set("Select your class")
                            voterHouse.set('Select your house')
                            captainRep.set('Select your captain')
                            vcaptainRep.set('Select your vice-captain')
                            tag1, tag2 = "", ""
                        except:
                            CTkMessagebox(title='Error', message='You have already voted')
                    else:
                        CTkMessagebox(title='Error', message='Please Select your representatives')
                else:
                    CTkMessagebox(title='Error', message='Admission number not valid')
            else:
                CTkMessagebox(title='Error', message='Enter Admno')
        else:
            CTkMessagebox(title='Error', message='Enter email-id')
    else:
        CTkMessagebox(title='Error', message='Enter name')


#Forming a Welcome label
CTkLabel(master=frame,
         text="Welcome!",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(20, 2), padx=(25, 0))

#Forming a warning label to enter data carefully
CTkLabel(master=frame,
         text="Enter data carefully\nVotes once casted can't be changed",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25))

#Forming a label asking for the voter's name
CTkLabel(master=frame,
         text="Your Name:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making an entry box to enter voter's name
voterName = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#EEEEEE",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
voterName.pack(anchor="w", padx=(25, 0))

#Forming a label asking for voter's school email ID
CTkLabel(master=frame,
         text="School Email-ID:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making an entry box to enter voter's email ID
voterEmail = (CTkEntry(master=frame,
                       width=225,
                       fg_color="#EEEEEE",
                       border_color="#601E88",
                       border_width=1,
                       text_color="#000000"))
voterEmail.pack(anchor="w", padx=(25, 0))

#Forming a label asking for admission number of voter
CTkLabel(master=frame,
         text="Admission Number:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making an entry box to enter voter's Admission number
voterAdmno = (CTkEntry(master=frame,
                       width=225,
                       fg_color="#EEEEEE",
                       border_color="#601E88",
                       border_width=1,
                       text_color="#000000"))
voterAdmno.pack(anchor="w", padx=(25, 0))

#Forming a label asking to choose the class voter is studying in
CTkLabel(master=frame,
         text="Choose your class: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making a dropdown menu to select class
voterClass = CTkOptionMenu(master=frame,
                           values=['Select your class', 'IV', 'V', 'VI', 'V', 'VI', 'VII',
                                   'VIII', 'IX', 'X', 'XI'],
                           command=classSelected,
                           width=225)
voterClass.pack(anchor="w", padx=(25, 0), pady=(1, 5))

#Forming a label asking for name of voter
CTkLabel(master=frame,
         text="Choose House: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making a dropdown menu to select house
voterHouse = CTkOptionMenu(master=frame,
                           values=["Select your house", "Gandhi", "Nehru", "Tagore", "Vivekanand"],
                           command=houseSelected,
                           width=225)
voterHouse.pack(anchor="w", padx=(25, 0), pady=(1, 5))

#Forming a label asking to choose Captain
CTkLabel(master=frame,
         text="Captain: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making a dropdown menu to select Captain
captainRep = CTkOptionMenu(master=frame,
                           values=["Select your captain"],
                           command=capSelected,
                           width=225)
captainRep.pack(anchor="w", padx=(25, 0), pady=(1, 5))

#Forming a label asking to choose Vice-Captain
CTkLabel(master=frame,
         text="Vice-Captain: ",
         text_color="#601E88",
         anchor="w",
         justify="center",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 0), padx=(25, 0))

#Making a dropdown menu to select Vice-Captain
vcaptainRep = CTkOptionMenu(master=frame,
                            values=["Select your vice-captain"],
                            command=vcapSelected,
                            width=225)
vcaptainRep.pack(anchor="w", padx=(25, 0), pady=(1, 5))

#Forming a Vote button to cast final vote
CTkButton(master=frame,
          text="Vote",
          fg_color="#601E88",
          hover_color="#E44982",
          font=("Arial Bold", 12),
          text_color="#ffffff",
          width=225,
          command=vote).pack(anchor="w", pady=(10, 15), padx=(25, 0))

app.mainloop()