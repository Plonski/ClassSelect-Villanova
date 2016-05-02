from tkinter import Label, Menu, Frame, TOP, BOTH, Tk, BOTTOM, Button, HORIZONTAL, Entry, E
import retrieve
from tkinter import ttk


master = Tk()
master.title("Class Alert")


def contactInfo():
    contactWindow = Tk()

    contact = Label(contactWindow, text="Contact:\n Thomas Plonski\n"
                                        "thomas.plonski@yahoo.com\n"
                                        "github.com/plonski")
    contact.pack()
    contactWindow.mainloop()


def instructions():
    instructionsWindow = Tk()

    instructions = Label(instructionsWindow, text="1. Make sure to have Firefox installed\n"
                                                  "2. Input your Villanova username\n"
                                                  "3. Input a valid Course Registration Number(CRN)\n"
                                                  "4. Do not close the FireFox browser\n"
                                                  "5. An email will be sent to your @villanova address when a spot opens up in the class\n"
                         )
    instructions.pack()
    instructionsWindow.mainloop()


subMenu = Menu(master)
Menu(master).add_cascade(label="Help", menu=subMenu)
subMenu.add_cascade(label="Instructions", command=instructions)
subMenu.add_cascade(label="Contact", command=contactInfo)
master.config(menu=subMenu)

topFrame = Frame(master)
topFrame.pack(side=TOP, fill=BOTH)

userLabel = Label(topFrame, text="Enter Villanova username:", fg="red", font=("Helvetica", 16))
userLabel.grid(row=0, sticky=E, padx=20)

usernameEntry = Entry(topFrame, fg="red")
usernameEntry.grid(row=0, column=1)
cDone = False
uDone = False


def goodUser():
    errorMsg = Tk()

    goodCRN = Label(errorMsg, text="Please enter a valid Villanova username")

    goodCRN.pack()
    errorMsg.mainloop()


def getUser():
    if len(usernameEntry.get()) < 3:
        goodUser()
    else:
        userInfo['text'] = "Your Villanova email is: " + usernameEntry.get() + "@villanova.edu"
        check()


addUsernameButton = Button(topFrame, text="Add your Villanova username", fg="red", command=lambda: getUser())
addUsernameButton.grid(row=0, column=2)

bottomFrame = Frame(master)
bottomFrame.pack(side=BOTTOM, fill=BOTH)

crnLabel = Label(bottomFrame, text="Enter your desired CRN: ", fg="green", font=("Helvetica", 16))
crnLabel.grid(row=1, column=0, sticky=E, padx=20)

crnEntry = Entry(bottomFrame, fg="red")
crnEntry.grid(row=1, column=1)


def goodCRN():
    errorMsg = Tk()

    goodCRN = Label(errorMsg, text="Please enter a valid CRN:\n"
                                   "It is a 5 digit number used for registration\n"
                                   "It is NOT the class number"
                    )
    goodCRN.pack()
    errorMsg.mainloop()


def getCRN():
    if len(crnEntry.get()) != 5 or crnEntry.get().isdigit() == False:
        goodCRN()
    else:
        crnInfo['text'] = "Your desired CRN is: " + crnEntry.get()
        check()
        return cDone


addClassButton = Button(bottomFrame, text="Add class", fg="green", command=lambda: getCRN())
addClassButton.grid(row=1, column=2)

userInfo = Label(bottomFrame, text="Your Villanova email is: " + usernameEntry.get())
userInfo.grid(columnspan=2)

crnInfo = Label(bottomFrame, text="Your desired CRN is: " + crnEntry.get())
crnInfo.grid(columnspan=2)

registerMe = Button(bottomFrame, text="Register me", fg="green",
                    command=lambda: retrieve.registration(crnEntry.get(), usernameEntry.get()))
registerMe.grid(row=5, column=5)

if crnInfo['text'] == "Your desired CRN is: " and userInfo['text'] == "Your Villanova email is: ":
    registerMe.config(state="disabled")


def check():
    if crnInfo['text'] == "Your desired CRN is: " or userInfo['text'] == "Your Villanova email is: ":
        registerMe.config(state="disabled")
    else:
        registerMe.config(state="active")
        registerMe["command"] = lambda: retrieve.registration(crnEntry.get(), usernameEntry.get())


e = ttk.Progressbar(bottomFrame, orient=HORIZONTAL, length=200)
e.grid(row=5, column=1)

master.mainloop()

