import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import xbox
import time as time
import os
import gpiozero as gp
from AcousticHandler import AcousticHandler

#os.system("sudo pigpiod")
#os.system("sudo systemctl enable pigpiod")


AcousticModule = AcousticHandler()
ACOUSTIC_PARAMS = {"acoustic_freq": 10000}
#acoustic_slider = None

scalex= 1
scaley= .75
scalez= .5 #how much to scale the 0-1 duty cycles by, ensure we dont draw too
#current since PS has peak draw of 3 A
'''
To Do:
optional: continues rolling xbox
'''


'''
Funtionality:
1) Quick Field Direction Control in +- X and Y directions
2) Xbox Controller Compatibility with Left Joystick controlling 360 deg XY DOF and Left
    and right triggers controlling -+ Z direction strength respectivly
3) Vibration Button for vibration frequnecies up to to but not limited to 50 Hz
4) Visual Display of Direction and Strength at all times using circular gauge
5) Ability to toggle between shared coil status(Non_Tweezer mode)
    and single coil status (Tweezer ON mode) for quick field direction control and
    vibration control. In other words the ability to send opposite signals to 2 opposite
    facing coils to enhance the field, or directly to a single coil.
6) zrolling now has wobble option via the cone angle psi
    
Specs:
- Rasberry Pi needs at least 5.1 V at 2.5 A. 3 A is suggested
- Input to the coils is 12V at 3A
- Maximum center field strength is 6 mT
- Maximum near field srength is 140 mT
- Maximum current input 43 Amps
Coil 1 = Y
Coil 2 = X
Coil 3 = -Y
Coil 4 = -X
Coil 5 = Z
Coil 6 = -Z 
Throttled all strengths by 0.5
'''
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Inititlization GPIO
#Coil duty cycle (-1 to 1)
#Coil frequency (1.14 Hz - 19.2 MHz)

#remote connection to raspi. must be on same wifi
#raspi_addr = '192.168.1.17'
#remote_factory = PiGPIOFactory(host = raspi_addr)



freq = 5000
#COIL 1
P1a = 4 #motor 1 forward pin
P1b = 17 #motor 1 backward pin
E1 = 19 #motor 1 enable pin
Coil1 = gp.Motor(forward = P1a, backward = P1b, enable = E1, pwm = True, pin_factory = None)
Coil1.forward_device.frequency = freq #Hz
Coil1.backward_device.frequency = freq

#COIL 2
P2a = 27 #motor 1 forward pin
P2b = 22 #motor 1 backward pin
E2 = 16 #motor 1 enable pin
Coil2 = gp.Motor(forward = P2a, backward = P2b, enable = E2, pwm = True, pin_factory = None)
Coil2.forward_device.frequency = freq #Hz
Coil2.backward_device.frequency = freq 

#COIL 3
P3a = 5 #motor 1 forward pin
P3b = 6 #motor 1 backward pin
E3 = 12 #motor 1 enable pin
Coil3 = gp.Motor(forward = P3a, backward = P3b, enable = E3, pwm = True, pin_factory = None)
Coil3.forward_device.frequency = freq #Hz
Coil3.backward_device.frequency = freq 

#COIL 4
P4a = 13 #motor 1 forward pin
P4b = 26 #motor 1 backward pin
E4 = 20 #motor 1 enable pin
Coil4 = gp.Motor(forward = P4a, backward = P4b, enable = E4, pwm = True, pin_factory = None)
Coil4.forward_device.frequency = freq #Hz
Coil4.backward_device.frequency = freq 

#COIL 5
P5a = 18 #motor 1 forward pin
P5b = 23 #motor 1 backward pin
E5 = 7 #motor 1 enable pin
Coil5 = gp.Motor(forward = P5a, backward = P5b, enable = E5, pwm = True, pin_factory = None)
Coil5.forward_device.frequency = freq #Hz
Coil5.backward_device.frequency = freq 

#COIL 6
P6a = 24 #motor 1 forward pin
P6b = 25 #motor 1 backward pin
E6 = 21 #motor 1 enable pin
Coil6 = gp.Motor(forward = P6a, backward = P6b, enable = E6, pwm = True, pin_factory = None)
Coil6.forward_device.frequency = freq #Hz
Coil6.backward_device.frequency = freq 





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Inititlization GUI
'''
Create GUI window and geometry 
Create textbox to record/log outputs from program
'''



window = tk.Tk() #initilize a window window.title("MagneticFieldGui2")
#icon = tk.PhotoImage(file = "/home/bizzaro/Desktop/MagneticApp/GUI/MMM.png")
#window.iconphoto(True, icon)

# get the screen dimension

window.geometry("1024x768")
window.attributes('-fullscreen', True)

rows = [0,1,2,3,4,5,6,7]
columns = [0,1,2,3,4,5,6,7]
window.columnconfigure(rows, minsize=128)
window.rowconfigure(columns, minsize = 96)

'''
for i in range(len(rows)):
    for j in range(len(columns)):
        frame = tk.Frame(master = window,
                          width = 128,
                          height = 96,
                          relief = tk.RAISED,
                          borderwidth = 5)
        frame.grid(row = rows[i], column = columns[j])
'''

#Initilize textbox to update with tousputs from each button
Text_Box = tk.Text(master = window, width = 22, height = 5)
Scroll_Bar = tk.Scrollbar(master= window, command = Text_Box.yview, orient = 'vertical')
Text_Box.configure(yscrollcommand = Scroll_Bar.set)
Text_Box.grid(row = 7, column=5, rowspan = 1, columnspan = 2, sticky = "nwse")

Text_Box.insert(tk.END,str(os.popen("ip -4 addr | grep 'inet'").read()))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Create Tweezer Toggle
'''
Buttons to toggle the state of the tweezer and global assigns the status
'''
Tweezer_Status = False
def TweezerOn():
    global Tweezer_Status
    Tweezer_Status = True
    Text_Box.insert(tk.END, "Tweezer Status = " + str(Tweezer_Status)+"\n")
    Text_Box.see("end")
