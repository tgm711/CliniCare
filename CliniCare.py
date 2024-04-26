from tkinter import *
import re
from tkinter import ttk
import tkinter.messagebox
import random
import mysql.connector
from tkinter.ttk import Treeview
from datetime import datetime
from tkcalendar import DateEntry

con = mysql.connector.connect(host='localhost', database='CliniCare', user='root', password='root')
cur=con.cursor()

windows = []
v = []

def db_entry():
    global uid, bgselvar, root1
    p1 = uid
    p2 = e2.get()
    if not re.match(r'([A-Z][a-z])*',p2):
        tkinter.messagebox.showerror("Error", "Name should not contain numbers!")
        return
    if e3.get() != "":
        age = e3.get()
        if not age.isdigit():
            tkinter.messagebox.showerror("Error", "Age must be a number!")
            return
        else:
            p3 = int(age)
            if p3 > 100 or p3 < 0:
                tkinter.messagebox.showerror("Error", "Invalid Age!")
                return
    else:
        p3 = 0 
    p4 = bgselvar.get()
    p5 = e5.get()
    if not re.match(r'\d{10}', p5):  
        tkinter.messagebox.showerror("Error", "Phone number should contain 10 digits only!")
        return
    p6 = gselvar.get()
    
    if ([p1 != "" and p2 != "" and p4 != "None" and p5 != "" and p6 != "None"] and p3 != "0"):
        ins = "INSERT INTO UserDetails (UserID, Name, Age, Gender, PhoneNo, BloodGroup) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(ins, (p1, p2, p3, p6, p5, p4))

        v = 0
        cur.execute("INSERT INTO VisitCount (UserID, VisitCount) VALUES (%s, %s)", (p1, v))
        
        con.commit()  
        tkinter.messagebox.showinfo("Registration","Registration Successful!")
        root1.destroy()
        
    else:
        tkinter.messagebox.showerror("Error","Form Incomplete!")
        
    
def register():
    global uid,e2,e3,e5,e6,root1
    global bgselvar
    global gselvar
    root1 = Toplevel()
    root1.title("Registration Form")
    root1.geometry(f"600x450+{500}+{200}")
    root1.config(background='light blue')

    windows.append(root1)
    
    label=Label(root1,text="Registration Form",font='arial 25 bold', bg = 'light blue')
    label.pack()
    frame=Frame(root1,height=400,width=600, bg = 'light blue')
    frame.pack()
    bgselvar = StringVar()
    bgselvar.set("None")
    
    gselvar = StringVar()
    gselvar.set("None")

    nt=Label(root1,text='All fields should be filled mandatorily!', font="Arial 10", bg = 'light blue', fg ='red')
    nt.place(x=20,y=70)
    uid = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
    
    uidl = Label(frame, text = "User-ID :", font = "Arial 12 bold", bg = 'light blue')
    uidd = Label(frame, text = uid, font = "Arial 12", bg = 'light blue')
    uidl.place(x = 20, y = 60)
    uidd.place(x = 150,y = 60)
    l2=Label(root1,text="Name",font="Arial 12 bold", bg = 'light blue')
    l2.place(x=20,y=140)
    e2=tkinter.Entry(root1, width=30)
    e2.place(x=150,y=140)
    l3=Label(root1,text="Age",font="Arial 12 bold", bg = 'light blue')
    l3.place(x=20,y=180)
    e3=tkinter.Entry(root1, width=30)
    e3.place(x=150,y=180)
    l4=Label(root1,text="Gender",font="Arial 12 bold", bg = 'light blue')
    l4.place(x=20,y=220)
    r1=Radiobutton(frame, font=("arial",12), text="Male",variable=gselvar, value="Male", bg = 'light blue')
    r2=Radiobutton(frame, font=("arial",12), text="Female",variable=gselvar, value="Female", bg = 'light blue')
    r1.place(x=150,y=175)
    r2.place(x=300,y=175)
    l5=Label(root1,text="PhoneNo.",font="Arial 12 bold", bg = 'light blue')
    l5.place(x=20,y=260)
    e5=tkinter.Entry(root1, width=30)
    e5.place(x=150,y=260)
    l6=Label(root1,text="Blood Group",font="Arial 12 bold", bg = 'light blue')
    l6.place(x=20,y=300)
    bg1=Radiobutton(frame, font=("arial",12), text="A+", variable=bgselvar, value="A+", bg = 'light blue')
    bg2=Radiobutton(frame, font=("arial",12), text="A-",variable=bgselvar, value="A-", bg = 'light blue')
    bg3=Radiobutton(frame, font=("arial",12), text="B+",variable=bgselvar, value="B+", bg = 'light blue')
    bg4=Radiobutton(frame, font=("arial",12), text="B-",variable=bgselvar, value="B-", bg = 'light blue')
    bg5=Radiobutton(frame, font=("arial",12), text="O+",variable=bgselvar, value="O+", bg = 'light blue')
    bg6=Radiobutton(frame, font=("arial",12), text="O-",variable=bgselvar, value="O-", bg = 'light blue')
    bg7=Radiobutton(frame, font=("arial",12), text="AB+",variable=bgselvar, value="AB+", bg = 'light blue')
    bg8=Radiobutton(frame, font=("arial",12), text="AB-",variable=bgselvar, value="AB-", bg = 'light blue')
    bg1.place(x=150,y=255)
    bg2.place(x=250,y=255)
    bg3.place(x=350,y=255)
    bg4.place(x=450,y=255)
    bg5.place(x=150,y=275)
    bg6.place(x=250,y=275)
    bg7.place(x=350,y=275)
    bg8.place(x=450,y=275)
    b1=Button(root1,text="Submit", font='arial 10 bold',bg='white',width = 20,command=db_entry)
    b1.place(x=200,y=375)
    
    root1.resizable(False,False)
    root1.mainloop()

