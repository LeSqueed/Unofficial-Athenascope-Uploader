from mttkinter import mtTkinter as tk
import tkinter.filedialog as filedialog
import subprocess
import threading
import psutil, os
import sys

root = tk.Tk()

#Convert to mttkinter
Label = tk.Label
Entry = tk.Entry
Button = tk.Button
END = tk.END
DISABLED = tk.DISABLED


Text = tk.Text
root.title("Unofficial Athenascope uploader")

def ffmpeg(inp, out):
    def cleanExit(pid, including_parent=True):
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        gone, still_alive = psutil.wait_procs(children, timeout=5)
        if including_parent:
            parent.kill()
            parent.wait(5)

    cmd = "ffmpeg -i "+inp+" "+out
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    buttonExit.config(command=lambda: cleanExit(process.pid))
    
    while process.poll() is None:
        for line in process.stdout:
            textProgress.delete(1.0, END)
            textProgress.insert(END, line)
    
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
    outputArguments = "-c copy -f flv "
    streamOutput = outputArguments+outputLink.strip()
    fProcess = ffmpeg(fileInput, streamOutput)

t = threading.Thread(target=startUpload)

#Creating labels and corresponding input fields.
labelWarning = Label(root, text="Make sure to use the exit button to close this program to make sure all processes end and nothing continues running in the background.")
labelWarning.grid(row=0, column=0, columnspan=2)
labelInput = Label(root, text="Input video:")
entryInput = Entry(root, width=50, border=2)
labelStreamKey = Label(root, text="Athena stream key (only stream key):")
entryStreamKey = Entry(root, width=50, border=2)

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
