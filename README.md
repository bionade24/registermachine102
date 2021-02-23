register machine 102
==

Better implementation of rm101, a fake assembler for educational purposes.  

![Open Window of rm102](rm102.jpg "rm102 window")

Installation
==
A python3 environment and pip are required.  
`make`  
`make install`  

Package rm102 to a single excutable for Linux, macOS or Windows
==
`python3 -m pip install pyinstaller`  

Linux and Mac:  
=
`pyinstaller --noconsole --onefile ./bin/rm102`

Windows:  
=
`pyinstaller.exe --noconsole --onefile .\bin\rm102`
