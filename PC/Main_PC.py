#Import librairie
import time 
from ctypes import *
import ctypes
from pynput.keyboard import Key, Controller
import os
import serial

#Import other function
from Macro import *

def Add_Line(file,text):
    with open(file, 'a') as file :
            file.write(text + "\n")
    file.close()
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def Pointer_Pos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return([pt.x,pt.y])

def Write_click(Maccro_Data_File,data):
    Position = Pointer_Pos()
    Add_Line(Maccro_Data_File,data + "_" + str(Position[0]) + "_" + str(Position[1]) )

def Detect_click(event):
    Left = 0x01
    Right = 0x02
    if ctypes.windll.user32.GetKeyState(Left) > 200 and not event[0][1] :
        event[0] = [True,True]
    if ctypes.windll.user32.GetKeyState(Left) < 200 and event[0][1] :
        event[0] = [True,False]
    if ctypes.windll.user32.GetKeyState(Right) > 200 and not event[1][1] :
        event[1] = [True,True]
    if ctypes.windll.user32.GetKeyState(Right) < 200 and event[1][1] :
        event[1] = [True,False]
    return event

#Execute une macro
def Execute_Macros(ser,Button,file):
    print("Execution maccro " + str(Button) )
    Maccro_Data_File = file + str(Button) +".txt"
    with open(Maccro_Data_File, 'r') as Maccro :
            line = Maccro.readlines()
            for Actions in line :
                time.sleep(1)
                Data_Action = Actions.split("_")
                x = int(Data_Action[2])
                y = int(Data_Action[3])
                ctypes.windll.user32.SetCursorPos(x, y)
                if Data_Action[0] == "L" :
                    if Data_Action[1] == "1" :
                        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)
                    elif Data_Action[1] == "0" :
                        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)

            #Maccro.close()
            print("Finished" + str(Button))
            data = str(Button)
            WriteSerial(ser,data)

#Enregistrement de maccro
def Record_Macros(ser,Button,Maccro_Data_File):
    print("Reccording " + str(Button))
    #On creer le fichier de sauvegarde
    Maccro_Data_File = Maccro_Data_File + str(Button) +".txt"
    Command_to_pc = " "
    Data = "e"
    Maccro = open(Maccro_Data_File ,'w')
    Maccro.close()
    Last_Event = time.time()  
    #         change state change state
    Event = [[False,False],[False,False]]
    while  Command_to_pc[0] != "S" :

        if( (time.time()   - Last_Event) > 3): #On ne check le port usb que si on a rien fait depuis un moment
            Data = ReadSerial(ser) #LENT

        if(len(Data) >= 1 and Command_to_pc != Data):
            Command_to_pc = Data

        Event = Detect_click(Event)
        if Event[1][0] :
            Last_Event = time.time()  
            if Event[1][1] :
                Click = "R_1"
            else :
                Click = "R_0"
            Event[1][0] = False
            Write_click(Maccro_Data_File,Click)

        if Event[0][0] :
            Last_Event = time.time()  
            if Event[0][1] :
                Click = "L_1"
            else :
                Click = "L_0"
            Event[0][0] = False
            Write_click(Maccro_Data_File,Click)

    print("Stop Record maccro " + str(Button) )

def ReadSerial(ser):
    Command_to_pc = str(ser.readline())
    Data = ""
    for n in range(2,len(Command_to_pc)-1):
        Data = Data + Command_to_pc[n]
    #print("Received : " + Data , "    Len : " + str(len(Data)))
    return Data

def WriteSerial(ser,data):
    ser.write(data.encode('utf-8'))
    print("Sent : " + data)

def Link():
    Maccro_Data_File = "Macros_Data/Maccro_"

    print("Checking USB...")
    ser = serial.Serial("COM5",timeout=1)       #Demare liaison USB
    print (ser)
    
    Running = True
    while Running :             
        time.sleep(0.5)
        Command_to_pc = ReadSerial(ser)         #Lis le port serie

        if len(Command_to_pc) >= 1 :       #Si on a pas recu un message
            if Command_to_pc[0] == "P" :        #Si on dois executer une fonction 
                Execute_Macros(ser,Command_to_pc[1],Maccro_Data_File)       #On l'execute
                
            elif Command_to_pc[0] == "R" :      #Si on doit register
                Record_Macros(ser,Command_to_pc[1],Maccro_Data_File)    #On register

Link()
        