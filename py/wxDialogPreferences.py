#-----------------------------------------------------------------------------
#Boa:Dialog:wxPreferencesDlg

#-----------------------------------------------------------------------------
# Name:        wxDialogPreferences.py
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
from wxPython.lib.intctrl import *
from wxPython.lib.timectrl import *
import MsgBox
import sys

def create(parent, config=None):
    return wxPreferencesDlg(parent, config)

def Configure(parent, config):
    dlg = create(parent, config)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()            
        

[wxID_WXPREFERENCESDLG, wxID_WXPREFERENCESDLGBUTTONBROWSECLAMSCAN, 
 wxID_WXPREFERENCESDLGBUTTONBROWSEFRESHCLAM, 
 wxID_WXPREFERENCESDLGBUTTONCANCEL, wxID_WXPREFERENCESDLGBUTTONOK, 
 wxID_WXPREFERENCESDLGBUTTONVIRDB, 
 wxID_WXPREFERENCESDLGCHECKBOXENABLEAUTOUPDATE, 
 wxID_WXPREFERENCESDLGCHECKBOXREMOVE, 
 wxID_WXPREFERENCESDLGCHECKBOXSCANRECURSIVE, wxID_WXPREFERENCESDLGCHOICEDAY, 
 wxID_WXPREFERENCESDLGCHOICEPRIORITY, 
 wxID_WXPREFERENCESDLGCHOICEUPDATEFREQUENCY, wxID_WXPREFERENCESDLGINTCTRLPORT, 
 wxID_WXPREFERENCESDLGNOTEBOOK, wxID_WXPREFERENCESDLGSPINBUTTONTIME, 
 wxID_WXPREFERENCESDLGSTATICBOXSCANOPTIONS, 
 wxID_WXPREFERENCESDLGSTATICLINETIMECTRL, 
 wxID_WXPREFERENCESDLGSTATICTEXTCLAMSCAN, wxID_WXPREFERENCESDLGSTATICTEXTDAY, 
 wxID_WXPREFERENCESDLGSTATICTEXTEXPLAIN, 
 wxID_WXPREFERENCESDLGSTATICTEXTFRESHCLAM, 
 wxID_WXPREFERENCESDLGSTATICTEXTPASSWORD, wxID_WXPREFERENCESDLGSTATICTEXTPORT, 
 wxID_WXPREFERENCESDLGSTATICTEXTPRIORITY, 
 wxID_WXPREFERENCESDLGSTATICTEXTPROXY, wxID_WXPREFERENCESDLGSTATICTEXTTIME, 
 wxID_WXPREFERENCESDLGSTATICTEXTUPDATEFREQUENCY, 
 wxID_WXPREFERENCESDLGSTATICTEXTUSER, wxID_WXPREFERENCESDLGSTATICTEXTVIRDB, 
 wxID_WXPREFERENCESDLGTEXTCTRLCLAMSCAN, 
 wxID_WXPREFERENCESDLGTEXTCTRLFRESHCLAM, 
 wxID_WXPREFERENCESDLGTEXTCTRLPASSWORD, wxID_WXPREFERENCESDLGTEXTCTRLPROXY, 
 wxID_WXPREFERENCESDLGTEXTCTRLUSER, wxID_WXPREFERENCESDLGTEXTCTRLVIRDB, 
 wxID_WXPREFERENCESDLG_PANELFILES, wxID_WXPREFERENCESDLG_PANELINTERNETUPDATE, 
 wxID_WXPREFERENCESDLG_PANELOPTIONS, wxID_WXPREFERENCESDLG_PANELPROXY, 
] = map(lambda _init_ctrls: wxNewId(), range(39))