def view_data():
    global root3, root8
    cur.execute("select * from UserDetails")
    print(cur.statement)
    records = cur.fetchall()
                
    if records:
        try:
            root8 = Tk()
            root8.title("View Data")
            root8.geometry(f"842x500+{330}+{150}")
            root8.config(bg = "light blue")

            windows.append(root8)
                
            f3 = Frame(root8, height = 500, width = 842,bg='light blue')
            f3.propagate()
            f3.pack()
            
            label = Label(f3, text = "Existing Records", font = 'arial 22 bold',bg='light blue')
            label.pack()
            
            tree = Treeview(f3, columns = (1, 2, 3, 4, 5, 6), height = 21, show = "headings")

            tree.column(1, anchor = CENTER, width = 100)
            tree.column(2, anchor = CENTER, width = 120)
            tree.column(3, anchor = CENTER, width = 120)
            tree.column(4, anchor = CENTER, width = 120)
            tree.column(5, anchor = CENTER, width = 120)
            tree.column(6, anchor = CENTER, width = 120)
            
                
            tree.heading(1, text = 'UserID')
            tree.heading(2, text = 'Name')
            tree.heading(3, text = 'Age')
            tree.heading(4, text = 'Gender')
            tree.heading(5, text = 'PhoneNo')
            tree.heading(6, text = 'BloodGroup')
            
                
            for record in records:
                tree.insert("", "end", values = (record[0], record[1], record[2], record[3], record[4], record[5]))
    
            tree.place(x = 0, y = 150)
            
            tree.pack()

            root8.resizable(False, False)
            root8.mainloop()
            
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Failed to fetch records from the database.")
    else:
        tkinter.messagebox.showinfo("View Data", "No records found in the database.")

def modifyForm1():
    global x3,ad, root3
    root3=Tk()
    root3.title("Modify Data")
    root3.geometry(f"400x200+{550}+{300}")
    root3.config(background="light blue")

    windows.append(root3)
    
    label=Label(root3,text="Modify Data",font='arial 25 bold',bg='light blue')
    label.pack()
    frame=Frame(root3,height=200,width=400, bg = "light blue")
    frame.pack()
    l1=Label(root3,text="User-ID", font="arial 12 bold", bg = "light blue")
    l1.place(x=50,y=80)
    x3=tkinter.Entry(root3, width=30)
    x3.place(x=150,y=80)
    ad=x3.get()
    b1=Button(root3,text='Submit',font='arial 10 bold',bg = "white", fg = "black", width=15,command = modifyForm2)
    b1.place(x=140,y=150)
    root3.resizable(False,False)
    root3.mainloop()

