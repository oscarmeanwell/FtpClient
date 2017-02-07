from tkinter import *
from ftplib import FTP
import os, shutil
root = Tk()
class BuildFtp():
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('FTP Client')
        self.parent.geometry("1100x600")
        self.parent.configure(background="steel blue")
        self.parent.grid()
        self.parent.resizable(0,0)
        self.CreateFrames()
        self.AddButtons()
        self.AddLabel()
        self.AddEntrys()
        self.AddListbox()
        self.PoppulateLocal()
        
    def CreateFrames(self):
        """Create The Frames"""
        self.EntryFrm = Frame(self.parent, bg = "steel blue")
        self.EntryFrm.grid(row = 0, column = 0)
        self.LstFrm = Frame(self.parent, bg = "steel blue")
        self.LstFrm.grid(row = 1, column = 0)
        self.BtnFrm = Frame(self.parent, bg = "steel blue")
        self.BtnFrm.grid(row = 2, column = 0)

    def AddButtons(self):
        """Add Button"""
        self.LoginBtn = Button(self.EntryFrm, text = "Login", height = 2, width = 10, fg = "black", activebackground = "yellow", bg = "light blue", command = self.Login)
        self.LocalUpLvl = Button(self.BtnFrm, text = "Up Level", fg = "black", activebackground = "yellow", bg = "light blue", command = self.UpLocal)
        self.RemoteUpLvl = Button(self.BtnFrm, text = "Up Level", fg = "black", activebackground = "yellow", bg = "light blue", command = self.UpRemote)
        self.RemoteNewF = Button(self.BtnFrm, text = "New Folder", fg = "black", activebackground = "yellow", bg = "light blue", command = self.NewRemoteFolder)
        self.LocalNewF = Button(self.BtnFrm, text = "New Folder", fg = "black", activebackground = "yellow", bg = "light blue", command = self.NewLocalFolder)
        self.RemoteDel = Button(self.BtnFrm, text = "Delete", fg = "black", activebackground = "yellow", bg = "light blue", command = self.RemoteDel)
        self.LocalDel = Button(self.BtnFrm, text = "Delete", fg = "black", activebackground = "yellow", bg = "light blue", command = self.LocalDel)
        self.LoginBtn.grid(row = 0, column = 8, padx = 10, pady = 10)
        self.LocalUpLvl.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.LocalNewF.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.LocalDel.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.RemoteUpLvl.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.RemoteNewF.grid(row = 1, column = 4, padx = 10, pady = 10)
        self.RemoteDel.grid(row = 1, column = 5, padx = 10, pady = 10)
    def LocalDel(self):
        self.Selection3 = self.LocalLst.curselection()
        self.Value3 = self.LocalLst.get(self.Selection3[0])
        self.Cdir3 = os.getcwd()
        self.NewDir3 = self.Cdir3 + chr(92) + self.Value3
        self.Question = messagebox.askyesno("Delete Query", "Are you sure?")
        if self.Question:
            if '.' not in self.NewDir3:
                shutil.rmtree(self.NewDir3)
            else:
                os.remove(self.NewDir3)
            self.PoppulateLocal()
            
             
    def RemoteDel(self):
        self.Selection4 = self.RemoteLst.curselection()
        self.Value4 = self.RemoteLst.get(self.Selection4[0])
        self.Question2 = messagebox.askyesno("Delete Query", "Are you sure?")
        if self.Question2:
            if '.' in self.Value4:
                self.SERVER.delete(self.Value4)
            else:
                self.SERVER.rmd(self.Value4)
            self.PoppulateRemote()

    def AddListbox(self):
        self.LocalLst = Listbox(self.LstFrm, bd = 4, height = 20, width = 60, font = ("Calibri", 12), selectbackground = 'red', selectmode = EXTENDED)
        self.RemoteLst = Listbox(self.LstFrm, bd = 4, height = 20, width = 60, font = ("Calibri", 12), selectbackground = 'red', selectmode = EXTENDED)
        self.LocalLst.bind('<Double-Button-1>', self.Forwarddir)
        self.RemoteLst.bind('<Double-Button-1>', self.RemoteForwarddir)
        self.LocalLst.grid(row = 0, column = 0, padx = 30, pady = 10)
        self.RemoteLst.grid(row = 0, column = 1, padx = 30, pady = 10)
        
    def AddLabel(self):
        """Add Label"""
        self.HostLbl = Label(self.EntryFrm, text = "Hostname: ", bg = "steel blue", font = ("Calibri", 12))
        self.UserLbl = Label(self.EntryFrm, text = "Username: ", bg = "steel blue", font = ("Calibri", 12))
        self.PwdLbl = Label(self.EntryFrm, text = "Password: ", bg = "steel blue", font = ("Calibri", 12))
        self.PortLbl = Label(self.EntryFrm, text = "Port: ", bg = "steel blue", font = ("Calibri", 12))
        self.HostLbl.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.UserLbl.grid(column = 2, row = 0, padx = 10, pady = 10)
        self.PwdLbl.grid(column = 4, row = 0, padx = 10, pady = 10)
        self.PortLbl.grid(column = 6, row = 0, padx = 10, pady = 10)

    def AddEntrys(self):
        """Add Entrys"""
        self.HostEnt = Entry(self.EntryFrm, bd = 4, width = 17, font = ("Calibri", 10))
        self.UserEnt = Entry(self.EntryFrm, bd = 4, width = 17, font = ("Calibri", 10))
        self.PwdEnt = Entry(self.EntryFrm, bd = 4, width = 17, font = ("Calibri", 10), show = '*')
        self.PortEnt = Entry(self.EntryFrm, bd = 4, width = 17, font = ("Calibri", 10))
        self.PortEnt.insert(END, "21")
        self.HostEnt.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.UserEnt.grid(column = 3, row = 0, padx = 10, pady = 10)
        self.PwdEnt.grid(column = 5, row = 0, padx = 10, pady = 10)
        self.PortEnt.grid(column = 7, row = 0, padx = 10, pady = 10)

    def UpLocal(self):
        os.chdir("..")
        self.PoppulateLocal()
        
    def UpRemote(self):
        self.SERVER.cwd("..")
        self.PoppulateRemote()
        
    def NewLocalFolder(self):
        x = True
        NewFolder(x)

    def NewRemoteFolder(self):
        x = False
        NewFolder(x)
        
    def Forwarddir(self, event):
        self.Widget = event.widget
        self.Selection = self.Widget.curselection()
        self.Value = self.Widget.get(self.Selection[0])
        self.Cdir = os.getcwd()
        self.NewDir = self.Cdir + chr(92) + self.Value
        try:
            os.chdir(self.NewDir)
            self.PoppulateLocal()
        except:pass
        
    def PoppulateLocal(self):
        self.LocalLst.delete(0, END)
        self.LocalDirLst = os.listdir()
        for i in range(len(self.LocalDirLst)):
            self.LocalLst.insert(i, self.LocalDirLst[i - 1])

    def PoppulateRemote(self):
        self.RemoteLst.delete(0, END)
        self.DirLst = self.SERVER.nlst()
        for i in range(len(self.DirLst)):
            self.RemoteLst.insert(i, (self.DirLst[i - 1]))

    def RemoteForwarddir(self, event):
        self.Widget2 = event.widget
        self.Selection2 = self.Widget2.curselection()
        self.Value2 = self.Widget2.get(self.Selection2[0])
        if '.' not in self.Value2:
            try:
                self.SERVER.cwd(self.Value2)
                self.PoppulateRemote()
            except:pass
        else:pass

    def Login(self):
        self.HostHold = self.HostEnt.get()
        self.UserHold = self.UserEnt.get()
        self.PwdHold = self.PwdEnt.get()
        self.PortHold = self.PortEnt.get()
        try:
            self.SERVER = FTP(self.HostHold)
        except:
            messagebox.showerror("Server Connection", "Cannot Connect to server")
        try:
            self.SERVER.login(self.UserHold, self.PwdHold)
            messagebox.showinfo("Server Connection", "Succesfully logged in! Welcome " + self.UserHold + ".")
            self.PoppulateRemote()
        except:
            messagebox.showerror("Server Login", "User Login details incorrect")

    def NewRm(self, new):
        try:
            self.SERVER.mkd(new)
        except:
            messagebox.showerror("Folder Creation", "Folder Creation Failed - Permission denied")
            
        
