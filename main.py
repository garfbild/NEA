import sqlite3
global currentFrame


class Basic():
    def __init__(self,objType):
        self.objType = objType
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS {}Table({}Id INTEGER PRIMARY KEY, {}Name TEXT)'''.format(self.objType,self.objType,self.objType))
       
    def get(self):
        self.c.execute('''SELECT * FROM {}Table'''.format(self.objType,self.objType))  
        return self.c.fetchall()
   
    def getNewID(self):
        self.c.execute('''SELECT {}Id FROM {}Table ORDER BY {}Id DESC;'''.format(self.objType,self.objType,self.objType))
        IDS = self.c.fetchall()
        if IDS == []:
            newID = 1
        else:
            newID = IDS[0][-1] + 1
        return newID
   
    def close(self):
        self.conn.commit()
        self.conn.close()

class Timeblocks:
    def __init__(self):
        Basic.__init__(self,"Timeblock")
        try:
            self.c.execute("ALTER TABLE {}Table add column {} INTEGER".format(self.objType,"StartTime"))
            self.c.execute("ALTER TABLE {}Table add column {} INTEGER".format(self.objType,"EndTime"))
            self.c.execute("ALTER TABLE {}Table add column {} INTEGER".format(self.objType,"Day"))
        except:
            print("column already initialised")
   
    def add(self,name,start,finish):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?)'''.format(self.objType),(newID,name))  
        self.conn.commit()
         
   
class Departments(Basic):
    #ID name
    def __init__(self):
        Basic.__init__(self,"Department")
    def add(self,name):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?)'''.format(self.objType),(newID,name))  
        self.conn.commit()
   
class Courses(Basic):
    #ID name DepartmentId
    def __init__(self):
        Basic.__init__(self,"Course")
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"DepartmentId"))
        except:
            print("column already initialised")
    def add(self,name,DepartmentId):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?)'''.format(self.objType),(newID,name,DepartmentId))  
        self.conn.commit()

class Rooms(Basic):
    #ID name DepartmentId Capacity
    def __init__(self):
        Basic.__init__(self,"Room")
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"DepartmentId"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"Capacity"))
        except:
            print("column already initialised")
    def add(self,name,department,capacity):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?)'''.format(self.objType),(newID,name,capacity,department))  
        self.conn.commit()

class Teachers(Basic):
    #ID name Courses Timeblocks
    def __init__(self):
        Basic.__init__(self,"Teacher")
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"DepartmentId"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"CourseId"))
        except:
            print("column already initialised")
    def add(self,name,CourseId):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?)'''.format(self.objType),(newID,name,CourseId))  
        self.conn.commit()

class System():
    TimeblockObj = Timeblocks()
    DepartmentObj = Departments()
    CourseObj = Courses()
    RoomObj = Rooms()
    TeacherObj = Teachers()
    @classmethod
    def getDepartments(self):
        return System.DepartmentObj.get()
    @classmethod
    def getCourses(self):
        return System.CourseObj.get()
    @classmethod
    def getRooms(self):
        return System.RoomObj.get()
    @classmethod
    def addDepartment(self,name):
        System.DepartmentObj.add(name)

    def random():
        System.RoomObj.add('Descartes',50,1)
       
   

#GUI front end
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk

global currentFrame



class DepartmentGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.pack()
        tk.Button(self.frame, text="Department", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Course", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Room", command = lambda:newFrame(RoomGUI(root))).pack()
        self.e = tk.Entry(self.frame)
        self.e.pack()
        tk.Button(self.frame, text="add", command = self.addDepartment).pack()

    def addDepartment(self):
        print(self.e.get())
        System.addDepartment(self.e.get())
        
    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getDepartments()
        for data in Data:
            self.tree.insert('',self.tree.size()[0],text = data[0], values = (data[1],))
            
class CourseGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.pack()
        tk.Button(self.frame, text="Department", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Course", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Room", command = lambda:newFrame(RoomGUI(root))).pack()
                         
    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getCourses()
        for data in Data:
            self.tree.insert('',self.tree.size()[0],text = data[0], values = (data[1],data[2]))

class RoomGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','Capacity','Department'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Capacity')
        self.tree.pack()
        tk.Button(self.frame, text="Department", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Course", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Room", command = lambda:newFrame(RoomGUI(root))).pack()
                         
    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getRooms()
        for data in Data:
            self.tree.insert('',self.tree.size()[0],text = data[0], values = (data[1],data[2]))
            
def newFrame(newFrame):
    global currentFrame
    if isinstance(newFrame,tk.Frame) == True:
        currentFrame.pack_forget()
        currentFrame = newFrame
        newFrame.pack()
    else:
        currentFrame.pack_forget()
        currentFrame = newFrame.frame
        newFrame.frame.pack()
        newFrame.updateTree()

def main():
    global currentFrame
    System.random()
    root = tk.Tk()
    root.geometry("1280x720")
    currentFrame = tk.Frame(root, width=1280, height=720, background="bisque")
    currentFrame.pack(fill=None, expand=False)
    tk.Button(currentFrame, text="Department", command = lambda:newFrame(DepartmentGUI(root))).pack()
    tk.Button(currentFrame, text="Course", command = lambda:newFrame(CourseGUI(root))).pack()
    
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("database files","*.db"),("all files","*.*")))
    while True:
        root.update_idletasks()
        root.update()

if __name__ == "__main__":
    main()
