# -*- coding: latin-1 -*-

''' 
 Freeciv - Copyright (C) 2009 - Andreas Røsdal   andrearo@pvv.ntnu.no
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
'''


import sys
import traceback
from time import gmtime, strftime
import os
import time

_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

startTime = time.time()

def get_debug_info(civcoms):
  code = "<html><head><meta http-equiv=\"refresh\" content=\"20\"></head><body><h2>Freeciv Web Proxy Status</h2>"
  code += "<font color=\"green\">Process status: OK</font><br>";

  code += "<h3>Process Uptime: " + str(int(time.time() - startTime)) + " s.</h3>";
  current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  code += "<b>Current time:</b><br> " + current_time;


  try:    
    code += ("<h3>Logged in users  (count %i) :</h3>" % len(civcoms));
    for key in civcoms.keys():
      code += ("username: <b>%s</b> <br>Civserver: (%s:%d)<br>Client IP:%s<br><br>" % (civcoms[key].username, civcoms[key].civserverhost, civcoms[key].civserverport,  civcoms[key].client_ip));
       

    try:   
      code += "<h3>Memory usage:</h3>";
      code += "Memory: " + str(memory()/1000000) + " MB <br>";
      code += "Resident: " + str(resident()/1000000) + " MB <br>";
      code += "Stacksize: " + str(stacksize()/1000000) + " MB <br>";
    except:
      code += "<br>No memory debugging.<br>";

    code += "<h3>Thread dumps:</h3>";

    for threadId, stack in sys._current_frames().items():
        code += ("<br><br><b><u># ThreadID: %s</u></b><br>" % threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code += ('File: "%s", line %d, in %s: ' % (filename, lineno, name))
            if line:
                code += (" <b>%s</b> <br>" % (line.strip()))



  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

  return code;


def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since
