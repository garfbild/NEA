import sqlite3
import random
import copy


class Basic():
    #Basic class is inherited by all other database facing objects. used to establish a connection between the program and the database
    def __init__(self,objType,filename):
        self.objType = objType
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS {}Table({}Id INTEGER PRIMARY KEY, {}Name TEXT)'''.format(self.objType,self.objType,self.objType))
    def get(self):
        self.c.execute('''SELECT * FROM {}Table'''.format(self.objType))
        return self.c.fetchall()
    def getById(self,Id):
        self.c.execute('''SELECT * FROM {}Table WHERE {}Id = {}'''.format(self.objType,self.objType,Id))
        return self.c.fetchall()[0]
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
    def getId(self,name):
        data = self.get()
        for x in range(len(data)):
            if data[x][1] == name:
                return data[x][0]
    def deleteID(self,Id):
        self.c.execute('''DELETE FROM {}Table WHERE {}Id = {}'''.format(self.objType,self.objType,Id))
        self.conn.commit()

class Timeblocks(Basic):
    #time blocks is unique because no new feilds are enterd but instead we only edit the number of periods on each day
    def __init__(self,filename):
        Basic.__init__(self,"Timeblock",filename)
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
    def __init__(self,filename):
        Basic.__init__(self,"Department",filename)
    def add(self,name):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?)'''.format(self.objType),(newID,name))
        self.conn.commit()


