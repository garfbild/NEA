import sqlite3
import random
import string
import copy
global path
global currentFrame


class Basic():
    def __init__(self,objType):
        self.objType = objType
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS {}Table({}Id INTEGER PRIMARY KEY, {}Name TEXT)'''.format(self.objType,self.objType,self.objType))
    def get(self):
        self.c.execute('''SELECT * FROM {}Table'''.format(self.objType))
        return self.c.fetchall()
    def getNewID(self):
        self.c.execute('''SELECT {}Id FROM {}Table ORDER BY {}Id DESC;'''.format(self.objType,self.objType,self.objType))
        IDS = self.c.fetchall()
        if IDS == []:
            return 1
        else:
            return IDS[0][-1] + 1

    def close(self):
        self.conn.commit()
        self.conn.close()

class Timeblocks(Basic):
    def __init__(self):
        Basic.__init__(self,"Timeblock")
        self.days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.c.execute('''PRAGMA table_info(TimeblockTable)''')
        if self.c.fetchall()[1][1] == "TimeblockName":
            self.c.execute('''DROP TABLE TimeblockTable''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS TimeblockTable(TimeblockId INTEGER PRIMARY KEY, Day TEXT, Periods INTEGER)''')

    def add(self,dayID,day,periods):
        try:
            for i in range(5):
                self.c.execute('''INSERT INTO {}Table VALUES (?,?,?)'''.format(self.objType),(i+1,self.days[i],0))
        except:
            pass
        self.c.execute('''UPDATE TimeblockTable SET Periods = {} WHERE TimeblockId = {}'''.format(periods,dayID))
        self.conn.commit()


class Departments(Basic):
    #ID name
    def __init__(self):
        Basic.__init__(self,"Department")
    def add(self,name):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?)'''.format(self.objType),(newID,name))
        self.conn.commit()
    def getId(self,name):
        data = self.get()
        for x in range(len(data)):
            if data[x][1] == name:
                return data[x][0]

class Courses(Basic):
    #ID name DepartmentId
    def __init__(self):
        Basic.__init__(self,"Course")
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"TimeRequirement"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"DepartmentId"))
        except:
            pass
    def add(self,name,DepartmentId,time):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?)'''.format(self.objType),(newID,name,DepartmentId,time))
        self.conn.commit()
    def getId(self,name):
        data = self.get()
        for x in range(len(data)):
            if data[x][1] == name:
                return data[x][0]

class Rooms(Basic):
    #ID name DepartmentId Capacity
    def __init__(self):
        Basic.__init__(self,"Room")
        try:
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"DepartmentId"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"Capacity"))
        except:
            pass
    def add(self,name,department,capacity):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?)'''.format(self.objType),(newID,name,department,capacity))
        self.conn.commit()

class Teachers(Basic):
    #ID name Courses Timeblocks
    def __init__(self):
        Basic.__init__(self,"Teacher")
        try:
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"DepartmentId"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"CourseId"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"TeachesMonday"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"TeachesTuesday"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"TeachesWednesday"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"TeachesThursday"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"TeachesFriday"))
        except:
            pass
    def add(self,name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?,?,?,?,?,?)'''.format(self.objType),(newID,name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday))
        self.conn.commit()

class Students(Basic):
    def __init__(self):
        Basic.__init__(self,"Student")
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"CourseOne"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"CourseTwo"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"CourseThree"))
        except:
            pass
    def add(self,name,CourseOne,CourseTwo,CourseThree):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?,?)'''.format(self.objType),(newID,name,CourseOne,CourseTwo,CourseThree))
        self.conn.commit()

