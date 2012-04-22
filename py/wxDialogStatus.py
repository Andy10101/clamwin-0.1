#-----------------------------------------------------------------------------
#Boa:Dialog:wxDialogStatus

#-----------------------------------------------------------------------------
# Name:        wxDialogStatus.py
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
from wxPython.lib.throbber import Throbber, __doc__ as docString
from threading import *
from throb import throbImages
import string
import time
import tempfile
import Process
import os, sys
import MsgBox

def create(parent, cmd, logfile, priority, bitmap_mask):
    return wxDialogStatus(parent, cmd, logfile, priority, bitmap_mask)

_FRESHCLAM_CONF_GENERAL = """
DatabaseMirror database.clamav.net
MaxAttempts 3
"""
_FRESHCLAM_CONF_PROXY = """
HTTPProxyServer %s
HTTPProxyPort %s
"""
_FRESHCLAM_CONF_PROXY_USER = """
HTTPProxyUsername %s
HTTPProxyPassword %s
"""

_WAIT_TIMEOUT = 5
if sys.platform.startswith("win"):    
    _KILL_SIGNAL = None    
    _WAIT_NOWAIT = 0
    _NEWLINE_LEN=2
else:
    import signal, os
    _KILL_SIGNAL = signal.SIGKILL
    _WAIT_NOWAIT = os.WNOHANG
    _NEWLINE_LEN=1


def SafeTempFile():
    fd = -1
    name = ''                            
    try:            
        if sys.version_info[0] < 2 or sys.version_info[1] < 3:            
            name = tempfile.mktemp()                
            fd = os.open(name, os.O_WRONLY|os.O_CREAT)
        else:
            fd, name = tempfile.mkstemp(text=true)                            
    except Exception, e:            
        print 'cannot create temp file. Error: ' + str(e)    
    return (fd, name)
    
def SaveFreshClamConf(config):
        data = _FRESHCLAM_CONF_GENERAL
        if len(config.Get('Proxy', 'Host')):
            data += _FRESHCLAM_CONF_PROXY % \
                    (config.Get('Proxy', 'Host'), config.Get('Proxy', 'Port'))
        if len(config.Get('Proxy', 'User')):        
            data += _FRESHCLAM_CONF_PROXY_USER % \
                (config.Get('Proxy', 'User'), config.Get('Proxy', 'Password'))
                            
        fd, name = SafeTempFile()                                    
        try:                        
            os.write(fd, data)                    
        finally:            
            if fd != -1:
                os.close(fd)                                        
        
        return name    
    
        
def UpdateVirDB(parent, config, autoClose = False):        
    freshclam_conf = SaveFreshClamConf(config)
    if not len(freshclam_conf):
        MsgBox.ErrorBox(parent, 'Unable to cerate freshclam configutration file. Please check there is enough space on the disk')
        return
        
    cmd = '"' + config.Get('ClamAV', 'FreshClam') + '"' + ' --stdout --datadir="' + \
            config.Get('ClamAV', 'Database') + '"' + \
            ' --config-file="%s"' % freshclam_conf

    dlg = create(parent, cmd, None, 'n', 'update')
    dlg.SetTitle('ClamWin Internet Update Status')
    dlg.SetAutoClose(autoClose)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy() 
        try:
            os.remove(freshclam_conf)        
        except Exception, e:
            print "couldn't remove file %s. Error: %s" % (freshclam_conf, str(e))

def Scan(parent, config, path):             
    logfile = tempfile.mktemp()
    cmd = '"' + config.Get('ClamAV', 'ClamScan') + '"'
    if config.Get('ClamAV', 'ScanRecursive') == '1':
        cmd += ' --recursive'
    if config.Get('ClamAV', 'RemoveInfected') == '1':
        cmd += ' --remove'
    cmd += ' --stdout --database="' + \
            config.Get('ClamAV', 'Database') + '" --log="' + \
            logfile + '" "' + path + '"'    
    try:
        priority = string.lower(config.Get('ClamAV', 'Priority')[:1])
    except:
        priority = 'n'      
    dlg = create(parent, cmd, logfile, priority, "scanprogress")
    dlg.SetTitle("ClamWin Scan Status")
    try:
        dlg.ShowModal()        
    finally:
        dlg.Destroy()