class NewFolder():
    def __init__(self, x):
        self.x = x
        self.parent = Tk()
        self.parent.title('Folder Name')
        self.parent.geometry("250x250")
        self.parent.configure(background="steel blue")
        self.parent.grid()
        self.parent.resizable(0,0)
        self.AddStuff()
        
    def AddStuff(self):
        self.Lbl = Label(self.parent, text = "Enter Folder Name", bg = "steel blue", font = ("Calibri", 12))
        self.Ent = Entry(self.parent, bd = 4, width = 25, font = ("Calibri", 10))
        self.Btn = Button(self.parent, text = "Create", height = 2, width = 10, fg = "black", activebackground = "yellow", bg = "light blue", command = self.Create)
        self.Lbl.grid(row = 0, column = 0, padx = 20, pady = 20)
        self.Ent.grid(row = 1, column = 0, padx = 20, pady = 20)
        self.Btn.grid(row = 2, column = 0, padx = 20, pady = 20)
        
    def Create(self):
        self.Breaker = True
        for x in self.Ent.get():
            if x in[' /', '?', '<', '>', ':,', '*', '|'] or x == chr(92):
                messagebox.showerror("User Error", "Folder name cannot contain  / ? < > \ : * |")
                self.Breaker = False
                break
            
        if len(self.Ent.get()) < 1: ####validation needed, e.g. ;' cannot be used as file names
            messagebox.showerror("User Error", "Folders need names!!")
    
        elif self.Breaker:
            if self.x:
                os.makedirs(self.Ent.get())
                buildftp.PoppulateLocal()
            else:
                z = self.Ent.get()
                buildftp.NewRm(z)
                buildftp.PoppulateRemote()
            self.parent.destroy()
                  
            
buildftp = BuildFtp(root)
root.mainloop()