class System(Basic):
    TimeblockObj = Timeblocks()
    DepartmentObj = Departments()
    CourseObj = Courses()
    RoomObj = Rooms()
    TeacherObj = Teachers()
    StudentObj = Students()
    @classmethod
    def getDepartments(self):
        return System.DepartmentObj.get()
    @classmethod
    def getDepartmentId(self,name):
        return System.DepartmentObj.getId(name)
    @classmethod
    def getCourses(self):
        return System.CourseObj.get()
    @classmethod
    def getCourseId(self,name):
        return System.CourseObj.getId(name)
    @classmethod
    def getRooms(self):
        return System.RoomObj.get()
    @classmethod
    def getTimeblocks(self):
        return System.TimeblockObj.get()
    @classmethod
    def getTeachers(self):
        return System.TeacherObj.get()
    @classmethod
    def getStudents(self):
        return System.StudentObj.get()
    @classmethod
    def addDepartment(self,name):
        System.DepartmentObj.add(name)
    @classmethod
    def addCourse(self,name,DepartmentId,time):
        System.CourseObj.add(name,DepartmentId,time)
    @classmethod
    def addRoom(self,name,DepartmentId,capacity):
        System.RoomObj.add(name,DepartmentId,capacity)
    @classmethod
    def addTimeblock(self,dayID,day,periods):
        System.TimeblockObj.add(dayID,day,periods)
    @classmethod
    def addTeacher(self,name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday):
        System.TeacherObj.add(name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday)
    @classmethod
    def addStudent(self,name,CourseOne,CourseTwo,CourseThree):
        System.StudentObj.add(name,CourseOne,CourseTwo,CourseThree)
    @classmethod
    def Two(self,x):
        if len(str(x)) == 1:
            bit = "0"+str(x)
        elif len(str(x)) == 2:
            bit = str(x)
        else:
            panic = True
        return bit
    @classmethod
    def MakeTimetable(self):
        # first course, second course, third course,course id, nth class
        # student classes
        sdata = System.getStudents()
        cdata = System.getCourses()
        dictionary = {}
        for datum in sdata:
            Key=""
            for i in sorted(datum[2:]):
                Key = Key+System.Two(i)

            try:
                dictionary[Key].append(datum[0])
            except:
                dictionary[Key] = []
                dictionary[Key].append(datum[0])
        classes = []
        for Key in dictionary:
            classsize = len(dictionary[Key])
            for i in range(0,5,2):
                x = cdata[int(Key[i:i+2])-1]
                a = System.Two(x[0])
                b = x[3]
                for c in range(b):
                    classes.append(Key+a+System.Two(c+1))
        print(classes)
        # teacher id ,day, period
        # teacher time block
        sessions = []
        tdata = System.getTeachers()
        ttdata = System.getTimeblocks()
        for teacher in tdata:
            Key = ""
            Key = Key+System.Two(teacher[0])
            for day in range(5):
                if teacher[4:][day] == 1:
                    for period in range(ttdata[day][2]):
                        sessions.append(Key+System.Two(day+1)+System.Two(period+1))
        print(sessions)
        graph = []
        for x in range(len(classes)):
            graph.append([])
            for y in range(len(sessions)):
                graph[x].append(0)

        for c in range(len(classes)):
            for t in range(len(sessions)):
                # if techer course == class course
                if tdata[int(sessions[t][:2])-1][3] == int(classes[c][6:8]):
                    graph[c][t] = 1

        matchings = HopfcroftKarp(graph)
        print(matchings)


#depth first search.
def DepthFirstSearch(visited,node,graph,M):
    #we pass the path as we back up through the recursion
    global path
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
            return visited
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            if visited != []:
                if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
                    path.append(node)
                    return visited
            if node[0] == "u":
                if int(n[1:]) == M[int(node[1])-1]:
                    visited = DepthFirstSearch(visited,n,graph,M)
            else:
                visited = DepthFirstSearch(visited,n,graph,M)
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
            return visited

    return visited