def TweezerOff():
    global Tweezer_Status
    Tweezer_Status = False
    Text_Box.insert(tk.END, "Tweezer Status = " + str(Tweezer_Status)+"\n")
    Text_Box.see("end")
    
TweezerON_Button = tk.Button(master = window, text = "Tweezer ON", width = 5, height = 1,
                             fg = "black",bg = "orange", command = TweezerOn)
    
TweezerOFF_Button = tk.Button(master = window, text = "Tweezer OFF", width = 5, height = 1,
                             fg = "black",bg = "gray", command = TweezerOff)

TweezerON_Button.grid(row=5, column=0,sticky = "nswe")
TweezerOFF_Button.grid(row=5, column=1,sticky = "nswe")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Create 3D Projection

#Create Gauge and initlize Pointer
aspect = 4/3
Diameter = 360
Gauge = tk.Canvas(master = window)
Circle_Coords = 0,0,Diameter,Diameter*aspect  # 96 pixels x 6 rows
Circ = Gauge.create_oval(Circle_Coords,fill = 'white' ,width = 1)
YAxis = Gauge.create_line(Diameter/2, 0,Diameter/2,Diameter*aspect, width = 1, fill = "black")
Xaxis = Gauge.create_line(0,(Diameter/2)*aspect,Diameter,(Diameter/2)*aspect, width = 1, fill = "black")
Pointer = Gauge.create_line(0,0,0,0)
Gauge.grid(row = 2, column = 2, columnspan = 3, rowspan = 5,sticky = "wnse")

#Update Arrow Function
def Move_Arrow(Direction):
    global Pointer
    Rx = (Diameter/2) #Radius of cicle
    Ry = (Diameter/2)*(4/3)
    X_Comp = Rx+Rx*np.cos(Direction * np.pi/180)
    Y_Comp = Ry-Ry*np.sin(Direction * np.pi/180) 
    Start_Point = Rx, Ry 
    End_Point = X_Comp, Y_Comp
    
    Gauge.delete(Pointer)
    Pointer = Gauge.create_line(Start_Point, End_Point, arrow = tk.LAST, width = 4, fill = "black", arrowshape = (15,20,8))
    Gauge.grid(row = 2, column = 2, columnspan = 3, rowspan = 5, sticky = "nswe")


    
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Create Adjustment Sliders
'''
Create Sliders for adjusting Field Strength, Field Direction and Vibration Frequency
Also create Arrow function to update the direction of the visual area when slider is changed
'''
Duty_Cycle = 0 
# Create Slider to Vary the Strength
def Set_Strength(Scale_Value1):
    global Duty_Cycle
    Duty_Cycle = Scale_Value1
    Field_Strength_Entry.delete(0, tk.END)
    Field_Strength_Entry.insert(0, str(Duty_Cycle))
   
  
    
Scale_Value1 = tk.DoubleVar()
Strength_Slider = tk.Scale(master = window, from_ = 0, to=1, variable = Scale_Value1,
                             orient = tk.HORIZONTAL, resolution = 0.01, command = Set_Strength, 
                             width = 70, length = 384, showvalue = 0)
Strength_Slider.grid(row = 0, column = 2, columnspan =3, rowspan = 1)


# Create Slider to Vary the Direction
def Set_Direction(Scale_Value2):
    global Direction_Val
    Direction_Val = Scale_Value2
    Field_Direction_Entry.delete(0, tk.END)
    Field_Direction_Entry.insert(0, str(Direction_Val))
    Move_Arrow(int(Field_Direction_Entry.get()))

    
    
Scale_Value2 = tk.DoubleVar()
Direction_Slider = tk.Scale(master = window, from_ = 0, to=360, variable = Scale_Value2,
                             orient = tk.HORIZONTAL, resolution = 5, command = Set_Direction, 
                             width = 70, length = 384, showvalue = 0)
Direction_Slider.grid(row = 1, column = 2, columnspan =3, rowspan = 1) 

start_time_list = []
end_time_list = []
Data_Vector_List = []  #Strores the field angle, magnitude, and elpased time from when the apply button is pressed to when the zero button is pressed
#Field Strength and Direction
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Create Apply and Zero handling Functions
'''
Apply and Zero functions
Handle_Apply to  be called when either the field direction slider is moved or Apply button is pressed
Handle_Zero to be called when Zero button is pressed. It will disrupt any current to coils and zero
all inputs
'''
def Handle_Apply():   
    '''
    need to add the code that will turn on each coil that represents the proper duty cycle.
    '''
    global Field_Angle 
    global Field_Mag

    Field_Angle = float(Field_Direction_Entry.get())
    Field_Mag = float(Field_Strength_Entry.get())
    zfield = float(Z_Strength_Entry.get())
    #Field_Strength_Entry.insert(0, Field_Mag)
    
    X_Duty_Cycle = Field_Mag * np.cos(Field_Angle * np.pi/180)
    Y_Duty_Cycle = Field_Mag * np.sin(Field_Angle * np.pi/180)
    
    Text_Box.insert(tk.END, str([X_Duty_Cycle, Y_Duty_Cycle])+"\n")
    Text_Box.see("end")
    
    Coil1.value = round(Y_Duty_Cycle*scaley,4) #converging
    Coil2.value = round(X_Duty_Cycle*scalex,4)  #converging
    Coil3.value = round(-Y_Duty_Cycle*scaley,4) #diverging
    Coil4.value = round(-X_Duty_Cycle*scalex,4) #diverging
    Coil5.value = round(zfield*scalez,4) #
    Coil6.value = round(-zfield*scalez,4) #
    
    '''
    #Begin Data Capture
    start = time.time()
    start_time_list.append(start)
    Text_Box.insert(tk.END, str([X_Duty_Cycle, Y_Duty_Cycle])+"\n")
    Text_Box.see("end")
    window.update()
    '''
   
    
    
    
    