class Courses(Basic):
    #ID name DepartmentId
    def __init__(self,filename):
        Basic.__init__(self,"Course",filename)
        try:
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"TimeRequirement"))
            self.c.execute("ALTER TABLE {}Table add column {}".format(self.objType,"DepartmentId"))
        except:
            pass
    def add(self,name,DepartmentId,time):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?)'''.format(self.objType),(newID,name,DepartmentId,time))
        self.conn.commit()

class Rooms(Basic):
    #ID name DepartmentId Capacity
    def __init__(self,filename):
        Basic.__init__(self,"Room",filename)
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
    def __init__(self,filename):
        Basic.__init__(self,"Teacher",filename)
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
    def __init__(self,filename):
        Basic.__init__(self,"Student",filename)
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

class Timetables(Basic):
    #ID name Courses Timeblocks
    def __init__(self,filename):
        Basic.__init__(self,"Timetable",filename)
        try:
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"StudentID"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"CourseID"))
            self.c.execute("ALTER TABLE {}Table ADD COLUMN {}".format(self.objType,"teacherID"))
        except:
            pass
    def add(self,name,student,course,teacher):
        newID = self.getNewID()
        self.c.execute('''INSERT INTO {}Table VALUES (?,?,?,?,?)'''.format(self.objType),(newID,name,student,course,teacher))
        self.conn.commit()

class System:
    def __init__(self,filename):
        self.TimeblockObj = Timeblocks(filename)
        self.DepartmentObj = Departments(filename)
        self.CourseObj = Courses(filename)
        self.RoomObj = Rooms(filename)
        self.TeacherObj = Teachers(filename)
        self.StudentObj = Students(filename)
        self.TimetableObj = Timetables(filename)

    def getDepartments(self):
        return self.DepartmentObj.get()
    def getTimetables(self):
        return self.TimetableObj.get()
    def getDepartmentId(self,name):
        return self.DepartmentObj.getId(name)
    def getCourses(self):
        return self.CourseObj.get()
    def getCourseId(self,name):
        return self.CourseObj.getId(name)
    def getRooms(self):
        return self.RoomObj.get()
    def getTimeblocks(self):
        return self.TimeblockObj.get()
    def getTeachers(self):
        return self.TeacherObj.get()
    def getStudents(self):
        return self.StudentObj.get()
    def addDepartment(self,name):
        self.DepartmentObj.add(name)
    def addCourse(self,name,DepartmentId,time):
        self.CourseObj.add(name,DepartmentId,time)
    def addRoom(self,name,DepartmentId,capacity):
        self.RoomObj.add(name,DepartmentId,capacity)
    def addTimeblock(self,dayID,day,periods):
        self.TimeblockObj.add(dayID,day,periods)
    def addTeacher(self,name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday):
        self.TeacherObj.add(name,department,course,TeachesMonday,TeachesTuesday,TeachesWednesday,TeachesThursday,TeachesFriday)
    def addStudent(self,name,CourseOne,CourseTwo,CourseThree):
        self.StudentObj.add(name,CourseOne,CourseTwo,CourseThree)
    def addTImetable(self,name,student,course,teacher):
        self.TimetableObj.add(name,student,course,teacher)
    def removeDepartment(self,Id):
        return self.DepartmentObj.deleteID(Id)
    def removeCourse(self,Id):
        return self.CourseObj.deleteID(Id)
    def removeRoom(self,Id):
        return self.RoomObj.deleteID(Id)
    def removeTeacher(self,Id):
        return self.TeacherObj.deleteID(Id)
    def removeStudent(self,Id):
        return self.StudentObj.deleteID(Id)
    def getDepartment(self,Id):
        return self.DepartmentObj.getById(Id)
    def getCourse(self,Id):
        return self.CourseObj.getById(Id)
    def getRoom(self,Id):
        return self.RoomObj.getById(Id)
    def getTeacher(self,Id):
        return self.TeacherObj.getById(Id)
    def getStudent(self,Id):
        return self.StudentObj.getById(Id)
    def getTimeblock(self,Id):
        return self.TimeblockObj.getById(Id)

    def MakeTimetable(self,maxclasssize):
        sdata = self.getStudents()
        cdata = self.getCourses()
        Dict = {}
        #for each combination of subjects students have chosen
        for datum in sdata:
            Key=""
            for i in sorted(datum[2:]):
                Key = Key+Two(i)
            try:
                Dict[Key].append(datum[0])
            except:
                Dict[Key] = []
                Dict[Key].append(datum[0])
        #Course1, Course2, Course3, Course, nth class, nth session
        #creating classes which obey the max class size constraint
        classDict = {}
        for Key in Dict:
            count = 1
            while count*maxclasssize < len(Dict[Key]):
                count +=1
            for i in range(0,5,2):
                courseDatum = self.getCourse(int(Key[i:i+2]))
                courseID = Two(courseDatum[0])
                RequiredSessions = courseDatum[3]
                for c in range(RequiredSessions):
                    for n in range(count):
                        tempKey = Key+courseID+Two(n+1)+Two(c+1)
                        classDict[tempKey] = Dict[Key][n*maxclasssize:(n+1)*maxclasssize]
        tdata = self.getTeachers()
        ttdata = self.getTimeblocks()
        sessions = []
        #teacherID nth session
        for datum in tdata:
            Key = ""
            Key = Key+Two(datum[0])
            count = 0
            for day in range(5):
                if datum[4:][day] == 1:
                    for period in range(ttdata[day][2]):
                        count+=1
                        sessions.append(Key+Two(count))

        U = copy.deepcopy(list(classDict.keys()))
        V = copy.deepcopy(sessions)
        random.shuffle(U)
        random.shuffle(V)
        if len(U) > len(V):
            print("insufficent timeslots to accomodate lessons. consider adding more teachers or increasing the maximum class size")
        graph = []
        for u in range(len(U)):
            graph.append([])
            for v in range(len(V)):
                if self.getTeacher(int(V[v][:2]))[3] == int(U[u][6:8]):
                    graph[u].append(1)
                else:
                    graph[u].append(0)

        matchings = HopfcroftKarp(graph)
        for i in matchings:
            print("Students",classDict[U[i[0]-1]]," have ",self.getCourse(int(U[i[0]-1][6:8]))[1]," with ",self.getTeacher(int(V[i[1]-1][:2]))[1])
            for student in classDict[U[i[0]-1]]:
                self.addTImetable(U[i[0]-1]+V[i[1]-1],student,int(U[i[0]-1][6:8]),int(V[i[1]-1][:2]))

def Two(x):
    if len(str(x)) == 1:
        bit = "0"+str(x)
    elif len(str(x)) == 2:
        bit = str(x)
    else:
        panic = True
    return bit

#depth first search.
def DepthFirstSearch(visited,node,graph,M,path):
    #we pass the path as we back up through the recursion
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
            return visited,path
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            if visited != []:
                if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
                    path.append(node)
                    return visited,path
            if node[0] == "u":
                if int(n[1:]) == M[int(node[1])-1]:
                    visited,path = DepthFirstSearch(visited,n,graph,M,path)
            else:
                visited,path = DepthFirstSearch(visited,n,graph,M,path)
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
    return visited,path

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
    for i in range(height):
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

    visited = []
    path = []
    #depth first search.
    #for each free vertex we find the augmenting path between two free vertices
    for freevertex in freevertices:
        path = []
        visited = []
        visited,path = DepthFirstSearch(visited,freevertex,adjgraph,M,path)
        path.reverse()
        if path != []:
            if M[int(path[-1][1:])-1] == 0:
                #symmetric difference of a path and matching
                for x in range(len(path)):
                    if path[x][0] == "u":
                        M[int(path[x][1:])-1] = int(path[x-1][1:])
            else:
                pass
        else:
            pass

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
class BasicGUI:
    def __init__(self,system,root):
        self.system = system
        self.root = root
        tk.Button(self.frame, text="Departments", command = lambda:newFrame(DepartmentGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Courses", command = lambda:newFrame(CourseGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Rooms", command = lambda:newFrame(RoomGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Timeblocks", command = lambda:newFrame(TimeblockGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Teachers", command = lambda:newFrame(TeacherGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Students", command = lambda:newFrame(StudentGUI(root,self.system))).pack()
        tk.Button(self.frame, text="Timetable", command = lambda:newFrame(TimetableGUI(root,self.system))).pack()


class DepartmentGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
        self.tree = ttk.Treeview(self.frame,columns=('Name'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.pack()

        BasicGUI.__init__(self,system,root)

        self.e = tk.Entry(self.frame)
        self.e.pack()
        tk.Button(self.frame, text="add department", command = self.addDepartment).pack()
        self.i = tk.Entry(self.frame)
        self.i.pack()
        tk.Button(self.frame, text="remove department", command = self.removeDepartment).pack()

    def addDepartment(self):
        if self.e.get != "":
            self.system.addDepartment(self.e.get())
            self.updateTree()

    def removeDepartment(self):
        self.system.removeDepartment(self.i.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getDepartments()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],))

class CourseGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department','TimeRequirement'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.heading('#3', text='TimeRequirement')
        self.tree.pack()

        BasicGUI.__init__(self,system,root)

        self.e = tk.Entry(self.frame)
        self.e.pack()
        self.comboBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getDepartments()])
        self.comboBox.pack()
        self.t = tk.Entry(self.frame)
        self.t.pack()
        tk.Button(self.frame, text="add course", command = self.addCourse).pack()

        self.i = tk.Entry(self.frame)
        self.i.pack()
        tk.Button(self.frame, text="remove course", command = self.removeCourse).pack()


    def addCourse(self):
        try:
            self.system.addCourse(self.e.get(),self.system.DepartmentObj.getId(self.comboBox.get()),int(self.t.get()))
            self.updateTree()
        except:
            print("ERROR: ",self.t.get(),"is not a valid amount of time. Make sure your using an integer")


    def removeCourse(self):
        self.system.removeCourse(self.i.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getCourses()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3]))

class RoomGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
        self.tree = ttk.Treeview(self.frame,columns=('Name','Department','Capacity'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Department')
        self.tree.heading('#3', text='Capacity')

        self.tree.pack()
        BasicGUI.__init__(self,system,root)

        self.n = tk.Entry(self.frame)
        self.n.pack()
        self.comboBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getDepartments()])
        self.comboBox.pack()
        self.c = tk.Entry(self.frame)
        self.c.pack()

        tk.Button(self.frame, text="add room", command = self.addRoom).pack()

        self.i = tk.Entry(self.frame)
        self.i.pack()
        tk.Button(self.frame, text="remove room", command = self.removeRoom).pack()

    def addRoom(self):
        try:
            self.system.addRoom(self.n.get(),self.system.getDepartmentId(self.comboBox.get()),int(self.c.get()))
            self.updateTree()
        except:
            print("ERROR: ",self.c.get(),"is not a valid amount of time. Make sure your using an integer")


    def removeRoom(self):
        self.system.removeRoom(self.i.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getRooms()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3]))

class TimeblockGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
        self.tree = ttk.Treeview(self.frame,columns=('Day','Periods'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Day')
        self.tree.heading('#2', text='Periods')
        self.tree.pack()

        BasicGUI.__init__(self,system,root)

        self.dict = {"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5}

        self.comboBox = ttk.Combobox(self.frame,
                            values=["Monday","Tuesday","Wednesday","Thursday","Friday"])
        self.comboBox.pack()
        tk.Label(self.frame, textvariable="periods")
        self.p = tk.Entry(self.frame)
        self.p.pack()
        tk.Button(self.frame, text="save", command = self.addTimeblocks).pack()

    def addTimeblocks(self):
        try:
            self.system.addTimeblock(self.dict[self.comboBox.get()],self.comboBox.get(),int(self.p.get()))
        except:
            print("ERROR: ",self.p.get(),"is not a valid number of periods. Make sure your using an integer")

    def updateTree(self):
        print(self.tree.get_children())
        print(*self.tree.get_children())
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getTimeblocks()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2]))

class TeacherGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
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

        BasicGUI.__init__(self,system,root)

        self.n = tk.Entry(self.frame)
        self.n.pack()

        self.DepartmentBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getDepartments()])
        self.DepartmentBox.pack()
        self.CourseBox = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getCourses()])
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

        self.i = tk.Entry(self.frame)
        self.i.pack()
        tk.Button(self.frame, text="remove teacher", command = self.removeTeacher).pack()

    def addTeacher(self):
        self.system.addTeacher(self.n.get(),self.system.getDepartmentId(self.DepartmentBox.get()),self.system.getCourseId(self.CourseBox.get()),self.Monday.get(),self.Tuesday.get(),self.Wednesday.get(),self.Thursday.get(),self.Friday.get())
        self.updateTree()

    def removeTeacher(self):
        self.system.removeTeacher(self.i.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getTeachers()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3],Data[i][4],Data[i][5],Data[i][6],Data[i][7],Data[i][8]))

class StudentGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)
        self.tree = ttk.Treeview(self.frame,columns=('Name','CourseOne','CourseTwo','CourseThree'))
        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='CourseOne')
        self.tree.heading('#3', text='CourseTwo')
        self.tree.heading('#4', text='CourseThree')
        self.tree.pack()

        BasicGUI.__init__(self,system,root)

        self.n = tk.Entry(self.frame)
        self.n.pack()

        self.CourseBoxOne = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getCourses()])
        self.CourseBoxOne.pack()
        self.CourseBoxTwo = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getCourses()])
        self.CourseBoxTwo.pack()
        self.CourseBoxThree = ttk.Combobox(self.frame,
                            values=[data[1] for data in self.system.getCourses()])
        self.CourseBoxThree.pack()

        tk.Button(self.frame, text="add student", command = self.addStudents).pack()

        self.i = tk.Entry(self.frame)
        self.i.pack()
        tk.Button(self.frame, text="remove student", command = self.removeStudent).pack()

    def addStudents(self):
        if self.CourseBoxOne.get() != self.CourseBoxTwo.get() and self.CourseBoxOne.get() != self.CourseBoxThree.get() and self.CourseBoxTwo.get() != self.CourseBoxThree.get() and self.CourseBoxOne.get() != "" and self.CourseBoxTwo.get() != "" and self.CourseBoxThree.get() != "" and self.n.get() != "":
            self.system.addStudent(self.n.get(),self.system.getCourseId(self.CourseBoxOne.get()),self.system.getCourseId(self.CourseBoxTwo.get()),self.system.getCourseId(self.CourseBoxThree.get()))
            self.updateTree()
        else:
            print("ERROR: please select three unique courses")

    def removeStudent(self):
        self.system.removeStudent(self.i.get())
        self.updateTree()

    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        Data = self.system.getStudents()
        for i in range(len(Data)-1,-1,-1):
            self.tree.insert('',self.tree.size()[0],text = Data[i][0], values = (Data[i][1],Data[i][2],Data[i][3],Data[i][4]))

class TimetableGUI(BasicGUI):
    def __init__(self,root,system):
        self.frame = tk.Frame(root, width=1280, height=720)

        BasicGUI.__init__(self,system,root)

        self.m = tk.Entry(self.frame)
        self.m.pack()
        tk.Button(self.frame, text="create timetable", command = self.buttonCommand).pack()

    def updateTree(self):
        pass

    def buttonCommand(self):
        maxclasssize = int(self.m.get())
        if maxclasssize > 0:
            self.system.MakeTimetable(maxclasssize)
        else:
            print("ERROR intger max class size 1")
        try:
            maxclasssize = int(self.m.get())
            if maxclasssize > 0:
                self.system.MakeTimetable(maxclasssize)
            else:
                print("ERROR intger max class size 1")
        except:
            print("ERROR intger max class size 2")
            pass

def newFrame(newFrame):
    for frame in newFrame.root.winfo_children():
        frame.forget()
    if isinstance(newFrame,tk.Frame) == True:
        newFrame.pack()
    else:
        newFrame.frame.pack()
        try:
            newFrame.updateTree()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    tk.Frame(root, width=1280, height=720).pack(fill=None, expand=False)
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("database files","*.db"),("all files","*.*")))
    system = System(root.filename)
    newFrame(DepartmentGUI(root,system))
    while True:
        root.update_idletasks()
        root.update()
