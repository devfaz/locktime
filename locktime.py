#!/bin/env python3
import PySimpleGUI as sg
import subprocess
import pickle
import pprint
from datetime import datetime, timedelta
import argparse
import sys

parser = argparse.ArgumentParser(description='locktime')
parser.add_argument('--arbeitszeit-cmd', dest='update_cmd', default='echo')
parser.add_argument('--screensaver-active-check', dest='screensaver_active_check', default='cinnamon-screensaver-command -q | grep inaktiv')
parser.add_argument('--screensaver-cmd', dest='screensaver_cmd', default='cinnamon-screensaver-command -l')
parser.add_argument('--datafile', dest='datafile', default='./.locktime.json')
parser.add_argument('--lock', dest='lock',  action='store_true')
args = parser.parse_args()

try:
  data = pickle.load( open( args.datafile, "rb" ) )
except:
  data = {}

pprint.pprint(data)
current = datetime.now()
current = current - timedelta(minutes=current.minute % 5, seconds=current.second, microseconds=current.microsecond)

if 'last_update' not in data:
  data['last_update'] = current


if args.lock:
  sg.theme('Default 1')
  # All the stuff inside your window.
  layout = [
              [sg.Text('What did you do so far?:'), sg.InputText()],
              [sg.Button('Ok', bind_return_key=True)],
            ]

  # Create the Window
  window = sg.Window('LockTime', layout)
  event, values = window.read()
  window.close()

  # exit
  if event in (None, 'Quit'):
    sys.exit(1)

  #subprocess.run(["cinnamon-screensaver-command", "-l"])
  work_start = data['last_update'].strftime("%H:%M")
  work_end = current.strftime("%H:%M")

  subprocess.run([args.update_cmd, "-normal", work_start + "-" + work_end])
  subprocess.run(args.screensaver_cmd, shell=True)

else:
  # check if screensaver is running
  if True:
    # screensaver is *NOT* running - save starttime, if no data exists
    print (data['last_update'].day)
    print (current.day)
    if data['last_update'].day != current.day:
      print("Setting last_update to %s", current)
      data['last_update'] = current

data['last_update'] = current
pickle.dump( data, open( args.datafile, "wb" ) )