def modifyForm2():
    global uid,x4,choice,new,x5,x3,root9,ad,dtch
    
    root9=Tk()
    root9.title("Modification Form")
    root9.geometry(f"500x480+{500}+{200}")
    root9.config(background="light blue")

    windows.append(root9)
    
    ad = x3.get()
    cur.execute("select * from UserDetails where UserID = %s",(ad,))
    dat=cur.fetchall()
    frame=Frame(root9,height=480,width=500,bg='light blue')
    frame.pack()
    l1=Label(root9,text='Data Modification',font="arial 20 bold",bg ='light blue')
    l1.place(x=150,y=10)
    
    l2=Label(root9,text='What do you want to modify ?',font="arial 15 bold",bg ='light blue')
    l2.place(x=45,y=185)
    l3=Label(root9,text='1. Name',font="arial 10 bold",bg ='light blue')
    l3.place(x=50,y=220)
    l4=Label(root9,text='2. Age',font="arial 10 bold",bg ='light blue')
    l4.place(x=50,y=240)
    l5=Label(root9,text='3. Gender',font="arial 10 bold",bg ='light blue')
    l5.place(x=50,y=260)
    l6=Label(root9,text='4. Phone',font="arial 10 bold",bg ='light blue')
    l6.place(x=50,y=280)
    l7=Label(root9,text='5. Blood Group',font="arial 10 bold",bg ='light blue')
    l7.place(x=50,y=300)
    x2=Label(root9,text='Enter Choice',font="arial 10 bold",bg ='light blue')
    x2.place(x=50,y=330)

    det = ["","Name","Age","Gender","Phone No", "Blood Group"] 
    d = StringVar() 
    dtch = ttk.Combobox(root9, width=32, textvariable=d, values=det)
    dtch.place(x=200, y=330) 
    dtch.current(0)

    '''x4=tkinter.Entry(root9)
    choice=x4.get()
    x4.place(x=200,y=330)'''

    L1=Label(root9,text='Old Details',font='arial 15 bold',bg ='light blue')
    L1.place(x=50,y=50)
    if dat:
        for i in dat:
            name=Label(root9,text='Name :',font="arial 10 bold",bg ='light blue')
            name.place(x=50,y=80)
            name1=Label(root9,text=i[1],font="arial 10 bold",bg ='light blue')
            name1.place(x=150,y=80)
            Age=Label(root9,text='Age :',font="arial 10 bold",bg ='light blue')
            Age.place(x=50,y=100)
            Age1=Label(root9,text=i[2],font="arial 10 bold",bg ='light blue')
            Age1.place(x=150,y=100)
            gen=Label(root9,text='Gender :',font="arial 10 bold",bg ='light blue')
            gen.place(x=50,y=120)
            gen1=Label(root9,text=i[3],font="arial 10 bold",bg ='light blue')
            gen1.place(x=150,y=120)
            pho=Label(root9,text='Phone No :',font="arial 10 bold",bg ='light blue')
            pho.place(x=50,y=140)
            pho1=Label(root9,text=i[4],font="arial 10 bold",bg ='light blue')
            pho1.place(x=150,y=140)
            bg=Label(root9,text='Blood Group :',font="arial 10 bold",bg ='light blue')
            bg.place(x=50,y=160)
            bg1=Label(root9,text=i[5],font="arial 10 bold",bg ='light blue')
            bg1.place(x=150,y=160)
    else:
        tkinter.messagebox.showerror("Error", "User doesn't exist!")
        
    p1 = x3.get()
    a=[]
    if dat:
        for i in dat:
            a.append(i)   
        if len(a)==0:
            tkinter.messagebox.showwarning("Error", "No Data Found!!")
    L2=Label(root9,text='Enter New Details',font='arial 10 bold',bg ='light blue')
    L2.place(x=50,y=360)
    x5=tkinter.Entry(root9,width=35)
    x5.place(x=200,y=360)
    
    b=Button(root9,text='Submit',font='arial 10 bold',bg='white',command=modify)
    b.place(x=220,y=420)
    
    root9.resizable(False,False)
    root9.mainloop()

