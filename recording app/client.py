
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse

import socket



# import tkinter as tk
import random
import pandas as pd
# import time
import threading
import pyaudio
import wave
# import cv2
#host = socket.gethostname()  # as both code is running on same pc
#host = '127.0.0.1'
# host = '10.196.30.13'
# port = 5000  # socket server port number

# client_socket = socket.socket()  # instantiate
# client_socket.connect((host, port))  # connect to the server

df = pd.read_csv('questions.csv', encoding='iso-8859-1')

n2=False

cnt = 0
n= df.shape[0]
q=[False]*n
s = set()
i =0 
j = [0]*n
list1 =[]
list2 = []
q_list = [0,1,3,4,6,7,8,10,11,12,13,15]
q2_list = [1,4,8,13]



def print_fun(a):
    if a==True:
        return "Please be truthful"
    elif a=="Impression management":
        return "Please speak to impress the interviewer whether truth or lie"
    else:
        return "Please tell a lie"

while(cnt<2*n-4):
    flag = 0
    # i = random.randrange(0, n)
    i =random.choice(q_list)
    # print(i)
    if i in s:
        continue
    if j[i]==0:
        if i==3 or i==6:
            cnt+=1
            s.add(i)
            if n2==False:               
                n1 = random.getrandbits(1)
                n2=True
                list1.append(df[df.columns[n1]].iloc[i])
                list2.append('Impression management')
            else:
                n1= abs(1-n1)
                list1.append(df[df.columns[n1]].iloc[i])
                list2.append('Impression management')
        elif i==15 or i==11:
            s.add(i)
            cnt+=1
            list1.append(df[df.columns[0]].iloc[i])
            list2.append('Impression management')            
        else:
            list1.append(df[df.columns[0]][i])
            k= bool(random.getrandbits(1))
            q[i] = k
            cnt+=1
            list2.append(k)
    elif j[i]==1:
        k = not q[i]
        s.add(i)
        cnt+=1
        list1.append(df[df.columns[0]][i])
        list2.append(k)
    if i in q2_list:
        list1.append(df[df.columns[0]][i+1])
        list2.append(k)
        cnt+=1

    # print(i,k,cnt)
    j[i]+=1

df2 = pd.DataFrame(columns =['question','truth or lie'])
for i in range(len(list1)):
    print(i,list1[i], list2[i])
    df2  = df2.append({'question': list1[i], 'truth or lie': list2[i]}, ignore_index = True)
df2.to_csv('questions_candidate.csv',index = False)    


LARGE_FONT= ("Verdana", 16)