class StatusUpdateBuffer(Process.IOBuffer):            
    def __init__(self,  caller, update, notify):
        Process.IOBuffer.__init__(self)
        self._caller = caller
        self.update = update
        self.notify = notify        
        
    def _doWrite(self, s):
        # sometimes there is more than one line in the buffer
        # so we need to call update method for every new line                                
        lines = s.replace('\r', '\n').splitlines(True)        
        for line in lines:              
            self.update(self._caller, line)             
        
        # do not call original implementation
        # Process.IOBuffer._doWrite(self, s)
        
    def _doClose(self):
        self.notify(self._caller)
        Process.IOBuffer._doClose(self)

# custom command events sent from worker thread when it finishes    
# and when status message needs updating
# the handler updates buttons and status text
THREADFINISHED = wxNewEventType() 
def EVT_THREADFINISHED( window, function ):     
    window.Connect( -1, -1, THREADFINISHED, function ) 
 
class ThreadFinishedEvent(wxPyCommandEvent): 
    eventType = THREADFINISHED 
    def __init__(self, windowID): 
        wxPyCommandEvent.__init__(self, self.eventType, windowID) 
 
    def Clone( self ): 
        self.__class__( self.GetId() )
 
THREADUPDATESTATUS = wxNewEventType() 
def EVT_THREADUPDATESTATUS( window, function ):     
    window.Connect( -1, -1, THREADUPDATESTATUS, function ) 
           
class ThreadUpdateStatusEvent(wxPyCommandEvent): 
    eventType = THREADUPDATESTATUS 
    def __init__(self, windowID, text, append): 
        self.text = text
        self.append = append
        wxPyCommandEvent.__init__(self, self.eventType, windowID) 
 
    def Clone( self ): 
        self.__class__( self.GetId() )
                 

[wxID_WXDIALOGSTATUS, wxID_WXDIALOGSTATUSBUTTONSAVE, 
 wxID_WXDIALOGSTATUSBUTTONSTOP, wxID_WXDIALOGSTATUSSTATICBITMAP1, 
 wxID_WXDIALOGSTATUSTEXTCTRLSTATUS, 
] = map(lambda _init_ctrls: wxNewId(), range(5))

