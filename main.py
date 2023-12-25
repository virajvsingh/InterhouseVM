#importing necessary modules/packages
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import mysql.connector as sqlcon
import pickle

flag = False
check = False

#Setting Appearance
set_appearance_mode("dark")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Interhouse Voting Machine - Home")
app.geometry("300x480")

#Forming the frame
frame = CTkFrame(master=app, width=700, height=480, fg_color="#ffffff")
frame.pack_propagate()
frame.pack(expand=True, side="right")

#Connecting and forming necessary database and tables (if they do not exist)
def connectionTest():
    ipAddressLst = ipAddress.get().split('.')
    if sql_pass_sys.get() == '':
        CTkMessagebox(title="Error",
                      message="Please enter the system's MySQL password.",
                      icon="warning")
    else:
        mydb = sqlcon.connect(
            host="localhost",
            user="root",
            password=sql_pass_sys.get(),
        )

        cursor = mydb.cursor()
        try:
            cursor.execute("CREATE USER 'root'@'%' identified by 'root'")
        except:
            cursor.execute("ALTER USER 'root'@'%' IDENTIFIED BY '{}'".format(sql_pass_sys.get()))
        finally:
            cmdlist = ["grant all privileges on *.* to 'root'@'%' with grant option",
                       "flush privileges"]

            for query in cmdlist:
                cursor.execute(query)
                mydb.commit()
                print("Flag1")
            CTkMessagebox(title="LAN Config",
                          message="Granted permission to your system\nto connect on LAN",
                          icon="check")

            if ipAddress.get() == '':
                CTkMessagebox(title="IP Address",
                              message="Please enter a valid IP Address",
                              icon="warning")
            elif len(ipAddressLst) != 4:
                CTkMessagebox(title="IP Address",
                              message="Please enter a valid IP Address",
                              icon="warning")
            else:
                if sql_pass_ser.get() !="":
                    for i in ipAddress.get():
                        print(i)
                        print(ord(i))
                        if ord(i) not in range(48,58) and ord(i) != 46:
                            CTkMessagebox(title="IP Address",
                                          message="Please enter a valid server IP Address(2)",
                                          icon="warning")
                            break
                    else:
                        sqldb = sqlcon.connect(
                            host=ipAddress.get(),
                            user="root",
                            password=sql_pass_ser.get(),
                        )
                        cursor = sqldb.cursor()
                        cursor.execute("CREATE DATABASE IF NOT EXISTS MySQLVotingServer")
                        sqldb.commit()

                        CTkMessagebox(title="Connection",
                                      message="Your system has been connected\n to the server",
                                      icon="check")

                        with open('temp.dat', 'wb') as file:
                            serverdata = {"host": ipAddress.get(), "pass": sql_pass_ser.get()}
                            pickle.dump(serverdata, file)
                            print("Flag2")

                            global flag
                            flag = True

                else:
                    CTkMessagebox(title="IP Address",
                                  message="Please enter a valid server password",
                                  icon="warning")

#Adding the server via configure button
def configure():
    try:
        connectionTest()
        if flag==True:
            os.system(f'python setup.py')
        else:
            CTkMessagebox(title="Error",
                          message=f"Error: Failed to establish a connection",
                          icon="warning")
    except:
        CTkMessagebox(title="Error",
                      message=f"We couldn't connect to a server\n"
                              f"Please try again.",
                      icon="warning")



#Connecting to the voting system via connect button
def connect():
    try:
        connectionTest()
        if flag == True:
            os.system(f'python voting.py')
        else:
            CTkMessagebox(title="Error",
                          message=f"Error: Failed to establish a connection",
                          icon="warning")
    except:
        CTkMessagebox(title="Error",
                      message=f"We couldn't connect to a server\n"
                              f"Please try again.",
                      icon="warning")


#Forming Welcome label
CTkLabel(master=frame,
         text="Welcome!",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(50, 2), padx=(25, 0))

#Forming a label to configure or connect to a server
CTkLabel(master=frame,
         text="Connect to a preconfigured server\nor setup a server on this system",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25))

#Forming a label asking for the MySQL password
CTkLabel(master=frame,
         text="Your System's MySQL Password:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(15, 5), padx=(25, 0))

#Making an entry box to enter MySQL password
sql_pass_sys = (CTkEntry(master=frame,
                         width=225,
                         fg_color="#EEEEEE",
                         border_color="#601E88",
                         border_width=1,
                         text_color="#000000"))
sql_pass_sys.pack(anchor="w", padx=(25, 0))

#Forming a label asking for IP Address of server
CTkLabel(master=frame,
         text="Server System IP Address:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

#Making an entry box to enter IP Address
ipAddress = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#EEEEEE",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
ipAddress.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Server's MySQL Password:",
         text_color="#601E88",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(15, 5), padx=(25, 0))

#Making an entry box to enter MySQL password
sql_pass_ser = (CTkEntry(master=frame,
                         width=225,
                         fg_color="#EEEEEE",
                         border_color="#601E88",
                         border_width=1,
                         text_color="#000000"))
sql_pass_ser.pack(anchor="w", padx=(25, 0))

#Forming a connect button
CTkButton(master=frame,
          text="Connect",
          fg_color="#601E88",
          hover_color="#E44982",
          font=("Arial Bold", 12),
          text_color="#ffffff",
          width=225,
          command=connect).pack(anchor="w", pady=(10, 15), padx=(25, 25))

#Forming a label asking to set up a server or edit configuration of an existing one
CTkLabel(master=frame,
         text="Want to setup a server\nor edit the configuration?",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25))

#Forming a configure button
CTkButton(master=frame,
          text="Configure",
          fg_color="#601E88",
          hover_color="#E44982",
          font=("Arial Bold", 12),
          text_color="#ffffff",
          width=225,
          command=configure).pack(anchor="w", pady=(10, 15), padx=(25, 0))

app.mainloop()