def Handle_Zero():
    '''
    need to add the code that will turn off all signals to ALL electromagnetic coils
    '''
    global Vibration_Status
    Vibration_Status = False
    
    global Rotation_Status
    Rotation_Status = False
    

    
    #turn off vibration when the zero button is pressed
    Text_Box.delete(1.0, tk.END)
    
  
    #Zero Field Direction Entry
    Field_Direction_Entry.delete(0, tk.END)
    Field_Direction_Entry.insert(0, str(0))
    Direction_Slider.set(0)
    #Zero Vibration Entry
    Vibration_Entry.delete(0, tk.END)
    Vibration_Entry.insert(0, str(0))
    Vibration_Slider.set(0)
    '''
    #Zero Rotation Entry
    Rotation_Entry.delete(0, tk.END)
    Rotation_Entry.insert(0, str(0))
    Rotate_Slider.set(0)
    '''
    Coil1.value = 0
    Coil2.value = 0
    Coil3.value = 0
    Coil4.value = 0
    Coil5.value = 0
    Coil6.value = 0
    

    Text_Box.insert(tk.END, "Zeroed"+"\n")
    Text_Box.see("end")
   

#Field Strength Input Fields
Field_Strength_Label = tk.Label(text = "Field Strength\n(mT)", borderwidth = 5)
Field_Strength_Label.grid(row = 0, column = 0)
Field_Strength_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Field_Strength_Entry.grid(row = 0, column = 1,sticky = "nswe")

#Field Angle Input Fields
Field_Direction_Label = tk.Label(text = "Field Direction\n(deg)")
Field_Direction_Label.grid(row = 1, column = 0)
Field_Direction_Entry = tk.Entry(master = window, borderwidth = 5, width = 5, font = "24")
Field_Direction_Entry.grid(row = 1, column = 1,sticky = "nswe")

#Zero everything iniitially
Field_Strength_Entry.insert(0,0)
Field_Direction_Entry.insert(0,0)


#Create Apply and Zero Buttons
Apply_Button = tk.Button(master = window,text = "Apply",width = 5,height = 1,
                  fg = "black",bg = "blue", command = Handle_Apply)
Zero_Button = tk.Button(master = window,text = "Zero",width = 5,height = 1,
                  fg = "black",bg = "gray", command = Handle_Zero)

Apply_Button.grid(row=2,column=0,sticky = "nswe")
Zero_Button.grid(row=2,column=1,sticky = "nswe")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Add Vibration Functionality
'''
Oscilate polaity of field in X direction when Tweezer Off
Oscilate current from negative X direction to positive X direction when Tweezer On 
'''
def Vibrate():
    global Vibration_Status
    Vibration_Status = True
    frequency = int(Vibration_Entry.get())
    Text_Box.insert(tk.END, str(Duty_Cycle) +"\n")
    period = 1/frequency
    start = time.time()
    
        #1/2 cycle
    while Vibration_Status == True:
        if Tweezer_Status == False:
            Text_Box.insert(tk.END, "On "+ str(time.time()-start) +"\n")
            Coil1.value = 0
            Coil2.value = float(Duty_Cycle)*scalex
            Coil3.value = 0
            Coil4.value = -float(Duty_Cycle)*scalex
            time.sleep(period)
            window.update()
            Text_Box.see("end")
            
            
            #1 cycle
            Text_Box.insert(tk.END, "Off "+str(time.time()-start) +"\n")
            Coil1.value = 0
            Coil2.value = -float(Duty_Cycle)*scalex
            Coil3.value = 0
            Coil4.value = float(Duty_Cycle)*scalex
            time.sleep(period)
            window.update()
            Text_Box.see("end")
        if Tweezer_Status == True:
            Text_Box.insert(tk.END, "On "+ str(time.time()-start) +"\n")
            Coil1.value = 0
            Coil2.value = float(Duty_Cycle)*scalex
            Coil3.value = 0
            Coil4.value = 0
            time.sleep(period)
            window.update()
            Text_Box.see("end")
            
            
            #1 cycle
            Text_Box.insert(tk.END, "Off "+str(time.time()-start) +"\n")
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = float(Duty_Cycle)*scalex
            time.sleep(period)
            window.update()
            Text_Box.see("end")
        
            
        
    window.update() 
    #Text_Box.insert(tk.END, "END VIBRATION " +"\n")
    Text_Box.see("end")
     

def Set_Frequency(Scale_Value3):
    #trouble with slider not updating fast enough during small frequencies.

    Vibration_Entry.delete(0, tk.END)
    Vibration_Entry.insert(0, str(Scale_Value3))
    #Vibrate()
    window.update()
    
    
#Vibration Scale Bar   
Scale_Value3 = tk.DoubleVar()
Vibration_Slider = tk.Scale(master = window, from_ = 0, to=50, variable = Scale_Value3,
                             orient = tk.HORIZONTAL, resolution = 1, command = Set_Frequency, 
                             width = 70, length = 384, showvalue = 0)
Vibration_Slider.grid(row = 7, column = 2, columnspan =3, rowspan = 1)

#Vibration Input Fields
Vibration_Label = tk.Label(text = "Vibration \nFrequency")
Vibration_Label.grid(row = 7, column = 0)
Vibration_Entry = tk.Entry(master = window, borderwidth = 5, width = 5, font = "24")
Vibration_Entry.grid(row = 7, column = 1,sticky = "nswe")
#Zero everything iniitially
Vibration_Entry.insert(0,0)


#Add Vibrater Button
Vibrate_Button = tk.Button(master = window,text = "Vibrate",width = 5,height = 1,
                  fg = "black",bg = "green", command = Vibrate)