def modify():
    global ad,x3,x4,x5,root9,d,choice,new
    print(ad)
    new=x5.get()
    print(new)
    choice=dtch.get()
    print(choice)
    if new != "" :
        if choice=='Name':
            cur.execute('update UserDetails set Name=%s where UserID=%s',(new,ad))
            con.commit()
            tkinter.messagebox.showinfo("Success", "Your Data has been Modified Successfully!")
        elif choice=='Age':
            if int(new) >= 0 and int(new) <= 100:
                cur.execute('update UserDetails set Age=%s where UserID = %s',(new,ad))
                con.commit()
                tkinter.messagebox.showinfo("Success", "Your Data has been Modified Successfully!")
            else:
                 tkinter.messagebox.showerror("Error", "Invalid Age!")
        elif choice=='Gender':
            if new == 'Female' or new == 'female' or new == 'Male' or new == 'male' :
                if new == 'female' :
                    new = 'Female'
                elif new == 'male' :
                    new = 'Male'
                cur.execute('update UserDetails set Gender=%s where UserID = %s', (new,ad))
                con.commit()
                tkinter.messagebox.showinfo("Success", "Your Data has been Modified Successfully!")
            else:
                tkinter.messagebox.showerror("Error", "Invalid Gender!")
        elif choice=='Phone No':
            if  new.isdigit() :
                cur.execute('update UserDetails set PhoneNo=%s where UserID=%s',(new,ad))
                con.commit()
                tkinter.messagebox.showinfo("Success", "Your Data has been Modified Successfully!")
            else:
                tkinter.messagebox.showerror("Error", "Invalid Phone Numbers! Enter Numbers only.")

        elif choice=='Blood Group':
            if new == 'A+' or new == 'A-' or new == 'B+' or new == 'B-' or new == 'O+' or new == 'O-' or new == 'AB+' or new == 'AB-' :
                if new == 'a+' :
                    new = 'A+'
                elif new == 'a-' :
                    new = 'A-'
                elif new == 'b+' :
                    new = 'B+'
                elif new == 'b-' :
                    new = 'B-'
                elif new == 'ab+' or new == 'Ab+' or new == 'aB+':
                    new = 'AB+'
                elif new == 'ab-' or new == 'Ab-' or new == 'aB-':
                    new = 'AB-'
                elif new == 'o+' :
                    new = 'O+'
                elif new == 'o-' :
                    new = 'O-'
                cur.execute('update UserDetails set BloodGroup=%s where UserID=%s',(new,ad))
                con.commit()
                tkinter.messagebox.showinfo("Success", "Your Data has been Modified Successfully!")
            else:
                 tkinter.messagebox.showerror("Error", "Invalid Blood Group!")
        else:
            pass
    else:
         tkinter.messagebox.showerror("Error", "New Data not Entered!")
    
#Appointment
def apt():
    global x1, root10
    root10=Tk()
    root10.title("Appointment")
    root10.geometry(f"300x200+{600}+{300}")
    root10.config(background="light blue")

    windows.append(root10)
    
    label=Label(root10,text="Appointment",font='arial 25 bold', bg = 'light blue')
    label.pack()
    frame=Frame(root10,height=200,width=300,bg='light blue')
    frame.pack()
    l1=Label(root10,text="UserID", font='arial 10 bold', bg = 'light blue')
    l1.place(x=30,y=80)
    x1=tkinter.Entry(root10, width = 30)
    x1.place(x=100,y=80)
    b1=Button(root10,text='Submit',font='arial 10 bold', bg='white',command=checkuidapt)
    b1.place(x=120,y=130)
    root10.resizable(False,False)
    root10.mainloop()

def checkuidapt():
    global u
    u = x1.get()
    if u and u != "":
        cur.execute("select UserID FROM UserDetails where UserID = %s",(u,))
        records = cur.fetchall()
        uid = records
        print(uid)
        if records:
            aptop()
        else:
            tkinter.messagebox.showerror("Error", "UserID does not exist!")
            if tkinter.messagebox.askokcancel("New Registration", "Would you like to register new user ?"):
                register()
    else:
        tkinter.messagebox.showerror("Error", "UserID cannot be blank!")