FONT2= ("Arial",16)
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok=False
        self.t = pd.DataFrame(columns =['page','time'])
        self.start = time.time()

        #timerac
        self.timer=ElapsedTimeClock(self.window)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        # self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        # self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT)

        #video control buttons

        self.btn_start=tk.Button(window, text='START', command=self.open_camera)
        self.btn_start.pack(side=tk.LEFT)

        self.btn_stop=tk.Button(window, text='STOP', command=self.close_camera)
        self.btn_stop.pack(side=tk.LEFT)

        # quit button
        self.btn_quit=tk.Button(window, text='QUIT', command=self.quit_func)
        self.btn_quit.pack(side=tk.LEFT)
        self.chunk = 1024 
        self.sample_format = pyaudio.paInt16 
        self.channels = 2
        self.fs = 44100  
    

        self.frames2 = []
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=10
        self.update()
        self.client_program()
        # self.window.mainloop()
        container = tk.Frame(self.window)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,PageSix, PageSeven, PageEight, PageNine, PageTen, PageEleven, PageTwelve, PageThirteen, PageFourteen, PageFifteen, PageSixteen, PageSeventeen, PageEighteen, PageNineteen, PageTwenty, PageTwentyOne, PageTwentyTwo, PageTwentyThree, PageTwentyFour, PageTwentyFive, PageTwentySix, PageTwentySeven, PageTwentyEight,EndPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage,"StartPage")
    def quit_func(self):
        self.close_camera()
        self.stoprecording()
        self.client_socket.close()
        quit()
    def show_frame(self, cont,n):
        print(cont)
        if n=='PageOne':
            message = 'start'
            # client_socket.sendall(b'start')
            self.client_socket.send(message.encode())
            self.open_camera()
            self.startrecording()
            self.start = time.time()


        # elif n=='StartPage':
        #     # message = 'stop'
        #     # self.client_socket.send(message.encode())
        #     # self.client_socket.sendall(b'stop')
        #     # self.client_socket.close()
        #     self.close_camera()
            # self.pause = time.time()
        elif n=='EndPage':
            self.close_camera()
            self.stoprecording()
        # self.t = self.t.append({'page':n,'time':time.time()-self.start}, ignore_index=True)
        self.t = self.t.append({'page':n,'time':self.timer.return_time()}, ignore_index=True)
        print(self.t)
        self.t.to_csv('time.csv',index = False)
        # t.to_csv('time.csv',index = False)
        frame = self.frames[cont]
        frame.tkraise()

    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

    def open_camera(self):
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")



    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")
        # self.stoprecording()
    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
        
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename='audio'
        self.filename = self.filename+".wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames2))
        wf.close()
        # main.destroy()
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames2.append(data)
        
    def client_program(self):
        # host = socket.gethostname()  # as both code is running on same pc
        host = '10.196.30.13'
        port = 5000  # socket server port number

        self.client_socket = socket.socket()  # instantiate
        # client_socket.setblocking(0)
        self.client_socket.connect((host, port))  # connect to the server

        # message = input(" -> ")  # take input

        # while message.lower().strip() != 'bye':
        #     client_socket.send(message.encode())  # send message
        #     # data = client_socket.recv(1024).decode()  # receive response

        #     # print('Received from server: ' + data)  # show in terminal

        #     message = input(" -> ")  # again take input

        # client_socket.close()  # close the connection
       
    def update(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            # self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="",  font = ("Arial",16),wraplength=300, justify="center")

        button = tk.Button(self, text="Start the interview",
                            command=lambda: controller.show_frame(PageOne,"PageOne"))
        button.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[0], font = ("Arial",16), wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[0]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage,"StartPage"))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwo,"PageTwo"))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[1], font= ("Arial",16),wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[1]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageOne,"PageOne"))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageThree,"PageThree"))
        button2.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[2], font= ("Arial",16), wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[2]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwo,"PageTwo"))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageFour,"PageFour"))
        button2.pack()
# #Page4
class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[3], font= ("Arial",16), wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[3]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageThree,"PageThree"))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageFive,"PageFive"))
        button2.pack()

# #Page5
class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[4], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[4]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageFour,'PageFour'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageSix,'PageSix'))
        button2.pack()
#Page6

class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[5], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[5]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageFive,'PageFive'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageSeven,'PageSeven'))
        button2.pack()
# #Page7
class PageSeven(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[6], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[6]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageSix,'PageSix'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageEight,'PageEight'))
        button2.pack()
# #Page8
class PageEight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[7], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[7]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageSeven,'PageSeven'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageNine,'PageNine'))
        button2.pack()
# #Page 9

class PageNine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[8], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[8]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageEight,'PageEight'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTen,'PageTen'))
        button2.pack()
# #PAge10
class PageTen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[9], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[9]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageNine,'PageNine'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageEleven,'PageEleven'))
        button2.pack()

# #Page11
class PageEleven(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[10], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[10]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTen,'PageTen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwelve,'PageTwelve'))
        button2.pack()

# #Page12
class PageTwelve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[11], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[11]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageEleven,'PageEleven'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageThirteen,'PageThirteen'))
        button2.pack()
        
# #Page13
class PageThirteen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[12], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[12]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwelve,'PageTwelve'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageFourteen,'PageFourteen'))
        button2.pack()