class wxPreferencesDlg(wxDialog):
    def _init_coll_notebook_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self._panelOptions, select=True,
              text='General')
        parent.AddPage(imageId=-1, page=self._panelInternetUpdate, select=False,
              text='Internet Updates')
        parent.AddPage(imageId=-1, page=self._panelProxy, select=False,
              text='Proxy Settings')
        parent.AddPage(imageId=-1, page=self._panelFiles, select=False,
              text='File Locations')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxDialog.__init__(self, id=wxID_WXPREFERENCESDLG, name='', parent=prnt,
              pos=wxPoint(523, 330), size=wxSize(419, 271),
              style=wxDEFAULT_DIALOG_STYLE, title='ClamWin Preferences')
        self.SetClientSize(wxSize(411, 244))
        self.SetAutoLayout(False)
        self.Center(wxBOTH)
        EVT_CHAR_HOOK(self, self.OnCharHook)

        self.notebook = wxNotebook(id=wxID_WXPREFERENCESDLGNOTEBOOK,
              name='notebook', parent=self, pos=wxPoint(7, 7), size=wxSize(398,
              198), style=0)
        self.notebook.SetAutoLayout(true)
        self.notebook.SetToolTipString('')

        self.buttonOK = wxButton(id=wxID_WXPREFERENCESDLGBUTTONOK, label='OK',
              name='buttonOK', parent=self, pos=wxPoint(132, 213),
              size=wxSize(72, 23), style=0)
        self.buttonOK.SetToolTipString('Closes the window and saves the changes')
        self.buttonOK.SetDefault()
        EVT_BUTTON(self.buttonOK, wxID_WXPREFERENCESDLGBUTTONOK, self.OnOK)

        self.buttonCancel = wxButton(id=wxID_WXPREFERENCESDLGBUTTONCANCEL,
              label='Cancel', name='buttonCancel', parent=self, pos=wxPoint(213,
              213), size=wxSize(75, 23), style=0)
        self.buttonCancel.SetToolTipString('Closes the window without saving the changes')
        EVT_BUTTON(self.buttonCancel, wxID_WXPREFERENCESDLGBUTTONCANCEL,
              self.OnCancel)

        self._panelOptions = wxPanel(id=wxID_WXPREFERENCESDLG_PANELOPTIONS,
              name='_panelOptions', parent=self.notebook, pos=wxPoint(0, 0),
              size=wxSize(390, 172), style=wxTAB_TRAVERSAL)
        self._panelOptions.SetToolTipString('')
        self._panelOptions.SetAutoLayout(False)

        self._panelProxy = wxPanel(id=wxID_WXPREFERENCESDLG_PANELPROXY,
              name='_panelProxy', parent=self.notebook, pos=wxPoint(0, 0),
              size=wxSize(390, 172), style=wxTAB_TRAVERSAL)
        self._panelProxy.SetToolTipString('')
        self._panelProxy.SetAutoLayout(False)

        self._panelInternetUpdate = wxPanel(id=wxID_WXPREFERENCESDLG_PANELINTERNETUPDATE,
              name='_panelInternetUpdate', parent=self.notebook, pos=wxPoint(0,
              0), size=wxSize(390, 172), style=wxTAB_TRAVERSAL)
        self._panelInternetUpdate.SetAutoLayout(False)

        self._panelFiles = wxPanel(id=wxID_WXPREFERENCESDLG_PANELFILES,
              name='_panelFiles', parent=self.notebook, pos=wxPoint(0, 0),
              size=wxSize(390, 172), style=wxTAB_TRAVERSAL)
        self._panelFiles.SetAutoLayout(False)

        self.staticTextProxy = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTPROXY,
              label='Proxy &Server:', name='staticTextProxy',
              parent=self._panelProxy, pos=wxPoint(6, 52), size=wxSize(80, 15),
              style=0)

        self.textCtrlProxy = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLPROXY,
              name='textCtrlProxy', parent=self._panelProxy, pos=wxPoint(91,
              48), size=wxSize(199, 21), style=0, value='')
        self.textCtrlProxy.SetToolTipString('Proxy Server domain name or IP address')

        self.staticTextPort = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTPORT,
              label='P&ort:', name='staticTextPort', parent=self._panelProxy,
              pos=wxPoint(296, 52), size=wxSize(34, 15), style=0)

        self.intCtrlPort = wxIntCtrl(allow_long=False, allow_none=False,
              default_color=wxBLACK, id=wxID_WXPREFERENCESDLGINTCTRLPORT,
              limited=False, max=65535, min=0, name='intCtrlPort',
              oob_color=wxRED, parent=self._panelProxy, pos=wxPoint(332, 48),
              size=wxSize(54, 21), style=0, value=3128)
        self.intCtrlPort.SetBounds((0, 65535))
        self.intCtrlPort.SetToolTipString('Proxy Server port number (0-65535)')

        self.staticTextUser = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTUSER,
              label='&User Name:', name='staticTextUser',
              parent=self._panelProxy, pos=wxPoint(6, 88), size=wxSize(80, 15),
              style=0)

        self.textCtrlUser = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLUSER,
              name='textCtrlUser', parent=self._panelProxy, pos=wxPoint(91, 84),
              size=wxSize(295, 21), style=0, value='')
        self.textCtrlUser.SetToolTipString('Proxy Server Account Name (optional)')

        self.staticTextPassword = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTPASSWORD,
              label='&Password:', name='staticTextPassword',
              parent=self._panelProxy, pos=wxPoint(6, 126), size=wxSize(80, 15),
              style=0)

        self.textCtrlPassword = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLPASSWORD,
              name='textCtrlPassword', parent=self._panelProxy, pos=wxPoint(91,
              122), size=wxSize(295, 21), style=wxTE_PASSWORD, value='')
        self.textCtrlPassword.SetToolTipString('Proxy Server account password (optional)')

        self.staticTextExplain = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTEXPLAIN,
              label='Leave these fields blank if you do not connect via Proxy Server',
              name='staticTextExplain', parent=self._panelProxy, pos=wxPoint(6,
              15), size=wxSize(378, 27), style=0)
        self.staticTextExplain.SetToolTipString('')

        self.checkBoxRemove = wxCheckBox(id=wxID_WXPREFERENCESDLGCHECKBOXREMOVE,
              label='&Remove Infected Files', name='checkBoxRemove',
              parent=self._panelOptions, pos=wxPoint(23, 42), size=wxSize(354,
              16), style=0)
        self.checkBoxRemove.SetToolTipString('Select if you wish to remove infected files automatically')

        self.checkBoxScanRecursive = wxCheckBox(id=wxID_WXPREFERENCESDLGCHECKBOXSCANRECURSIVE,
              label='&Scan In Subdirectories', name='checkBoxScanRecursive',
              parent=self._panelOptions, pos=wxPoint(23, 68), size=wxSize(354,
              15), style=0)
        self.checkBoxScanRecursive.SetToolTipString('Select if you wish to scan in subdirectories recursively')

        self.checkBoxEnableAutoUpdate = wxCheckBox(id=wxID_WXPREFERENCESDLGCHECKBOXENABLEAUTOUPDATE,
              label='&Enable Automatic Virus Database Updates',
              name='checkBoxEnableAutoUpdate', parent=self._panelInternetUpdate,
              pos=wxPoint(6, 15), size=wxSize(322, 20), style=0)
        self.checkBoxEnableAutoUpdate.SetToolTipString('Enable automatic virus database downloads ')
        EVT_CHECKBOX(self.checkBoxEnableAutoUpdate,
              wxID_WXPREFERENCESDLGCHECKBOXENABLEAUTOUPDATE,
              self.OnCheckBoxEnableAutoUpdate)

        self.staticTextDay = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTDAY,
              label='&Day Of The Week:', name='staticTextDay',
              parent=self._panelInternetUpdate, pos=wxPoint(23, 110),
              size=wxSize(123, 18), style=0)
        self.staticTextDay.SetToolTipString('')

        self.choiceDay = wxChoice(choices=['Monday', 'Tuesday', 'Wednesday',
              'Thursday', 'Friday', 'Saturday', 'Sunday'],
              id=wxID_WXPREFERENCESDLGCHOICEDAY, name='choiceDay',
              parent=self._panelInternetUpdate, pos=wxPoint(154, 107),
              size=wxSize(107, 21), style=0)
        self.choiceDay.SetColumns(2)
        self.choiceDay.SetToolTipString('When update frequency is weekly select day of the week for an update')
        self.choiceDay.SetStringSelection('Tuesday')
        EVT_CHOICE(self.choiceDay, wxID_WXPREFERENCESDLGCHOICEDAY,
              self.OnChoiceDayChoice)

        self.staticTextTime = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTTIME,
              label='&Time:', name='staticTextTime',
              parent=self._panelInternetUpdate, pos=wxPoint(23, 77),
              size=wxSize(123, 18), style=0)

        self.staticLineTimeCtrl = wxStaticLine(id=wxID_WXPREFERENCESDLGSTATICLINETIMECTRL,
              name='staticLineTimeCtrl', parent=self._panelInternetUpdate,
              pos=wxPoint(154, 75), size=wxSize(90, 22), style=0)
        self.staticLineTimeCtrl.Show(False)
        self.staticLineTimeCtrl.SetToolTipString('When the download should be started')

        self.spinButtonTime = wxSpinButton(id=wxID_WXPREFERENCESDLGSPINBUTTONTIME,
              name='spinButtonTime', parent=self._panelInternetUpdate,
              pos=wxPoint(244, 74), size=wxSize(16, 22),
              style=wxSP_ARROW_KEYS | wxSP_VERTICAL)
        self.spinButtonTime.SetToolTipString('')

        self.staticTextClamScan = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTCLAMSCAN,
              label='&ClamScan Location:', name='staticTextClamScan',
              parent=self._panelFiles, pos=wxPoint(6, 15), size=wxSize(354, 13),
              style=0)
        self.staticTextClamScan.SetToolTipString('')

        self.textCtrlClamScan = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLCLAMSCAN,
              name='textCtrlClamScan', parent=self._panelFiles, pos=wxPoint(6,
              33), size=wxSize(356, 20), style=0, value='')
        self.textCtrlClamScan.SetToolTipString('Specify location of clamscan')

        self.buttonBrowseClamScan = wxButton(id=wxID_WXPREFERENCESDLGBUTTONBROWSECLAMSCAN,
              label='...', name='buttonBrowseClamScan', parent=self._panelFiles,
              pos=wxPoint(363, 34), size=wxSize(20, 20), style=0)
        self.buttonBrowseClamScan.SetToolTipString('Click to browse for clamscan')
        EVT_BUTTON(self.buttonBrowseClamScan,
              wxID_WXPREFERENCESDLGBUTTONBROWSECLAMSCAN,
              self.OnButtonBrowseClamScan)

        self.textCtrlFreshClam = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLFRESHCLAM,
              name='textCtrlFreshClam', parent=self._panelFiles, pos=wxPoint(6,
              80), size=wxSize(355, 20), style=0, value='')
        self.textCtrlFreshClam.SetToolTipString('Specify location of freshclam')

        self.staticTextFreshClam = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTFRESHCLAM,
              label='&FreshClam Location:', name='staticTextFreshClam',
              parent=self._panelFiles, pos=wxPoint(6, 62), size=wxSize(354, 13),
              style=0)
        self.staticTextFreshClam.SetToolTipString('')

        self.buttonBrowseFreshClam = wxButton(id=wxID_WXPREFERENCESDLGBUTTONBROWSEFRESHCLAM,
              label='...', name='buttonBrowseFreshClam',
              parent=self._panelFiles, pos=wxPoint(363, 80), size=wxSize(20,
              20), style=0)
        self.buttonBrowseFreshClam.SetToolTipString('Click to browse for freshclam')
        EVT_BUTTON(self.buttonBrowseFreshClam,
              wxID_WXPREFERENCESDLGBUTTONBROWSEFRESHCLAM,
              self.OnButtonBrowseFreshClam)

        self.staticTextVirDB = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTVIRDB,
              label='&Virus Database Folder:', name='staticTextVirDB',
              parent=self._panelFiles, pos=wxPoint(6, 109), size=wxSize(354,
              13), style=0)
        self.staticTextVirDB.SetToolTipString('')

        self.textCtrlVirDB = wxTextCtrl(id=wxID_WXPREFERENCESDLGTEXTCTRLVIRDB,
              name='textCtrlVirDB', parent=self._panelFiles, pos=wxPoint(6,
              127), size=wxSize(355, 20), style=0, value='')
        self.textCtrlVirDB.SetToolTipString('Specify location of freshclam')

        self.buttonVirDB = wxButton(id=wxID_WXPREFERENCESDLGBUTTONVIRDB,
              label='...', name='buttonVirDB', parent=self._panelFiles,
              pos=wxPoint(362, 127), size=wxSize(20, 20), style=0)
        self.buttonVirDB.SetToolTipString('Click to browse for freshclam')
        EVT_BUTTON(self.buttonVirDB, wxID_WXPREFERENCESDLGBUTTONVIRDB,
              self.OnButtonBrowseVirDB)

        self.staticBoxScanOptions = wxStaticBox(id=wxID_WXPREFERENCESDLGSTATICBOXSCANOPTIONS,
              label='Scan Options', name='staticBoxScanOptions',
              parent=self._panelOptions, pos=wxPoint(6, 15), size=wxSize(380,
              136), style=0)

        self.staticTextPriority = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTPRIORITY,
              label='Scanner &Priority', name='staticTextPriority',
              parent=self._panelOptions, pos=wxPoint(25, 93), size=wxSize(128,
              15), style=0)

        self.choicePriority = wxChoice(choices=['Low', 'Normal', 'High'],
              id=wxID_WXPREFERENCESDLGCHOICEPRIORITY, name='choicePriority',
              parent=self._panelOptions, pos=wxPoint(27, 112), size=wxSize(125,
              21), style=0)
        self.choicePriority.SetToolTipString('Specify the process priority for the virus scanner.')
        self.choicePriority.SetStringSelection('Normal')
        self.choicePriority.SetLabel('')

        self.staticTextUpdateFrequency = wxStaticText(id=wxID_WXPREFERENCESDLGSTATICTEXTUPDATEFREQUENCY,
              label='&Update Frequency:', name='staticTextUpdateFrequency',
              parent=self._panelInternetUpdate, pos=wxPoint(23, 46),
              size=wxSize(123, 18), style=0)
        self.staticTextUpdateFrequency.SetToolTipString('')

        self.choiceUpdateFrequency = wxChoice(choices=['Hourly', 'Daily',
              'Workdays', 'Weekly'],
              id=wxID_WXPREFERENCESDLGCHOICEUPDATEFREQUENCY,
              name='choiceUpdateFrequency', parent=self._panelInternetUpdate,
              pos=wxPoint(154, 43), size=wxSize(107, 21), style=0)
        self.choiceUpdateFrequency.SetColumns(2)
        self.choiceUpdateFrequency.SetToolTipString('How often virus database is downloaded')
        self.choiceUpdateFrequency.SetStringSelection('Daily')
        EVT_CHOICE(self.choiceUpdateFrequency,
              wxID_WXPREFERENCESDLGCHOICEUPDATEFREQUENCY,
              self.OnChoiceUpdateFrequency)

        self._init_coll_notebook_Pages(self.notebook)

    def __init__(self, parent, config):
        self.config = None
        self.config = config
        
        self._init_ctrls(parent) 
        
        init_pages = [self._OptionsPageInit, self._InternetUpdatePageInit, 
                        self._ProxyPageInit, self._FilesPageInit]
        if not sys.platform.startswith("win"):        
            # remove internet updates page on unix
            init_pages.remove(self._InternetUpdatePageInit)
            self.notebook.RemovePage(1)
            
            # hide process priority control on Unix
            self.choicePriority.Show(False)
            self.staticTextPriority.Show(False)
            
        for init_page in init_pages:
            init_page()
            
        for i in range(0, self.notebook.GetPageCount()):
            self.notebook.GetPage(i).TransferDataToWindow()
        self._EnableInternetUpdateControls()

        
    def _EnableInternetUpdateControls(self):
        if sys.platform.startswith("win"):
            enable = self.checkBoxEnableAutoUpdate.GetValue() == 1    
            self.choiceDay.Enable(enable and self.choiceUpdateFrequency.GetStringSelection() == 'Weekly')
            self.choiceUpdateFrequency.Enable(enable)
            self.time.Enable(enable)
            self.spinButtonTime.Enable(enable)
                    


    def OnCancel(self, event):
        self.EndModal(wxID_CANCEL)

    def OnOK(self, event):  
        if self._Apply():
            self.EndModal(wxID_OK)


    def _Apply(self):                       
            pages = range(0, self.notebook.GetPageCount())
            # rearrange pages in order to validate the current one first
    	    for page in pages:    	        
    	        if self.notebook.GetSelection() == page:
    	            tmp = pages[0]
                    pages[0] = pages[page]
                    pages[page] = tmp
                    
            # validate and apply each page
            for page in pages:
    	        if not self.notebook.GetPage(page).Validate():
    	            # activate the invalid page
    	            self.notebook.SetSelection(page)
    	            return False
    	        self.notebook.GetPage(page).TransferDataFromWindow()
    	        
    	    # save config to properties file    
            if not self.config.Write():
                MsgBox.ErrorBox(self, 'An error occured whilst saving configuration file.')
                return False
            return True

    def _OptionsPageInit(self):        
        self.choicePriority.SetValidator(MyValidator(config=self.config, section='ClamAV', value='Priority', default='Normal'))
        self.checkBoxRemove.SetValidator(MyValidator(config=self.config, section='ClamAV', value='RemoveInfected', default='0'))
        self.checkBoxScanRecursive.SetValidator(MyValidator(config=self.config, section='ClamAV', value='ScanRecursive', default='1'))

    def _InternetUpdatePageInit(self):
        self.time = wxTimeCtrl(parent=self._panelInternetUpdate, pos=self.staticLineTimeCtrl.GetPosition(), size=self.staticLineTimeCtrl.GetSize(), fmt24hr=True)
        self.time.SetToolTipString(self.staticLineTimeCtrl.GetToolTip().GetTip())
        self.time.BindSpinButton(self.spinButtonTime)            
        self.checkBoxEnableAutoUpdate.SetValidator(MyValidator(config=self.config, section='Updates', value='Enable', default='1'))
        self.choiceUpdateFrequency.SetValidator(MyValidator(config=self.config, section='Updates', value='Frequency', default='Daily'))        
        self.time.SetValidator(MyValidator(config=self.config, section='Updates', value='Time', default='10:00:00'))
        self.choiceDay.SetValidator(MyWeekDayValidator(config=self.config, section='Updates', value='WeekDay', default='2'))
    
    def _ProxyPageInit(self):        
        self.textCtrlProxy.SetValidator(MyValidator(config=self.config, section='Proxy', value='Host'))        
        self.intCtrlPort.SetValidator(MyValidator(config=self.config, section='Proxy', value='Port'))        
        self.textCtrlUser.SetValidator(MyValidator(config=self.config, section='Proxy', value='User'))        
        self.textCtrlPassword.SetValidator(MyValidator(config=self.config, section='Proxy', value='Password'))             

    def _FilesPageInit(self):
        self.textCtrlClamScan.SetValidator(MyValidator(config=self.config, section='ClamAV', value='ClamScan', canEmpty=False))  
        self.textCtrlFreshClam.SetValidator(MyValidator(self.config, section='ClamAV', value='FreshClam', canEmpty=False))        
        self.textCtrlVirDB.SetValidator(MyValidator(self.config, section='ClamAV', value='Database', canEmpty=False))        
        

    def OnCharHook(self, event):
        if event.GetKeyCode() == WXK_ESCAPE:
            self.EndModal(wxID_CANCEL)
        else:
            event.Skip()   
        
   
    def OnButtonBrowseFreshClam(self, event):
        if sys.platform.startswith("win"):
            filename = 'freshclam.exe'
            mask = "Executable files (*.exe)|*.exe|All files (*.*)|*.*"
        else:
            filename = 'freshclam'
            mask = "All files (*)|*"
        dlg = wxFileDialog(self, "Choose a file", ".", filename, mask, wxOPEN)
        try:
            if dlg.ShowModal() == wxID_OK:
                filename = dlg.GetPath()                 
            self.textCtrlFreshClam.Clear()
            self.textCtrlFreshClam.WriteText(filename)   
        finally:
            dlg.Destroy()
            
    def OnButtonBrowseClamScan(self, event):
        if sys.platform.startswith("win"):
            filename = 'clamscan.exe'
            mask = "Executable files (*.exe)|*.exe|All files (*.*)|*.*"
        else:
            filename = 'clamscan'
            mask = "All files (*)|*"
        dlg = wxFileDialog(self, "Choose a file", ".", filename, mask, wxOPEN)
        try:
            if dlg.ShowModal() == wxID_OK:
                filename = dlg.GetPath()  
                self.textCtrlClamScan.Clear()
                self.textCtrlClamScan.WriteText(filename)   
        finally:
            dlg.Destroy()

    def OnButtonBrowseVirDB(self, event):
        dlg = wxDirDialog(self)
        try:
            if dlg.ShowModal() == wxID_OK:
                dir = dlg.GetPath()                            
                self.textCtrlVirDB.Clear()
                self.textCtrlVirDB.WriteText(dir)   
        finally:
            dlg.Destroy()

    def OnChoiceUpdateFrequency(self, event):        
        self._EnableInternetUpdateControls()
        event.Skip()

    def OnCheckBoxEnableAutoUpdate(self, event):
        self._EnableInternetUpdateControls()
        event.Skip()

    def OnChoiceDayChoice(self, event):
        event.Skip()