def aptop():
    global x1,x2, root4, u
    if x1.get() != "" :
        u = x1.get()
        print(u)
        root4=Tk()
        root4.title("Appointment")
        root4.geometry(f"300x250+{600}+{285}")
        root4.config(background="light blue")

        windows.append(root4)
        
        label=Label(root4,text="Appointment",font='arial 25 bold', bg = 'light blue')
        label.pack()
        frame=Frame(root4,height=250,width=300, bg = 'light blue')
        frame.pack()
        b2=Button(root4,text="Book Appointment",font='arial 15 bold', bg='white', width=15, command=bk_apt)
        b2.place(x=60,y=80)
        b2=Button(root4,text="View Appointments",font='arial 15 bold', bg='white', width=15, command=view_apt)
        b2.place(x=60,y=150)
        root4.resizable(False,False)
        root4.mainloop()
    else:
        tkinter.messagebox.showerror("Error", "Invalid UserID!")

def view_apt():
    global root5,x1,u
    UserID = u
    cur.execute("select * from Appointments  WHERE UserID = %s order by Date desc",(UserID,))
    print(cur.statement)
    records = cur.fetchall()
    print(records)
                
    if records:
        try:
            root5 = Tk()
            root5.title("View Appointments")
            root5.geometry(f"842x500+{330}+{150}")
            root5.config(bg = "light blue")

            windows.append(root5)
                
            f3 = Frame(root5, height = 500, width = 842,bg='light blue')
            f3.propagate()
            f3.pack()
            
            label = Label(f3, text = "Appointments", font = 'arial 25 bold',bg='light blue')
            label.pack()
            
            tree = Treeview(f3, columns = (1,2,3), height = 21, show = "headings")

            tree.column(1, anchor = CENTER, width = 180)
            tree.column(2, anchor = CENTER, width = 180)
            tree.column(3, anchor = CENTER, width = 260)
                        
            tree.heading(1, text = 'Service')
            tree.heading(2, text = 'Date')
            tree.heading(3, text = 'Time')
            
            for record in records:
                s = record[1].strip()
                tree.insert("", "end", values=(s, record[2], record[3]))
    
            tree.place(x = 0, y = 150)
            tree.pack()

            root5.resizable(False, False)
            root5.mainloop()

            
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Failed to fetch records from the database.")
    else:
        tkinter.messagebox.showinfo("View Data", "No records found in the database.")
   
