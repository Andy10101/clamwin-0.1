#-----------------------------------------------------------------------------
# Name:        Tray.py
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

#-----------------------------------------------------------------------------
# this code is based on win32gui_taskbar.py demo from Mark Hammond's
# win32 extensions.

import win32api, win32gui, win32con, win32event
import win32process, win32event
import sys, os, tempfile
import Scheduler
import Config
import wxDialogStatus
import Process
from threading import *
import time
import RedirectStd


def GetCurrentDir():    
    # attempt to read the folder form registry first
    key = None
    try:
        key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'Software\\ClamWin')
        currentDir = win32api.RegQueryValueEx(key, 'Path')[0]                                        
        win32api.CloseHandle(key)
        return currentDir
    except win32api.error:                      
        if key is not None:
            win32api.CloseHandle(key)
        # couldnt find it in the registry
        # get it from command line
        if hasattr(sys, "frozen"):
            if sys.frozen == "dll":            
                this_filename = win32api.GetModuleFileName(sys.frozendllhandle)
            else:
                this_filename = sys.executable
            currentDir = os.path.split(this_filename)[0]
        else:    
            currentDir = os.path.split(os.path.abspath(__file__))[0]
        return currentDir

class MainWindow:    
    MENU_OPEN_CLAM=1023
    MENU_UPDATE_DB=1024
    MENU_CONFIGURE=1025
    MENU_EXIT=1026
    ACTIVE_MUTEX='ClamWinTrayMutex01'     
    WM_CONFIG_UPDATED=win32con.WM_USER+21  
                  
    def __init__(self, config):        
        self._config = config
        self._scheduler = None
        self._proc = None
        self._out = None        
        self.scheduleRunning = False        
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated");
        message_map = {
                msg_TaskbarRestart: self.OnRestart,
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_COMMAND: self.OnCommand,
                win32con.WM_USER+20 : self.OnTaskbarNotify,
                win32con.WM_USER+21 : self.OnConfigUpdated,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "ClamWinTrayWindow"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( classAtom, "ClamWin", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        
        # create mutex to prevent further instances
        self._hActiveMutex = win32event.CreateMutex(None, True, self.ACTIVE_MUTEX)
        self._DoCreateIcons()
        self._InitScheduler()
        
        # start config monitor thread
        self._configMonitor = MonitorConfig(self.NotifyConfig, (self.hwnd,))
        self._configMonitor.start()
        
    def _IsProcessRunning(self, wait=False):
        if wait:
            timeout = 5
        else:
            timeout = 0            
        try:        
            self._proc.wait(timeout)
        except Exception, e:
            if isinstance(e, Process.ProcessError):
                if e.errno == Process.ProcessProxy.WAIT_TIMEOUT:        
                    return True     
                else:
                    return False
        return False

    def _StopProcess(self):  
        # check if process is still running
        if self._IsProcessRunning():       
            # still running - kill            
            self._proc.kill()            
            #wait to finish
            if self._IsProcessRunning(True):       
                #still running - complain and terminate
                win32gui.MessageBox(self.hwnd, 'Unable to stop scheduled process, terminating', 'ClamWin', win32con.MB_OK | win32con.MB_ICONSTOP)
                os._exit(0)  
            self._proc.close()
            self._out.close()                 
        
    def _InitScheduler(self):      
        self._StopProcess()       
        if self._config.Get('Updates', 'Enable') == '1':            
            self._scheduler = Scheduler.Scheduler(self._config.Get('Updates', 'Frequency'),
                                self._config.Get('Updates', 'Time'),
                                int(self._config.Get('Updates', 'WeekDay')), 
                                win32gui.PostMessage, (self.hwnd, win32con.WM_COMMAND, self.MENU_UPDATE_DB, 1))
            
            self._scheduler.start()        
            
            
    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst =  win32api.GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0],"img/FrameIcon.ico"))
        if not os.path.isfile(iconPathName):
            # Look in the current folder tree.
            iconPathName = "img/FrameIcon.ico"
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:            
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "ClamWin Antivirus")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):                  
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        self._StopThreads()        
        win32event.ReleaseMutex(self._hActiveMutex)
        win32api.CloseHandle(self._hActiveMutex)
        self._StopProcess()
        win32gui.PostQuitMessage(0) # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONUP:
            pass
        elif lparam==win32con.WM_LBUTTONDBLCLK:
           self.OnCommand(hwnd, win32con.WM_COMMAND, self.MENU_OPEN_CLAM, 0)
        elif lparam==win32con.WM_RBUTTONUP:            
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu( menu, win32con.MF_STRING, self.MENU_OPEN_CLAM, "Open ClamWin")
            win32gui.AppendMenu( menu, win32con.MF_STRING, self.MENU_UPDATE_DB, "Download Virus Database Update")
            win32gui.AppendMenu( menu, win32con.MF_STRING, self.MENU_CONFIGURE, "Configure ClamWin")
            win32gui.AppendMenu( menu, win32con.MF_STRING, self.MENU_EXIT, "Exit" )
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            try:
                win32gui.SetMenuDefaultItem(menu, 0, 1)
            except NameError:
                pass

            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == self.MENU_OPEN_CLAM:
            self._ShowClamWin()
        elif id == self.MENU_UPDATE_DB:
            self._UpdateDB(lparam)
        elif id == self.MENU_CONFIGURE:
            self._ShowConfigure()
        elif id == self.MENU_EXIT:  
            self.OnExit()
            
    def OnConfigUpdated(self, hwnd, msg, wparam, lparam):
    	    self._config.Read()
    	    self._InitScheduler()    	    
            
    def _StopThreads(self):
        # stop running threads
        threads = (self._scheduler, self._configMonitor)
        for thread in threads:
            if thread is not None:
                thread.stop()
                thread.join(2)        
                             
    def OnExit(self):
        self._StopThreads()
        win32gui.DestroyWindow(self.hwnd)
        win32gui.PostQuitMessage(0)
                
    
    
    def _ShowClamWin(self):        
        try:  
            curDir = GetCurrentDir()
            os.spawnl(os.P_NOWAIT , curDir + '\\ClamWin.exe',  ' --mode=main', ' --config_file=%s' % curDir + '\\ClamWin.conf')            
        except Exception, e:            
            win32gui.MessageBox(self.hwnd, 'An error occured while starting ClamWin scanner.\n' + str(e), 'ClamWin', win32con.MB_OK | win32con.MB_ICONERROR)                              
    
    def _UpdateDB(self, hide):                
        if not hide:                        
            try:
                os.spawnl(os.P_NOWAIT, GetCurrentDir() + '\\ClamWin.exe', ' --mode=update')                    
            except Exception, e:
                win32gui.MessageBox(self.hwnd, 'An error occured while starting ClamWin Update.\n' + str(e), 'ClamWin', win32con.MB_OK | win32con.MB_ICONERROR)                                  
        else:            
            # update virus db silently
            if self.scheduleRunning:
                print 'Schedule is still running'
                return
            freshclam_conf = wxDialogStatus.SaveFreshClamConf(self._config)
            try:
                if not len(freshclam_conf):
                    win32gui.MessageBox(self.hwnd, 'Unable to cerate freshclam configuration file. Please check there is enough space on the disk', 'Error', win32con.MB_OK | win32con.MB_ICONSTOP)
                    return
                
                cmd = '"' + self._config.Get('ClamAV', 'FreshClam') +  '" --stdout --datadir="' + \
                        self._config.Get('ClamAV', 'Database') + '"' + \
                        ' --config-file="%s"' % freshclam_conf                
                
                try:
                    self._SpawnProcess(cmd)
                    self.scheduleRunning = True
                except Process.ProcessError, e:
                    print 'Unable to spawn schedulted process.\nCommand line: %s\nError: %s' % (cmd , str(e))
                    os.remove(freshclam_conf)
                    return
                # wait 2 seconds for the process to start, then delete
                # temp file
                try:
                    self._proc.wait(2)
                except:
                    pass
                os.remove(freshclam_conf)
            except Exception, e:            
                self.scheduleRunning = False    
                print 'Error performing Scheduled Update.', str(e)
                os.remove(freshclam_conf)                  
                    
    
    def _ShowConfigure(self):
        try:                           
            curDir = GetCurrentDir()
            os.spawnl(os.P_NOWAIT,  curDir + '\\ClamWin.exe', ' --mode=configure', ' --config_file=%s' % curDir + '\\ClamWin.conf')
        except Exception, e:            
            win32gui.MessageBox(self.hwnd, 'An error occured while starting ClamWin Preferences.\n' + str(e), 'ClamWin', win32con.MB_OK | win32con.MB_ICONERROR)
            
    def _SpawnProcess(self, cmd):
        # initialise environment var TMPDIR
        # cygwin seems to set this var on Windows 2000 only
        # hence causes liblamav to exit with error on other 
        # versions of Windows
        try:
            if os.getenv('TMPDIR') is None:
                os.putenv('TMPDIR', tempfile.gettempdir())
        except Exception, e:
            print 'Could Not Set TMPDIR environment variable. Error: %s' % str(e)            
            
        # check that we got the command line        
        if cmd is None:   
            raise Process.ProcessError('Could not start process. No Command Line specified')                                                     
        
        # start our process    
        try:                
            # check if the file exists first
            executable = cmd.split('" ' ,1)[0].lstrip('"')
            if not os.path.exists(executable):
                raise Process.ProcessError('Could not start process.\n%s\nFile does not exist.' % executable)                
            # create our stdout implementation that updates status window                
            self._out = StatusPrintBuffer(self, self.NotifyUpdate)
            self._proc = Process.ProcessProxy(cmd, stdout=self._out)                                                                
            self._proc.wait(0)
        except Exception, e:             
            if isinstance(e, Process.ProcessError):
                if e.errno != Process.ProcessProxy.WAIT_TIMEOUT:                                       
                    raise Process.ProcessError('Could not start process:\n%s\nError: %s' % (cmd, str(e)))                     
            else:
                raise Process.ProcessError('Could not start process:\n%s\nError: %s' % (cmd, str(e)))                 
            
    def NotifyConfig(hwnd):        
        win32api.PostMessage(hwnd, MainWindow.WM_CONFIG_UPDATED, 0, 0)
    NotifyConfig = staticmethod(NotifyConfig)
    
    def NotifyUpdate(owner):        
        owner.scheduleRunning = False
        print 'Scheduled task finished'
    NotifyUpdate = staticmethod(NotifyUpdate)
        