Vibrate_Button.grid(row=6,column=0,sticky = "nswe")


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Quick Field Directions
'''
Both Tweezer and Non-Tweezer Functionality  depending on  Tweezer_Status boolean
Tweezer On = current sent to single coil
Tweezer Off = Curret sent to both opposite facing coils in opposite polarity to enhance field uniformity
'''
def Handle_Y():
    '''
    MOTOR 1
    need to add the code that will turn the magnetic field on in the Y direction
    '''
    if Tweezer_Status == False:
        Coil1.value = float(Duty_Cycle)*scaley
        Coil2.value = 0
        Coil3.value = -float(Duty_Cycle)*scaley
        Coil4.value = 0
    if Tweezer_Status == True:
        Coil1.value = float(Duty_Cycle)*scaley
        Coil2.value = 0
        Coil3.value = 0
        Coil4.value = 0
    
    Move_Arrow(90)
    
    
def Handle_negX():
    '''
    MOTOR 4
    need to add the code that will turn the magnetic field on in the -X direction
    '''
    if Tweezer_Status == False:
        Coil1.value = 0
        Coil2.value = float(Duty_Cycle)*scalex
        Coil3.value = 0
        Coil4.value = -float(Duty_Cycle)*scalex
    if Tweezer_Status == True:
        Coil1.value = 0
        Coil2.value = 0
        Coil3.value = 0
        Coil4.value = float(Duty_Cycle)*scalex
    
    Move_Arrow(180)
    
def Handle_X():
    '''
    MOTOR 2
    need to add the code that will turn the magnetic field on in the X direction
    '''
    if Tweezer_Status == False:
        Coil1.value = 0
        Coil2.value = -float(Duty_Cycle)*scalex
        Coil3.value = 0
        Coil4.value = float(Duty_Cycle)*scalex
    if Tweezer_Status == True:
        Coil1.value = 0
        Coil2.value = float(Duty_Cycle)*scalex
        Coil3.value = 0
        Coil4.value = 0
    Move_Arrow(0)
    
def Handle_negY():
    print("-Y")
    '''
    MOTOR 3
    need to add the code that will turn the magnetic field on in the -Y direction
    '''
    if Tweezer_Status == False:
        Coil1.value = -float(Duty_Cycle)*scaley
        Coil2.value = 0
        Coil3.value = float(Duty_Cycle)*scaley
        Coil4.value = 0
    if Tweezer_Status == True:
        Coil1.value = 0
        Coil2.value = 0
        Coil3.value = float(Duty_Cycle)*scaley
        Coil4.value = 0
    Move_Arrow(270)
    
    
    