def bk_apt():
    global x1,x2,x3,x4,x5,root10, root2,srv,p1,tm
    p1=x1.get()
    print(p1)
    cur.execute('select * from UserDetails where UserID=%s',(p1,))
    dat=cur.fetchall()
    if dat:
        root2=Tk()
        root2.title("Appointment")
        root2.geometry(f"450x530+{500}+{150}")
        root2.config(background="light blue")

        windows.append(root2)
        
        label=Label(root2,text="Appointment",font='arial 25 bold',bg="light blue")
        label.pack()
        frame=Frame(root2,height=530,width=450,bg='light blue')
        frame.pack()
        for i in dat:
            name=Label(root2,text='Welcome', font='arial 10 bold', bg='light blue')
            name.place(x=25,y=50)
            name1=Label(root2,text=i[1]+"!", font='arial 10 bold', bg='light blue')
            name1.place(x=95,y=50)
            age=Label(root2,text='Age :', font='arial 10 bold', bg='light blue')
            age.place(x=25,y=70)
            age1=Label(root2,text=i[2], font='arial 10 bold', bg='light blue')
            age1.place(x=75,y=70)
            phone=Label(root2,text='Phone :', font='arial 10 bold', bg='light blue')
            phone.place(x=25,y=90)
            phone1=Label(root2,text=i[4], font='arial 10 bold', bg='light blue')
            phone1.place(x=80,y=90)
            bg=Label(root2,text='Blood Group :', font='arial 10 bold', bg='light blue')
            bg.place(x=25,y=110)
            bg1=Label(root2,text=i[5], font='arial 10 bold', bg='light blue')
            bg1.place(x=125,y=110)
        l1=Label(root2,text='Services Available',font="Arial 16 bold", bg = "light blue")
        l1.place(x=25, y=140)
        f=["1. General Health Check-up","2. Child Care Center","3. Female Care Center","4. Prenatal Care Center", "5. Blood Pressure Monitoring","6. Nebulizer Treatment","7. Vaccination Center","8. Pathology-All types of Blood Investigations"]
        c=160
        for i in f:
           c = c + 20
           l3=Label(root2,text=i,font="Arial 10 bold", justify = "center", bg = "light blue")
           l3.place(x=25,y=c)
        L9=Label(root2,text=('Select Choice of Service'), font='arial 10 bold', bg='light blue').place(x=25,y=360) 
        srv = ["","General Health Check-up","Child Care Center","Female Care Center","Prenatal Care Center", "Blood Pressure Monitoring","Nebulizer Treatment","Vaccination Center","Pathology"] 
        s = StringVar() 
        srv = ttk.Combobox(root2, width=32, textvariable=s, values=srv,state="readonly")
        srv.place(x=200, y=360) 
        srv.current(0)
        
        #x5=tkinter.Entry(root2,width = 35)
        #x5.place(x=200,y=360)
        L7=Label(root2,text=('Select Date'), font='arial 10 bold', bg='light blue').place(x=25,y=390)
        x3 = DateEntry(root2, date_pattern = "yyyy-mm-dd", width = 32)
        x3.place(x = 200, y = 390)

        L8=Label(root2,text=('Select Time (24 Hr Format)'), font='arial 10 bold', bg='light blue').place(x=25,y=420)

        tm = ["","10:00", "10:30", "11:00", "11:30", "12:00",  "12:30", "13:00","16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00"] 
        t = StringVar() 
        tm = ttk.Combobox(root2, width=32, textvariable=t, values=tm, state="readonly")
        tm.place(x=200, y=420) 
        tm.current(0)
        
    else:
        tkinter.messagebox.showerror("Error", "User doesnot exist!")
        if tkinter.messagebox.askokcancel("New Registration", "Would you like to register new user ?"):
                register()
        
    B1=Button(root2,text='Submit',font='arial 10 bold', command=apt_details)
    B1.place(x=220,y=480)   
    root2.resizable(False,False)
    root2.mainloop()

def apt_details():
    global x1,x5,x2,h,p1,p2,p3,o,x4,x3,srv,tm
    #p1=x1.get()
    print(p1)
    p2=srv.get()
    p3=x3.get()
    p4=tm.get()

    sel_dt = datetime.strptime(p3 + ' ' + p4, '%Y-%m-%d %H:%M')
    curr_dt = datetime.now()

    if p2 != "" and p2 != "" and p3 != "" and p4 != "" :
        if sel_dt > curr_dt:
            cur.execute('SELECT * FROM Appointments WHERE UserID=%s AND Date=%s AND Time=%s', (p1, p3, p4))
            exist = cur.fetchone()
            if exist:
                tkinter.messagebox.showerror("Error", "Appointment already exists for this date and time.")
            else:
                dt="Your Appointment is Fixed","\nDate :",p3,"\nTime : ",p4
                query="insert into Appointments (UserID, Service, Date, Time) VALUES (%s, %s, %s, %s)"
                cur.execute(query, (p1, p2, p3, p4))
                con.commit()
                tkinter.messagebox.showinfo("Success", "Appointment Fixed Successfully!")
        else:
            tkinter.messagebox.showerror("Error", "Appointment date and time should be greater than the current date and time.")
    else:
        tkinter.messagebox.showerror("Error", "Invalid Details!")
        
