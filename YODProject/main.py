# -*- coding: cp1251 -*-

from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import cv2
import dataReader
from PIL import Image, ImageTk 
import detector
import datetime
import numpy as np
import pandas as pd

root = Tk()
video = cv2.VideoCapture(0)
minPeople = 5
maxPeople = 10

text_box_min_people = None
text_box_max_peple = None
plot1 = None 

lastSaveTime = datetime.datetime.now()
new_window = None
DateTextBox = None

def getInfo():
    global new_window
    fig = Figure(figsize = (5, 5), 
                 dpi = 80) 
    arg = DateTextBox.get(1.0, "end-1c")
    # list of squares 
    dateString = arg
    data =  dataReader.currentDaysLog(dateString)
   
    # определяем столбцы
    columns = ("Time", "Status")
 
    tree = ttk.Treeview(new_window, columns=columns, show="headings")
  
    tree.place(x = 5, y = 40)
    # определяем заголовки
    tree.heading("Time", text="Time")
    tree.heading("Status", text="Status")
    ##tree.heading("email", text="Email")
    # добавляем данные
    for person in data:
        tree.insert("", END, values=person)

    # Plotting the time series of given dataframe
   
    plot2 = fig.add_subplot(111) 
    plot2.set_anchor('SW')
    # plotting the graph 

 
    array = dataReader.currentDaysLogPepleCount(dateString)
    print(dateString)
    print(array)
    if(len(array) != 0):
        dataframe = pd.DataFrame({'time': np.array([array[i][0] for i in range(len(array))]), 'person_count': np.array([array[i][1] for i in range(len(array))])       })
    else:
         dataframe = pd.DataFrame({'time': np.array([0]), 'person_count': np.array([0])       })
    plot2.plot(dataframe.time, dataframe.person_count)
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = new_window)   
    ##canvas.place(x =0, y = 50)

    canvas.draw() 

    # placing the canvas on the Tkinter window 
    #canvas.get_tk_widget().place() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   new_window) 
    toolbar.update() 
    
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().place(x = 7, y = 275) 
    pass

def info_window():
    global DateTextBox
    global new_window
    new_window = Toplevel(root)
    new_window.title("Info")
    new_window.geometry("500x750")
    new_window.resizable(0,0)

    frame = Frame(new_window, bg = '#fafafa', width= 10, height = 10)
    frame.place(relx = 0, rely = 0, relwidth= 1, relheight= 1)
    
    DateTextBox = Text(frame, height=1, width=10)
    DateTextBox.place(x = 0, y = 0)

    btn = ttk.Button(frame, text="Get data", command=getInfo)
    btn.place(x = 100, y = 0, width=100, height=25)



def open_camera(): 
    global lastSaveTime
    # Set the width and height 
    
   # print('Detecting people...')
    
    frame = video.read()
    #img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BayerBG2BGR))
    frame = detector.detect(frame[1])
    label_widget = Label(root) 
    label_widget.place(x = 450, y = 100) 
  

    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
  
    # Capture the latest frame and transform to image 
    captured_image = Image.fromarray(opencv_image) 
  
    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
  
    # Displaying photoimage in the label 
    label_widget.photo_image = photo_image 
  
    
    # Configure image in the label 
    label_widget.configure(image=photo_image) 
    if( (datetime.datetime.now() - lastSaveTime).total_seconds() >= 60 ):
        lastSaveTime = datetime.datetime.now()
        if(detector.personCount < int(text_box_min_people.get(1.0, "end-1c"))):
            saveData(detector.personCount, event = 'There are few people')

        if(detector.personCount > int(text_box_max_people.get(1.0, "end-1c"))):
            saveData(detector.personCount, event = 'There are a lot of people')

        if((detector.personCount <= int(text_box_max_people.get(1.0, "end-1c")) )and (detector.personCount >= int(text_box_min_people.get(1.0, "end-1c")))):
            saveData(detector.personCount, event = 'Normal number of people')

        dateString = str(datetime.datetime.now().day) + '/' +  str(datetime.datetime.now().month) + '/' +  str(datetime.datetime.now().year)
        data =  dataReader.currentDaysLog(dateString)
             
        array = dataReader.currentDaysLogPepleCount(dateString)
        if(len(array) != 0):
            dataframe = pd.DataFrame({'time': np.array([array[i][0] for i in range(len(array))]), 'person_count': np.array([array[i][1] for i in range(len(array))])       })
        else:
             dataframe = pd.DataFrame({'time': np.array([0]), 'person_count': np.array([0])       })
        plot1.plot(dataframe.time, dataframe.person_count)

        tree.delete(*tree.get_children())
        for person in data:
            tree.insert("", END, values=person)
    # Repeat the same process after every 10 seconds 

    label_widget.after(10, open_camera) 