class wxDialogStatus(wxDialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxDialog.__init__(self, id=wxID_WXDIALOGSTATUS, name='wxDialogStatus',
              parent=prnt, pos=wxPoint(449, 269), size=wxSize(568, 392),
              style=wxDEFAULT_DIALOG_STYLE, title='ClamWin Status')
        self.SetClientSize(wxSize(560, 365))
        self.SetAutoLayout(false)
        self.Center(wxBOTH)
        self.SetToolTipString('')
        EVT_CLOSE(self, self.OnWxDialogStatusClose)

        self.textCtrlStatus = wxTextCtrl(id=wxID_WXDIALOGSTATUSTEXTCTRLSTATUS,
              name='textCtrlStatus', parent=self, pos=wxPoint(89, 11),
              size=wxSize(455, 300),
              style=wxTAB_TRAVERSAL | wxTE_MULTILINE | wxTE_READONLY, value='')

        self.staticBitmap1 = wxStaticBitmap(bitmap=wxNullBitmap,
              id=wxID_WXDIALOGSTATUSSTATICBITMAP1, name='staticBitmap1',
              parent=self, pos=wxPoint(16, 9), size=wxSize(56, 300), style=0)

        self.buttonStop = wxButton(id=wxID_WXDIALOGSTATUSBUTTONSTOP,
              label='&Stop', name='buttonStop', parent=self, pos=wxPoint(291,
              328), size=wxSize(85, 24), style=0)
        self.buttonStop.Enable(True)
        self.buttonStop.SetDefault()
        EVT_BUTTON(self.buttonStop, wxID_WXDIALOGSTATUSBUTTONSTOP,
              self.OnButtonStop)

        self.buttonSave = wxButton(id=wxID_WXDIALOGSTATUSBUTTONSAVE,
              label='S&ave Report', name='buttonSave', parent=self,
              pos=wxPoint(192, 328), size=wxSize(86, 24), style=0)
        self.buttonSave.Enable(False)
        EVT_BUTTON(self.buttonSave, wxID_WXDIALOGSTATUSBUTTONSAVE,
              self.OnButtonSave)

    def __init__(self, parent, cmd=None, logfile=None, priority='n', bitmapMask=""):
        self._autoClose = False
        self._cancelled = False
        self._logfile = logfile
        self.returnCode = -1
        self.terminating = False       
        self._out = None
        self._proc = None 
        
        self._init_ctrls(parent)
        
        EVT_THREADFINISHED(self, self.OnThreadFinished)        
        EVT_THREADUPDATESTATUS(self, self.OnThreadUpdateStatus)        
        
         # set window icons
        icons = wxIconBundle()
        icons.AddIconFromFile('img/FrameIcon.ico', wxBITMAP_TYPE_ICO)
        self.SetIcons(icons)        

        # change colour of read-only controls (gray)
        self.textCtrlStatus.SetBackgroundColour(wxSystemSettings_GetColour(wxSYS_COLOUR_BTNFACE))

        # initilaise our throbber (an awkward way to display animated images)
        images = [throbImages.catalog[i].getBitmap()
                  for i in throbImages.index
                  if i.find(bitmapMask) != -1]

        self.throbber = Throbber(self, -1, images, frameDelay=0.1,
              pos=self.staticBitmap1.GetPosition(), size=self.staticBitmap1.GetSize(),
              style=self.staticBitmap1.GetWindowStyleFlag(), name='staticThrobber')
        self.throbber.Start()
        
        # spawn and monitor our process
        try:
            self._SpawnProcess(cmd, priority)            
        except Process.ProcessError, e:
            event = ThreadUpdateStatusEvent(self.GetId(), str(e), False)                         
            self.GetEventHandler().AddPendingEvent(event)                 
            event = ThreadFinishedEvent(self.GetId()) 
            self.GetEventHandler().AddPendingEvent(event)                             
        
    def SetAutoClose(self, autoClose):
        self._autoClose = autoClose

    
    def OnWxDialogStatusClose(self, event):          
         self.terminating = True         
         self._StopProcess()            
         if self._logfile is not None:
             try:
                 os.remove(self._logfile)
             except Exception, e:
                 print 'could not delete logfile : %s. Error: %s' % (self._logfile, str(e))                 
         event.Skip()
    
    def _IsProcessRunning(self, wait=False):
        if self._proc is None:
            return False
        
        if wait:
            timeout = _WAIT_TIMEOUT
        else:
            timeout = _WAIT_NOWAIT
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
            # terminate process and use KILL_SIGNAL to terminate gracefully
            # do not wait too long for the process to finish                
            self._proc.kill(sig=_KILL_SIGNAL)
            
            #wait to finish
            if self._IsProcessRunning(True):       
                # still running, huh
                # kill unconditionally
                try:
                    self._proc.kill()
                except Process.ProcessError:
                    pass                               
                
                # last resort if failed to kill the process
                if self._IsProcessRunning():       
                    MsgBox.ErrorBox(self, 'Unable to stop runner thread, terminating')
                    os._exit(0)      
                    
            self._proc.close()
            self._out.close()                                                    
                
    def OnButtonStop(self, event):      
        if self._IsProcessRunning():           
            self._cancelled = True 
            self._StopProcess()            
        else:
            self.Close()                    

    def OnButtonSave(self, event):
        filename = "clamav_report_" + time.strftime("%d%m%y_%H%M%S")
        if sys.platform.startswith("win"):
            filename +=  ".txt"
            mask = "Report files (*.txt)|*.txt|All files (*.*)|*.*"
        else:            
            mask = "All files (*)|*"
        dlg = wxFileDialog(self, "Choose a file", ".", filename, mask, wxSAVE)
        try:
            if dlg.ShowModal() == wxID_OK:
                filename = dlg.GetPath()
                try:
                    file(filename, "w").write(self.textCtrlStatus.GetLabel())
                except:
                    dlg = wxMessageDialog(self, 'Could not save report to the file ' + \
                                            filename + ". Please check that you have write "
                                            "permissions to the folder and there is enough space on the disk.",
                      'ClamWin', wxOK | wxICON_ERROR)
                    try:
                        dlg.ShowModal()
                    finally:
                        dlg.Destroy()
        finally:
            dlg.Destroy()
            
            
    def ThreadFinished(owner):    
        if owner.terminating:            
            return
        event = ThreadFinishedEvent(owner.GetId()) 
        owner.GetEventHandler().AddPendingEvent(event)                 
    ThreadFinished = staticmethod(ThreadFinished)
    
    def ThreadUpdateStatus(owner, text, append=True):
        if owner.terminating:            
            return
        event = ThreadUpdateStatusEvent(owner.GetId(), text, append)             
        owner.GetEventHandler().AddPendingEvent(event)                    
    ThreadUpdateStatus = staticmethod(ThreadUpdateStatus)
    
    def OnThreadFinished(self, event):
        self.buttonSave.Enable(True)
        self.throbber.Stop()
        self.buttonStop.SetFocus()
        self.buttonStop.SetLabel('&Close')                   
                
       
        data = ''
        if self._logfile is not None:
            try:
                data = file(self._logfile, 'rt').read()
            except Exception, e:
                print 'Could not read from log file %s. Error: %s' % (self._logfile, str(e))
        if data:
            self.ThreadUpdateStatus(self, data, False)
        
        if not self._cancelled:    
           self.ThreadUpdateStatus(self, "\n-------------------\nCompleted\n-------------------\n")                  
        else:
            self.ThreadUpdateStatus(self, "\n-------------------\nCommand has been interrupted...\n-------------------\n")        
        
        try:                
            self._returnCode = self._proc.wait(_TIMEOUT)
        except:
            self._returnCode = -1
            
        if self.returnCode != 0:
            i = 0
            while i < 3:
                wxBell()
                time.sleep(0.3)
                i+=1                        
        
        # close the window automatically if requested
        if self._autoClose:             
            time.sleep(0)
            e = wxCommandEvent(wxEVT_COMMAND_BUTTON_CLICKED, self.buttonStop.GetId())
            self.buttonStop.AddPendingEvent(e)                                
                    
    def OnThreadUpdateStatus(self, event):
        ctrl = self.textCtrlStatus     
        text = event.text           
        if event.append == True:
            
            # Check if we reached 30000 characters
            # and need to purge topmost line           
            if ctrl.GetLastPosition() + len(text) + _NEWLINE_LEN >= 30000:
                ctrl.Clear()
            
            line_number = ctrl.GetNumberOfLines() - 2
            # detect progress message in the new text
            progress_markers = ['[|]', '[/]', '[-]', '[\]', '[*]']
            print_over = False
            # check if the current line contains progress marker
            for marker in progress_markers:
                if text.find(marker) != -1:
                    print_over = True                    
                    break
            if print_over:
                print_over = False
                # check if we need to overwrite last line
                # (it contains progress marker)
                last_line_text = ctrl.GetLineText(line_number)                
                for marker in progress_markers:
                    if last_line_text.find(marker) != -1:
                        print_over = True
                        break            
            if print_over:
                line_end = ctrl.GetLastPosition()
                line_start = ctrl.GetLastPosition() - \
                                ctrl.GetLineLength(line_number) - _NEWLINE_LEN                                                
                ctrl.Remove(line_start, line_end)

            ctrl.AppendText(text)
        else:
            ctrl.SetValue(text)    
        
    def GetExitCode(self):
        return self._returnCode 
   
    def _SpawnProcess(self, cmd, priority):
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
            self._out = StatusUpdateBuffer(self, self.ThreadUpdateStatus, self.ThreadFinished)                                                    
            self._proc = Process.ProcessProxy(cmd, stdout=self._out, priority=priority)                                                                
            self._proc.wait(_WAIT_NOWAIT)
        except Exception, e:             
            if isinstance(e, Process.ProcessError):
                if e.errno != Process.ProcessProxy.WAIT_TIMEOUT:                                       
                    raise Process.ProcessError('Could not start process:\n%s\nError: %s' % (cmd, str(e)))                     
            else:
                raise Process.ProcessError('Could not start process:\n%s\nError: %s' % (cmd, str(e)))
                    	                	    