class MyWeekDayValidator(wxPyValidator):
     def __init__(self, config, section, value, default=''):         
         wxPyValidator.__init__(self)         
         self._config = config
         self._section = section
         self._value = value       
         self._default = default  
         
     def Clone(self):         
         return MyWeekDayValidator(self._config, self._section, self._value, self._default)

     def Validate(self, win):         
         return True           

     def TransferToWindow(self):
         value = self._config.Get(self._section, self._value)
         if not len(value):
             value = self._default
         ctrl = self.GetWindow()                                           
         ctrl.SetSelection(int(value))         
         return True


     def TransferFromWindow(self):
         ctrl = self.GetWindow()
         value = ctrl.GetSelection()                  
         self._config.Set(self._section, self._value, str(value)) 
            
class MyValidator(wxPyValidator):
     def __init__(self, config, section, value, default='', canEmpty=True):         
         wxPyValidator.__init__(self)         
         self._config = config
         self._section = section
         self._value = value       
         self._default = default  
         self._canEmpty = canEmpty

     def Clone(self):         
         return MyValidator(self._config, self._section, self._value, self._default, self._canEmpty)

     def Validate(self, win):         
         ctrl = self.GetWindow()
         if isinstance(ctrl, (wxIntCtrl, wxChoice, wxCheckBox)) or self._canEmpty:
             return True   
              
         text = ctrl.GetValue()
         if len(text) == 0:
             page = self.GetWindow().GetParent()
             wxMessageBox("Value cannot be empty", "ClamWin", style=wxICON_EXCLAMATION|wxOK)
             ctrl.SetBackgroundColour("yellow")
             ctrl.SetFocus()
             ctrl.Refresh()
             return False
         else:
             ctrl.SetBackgroundColour(wxSystemSettings_GetColour(wxSYS_COLOUR_WINDOW))
             ctrl.Refresh()
             return True


     def TransferToWindow(self):
         value = self._config.Get(self._section, self._value)
         ctrl = self.GetWindow()                          
         if isinstance(ctrl, (wxIntCtrl, wxCheckBox)):
             value = int(value)
         else:
             if not len(value):
                value = self._default
         if(isinstance(ctrl, wxChoice)):
             ctrl.SetStringSelection(value)
         else:
             ctrl.SetValue(value)         
         return True


     def TransferFromWindow(self):
         ctrl = self.GetWindow()
         if(isinstance(ctrl, wxChoice)):
             value = ctrl.GetStringSelection()         
         elif isinstance(ctrl, wxCheckBox):
             value = str(ctrl.GetValue())
         else:
             value = ctrl.GetValue()         
        
         self._config.Set(self._section, self._value, value)         
         return True

        
         
