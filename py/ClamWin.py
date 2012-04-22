#!/usr/bin/python
#Boa:App:BoaApp

#-----------------------------------------------------------------------------
# Name:        ClamWin.py
# Product:     ClamWin Antivirus
#
# Author:      Alex Cherney [alex at cher dot id dot au]
#
# Created:     2004/19/03
# Copyright:   Copyright Alex Cherney (c) 2004
# Licence:     
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from wxPython.wx import *

import wxFrameMain
import wxDialogStatus
import wxDialogPreferences
import Config
import os
import RedirectStd



modules ={'CloseWindows': [0, '', 'CloseWindows.py'],
 'Config': [0, '', 'Config.py'],
 'ExplorerShell': [0, '', 'ExplorerShell.py'],
 'Process': [0, '', 'Process.py'],
 'RedirectStd': [0, '', 'RedirectStd.py'],
 'Scheduler': [0, '', 'Scheduler.py'],
 'Tray': [0, '', 'Tray.py'],
 'wxDialogAbout': [0, '', 'wxDialogAbout.py'],
 'wxDialogPreferences': [0, '', 'wxDialogPreferences.py'],
 'wxDialogStatus': [0, '', 'wxDialogStatus.py'],
 'wxFrameMain': [1, 'Main frame of Application', 'wxFrameMain.py']}

class BoaApp(wxApp):
    def __init__(self, params, config, mode='main', autoClose=False, path=''):
        self.config = config
        self.mode = mode       
        self.path = path
        self.autoClose = autoClose
        wxApp.__init__(self, params)

    def OnInit(self):
        wxInitAllImageHandlers()
        if self.mode == 'scanner':        
            wxDialogStatus.Scan(parent=None, config=self.config, path=self.path)         
        elif self.mode == 'update':            
            wxDialogStatus.UpdateVirDB(parent=None, config=self.config, autoClose=self.autoClose)
        elif self.mode == 'configure':            
            wxDialogPreferences.Configure(parent=None, config=self.config)
        else: #  mode == 'main'
            self.main = wxFrameMain.create(parent=None, config=self.config)
            self.main.Show()
            #workaround for running in wxProcess        
            self.SetTopWindow(self.main)            
        return True


def main(config=None, mode='main', autoClose=False, path='', config_file=None):
    # get the directory of our exetutable file
    # when running as pyexe built module
    try:
        if hasattr(sys, "frozen"):        
            if sys.frozen == "dll":            
                this_filename = win32api.GetModuleFileName(sys.frozendllhandle)
            else:
                this_filename = sys.executable
            currentDir = os.path.split(this_filename)[0]
        else:    
            currentDir = os.path.split(os.path.abspath(__file__))[0]
    except NameError: # No __file__ attribute (in boa debugger)
        currentDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    os.chdir(currentDir)    
    
    if config is None:
        if(config_file is None):
            config_file = os.path.join(currentDir,'ClamWin.conf')
            if not os.path.isfile(config_file):
                config_file = 'ClamWin.conf'                    
        config = Config.Settings(config_file)    
        config.Read()
        
    app = BoaApp(0, config, mode=mode, autoClose=autoClose, path=path)   
    app.MainLoop()    



if __name__ == '__main__':
    close = False
    mode = 'main'
    path = ''
    config_file = None
    for arg in sys.argv[1:]:
        if arg == '--close':
            close = True
        if arg.find('--mode=') == 0:
            mode = arg[len('--mode='):]
        if arg.find('--path=') == 0:
            path = arg[len('--path='):]            
        if arg.find('--config_file=') == 0:
            path = arg[len('--config_file='):]
                                
        
    main(mode=mode, autoClose=close, path=path, config_file=config_file)