# #Page14
class PageFourteen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[13], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[13]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageThirteen,'PageThirteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageFifteen,'PageFifteen'))
        button2.pack()
# #Page15

class PageFifteen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[14], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[14]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageFourteen,'PageFourteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageSixteen,'PageSixteen'))
        button2.pack()
# #Page16
class PageSixteen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[15], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[15]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageFifteen,'PageFifteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageSeventeen,'PageSeventeen'))
        button2.pack()
# #Page17
class PageSeventeen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[16], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[16]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageSixteen,'PageSixteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageEighteen,'PageEighteen'))
        button2.pack()
# #Page18
class PageEighteen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[17], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[17]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageSeventeen,'PageSeventeen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageNineteen,'PageNineteen'))
        button2.pack()
# #PAge19
class PageNineteen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[18], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[18]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageEighteen,'PageEighteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwenty,'PageTwenty'))
        button2.pack()

# #PAge20
class PageTwenty(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[19], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[19]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageNineteen,'PageNineteen'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyOne,'PageTwentyOne'))
        button2.pack()
# #Page21
class PageTwentyOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[20], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[20]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwenty,'PageTwenty'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyTwo,'PageTwentyTwo'))
        button2.pack()

# #Page22
class PageTwentyTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[21], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[21]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyOne,'PageTwentyOne'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyThree,'PageTwentyThree'))
        button2.pack()
        
# #Page23
class PageTwentyThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[22], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[22]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyTwo,'PageTwentyTwo'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyFour,'PageTwentyFour'))
        button2.pack()

# #Page24
class PageTwentyFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[23], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[23]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyThree,'PageTwentyThree'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyFive,'PageTwentyFive'))
        button2.pack()
# #Page25

class PageTwentyFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[24], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[24]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyFour,'PageTwentyFour'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentySix,'PageTwentySix'))
        button2.pack()
# #Page26
class PageTwentySix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[25], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[25]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyFive,'PageTwentyFive'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentySeven,'PageTwentySeven'))
        button2.pack()
# #Page27
class PageTwentySeven(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[26], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[26]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentySix,'PageTwentySix'))
        button1.pack()

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwentyEight,'PageTwentyEight'))
        button2.pack()
# #Page28
class PageTwentyEight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=list1[27], font= FONT2, wraplength=300, justify="center")
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=print_fun(list2[27]), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentySeven,'PageTwentySeven'))
        button1.pack()

        button2 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(EndPage, 'EndPage'))
        button2.pack()

class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwentyEight,'PageTwentyEight'))
        button1.pack()

        button2 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage, 'StartPage'))
        button2.pack()

class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.FPS = 1/40
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args=CommandLineParser().args

        
        #create videowriter

        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc=VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res


    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            time.sleep(self.FPS)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class ElapsedTimeClock:
    def __init__(self,window):
        self.T=tk.Label(window,text='00:00:00',font=('times', 20, 'bold'), bg='green')
        self.T.pack(fill=tk.BOTH, expand=1)
        self.elapsedTime=dt.datetime(1,1,1)
        self.running=0
        self.lastTime=''
        t = time.localtime()
        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
        # self.tick()

 
    def tick(self):
        # get the current local time from the PC
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.updwin=self.T.after(100, self.tick)

    def return_time(self):
        return self.lastTime


    def start(self):
            if not self.running:
                self.zeroTime=dt.datetime(1, 1, 1).now()-self.elapsedTime
                self.tick()
                self.running=1

    def stop(self):
            if self.running:
                self.T.after_cancel(self.updwin)
                self.elapsedTime=dt.datetime(1, 1, 1).now()-self.zeroTime
                self.time2=self.elapsedTime
                self.running=0


class CommandLineParser:
    
    def __init__(self):

        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()



def main():
    # Create a window and pass it to the Application object
    app= App(tk.Tk(),'Video Recorder')
    app.window.mainloop()

main()    
