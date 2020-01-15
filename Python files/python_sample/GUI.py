# import tkinter module
from tkinter import *
from tkinter.ttk import *
from Driving import *
import Locations

# Tetris = compo("Tetris",0,23,[""])
# lijst = compList(Tetris)
# print(compList[0])
class App:
    def getValue(self, *args):
        print(locvar.get())


    def __init__(self, master):
        global testText
        testText = StringVar()
        frame = Frame(master)
        frame.l1 = Label(master, text="Variables")
        frame.l2 = Label(master, text="Target X:")
        frame.l3 = Label(master, text="Target Y:")
        frame.l4 = Label(master, text="Group size:")
        frame.l5 = Label(master, text="Robot:")
        frame.l6 = Label(master, text="Command:")
        frame.l7 = Label(master, text="Target city:")
        frame.l8 = Label(master, text="Manual command:")

        var1 = False
        Checkbutton(master, text="Use coords", variable=var1).grid(row=1, column=3, padx=2, pady=2)

        frame.l1.grid(row=0, column=1, pady=2)
        frame.l2.grid(row=1, column=0, pady=2)
        frame.l3.grid(row=2, column=0, pady=2)
        frame.l4.grid(row=3, column=0, pady=2)
        frame.l5.grid(row=4, column=0, pady=2)
        frame.l6.grid(row=5, column=0, pady=2)
        frame.l7.grid(row=6, column=0, pady=2)
        frame.l8.grid(row=7, column=0, pady=2)

        # data_string = StringVar()
        # data_string.set("Test")
        # frame.lala = Entry(master)
        # frame.lala.insert(END,"Test")
        # frame.lala.grid(row=2,column=5,columnspan=3,padx=2)
        # frame.lala.configure(state="disabled")

        frame.e1 = Entry(master)
        frame.e2 = Entry(master)
        frame.e3 = Entry(master)
        frame.e4 = Entry(master, textvariable=testText)

        frame.e1.grid(row=1, column=1, pady=2)
        frame.e2.grid(row=2, column=1, pady=2)
        frame.e3.grid(row=3, column=1, pady=2)
        frame.e4.grid(row=7, column=1, pady=2)

        frame.b1 = Button(master, text="Send command", command=self.submit)
        frame.b2 = Button(master, text="Update money", command=self.add_conflict)
        frame.b3 = Button(master, text="Quit", command=frame.quit)
        frame.b4 = Button(master, text="Manual command", command=self.exec_command)
        frame.b1.grid(row=4, column=3, pady=2)
        frame.b2.grid(row=5, column=3, pady=2)
        frame.b3.grid(row=7, column=3, pady=2)
        frame.b4.grid(row=6, column=3, pady=2)

        #      frame.b4.grid(row = 3,column = 3, pady = 2)
        #       frame.b5.grid(row = 4,column = 2, pady = 2)
        #       frame.b6.grid(row = 4,column = 4, pady = 2)
        #       frame.b7.grid(row = 4,column = 3, pady = 2)
        tkvar = StringVar(root)
        compos = [1, 2]
        frame.Robot = OptionMenu(master, tkvar, compos[1], *compos)
        frame.Robot.grid(row=4, column=1, pady=2)
        tkvar.set(compos[0])

        testvar = StringVar(root)
        commands = ["Test", "Test2"]
        frame.commandChoice = OptionMenu(master, testvar, commands[1], *commands)
        frame.commandChoice.grid(row=5, column=1, pady=2)
        testvar.set(commands[0])

        global locvar
        locvar = StringVar(root)
        locations = ["Lab8", "FunnelLabEuropa1", "FunnelLabEuropa2", "FunnelEuropaAfrica1", "FunnelEuropaAfrica2", "FunnelAfricaAmerica1", "FunnelAfricaAmerica2", "FunnelAmericaLab1", "FunnelAmericaLab2", "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "MiddleLabland", "MiddleEurope", "MiddleAfrica", "MiddleAmerica"]
        frame.locChoice = OptionMenu(master, locvar, locations[0], *locations)
        frame.locChoice.grid(row=6, column=1, pady=2)
        locvar.set(locations[0])
        global test
        test = locvar.trace('w', self.getValue)

    def submit(self):
        print(f"Coordinates")

    def add_conflict(self):
        print("Conflict added")

    def exec_command(self):
        testcmd = testText.get()
        exec(testcmd)




root = Tk()
app = App(root)
root.mainloop()