Y_Button = tk.Button(master = window,text = "\u25b2",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black", command = Handle_Y)
negX_Button = tk.Button(master = window,text = "\u25c0",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negX)
X_Button = tk.Button(master = window,text = "\u25b6",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_X)
negY_Button = tk.Button(master = window,text = "\u25bc",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negY)
Y_Button.grid(row=0,column=6,sticky = "nswe")
negX_Button.grid(row=1,column=5,sticky = "nswe")
X_Button.grid(row=1,column=7,sticky = "nswe")
negY_Button.grid(row=2,column=6,sticky = "nswe")



#Z AXSIS Strength Input Fields
Z_Strength_Label = tk.Label(text = "Z Strength\n(mT)", borderwidth = 5)
Z_Strength_Label.grid(row = 3, column = 0)
Z_Strength_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Z_Strength_Entry.grid(row = 3, column = 1,sticky = "nswe")
Z_Strength_Entry.insert(0,0)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#create function for adjusting gamma value. I believe its 0-180
def Set_Gamma(Gamma_Value):
    Rotation_Gamma = Gamma_Value
    Gamma_Entry.delete(0, tk.END)
    Gamma_Entry.insert(0, str(Rotation_Gamma))
    

Gamma_Value = tk.DoubleVar()
Gamma_Slider = tk.Scale(master = window, from_ = 0, to=180, variable = Gamma_Value,
                             orient = tk.VERTICAL, resolution = 5, command = Set_Gamma, 
                             width = 70, length = 190, showvalue = 0)
Gamma_Slider.grid(row = 5, column = 6, columnspan =1, rowspan = 2)
Gamma_Label = tk.Label(text = "Gamma/Pitch\n(deg)", borderwidth = 5)
Gamma_Label.grid(row = 3, column = 6)
Gamma_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Gamma_Entry.grid(row = 4, column = 6,sticky = "nswe")
Gamma_Entry.insert(0,90)
Gamma_Slider.set(90)

#create function for adjusting psi value, 90-0
def Set_Psi(Psi_Value):
    Rotation_Psi = Psi_Value
    Psi_Entry.delete(0, tk.END)
    Psi_Entry.insert(0, str(Rotation_Psi))
    

Psi_Value = tk.DoubleVar()
Psi_Slider = tk.Scale(master = window, from_ = 10, to=90, variable = Psi_Value,
                             orient = tk.VERTICAL, resolution = 10, command = Set_Psi, 
                             width = 70, length = 190, showvalue = 0)
Psi_Slider.grid(row = 5, column = 5, columnspan =1, rowspan = 2)
Psi_Label = tk.Label(text = "Psi/Wobble\n(deg)", borderwidth = 5)
Psi_Label.grid(row = 3, column = 5)
Psi_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Psi_Entry.grid(row = 4, column = 5,sticky = "nswe")
Psi_Entry.insert(10,90)
Psi_Slider.set(90)

#create function for adjusting gamma value
def Set_Rotation_Frequency(Rot_Freq_Value):
    Rotation_Frequency = Rot_Freq_Value
    Rot_Freq_Entry.delete(0, tk.END)
    Rot_Freq_Entry.insert(0, str(Rotation_Frequency))

Rot_Freq_Value = tk.DoubleVar()
Rot_Freq_Slider = tk.Scale(master = window, from_ = 0, to=40, variable = Rot_Freq_Value,
                             orient = tk.VERTICAL, resolution = 1, command = Set_Rotation_Frequency, 
                             width = 70, length = 190, showvalue = 0)
Rot_Freq_Slider.grid(row = 5, column = 7, columnspan =1, rowspan = 2)
Rot_Freq_Label = tk.Label(text = "Rotation \n Frequency (Hz)", borderwidth = 5)
Rot_Freq_Label.grid(row = 3, column = 7)
Rot_Freq_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Rot_Freq_Entry.grid(row = 4, column = 7,sticky = "nswe")
Rot_Freq_Entry.insert(0,1)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Rotating Magnetic Functionality
'''
add buttons and functionaity for XZ YZ and XY rotation via a rotating magnetic field 
'''
def Rotate():
    global Rotation_Status
    Rotation_Status = True
    Text_Box.insert(tk.END, "Rotate"+"\n")
    Text_Box.see("end")
    
    
    A = float(Duty_Cycle) #amplitude of rotating magetnic field
    psi = float(Psi_Entry.get()) * (np.pi/180)
    alpha = (float(Field_Direction_Entry.get())-90) * (np.pi/180)  # yaw angle converted to radians
    gamma = float(Gamma_Entry.get()) * (np.pi/180)  # pitch angle converted to radians
    omega = 2*np.pi* float(Rot_Freq_Entry.get())  #angular velocity of rotating field defined from input from Rotating Frequency Entry

   
    start = time.time()
    while Rotation_Status == True:
        tp = time.time() - start
        #new eqs7/3/23:
        Bx = A * ((-np.sin(self.alpha) * np.sin(self.omega*tp)) + (-np.cos(self.alpha) * np.cos(self.gamma)  * np.cos(self.omega*tp))) 
        By = A * ((np.cos(self.alpha) * np.sin(self.omega*tp)) + (-np.sin(self.alpha) * np.cos(self.gamma) *  np.cos(self.omega*tp))) 
        Bz = A * np.sin(self.gamma) * np.cos(self.omega*tp)
        print('Bx:'+str(Bx)+' By: '+str(By)+' Bz: '+str(Bz)+' gamma: '+str(gamma)+' alpha: '+str(alpha))
        
        
        if psi < np.pi/2:
            if alpha % (np.pi/2) == 0:
                alpha = alpha + 0.00001#for some strange reason the eqns give wrong answers when alpha is pi/2
            if gamma == 0 or gamma % (np.pi/2) == 0:
                gamma = gamma + 0.00001
            c = A/np.tan(psi)
            BxPer = c*np.cos(alpha)*np.sin(gamma)
            ByPer = np.tan(alpha)*BxPer
            BzPer = BxPer*np.cos(alpha)**(-1)*np.tan(gamma)**(-1)
            print('Bxper:'+str(BxPer)+' Byper: '+str(ByPer)+' Bzper: '+str(BzPer)+' gamma: '+str(gamma))
            
        else:
            BxPer = 0
            ByPer = 0
            BzPer = 0
            c = 0
        
        Coil1.value =   round((By+ByPer)*scaley/(1+c/A),4) # +Y
        Coil2.value =   round((Bx+BxPer)*scalex/(1+c/A),4) # +X
        Coil3.value =  -round((By+ByPer)*scaley/(1+c/A),4)  # -Y
        Coil4.value =  -round((Bx+BxPer)*scalex/(1+c/A),4) # -X
        Coil5.value =   round((Bz+BzPer)*scalez/(1+c/A),4)  # +Z
        Coil6.value =  -round((Bz+BzPer)*scalez/(1+c/A),4)  # -Z
    
        
        
        
        Text_Box.insert(tk.END, str(round(tp,2))+"\n")
        Text_Box.see("end")
        window.update()
       
    
    Coil1.value = 0
    Coil2.value = 0
    Coil3.value = 0
    Coil4.value = 0
    Coil5.value = 0
    Coil6.value = 0
    
    
    
Rotate_Button = tk.Button(master = window, text = "Rotate", width = 5, height = 1,
                             fg = "black",bg = "yellow", command = Rotate)
Rotate_Button.grid(row=2, column=5,sticky = "nswe")




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Xbox Controller Functions


def Handle_Xbox():
    
    Text_Box.insert(tk.END, "XBOX Connected\n")
    Text_Box.see("end")
    joy = xbox.Joystick() # Instantiate the controller
    start = time.time()  #begin timer for rotating field
    '''
    functions assigned to each button of the controller
    '''
    #Spin --> Hold Y to Spin MR

    
    #Triggers --> Variable +- Z Field
    def Triggers():
        if joy.rightTrigger() > 0:
            #Output positive Z Field
            Coil5.value = round(joy.rightTrigger(),2)*scalez
            Coil6.value = -round(joy.rightTrigger(),2)*scalez
            #Display joystick readings in entry box
            Z_Strength_Entry.delete(0, tk.END)
            Z_Strength_Entry.insert(0, str(round(joy.rightTrigger(),2))) #print 0 -> +1 as positive 
            Text_Box.insert(tk.END, 'right trigger activated\n')
            Text_Box.see("end")
                
        #negative Z
        elif joy.leftTrigger() > 0:
            #Output negative Z Field
            Coil5.value = -round(joy.leftTrigger(),2)*scalez
            Coil6.value = round(joy.leftTrigger(),2)*scalez
            #Display joystick readings in entry box
            Z_Strength_Entry.delete(0, tk.END)
            Z_Strength_Entry.insert(0, str(-round(joy.leftTrigger(),2))) #print 0 -> -1 as negatie Z
            Text_Box.insert(tk.END, 'left trigger activated\n')
            Text_Box.see("end")
        



    #D-Pad --> Tweezer Quick Field
    def D_Pad():
        if joy.dpadUp() != 0:
            Coil1.value = float(Duty_Cycle)
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad up activated\n')
            Text_Box.see("end")
      
        elif joy.dpadRight() != 0:
            Coil1.value = 0
            Coil2.value = float(Duty_Cycle)
            Coil3.value = 0
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad right activated\n')
            Text_Box.see("end")
           
        elif joy.dpadDown() != 0:
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = float(Duty_Cycle)
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad down activated\n')
            Text_Box.see("end")
       
        elif joy.dpadLeft() != 0:
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = float(Duty_Cycle)
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad left activated\n')
            Text_Box.see("end")
      
       
    
    #Left Joystick --> Uniform Field
    def Left_Joystick():
        #Output Uniform Signal
        Coil1.value = round(joy.leftY(),2)*scaley  #converging
        Coil2.value = round(joy.leftX(),2)*scalex  #converging
        Coil3.value = -round(joy.leftY(),2)*scaley #diverging
        Coil4.value = -round(joy.leftX(),2)*scalex #diverging
        #Update Display Wheel
        if joy.leftX() == 0 and joy.leftY() >0:
            Move_Arrow(90)
        elif joy.leftX() == 0 and joy.leftY() <0:
            Move_Arrow(270)
        elif joy.leftX() != 0 and joy.leftY() != 0:
            Left_Joy_Direction = (180/np.pi)*np.arctan2(joy.leftY() ,joy.leftX())
            Move_Arrow(round(Left_Joy_Direction,2))
            
    


    def Right_Joystick():#i, t_list, Bx_List, By_List, Bz_List):
        
        #Outputing rotating field
        #Update Display Wheel
        tp = time.time() - start
        A = float(Duty_Cycle) #amplitude of rotating magetnic field
        
        gamma = float(Gamma_Entry.get()) * (np.pi/180)
        psi = float(Psi_Entry.get()) * (np.pi/180)
        
        #taking magntiude of x,y joystick position and multipling it by 20. so rolling speed varys with joystick yaw
        mapped_frequency = np.sqrt(joy.rightX()**2 + joy.rightY()**2) * 20  
        omega =2*np.pi* float(Rot_Freq_Entry.get())# 2*np.pi* float(mapped_frequency) #2*np.pi* float(Rot_Freq_Entry.get())  #angular velocity of rotating field defined from input from Rotating Frequency Entry
        
        if joy.rightX() == 0 and joy.rightY() > 0:
            Right_Joy_Direction = 90
            Move_Arrow(90)
            
            alpha = (90-90) * (np.pi/180)  # yaw angle converted to radians
            #new eqs7/3/23:
            Bx = A * ((-np.sin(self.alpha) * np.sin(self.omega*tp)) + (-np.cos(self.alpha) * np.cos(self.gamma)  * np.cos(self.omega*tp))) 
            By = A * ((np.cos(self.alpha) * np.sin(self.omega*tp)) + (-np.sin(self.alpha) * np.cos(self.gamma) *  np.cos(self.omega*tp))) 
            Bz = A * np.sin(self.gamma) * np.cos(self.omega*tp)
            
            if psi < np.pi/2:
                if alpha % (np.pi/2) == 0:
                    alpha = alpha + 0.00001#for some strange reason the eqns give wrong answers when alpha is pi/2
                if gamma == 0 or gamma % (np.pi/2) == 0:
                    gamma = gamma + 0.00001
                A=1
                c = A/np.tan(psi)
                BxPer = c*np.cos(alpha)*np.sin(gamma)
                ByPer = np.tan(alpha)*BxPer
                BzPer = BxPer*np.cos(alpha)**(-1)*np.tan(gamma)**(-1)
                #print('Bxper:'+str(BxPer)+' Byper: '+str(ByPer)+' Bzper: '+str(BzPer)+' gamma: '+str(gamma))
                
            else:
                A=1
                BxPer = 0
                ByPer = 0
                BzPer = 0
                c = 0
            
            Coil1.value =   round((By+ByPer)*scaley/(1+c/A),4) # +Y
            Coil2.value =   round((Bx+BxPer)*scalex/(1+c/A),4) # +X
            Coil3.value =  -round((By+ByPer)*scaley/(1+c/A),4)  # -Y
            Coil4.value =  -round((Bx+BxPer)*scalex/(1+c/A),4) # -X
            Coil5.value =   round((Bz+BzPer)*scalez/(1+c/A),4)  # +Z
            Coil6.value =  -round((Bz+BzPer)*scalez/(1+c/A),4)  # -Z
            
        elif joy.rightX() == 0 and joy.rightY() <0:
            Right_Joy_Direction = 270
            Move_Arrow(270)
            
            alpha = (270-90) * (np.pi/180)  # yaw angle converted to radians
            #new eqs7/3/23:
            Bx = A * ((-np.sin(self.alpha) * np.sin(self.omega*tp)) + (-np.cos(self.alpha) * np.cos(self.gamma)  * np.cos(self.omega*tp))) 
            By = A * ((np.cos(self.alpha) * np.sin(self.omega*tp)) + (-np.sin(self.alpha) * np.cos(self.gamma) *  np.cos(self.omega*tp))) 
            Bz = A * np.sin(self.gamma) * np.cos(self.omega*tp)
            

            if psi < np.pi/2:
                if alpha % (np.pi/2) == 0:
                    alpha = alpha + 0.00001#for some strange reason the eqns give wrong answers when alpha is pi/2
                if gamma == 0 or gamma % (np.pi/2) == 0:
                    gamma = gamma + 0.00001
                A=1
                c = A/np.tan(psi)
                BxPer = c*np.cos(alpha)*np.sin(gamma)
                ByPer = np.tan(alpha)*BxPer
                BzPer = BxPer*np.cos(alpha)**(-1)*np.tan(gamma)**(-1)
                #print('Bxper:'+str(BxPer)+' Byper: '+str(ByPer)+' Bzper: '+str(BzPer)+' gamma: '+str(gamma))
                
            else:
                A=1
                BxPer = 0
                ByPer = 0
                BzPer = 0
                c = 0
            
            Coil1.value =   round((By+ByPer)*scaley/(1+c/A),4) # +Y
            Coil2.value =   round((Bx+BxPer)*scalex/(1+c/A),4) # +X
            Coil3.value =  -round((By+ByPer)*scaley/(1+c/A),4)  # -Y
            Coil4.value =  -round((Bx+BxPer)*scalex/(1+c/A),4) # -X
            Coil5.value =   round((Bz+BzPer)*scalez/(1+c/A),4)  # +Z
            Coil6.value =  -round((Bz+BzPer)*scalez/(1+c/A),4)  # -Z
        
        else:
            Right_Joy_Direction = (180/np.pi)*np.arctan2(joy.rightY() ,joy.rightX())
            Move_Arrow(round(Right_Joy_Direction,2))
            
            alpha = (Right_Joy_Direction-90) * (np.pi/180)  # yaw angle converted to radians
            #new eqs7/3/23:
            Bx = A * ((-np.sin(self.alpha) * np.sin(self.omega*tp)) + (-np.cos(self.alpha) * np.cos(self.gamma)  * np.cos(self.omega*tp))) 
            By = A * ((np.cos(self.alpha) * np.sin(self.omega*tp)) + (-np.sin(self.alpha) * np.cos(self.gamma) *  np.cos(self.omega*tp))) 
            Bz = A * np.sin(self.gamma) * np.cos(self.omega*tp)

            if psi < np.pi/2:
                if alpha % (np.pi/2) == 0:
                    alpha = alpha + 0.00001#for some strange reason the eqns give wrong answers when alpha is pi/2
                if gamma == 0 or gamma % (np.pi/2) == 0:
                    gamma = gamma + 0.00001
                A=1
                c = A/np.tan(psi)
                BxPer = c*np.cos(alpha)*np.sin(gamma)
                ByPer = np.tan(alpha)*BxPer
                BzPer = BxPer*np.cos(alpha)**(-1)*np.tan(gamma)**(-1)
                #print('Bxper:'+str(BxPer)+' Byper: '+str(ByPer)+' Bzper: '+str(BzPer)+' gamma: '+str(gamma))
                
            else:
                A=1
                BxPer = 0
                ByPer = 0
                BzPer = 0
                c = 0
            
            Coil1.value =   round((By+ByPer)*scaley/(1+c/A),4) # +Y
            Coil2.value =   round((Bx+BxPer)*scalex/(1+c/A),4) # +X
            Coil3.value =  -round((By+ByPer)*scaley/(1+c/A),4)  # -Y
            Coil4.value =  -round((Bx+BxPer)*scalex/(1+c/A),4) # -X
            Coil5.value =   round((Bz+BzPer)*scalez/(1+c/A),4)  # +Z
            Coil6.value =  -round((Bz+BzPer)*scalez/(1+c/A),4)  # -Z
        
  
        window.update() 

    button_state = 0
    last_state = 0
    counter = 0
    switch_state = 0
    while not joy.Back():
        
        #check dpad tweezer inputs
        #D_Pad()

        #check trigger z inputs
        #Triggers()

        #check spin y button input
        

        #A Button Function --> Acoustic Module Toggle
        button_state = joy.A()
        if button_state != last_state:
            if button_state == True:
                counter +=1
        last_state = button_state
        if counter %2 != 0 and switch_state !=0:
            switch_state = 0
            AcousticModule.start(ACOUSTIC_PARAMS["acoustic_freq"])
            Text_Box.insert(tk.END, str(ACOUSTIC_PARAMS["acoustic_freq"]) + '\n')
            Text_Box.see("end")
        elif counter %2 == 0 and switch_state !=1:
            switch_state = 1
            AcousticModule.stop()
            Text_Box.insert(tk.END, '--------OFF--------\n')
            Text_Box.see("end")
        
        
        
        
        elif joy.Y() > 0:
            tp = time.time() - start
            A = 1 #amplitude of rotating magetnic field
            gamma = 0
            #mapped_frequency = np.sqrt(joy.rightX()**2 + joy.rightY()**2) * 20  
            omega = 2*np.pi* float(Rot_Freq_Entry.get()) #2*np.pi* float(Rot_Freq_Entry.get())  #angular velocity of rotating field defined from input from Rotating Frequency Entry
        
            alpha = 1
            #new eqs7/3/23:
            Bx = A * ((-np.sin(self.alpha) * np.sin(self.omega*tp)) + (-np.cos(self.alpha) * np.cos(self.gamma)  * np.cos(self.omega*tp))) 
            By = A * ((np.cos(self.alpha) * np.sin(self.omega*tp)) + (-np.sin(self.alpha) * np.cos(self.gamma) *  np.cos(self.omega*tp))) 
            Bz = A * np.sin(self.gamma) * np.cos(self.omega*tp)
            
            Coil1.value =   round(By*scaley) # +Y
            Coil2.value =   round(Bx*scalex) # +X
            Coil3.value =  -round(By*scaley)  # -Y
            Coil4.value =  -round(Bx*scalex) # -X
            Coil5.value =   round(Bz*scalez)  # +Z
            Coil6.value =  -round(Bz*scalez)  # -Z
            
            Text_Box.insert(tk.END, 'y activated\n')
            Text_Box.see("end")
            
            
        elif joy.rightTrigger() > 0:
            #Output positive Z Field
            Coil5.value = round(joy.rightTrigger(),2)*scalez
            Coil6.value = -round(joy.rightTrigger(),2)*scalez
            #Display joystick readings in entry box
            Z_Strength_Entry.delete(0, tk.END)
            Z_Strength_Entry.insert(0, str(round(joy.rightTrigger(),2))) #print 0 -> +1 as positive 
            Text_Box.insert(tk.END, 'right trigger activated\n')
            Text_Box.see("end")
                
        #negative Z
        elif joy.leftTrigger() > 0:
            #Output negative Z Field
            Coil5.value = -round(joy.leftTrigger(),2)*scalez
            Coil6.value = round(joy.leftTrigger(),2)*scalez
            #Display joystick readings in entry box
            Z_Strength_Entry.delete(0, tk.END)
            Z_Strength_Entry.insert(0, str(-round(joy.leftTrigger(),2))) #print 0 -> -1 as negatie Z
            Text_Box.insert(tk.END, 'left trigger activated\n')
            Text_Box.see("end")
        

        #Dpad
        elif joy.dpadUp() != 0:
            Coil1.value = float(Duty_Cycle)
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad up activated\n')
            Text_Box.see("end")
      
        elif joy.dpadRight() != 0:
            Coil1.value = 0
            Coil2.value = float(Duty_Cycle)
            Coil3.value = 0
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad right activated\n')
            Text_Box.see("end")
           
        elif joy.dpadDown() != 0:
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = float(Duty_Cycle)
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad down activated\n')
            Text_Box.see("end")
       
        elif joy.dpadLeft() != 0:
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = float(Duty_Cycle)
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'dpad left activated\n')
            Text_Box.see("end")
                
        #uniform field
        elif not joy.leftX() == 0 or not joy.leftY() == 0:
            Text_Box.insert(tk.END, 'left joy activated\n')
            Text_Box.see("end")
            Left_Joystick()
        
        #rotating field
        elif not joy.rightX() == 0 or not joy.rightY() == 0:
            Text_Box.insert(tk.END, 'right joy activated\n')
            Text_Box.see("end")
            Right_Joystick()
        
        else:
            Coil1.value = 0
            Coil2.value = 0
            Coil3.value = 0
            Coil4.value = 0
            Coil5.value = 0
            Coil6.value = 0
            Text_Box.insert(tk.END, 'zeroed\n')
            Text_Box.see("end")
            Z_Strength_Entry.delete(0, tk.END)
            Z_Strength_Entry.insert(0, str(0))
        
        
        
        
             
        
        
        window.update()
    Coil1.value = 0
    Coil2.value = 0
    Coil3.value = 0
    Coil4.value = 0
    Coil5.value = 0
    Coil6.value = 0
    joy.close()
    Text_Box.insert(tk.END, "\nXBOX Disconnected")
    Text_Box.see("end")
    
    

    