def plot(): 
    global plot1
    fig = Figure(figsize = (5, 5), 
                 dpi = 80) 
  
    # list of squares 


    # Plotting the time series of given dataframe
   
    plot1 = fig.add_subplot(111) 
    plot1.set_anchor('SW')
    # plotting the graph 

    dateString = str(datetime.datetime.now().day) + '/' +  str(datetime.datetime.now().month) + '/' +  str(datetime.datetime.now().year)
    array = dataReader.currentDaysLogPepleCount(dateString)
    if(len(array) != 0):
        dataframe = pd.DataFrame({'time': np.array([array[i][0] for i in range(len(array))]), 'person_count': np.array([array[i][1] for i in range(len(array))])       })
    else:
         dataframe = pd.DataFrame({'time': np.array([0]), 'person_count': np.array([0])       })
    plot1.plot(dataframe.time, dataframe.person_count)
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = root)   
    ##canvas.place(x =0, y = 50)

    canvas.draw() 

    # placing the canvas on the Tkinter window 
    #canvas.get_tk_widget().place() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   root) 
    toolbar.update() 
    
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().place(x = 7, y = 275) 

tree = None

def initUI():
    global tree
    global text_box_min_people
    global text_box_max_people

    root['bg'] = '#fafafa'

    root.title('name')

    root.geometry('1200x720')
    root.resizable(width = False, height= False)

    canvas = Canvas(root, height= 600, width= 900)
    canvas.place()

    frame = Frame(root, bg = '#fafafa', width= 10, height = 10)
    frame.place(relx = 0, rely = 0, relwidth= 1, relheight= 1)
     

    min_people_label = Label(frame, text = 'Min persons count: ', bg = '#fafafa', height = 1, width = 20)

    min_people_label.place(x = 440, y = 50)

    text_box_min_people = Text(frame, height=1, width=10)
    text_box_min_people.place(x = 570, y = 50)

    max_people_label = Label(frame, text = 'Max persons count: ', bg = '#fafafa', height = 1, width = 20)

    max_people_label.place(x = 440, y = 75)

    text_box_max_people = Text(frame, height=1, width=10)
    text_box_max_people.place(x = 570, y = 75)
    ##btn = Button(frame, text = 'open file', bg = 'white')
    ##btn.place(x = 0, y = 0)



    dateString = str(datetime.datetime.now().day) + '/' +  str(datetime.datetime.now().month) + '/' +  str(datetime.datetime.now().year)
    data =  dataReader.currentDaysLog(dateString)
   
    # определяем столбцы
    columns = ("Time", "Status")
 
    tree = ttk.Treeview(frame, columns=columns, show="headings")
  
    tree.place(x = 5, y = 40)
  
    btn = ttk.Button(frame, text="Open data", command=info_window)
    btn.place(x = 5, y = 0, width=100, height=25)
    # определяем заголовки
    tree.heading("Time", text="Time")
    tree.heading("Status", text="Status")
    ##tree.heading("email", text="Email")
    # добавляем данные
    for person in data:
        tree.insert("", END, values=person)



        # the figure that will contain the plot 

def saveData(peopleCount, event = ''):
    dateString = str(datetime.datetime.now().day) + '/' +  str(datetime.datetime.now().month) + '/' +  str(datetime.datetime.now().year)
    timeString = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
    dataReader.databaseAdd(
    dateString,
    timeString,
    #currentTime.time().strftime("%Y"),
    #'25.05.2025',
    # '15:00',
    peopleCount,
    event
    )
    



if __name__ == "__main__":
   
    
    #saveData(22, 'A lot of people')

    #dataReader.dataBaseCler()
    #detector.detect()
    dataReader.databaseCreate()
    initUI()
    plot()
    open_camera()
    root.mainloop()