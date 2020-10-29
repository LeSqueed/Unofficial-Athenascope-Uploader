from mttkinter import mtTkinter as tk
import shlex
import tkinter.filedialog as filedialog
import youtube_dl
import re
import subprocess
import threading
import psutil, os
import sys
import configparser

root = tk.Tk()

videoPath = "./Temp_Imported_vid.mp4"
#Convert to mttkinter
Label = tk.Label
Entry = tk.Entry
Button = tk.Button
END = tk.END
DISABLED = tk.DISABLED

Text = tk.Text
root.title("Unofficial Athenascope uploader")

#Load config file
config = configparser.ConfigParser()
config.read('config.ini')

streamkey = ''
if config.has_option('ATHENA', 'streamkey'):
    streamkey = tk.StringVar(root, value=config['ATHENA']['Streamkey'])

#Check if old video data exists and if so deletes it.
if os.path.exists(videoPath):
    os.remove(videoPath)
dir = "./"
files = os.listdir(dir)
for file in files:
    if file.endswith(".ytdl") or file.endswith(".part"):
        os.remove(os.path.join(dir,file))

def ffmpeg(inp, out):
    class MyLogger(object):
        def debug(self, msg):
            print("DEBUG " + msg)
            pass

        def warning(self, msg):
            print("WARNING " + msg)
            pass

        def error(self, msg):
            print("ERROR " + msg)

    def progress_hook(response):
        if response["status"] == "downloading":
            try:
                textProgress.delete(1.0, END)
                textProgress.insert(END, "Downloading: "+str(round(response["downloaded_bytes"]*100/response["total_bytes"],2))+"%")
            except:
                textProgress.delete(1.0, END)
                textProgress.insert(END, "Downloading: Unable to load progress. Possibly not supported for website in question.")
            try:
                textProgress.insert(END, "Downloading at: "+ str(round((response["speed"]/1024))) + " kilobytes/s")
            except:
                print("Unable to get speed from youtube-dl.")

        if response["status"] == "finished":
            uploadLocal(videoPath, out)
        if response["status"] == "error":
            textProgress.delete(1.0, END)
            textProgress.insert(END, "Error occured while downloading video.")
    def cleanExit(pid, including_parent=True):
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        gone, still_alive = psutil.wait_procs(children, timeout=5)
        if including_parent:
            parent.kill()
            parent.wait(5)

    def uploadLocal(inp, out):
            cmd = "ffmpeg -i \""+inp+"\" -codec copy -f flv "+out
            print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            buttonExit.config(command=lambda: cleanExit(process.pid))
            
            while process.poll() is None:
                for line in process.stdout:
                    textProgress.delete(1.0, END)
                    textProgress.insert(END, line)

    def uploadWeb(inp, out):
            textProgress.insert(END, 'Downloading video from: ' + inp)
            ydl_opts = {
                'outtmpl': videoPath,
                'format': 'best',
                'logger': MyLogger(),
                "progress_hooks": [progress_hook],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([inp])

    #Check if input is a valid url, if not assume it is a local file.
    if re.match(isURL, inp) is not None:
        print('Trying to upload from URL.')
        uploadWeb(inp, out)
    else:
        print('Not an URL, trying to upload local file.')
        uploadLocal(inp, out)

    #FFMpeg finished running. 
    buttonExit.config(command=sys.exit)
    textProgress.delete(1.0, END)
    textProgress.insert(END, "Finished running. You can close this program now.")

def browseFile():
    filename = filedialog.askopenfilename()
    entryInput.delete(0, END)
    entryInput.insert(0, filename)

def startUpload():
    buttonUpload.config(text="Uploading...", state=DISABLED)
    buttonBrowse.config(state=DISABLED)
    entryInput.config(state=DISABLED)
    entryStreamKey.config(state=DISABLED)

    outputLink = "rtmp://stream.athenascope.com/" + entryStreamKey.get()
    
    textProgress.insert(END, "Starting upload process. \n")
    
    #Start upload.
    fileInput = entryInput.get().strip()
    streamOutput = outputLink.strip()
    fProcess = ffmpeg(fileInput, streamOutput)

t = threading.Thread(target=startUpload)

isURL = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#Creating labels and corresponding input fields.
labelWarning = Label(root, text="Make sure to use the exit button to close this program to make sure all processes end and nothing continues running in the background.")
labelWarning.grid(row=0, column=0, columnspan=2)
labelInput = Label(root, text="Input video:")
entryInput = Entry(root, width=50, border=2)
labelStreamKey = Label(root, text="Athena stream key (only stream key):")
entryStreamKey = Entry(root, width=50, border=2, textvariable=streamkey)

labelInput.grid(row=1, column=0)
entryInput.grid(row=1, column=1)
labelStreamKey.grid(row=2, column=0)
entryStreamKey.grid(row=2, column=1)

#Buttons
buttonUpload = Button(root, text="Upload", command=t.start)
buttonExit = Button(root, text="Exit", command=sys.exit)
buttonBrowse = Button(root, text="Browse", command=browseFile)
buttonBrowse.grid(row=1, column=2)

buttonUpload.grid(row=3, column=0)
buttonExit.grid(row=3, column=1)

#Progress
textProgress = Text(root, height=2, border=2, pady=5, padx=5)
textProgress.grid(row=4, column=0, columnspan=2)
textProgress.insert(END, "Ready to start upload process.\n")
root.mainloop()