class StatusPrintBuffer(Process.IOBuffer):            
    def __init__(self,  caller, notify):
        Process.IOBuffer.__init__(self)
        self._caller = caller
        self.notify = notify
        
    def _doWrite(self, s):
        progress_markers = ['[|]', '[/]', '[-]', '[\]', '[*]']
        # check if the current line contains progress marker
        lines = s.replace('\r', '\n').splitlines(True)        
        for line in lines:              
            printable = True
            for marker in progress_markers:
                if line.find(marker) != -1:
                    printable = False
                    break
            if printable:
                print line
                                                
    def _doClose(self):
        self.notify(self._caller)
        Process.IOBuffer._doClose(self)
                    
class MonitorConfig(Thread):   
    def __init__(self, notify, args):
        self.notify = notify
        self.args = args
        self._terminate = False
        Thread.__init__(self)
        
    def __del__(self):        
        self.stop()        

    def run(self):
        self._terminate = False
        try:
           hEvent = win32event.CreateEvent(None, True, False, Config.CONFIG_EVENT)
        except win32api.error:
            return
                
        while not self._terminate:
            wait = win32event.WaitForSingleObject(hEvent, 1000);
            if wait != win32event.WAIT_TIMEOUT:
                self.notify(*self.args)                            

    def stop(self):
        if not self.isAlive():
            return
        self._terminate = True
                
    def is_cancelled(self):
        return self._cancelled

    def get_returnCode(self):
        return self._ret
                     
    
                
def main():
     # get the directory of our exetutable file
    # when running as pyexe built module
    try:
        if hasattr(sys, "frozen"):
            currentDir = os.path.split(sys.executable)[0]
        else:    
            currentDir = os.path.split(os.path.abspath(__file__))[0]
    except NameError: # No __file__ attribute (in boa debugger)
        currentDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    os.chdir(currentDir)    
    
    # see if we are already running and exit if so
    try:
        # try to acquire our active mutex       
        hMutex = win32event.OpenMutex(win32con.SYNCHRONIZE, False, MainWindow.ACTIVE_MUTEX)
        # could open it - most likely another window is active
        # just to be sure wait for it to see if it is claimed
        if win32event.WaitForSingleObject(hMutex, 0) == win32event.WAIT_TIMEOUT:           
            # mutex is claimed, another window is already running - terminate
            return
        CloseHandle(hMutex)
    except win32api.error:
        pass
    
    
    conf_file = os.path.join(currentDir,'ClamWin.conf')
    if not os.path.isfile(conf_file):
        conf_file = 'ClamWin.conf'    
    config = Config.Settings(conf_file)    
    config.Read()
        
    w=MainWindow(config)
    win32gui.PumpMessages()

if __name__=='__main__':
    main()