# Function to update prescription in MySQL
def update_prescription():
    global root14, x1, x2, x3, u, x4, x5
    print(u)
    root14 = Tk()
    root14.title("Add Prescription")
    root14.geometry(f"300x400+{600}+{200}")
    root14.config(background="light blue")

    windows.append(root14)
    
    label = Label(root14, text="Prescription", font='arial 25 bold', bg='light blue')
    label.pack()
    frame = Frame(root14, height=400, width=300, bg='light blue')
    frame.pack()

    l3 = Label(root14, text="Date", font='arial 10 bold', bg='light blue')
    l3.place(x=30, y=55)
    x4 = DateEntry(root14, date_pattern = "yyyy-mm-dd", width = 35)
    x4.place(x=30, y=85)

    l4 = Label(root14, text="Fees Paid", font='arial 10 bold', bg='light blue')
    l4.place(x=30, y=115)
    x5 = Entry(root14, width=33, font='arial 10')
    x5.place(x=30, y=145)
    
    l2 = Label(root14, text="Medical Condition", font='arial 10 bold', bg='light blue')
    l2.place(x=30, y=175)
    x3 = Text(root14, height=2, width=33, font='arial 10')
    x3.place(x=30, y=205)

    l1 = Label(root14, text="Treatment, Medicines Prescribed", font='arial 10 bold', bg='light blue')
    l1.place(x=30, y=240)
    x2 = Text(root14, height=4, width=33, font='arial 10')
    x2.place(x=30, y=270)
    
    b1 = Button(root14, text="Submit", font='arial 10 bold', command=add_prescription)
    b1.place(x=120, y=350)

    root14.resizable(False, False)
    root14.mainloop()
    
def add_prescription():
    global x1, x2, x3, u, x4, x5
    print(u)
    if u and u != "":
        #u = x1.get()
        p = x2.get("1.0", "end")
        c = x3.get("1.0", "end")
        d = x4.get()
        f = x5.get()
        if f != "":
            if not re.match(r'[0-9]', f) or int(f) > 5000 or int(f) < 0:  
                tkinter.messagebox.showerror("Error", "Invalid Amount!")
                return
        else:
            tkinter.messagebox.showerror("Error", "Fees cannot be blank!")
    
        cur.execute("SELECT max(Date) FROM Prescriptions WHERE UserID = %s", (u,))
        ltdt = cur.fetchone()
        ltdt = ltdt[0]
        if ltdt and datetime.strptime(d, "%Y-%m-%d") < datetime.strptime(ltdt, "%Y-%m-%d"):
            tkinter.messagebox.showerror("Error", "New prescription date cannot be before the latest existing prescription date.")
            return

        cur.execute("SELECT VisitCount FROM VisitCount WHERE UserID = %s", (u,))
        v = cur.fetchone()
        print(v)
        if v:
            v = v[0] + 1
            cur.execute("UPDATE VisitCount SET VisitCount = %s WHERE UserID = %s", (v, u))
        else:
            cur.execute("UPDATE VisitCount SET VisitCount = %s WHERE UserID = %s", (1, u))

        sql = "INSERT INTO Prescriptions (UserID, Date, Visit, Conditions, Prescription, Fees) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (u, d, v, c, p, f)  
        cur.execute(sql, val)

        con.commit()
        tkinter.messagebox.showinfo("Success", "Prescription Added Successfully!")
    else:
        tkinter.messagebox.showerror("Error", "Invalid UserID")

    
def view_prescription():
    global root12
    UserID = x1.get()
    cur.execute("select * from Prescriptions WHERE UserID = %s order by Date desc",(UserID,))
    print(cur.statement)
    records = cur.fetchall()
    print(records)
                
    if records:
        try:
            root12 = Tk()
            root12.title("View Data")
            root12.geometry(f"1050x500+{330}+{150}")
            root12.config(bg = "light blue")

            windows.append(root12)
                
            f3 = Frame(root12, height = 500, width = 1050,bg='light blue')
            f3.propagate()
            f3.pack()
            
            label = Label(f3, text = "Prescription", font = 'arial 25 bold',bg='light blue')
            label.pack()
            
            tree = Treeview(f3, columns = (1,2,3,4,5), height = 21, show = "headings")

            tree.column(1, anchor = CENTER, width = 150)
            tree.column(2, anchor = CENTER, width = 150)
            tree.column(3, anchor = CENTER, width = 200)
            tree.column(4, anchor = CENTER, width = 400)
            tree.column(5, anchor = CENTER, width = 100)

            tree.heading(1, text = 'Date')
            tree.heading(2, text = 'No. of Visit')
            tree.heading(3, text = 'Medical Condition')
            tree.heading(4, text = 'Prescription')
            tree.heading(5, text = 'Fees (Rs.)')
                
            for record in records:
                p = record[4].strip()
                tree.insert("", "end", values=(record[1], record[2], record[3], p, record[5]))
    
            tree.place(x = 0, y = 150)
            tree.pack()

            root12.resizable(False, False)
            root12.mainloop()

            
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Failed to fetch records from the database.")
    else:
        tkinter.messagebox.showinfo("View Data", "No records found in the database.")
        
        
