#!/bin/env python3
import PySimpleGUI as sg
import subprocess
import pickle
import pprint
from datetime import datetime, timedelta

arbeitszeit_cmd = "echo"
datafile = "./.locktime.json"

try:
  data = pickle.load( open( datafile, "rb" ) )
except:
  data = {}

pprint.pprint(data)

# show window

sg.theme('Default 1')
# All the stuff inside your window.
layout = [  
            [sg.Text('What did you do so far?:'), sg.InputText()],
            [sg.Button('Ok', bind_return_key=True)],
          ]

# Create the Window
window = sg.Window('LockTime', layout)
event, values = window.read()

current = datetime.now() 
current = current - timedelta(minutes=current.minute % 5,
                             seconds=current.second,
                             microseconds=current.microsecond)

#subprocess.run(["cinnamon-screensaver-command", "-l"])
if 'last_update' not in data:
  data['last_update'] = current

work_start = data['last_update'].strftime("%H:%M")
work_end = current.strftime("%H:%M")

subprocess.run([arbeitszeit_cmd, "-normal", work_start + "-" + work_end])

data['last_update'] = current
pickle.dump( data, open( datafile, "wb" ) )

window.close()
