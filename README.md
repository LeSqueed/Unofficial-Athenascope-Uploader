# Unofficial Athenascope Uploader
 Tool to upload videos to [Athenascope.com](https://athenascope.com/) as a session.
 This tool is not an officially supported program from Athenascope.

### How to use:
Either download the executable from the releases or clone this repository and install the required dependencies.

#### Running executable.

Make sure you have FFmpeg installed on your system and it is added to your system PATH.
After this you can just run the executable file you find in releases.

#### Cloning Repository instructions.

##### Dependencies:
FFmpeg (has to be in your PATH).

Python Modules:
mttkinter, subprocess, threading

Run the uploader.py file. This will open a dialog window.
Here you can select the file to upload and enter your stream key. The stream key can be found on the [Athenascope website](https://athenascope.com/) in your settings.

Do **NOT** add the entire URL, only the stream key!