def prescriptionop():
    global x1,x2, root11, u
    if x1.get() != "" :
        u = x1.get()
        print(u)
        root11=Tk()
        root11.title("Prescription")
        root11.geometry(f"300x250+{600}+{285}")
        root11.config(background="light blue")

        windows.append(root11)
        
        label=Label(root11,text="Prescription",font='arial 25 bold', bg = 'light blue')
        label.pack()
        frame=Frame(root11,height=250,width=300, bg = 'light blue')
        frame.pack()
        b2=Button(root11,text="Add Prescription",font='arial 15 bold', bg='white', width=15, command=update_prescription)
        b2.place(x=60,y=80)
        b2=Button(root11,text="View Prescriptions",font='arial 15 bold', bg='white', width=15, command=view_prescription)
        b2.place(x=60,y=150)
        root11.resizable(False,False)
        root11.mainloop()
    else:
        tkinter.messagebox.showerror("Error", "Invalid Username!")
        
def prescriptionform():
    global root13,x1,u
    root13=Tk()
    root13.title("Prescription")
    root13.geometry(f"300x200+{600}+{300}")
    root13.config(background="light blue")

    windows.append(root13)
    
    label=Label(root13,text="Prescription",font='arial 25 bold', bg = 'light blue')
    label.pack()
    frame=Frame(root13,height=200,width=300, bg = 'light blue')
    frame.pack()
    l1=Label(root13,text="UserID", font='arial 10 bold', bg = 'light blue')
    l1.place(x=30,y=80)
    x1=tkinter.Entry(root13, width=30)
    x1.place(x=90,y=80)
    b1=Button(root13,text="Submit", font='arial 10 bold', bg ='white', command=checkuidp)
    b1.place(x=130,y=140)
    root13.resizable(False,False)
    root13.mainloop()

def checkuidp():
    global u
    u = x1.get()
    if u and u != "":
        cur.execute("select UserID FROM UserDetails where UserID = %s",(u,))
        records = cur.fetchall()
        if records:
            prescriptionop()
        else:
            tkinter.messagebox.showerror("Error", "UserID does not exist!")
            if tkinter.messagebox.askokcancel("New Registration", "Would you like to register new user ?"):
                register()
    else:
        tkinter.messagebox.showerror("Error", "UserID cannot be blank!")


def exit():
    global root1, root2, root3, root4, root5, root8, root9, root10, root11, root12, root13, root14
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        for w in windows :
            if w and w != root:
                try:
                    w.destroy()
                except tkinter.TclError:
                    pass
        root.destroy()

root=Tk()
root.title("CliniCare")
root.geometry(f"900x700+{300}+{50}")
c=Canvas(root,bg="light blue",width=900,height=700)
bgim=PhotoImage(file="Bg.png")
bg=c.create_image(450,350,image=bgim)
hd=c.create_text(450,150,text="CliniCare",font="Impact 100 ",fill="black",activefill="white")

b1=Button(text="Registration",font='arial 18 bold',width=15,height=1,bg="white",command=register)
b2=Button(text="View Data",font='arial 18 bold',width=15,height=1,bg="white",command=view_data)
b3=Button(text="Modify Data",font='arial 18 bold',width=15,height=1,bg='white',command=modifyForm1)
b4=Button(text="Prescription",font='arial 18 bold',width=15,height=1,bg='white',command=prescriptionform)
b5=Button(text="Appointment",font="arial 18 bold",width=15,height=1,bg='white',command=apt)
b6=Button(text="Exit",font='arial 18 bold',width=15,height=1,bg='white',command=exit)
b1.place(x=60,y=350)
b2.place(x=335,y=350)
b3.place(x=610,y=350)
b4.place(x=60,y=500)
b5.place(x=335,y=500)
b6.place(x=610,y=500)
c.pack()

root.protocol("WM_DELETE_WINDOW", exit) 

root.resizable(False,False)
root.mainloop()
