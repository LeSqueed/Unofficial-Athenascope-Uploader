# Unofficial Athenascope Uploader
 Tool to upload videos to [Athenascope.com](https://athenascope.com/) as a session.
 This tool is not an officially supported program from Athenascope.

### Usage: 
After launching the program you select a file to upload in the first field. If you want to download a video from a website like YouTube enter the full URL (including the http/https). Enter your stream key in the second one. The stream key can be found on the [Athenascope website](https://athenascope.com/) in your settings.

Copy config.example.ini to config.ini. After that open the file and place your streamkey after the "Streamkey = " value.
You can also manually type in your streamkey after launching the application but it won't save it for the next time you launch the application.

Do **NOT** add the entire URL, only the stream key!

#### Running executable.

Make sure you have FFmpeg installed on your system and it is added to your system PATH.
After this you can just run the executable file you find in releases.

#### Cloning Repository instructions.

##### Dependencies:
FFmpeg (has to be in your PATH).

Python Modules:
mttkinter, subprocess, threading

Run the uploader.py file with python 3+.