def HopfcroftKarp(rawgraph):
    height,width = len(rawgraph),len(rawgraph[0])
    graph = []
    for u in range(height+1):
        graph.append([])
        for v in range(width+1):
            graph[u].append(0)

    for u in range(height):
        for v in range(width):
            graph[u+1][v+1] = rawgraph[u][v]

    #1----1
    #2-\  2
    #3  \-3

    # 1 2 3
    #1.
    #2  .
    #3    .
    M = []
    for i in range(width):
        M.append(0)
    #u    v
    #u1    v3
    #u2    v2
    #u3    v4
    #...
    graphcopy = copy.deepcopy(graph)
    #adding labels around the edge
    for u in range(width):
        graph[0][u+1] = u+1
    for v in range(height):
        graph[v+1][0] = v+1

    #bfs to get initial matching
    for u in range(1,height+1):
        for v in range(1,width+1):
            if graph[u][v] == 1:
                M[u-1] = v
                for p in range(1,width+1):
                    graph[u][p] = 0
                for p in range(1,height+1):
                    graph[p][v] = 0
                break

    #finding free freevertices
    freevertices = []
    for node in range(width):
        freevertices.append(node+1)
    for m in M:
        if m != 0:
            freevertices[m-1] = "#"

    i = 0
    while i < len(freevertices):
        if freevertices[i] == "#":
            del freevertices[i]
        else:
            freevertices[i] = "v{}".format(freevertices[i])
            i+=1

    #converting adjacency matrix into adjacency list
    adjgraph = {}
    graph = copy.deepcopy(graphcopy)
    for u in range(1,height+1):
        temp = []
        for v in range(1,width+1):
            if graph[u][v] == 1:
                temp.append("v{}".format(v))
        adjgraph["u{}".format(u)] = temp

    for v in range(1,width+1):
        temp = []
        for u in range(1,height+1):
            if graph[u][v] == 1:
                temp.append("u{}".format(u))
        adjgraph["v{}".format(v)] = temp

    global path
    visited = []
    path = []
    #depth first search.
    #for each free vertex we find the augmenting path between two free vertices
    print(freevertices)
    for freevertex in freevertices:
        path = []
        visited = []
        DepthFirstSearch(visited,freevertex,adjgraph,M)
        path.reverse()
        print(path)
        if path != []:
            if M[int(path[-1][1:])-1] == 0:
                #symmetric difference of a path and matching
                for x in range(len(path)):
                    if path[x][0] == "u":
                        M[int(path[x][1:])-1] = int(path[x-1][1:])
            else:
                print(freevertex,"has no augmentingpath")
        else:
            print(freevertex,"has no augmentingpath")

    matchings = []
    for x in range(len(M)):
        if M[x] != 0:
            matchings.append([x+1,M[x]])
    return matchings

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
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()
        tk.Button(self.frame, text="Timeblocks", command = lambda:newFrame(TimeblockGUI(root))).pack()
        tk.Button(self.frame, text="Teachers", command = lambda:newFrame(TeacherGUI(root))).pack()
        tk.Button(self.frame, text="Students", command = lambda:newFrame(StudentGUI(root))).pack()
        tk.Button(self.frame, text="Create Timetable", command = lambda:newFrame(TimetableGUI(root))).pack()
        tk.Button(self.frame, text="create timetable", command = System.MakeTimetable).pack()



        self.e = tk.Entry(self.frame)
        self.e.pack()
        tk.Button(self.frame, text="add department", command = self.addDepartment).pack()

    def addDepartment(self):
        System.addDepartment(self.e.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getDepartments()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],))

class CourseGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department','TimeRequirement'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.heading('#3', text='TimeRequirement')
        self.tree.pack()
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()
        self.e = tk.Entry(self.frame)
        self.e.pack()
        self.comboBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getDepartments()])
        self.comboBox.pack()
        self.t = tk.Entry(self.frame)
        self.t.pack()
        tk.Button(self.frame, text="add course", command = self.addCourse).pack()


    def addCourse(self):
        System.addCourse(self.e.get(),System.DepartmentObj.getId(self.comboBox.get()),int(self.t.get()))
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getCourses()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3]))

class RoomGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department','Capacity'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.heading('#3', text='Capacity')

        self.tree.pack()
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()

        self.n = tk.Entry(self.frame)
        self.n.pack()
        self.comboBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getDepartments()])
        self.comboBox.pack()
        self.c = tk.Entry(self.frame)
        self.c.pack()

        tk.Button(self.frame, text="add room", command = self.addRoom).pack()

    def addRoom(self):
        System.addRoom(self.n.get(),System.getDepartmentId(self.comboBox.get()),self.c.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getRooms()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3]))

class TimeblockGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()
        self.dict = {"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5}

        self.comboBox = ttk.Combobox(self.frame,
                            values=["Monday","Tuesday","Wednesday","Thursday","Friday"])
        self.comboBox.pack()
        tk.Label(self.frame, textvariable="periods")
        self.p = tk.Entry(self.frame)
        self.p.pack()
        tk.Button(self.frame, text="save", command = self.addTimeblocks).pack()

    def addTimeblocks(self):
        periods = self.p.get()
        System.addTimeblock(self.dict[self.comboBox.get()],self.comboBox.get(),periods)

    def updateTree(self):
        pass

class TeacherGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department','Course','TeachesMonday','TeachesTuesday','TeachesWednesday','TeachesThursday','TeachesFriday'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.heading('#3', text='Course')
        self.tree.heading('#4', text='TeachesMonday')
        self.tree.heading('#5', text='TeachesTuesday')
        self.tree.heading('#6', text='TeachesWednesday')
        self.tree.heading('#7', text='TeachesThursday')
        self.tree.heading('#8', text='TeachesFriday')
        self.tree.pack()
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()

        self.n = tk.Entry(self.frame)
        self.n.pack()

        self.DepartmentBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getDepartments()])
        self.DepartmentBox.pack()
        self.CourseBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getCourses()])
        self.CourseBox.pack()

        self.Monday = tk.IntVar()
        self.Tuesday = tk.IntVar()
        self.Wednesday = tk.IntVar()
        self.Thursday = tk.IntVar()
        self.Friday = tk.IntVar()

        tk.Checkbutton(self.frame, text="Monday", variable=self.Monday).pack()
        tk.Checkbutton(self.frame, text="Tuesday", variable=self.Tuesday).pack()
        tk.Checkbutton(self.frame, text="Wednesday", variable=self.Wednesday).pack()
        tk.Checkbutton(self.frame, text="Thursday", variable=self.Thursday).pack()
        tk.Checkbutton(self.frame, text="Friday", variable=self.Friday).pack()

        tk.Button(self.frame, text="add teacher", command = self.addTeacher).pack()

    def addTeacher(self):
        System.addTeacher(self.n.get(),System.getDepartmentId(self.DepartmentBox.get()),System.getCourseId(self.CourseBox.get()),self.Monday.get(),self.Tuesday.get(),self.Wednesday.get(),self.Thursday.get(),self.Friday.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getTeachers()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3],Data[i][4],Data[i][5],Data[i][6],Data[i][7],Data[i][8]))

class StudentGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        self.tree = ttk.Treeview(self.frame,columns=('Name','CourseOne','CourseTwo','CourseThree'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='CourseOne')
        self.tree.heading('#3', text='CourseTwo')
        self.tree.heading('#4', text='CourseThree')
        self.tree.pack()

        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root))).pack()

        self.n = tk.Entry(self.frame)
        self.n.pack()

        self.CourseBoxOne = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getCourses()])
        self.CourseBoxOne.pack()
        self.CourseBoxTwo = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getCourses()])
        self.CourseBoxTwo.pack()
        self.CourseBoxThree = ttk.Combobox(self.frame,
                            values=[data[1] for data in System.getCourses()])
        self.CourseBoxThree.pack()

        tk.Button(self.frame, text="add student", command = self.addStudents).pack()

    def addStudents(self):
        System.addStudent(self.n.get(),System.getCourseId(self.CourseBoxOne.get()),System.getCourseId(self.CourseBoxTwo.get()),System.getCourseId(self.CourseBoxThree.get()))
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = System.getStudents()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3],Data[i][4]))

class TimetableGUI:
    def __init__(self,root):
        self.frame = tk.Frame(root, width=1280, height=720, background="bisque")
        tk.Button(self.frame, text="create timetable", command = System.MakeTimetable).pack()

    def updateTree(self):
        pass

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
        try:
            newFrame.updateTree()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    currentFrame = tk.Frame(root, width=1280, height=720, background="bisque")
    currentFrame.pack(fill=None, expand=False)
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("database files","*.db"),("all files","*.*")))
    newFrame(DepartmentGUI(root))
    while True:
        root.update_idletasks()
        root.update()