Xbox_Button = tk.Button(master = window,text = "Xbox Controller. \n Press Back Button to Exit",
                  fg = "white",bg = "red",command = Handle_Xbox)
Xbox_Button.grid(row=4,column=0, sticky = "nswe", columnspan = 2)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



def edit_acoustic_params():
        """
        Creates a new window to control the AD9850 Signal generator module. 
        genereates sinusoidal or square waveforms from 0-40 MHz
        Args:
            None
        Returns:
            None
        """
        acousticwindow = tk.Toplevel(window)
        acousticwindow.title("Acoustic Module")

        
        
        def apply_freq():
            AcousticModule.start(int(acoustic_slider.get()))
            print(" -- waveform ON --")
        
        def test_freq():
            AcousticModule.start(int(10000))
            
        def stop_freq():
            AcousticModule.stop()
            print(" -- waveform OFF --")
        
        def update_loop_slider_values(event):
            """
            Constantly updates acoustic params when the sliders are used.
            Params:
                event
            Returns:
                None
            """
            ACOUSTIC_PARAMS["acoustic_freq"] = int(acoustic_slider.get())
            apply_freq()
            window.update()

        #create apply widget
        apply_button = tk.Button(
            acousticwindow, 
            text="Apply", 
            command=apply_freq, 
            height=5, width=10,
            bg = 'blue',
            fg= 'white'
        )
        apply_button.pack()
        
        #create stop widget
        stop_button = tk.Button(
            acousticwindow, 
            text="Stop", 
            command=stop_freq, 
            height=5, width=10,
            bg = 'red',
            fg= 'white'
        )
        
        stop_button.pack()
        
        #create test widget
        test_button = tk.Button(
            acousticwindow, 
            text="Test 10kHz", 
            command=test_freq, 
            height=5, width=10,
            bg = 'green',
            fg= 'white'
        )
        
        test_button.pack()


        #create freq widget
        acoustic_frequency = tk.DoubleVar()
        acoustic_slider = tk.Scale(
            master=acousticwindow,
            label="Acoustic Frequency",
            from_=1000000,
            to=2000000,
            resolution=1000,
            variable=acoustic_frequency,
            width=50,
            length=1000,
            orient=tk.HORIZONTAL,
            command=update_loop_slider_values,
        )
       
        acoustic_slider.set(10000)        
        acoustic_slider.pack()
        



acoustic_params_button = tk.Button(
            window,
            text="Edit \nAcoustic Params",
            command=edit_acoustic_params,
            width = 5,
            height = 1,
            bg = 'cyan',
            fg= 'black'
        )

acoustic_params_button.grid(row=0, column=5, sticky = "nswe" )



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



#Close Window
def EXIT():
    Coil1.value = 0  #converging
    Coil2.value = 0 #converging
    Coil3.value = 0 #diverging
    Coil4.value = 0 #diverging
    Coil5.value = 0
    Coil6.value = 0
    
    Coil1.close()
    Coil2.close()
    Coil3.close()
    Coil4.close()
    Coil5.close()
    Coil6.close()
    
    window.quit()
    window.destroy()
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl enable GUI.service")
    #os.system("sudo shutdown -h now")
Close_Button = tk.Button(master = window,text = "Close",width = 5,height = 1,
                  fg = "white",bg = "black",command = EXIT)
Close_Button.grid(row=rows[7], column = columns[7], sticky = "nswe")


window.mainloop()






                                                                                                               

