#-----------------------------------------------------------------------------
#Boa:Frame:wxMainFrame

#-----------------------------------------------------------------------------
# Name:        wxFrameMain.py
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

import os
import sys
from wxPython.wx import *
import wxDialogPreferences
import wxDialogAbout
import wxDialogStatus

def create(parent, config):
    return wxMainFrame(parent, config)

[wxID_WXMAINFRAME, wxID_WXMAINFRAMEBUTTONCLOSE, wxID_WXMAINFRAMEBUTTONSCAN, 
 wxID_WXMAINFRAMEDIRCTRLSCAN, wxID_WXMAINFRAMEPANELFRAME, 
 wxID_WXMAINFRAMESTATIC1, wxID_WXMAINFRAMESTATUSBAR, wxID_WXMAINFRAMETOOLBAR, 
] = map(lambda _init_ctrls: wxNewId(), range(8))


[wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE, wxID_WXMAINFRAMETOOLBARTOOLS_PREFS, 
] = map(lambda _init_coll_toolBar_Tools: wxNewId(), range(2))

[wxID_WXMAINFRAMEFILEITEMS0] = map(lambda _init_coll_File_Items: wxNewId(), range(1))

[wxID_WXMAINFRAMEHELPITEMS0] = map(lambda _init_coll_Help_Items: wxNewId(), range(1))

[wxID_WXMAINFRAMETOOLSPREFERENCES] = map(lambda _init_coll_Tools_Items: wxNewId(), range(1))

class wxMainFrame(wxFrame):    
    def _init_coll_flexGridSizerPanel_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(8, 8, border=0, flag=0)
        parent.AddWindow(self.static1, 0, border=5,
              flag=wxLEFT | wxRIGHT | wxBOTTOM | wxALIGN_LEFT)
        parent.AddWindow(self.dirCtrlScan, 0, border=10,
              flag=wxLEFT | wxRIGHT | wxGROW)

    def _init_coll_flexGridSizerPanel_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(2)
        parent.AddGrowableCol(0)

    def _init_coll_gridSizerFrame_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panelFrame, 0, border=0, flag=wxGROW)

    def _init_coll_gridSizerButtons_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonScan, 0, border=10,
              flag=wxALIGN_RIGHT | wxALL)
        parent.AddWindow(self.buttonClose, 0, border=10,
              flag=wxALIGN_LEFT | wxALL)

    def _init_coll_Tools_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='Displays the configuration window',
              id=wxID_WXMAINFRAMETOOLSPREFERENCES, item='&Preferences',
              kind=wxITEM_NORMAL)
        EVT_MENU(self, wxID_WXMAINFRAMETOOLSPREFERENCES,
              self.OnToolsPreferences)

    def _init_coll_menuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.File, title='&File')
        parent.Append(menu=self.Tools, title='&Tools')
        parent.Append(menu=self.Help, title='&Help')

    def _init_coll_Help_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='Displays the  About Box',
              id=wxID_WXMAINFRAMEHELPITEMS0, item='&About', kind=wxITEM_NORMAL)
        EVT_MENU(self, wxID_WXMAINFRAMEHELPITEMS0, self.OnHelpAbout)

    def _init_coll_File_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='Exits the application',
              id=wxID_WXMAINFRAMEFILEITEMS0, item='E&xit', kind=wxITEM_NORMAL)
        EVT_MENU(self, wxID_WXMAINFRAMEFILEITEMS0, self.OnFileExit)

    def _init_coll_toolBar_Tools(self, parent):
        # generated method, don't edit
        parent.DoAddTool(bitmap=wxBitmap('img/Control.png', wxBITMAP_TYPE_PNG),
              bmpDisabled=wxNullBitmap, id=wxID_WXMAINFRAMETOOLBARTOOLS_PREFS,
              kind=wxITEM_NORMAL, label='Preferences',
              longHelp='Displays Preferences Window',
              shortHelp='Displays Preferences Window')
        parent.DoAddTool(bitmap=wxBitmap('img/World.png', wxBITMAP_TYPE_PNG),
              bmpDisabled=wxNullBitmap,
              id=wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE, kind=wxITEM_NORMAL,
              label='Update',
              longHelp='Updates virus databases over the Internet',
              shortHelp='Starts Internet Update')
        EVT_TOOL(self, wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE,
              self.OnToolsUpdate)
        EVT_TOOL(self, wxID_WXMAINFRAMETOOLBARTOOLS_PREFS,
              self.OnToolsPreferences)

        parent.Realize()

    def _init_sizers(self):
        # generated method, don't edit
        self.gridSizerFrame = wxGridSizer(cols=1, hgap=0, rows=1, vgap=0)

        self.flexGridSizerPanel = wxFlexGridSizer(cols=1, hgap=0, rows=4,
              vgap=0)

        self.gridSizerButtons = wxGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self._init_coll_gridSizerFrame_Items(self.gridSizerFrame)
        self._init_coll_flexGridSizerPanel_Items(self.flexGridSizerPanel)
        self._init_coll_flexGridSizerPanel_Growables(self.flexGridSizerPanel)
        self._init_coll_gridSizerButtons_Items(self.gridSizerButtons)

        self.SetSizer(self.gridSizerFrame)
        self.panelFrame.SetSizer(self.flexGridSizerPanel)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar = wxMenuBar()

        self.File = wxMenu(title='')

        self.Tools = wxMenu(title='')

        self.Help = wxMenu(title='')

        self._init_coll_menuBar_Menus(self.menuBar)
        self._init_coll_File_Items(self.File)
        self._init_coll_Tools_Items(self.Tools)
        self._init_coll_Help_Items(self.Help)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxFrame.__init__(self, id=wxID_WXMAINFRAME, name='wxMainFrame',
              parent=prnt, pos=wxPoint(449, 263), size=wxSize(568, 430),
              style=wxDEFAULT_FRAME_STYLE, title='ClamWin Antivirus')
        self._init_utils()
        self.SetClientSize(wxSize(560, 403))
        self.SetMenuBar(self.menuBar)
        self.SetHelpText('ClamWin Virus Scanner')
        self.Center(wxBOTH)

        self.toolBar = wxToolBar(id=wxID_WXMAINFRAMETOOLBAR, name='toolBar',
              parent=self, pos=wxPoint(0, 0), size=wxSize(560, 41),
              style=wxTB_FLAT | wxTB_HORIZONTAL | wxNO_BORDER)
        self.toolBar.SetToolTipString('')
        self.toolBar.SetToolBitmapSize(wxSize(32, 32))
        self.SetToolBar(self.toolBar)

        self.statusBar = wxStatusBar(id=wxID_WXMAINFRAMESTATUSBAR,
              name='statusBar', parent=self, style=0)
        self.statusBar.SetSize(wxSize(537, 20))
        self.statusBar.SetPosition(wxPoint(0, 218))
        self.statusBar.SetToolTipString('Status Bar')
        self.SetStatusBar(self.statusBar)

        self.panelFrame = wxPanel(id=wxID_WXMAINFRAMEPANELFRAME,
              name='panelFrame', parent=self, pos=wxPoint(0, 0),
              size=wxSize(560, 403), style=wxTAB_TRAVERSAL)

        self.static1 = wxStaticText(id=wxID_WXMAINFRAMESTATIC1,
              label='Select a folder or a file to scan:', name='static1',
              parent=self.panelFrame, pos=wxPoint(5, 8), size=wxSize(435, 14),
              style=0)

        self.dirCtrlScan = wxGenericDirCtrl(defaultFilter=0, dir='.', filter='',
              id=wxID_WXMAINFRAMEDIRCTRLSCAN, name='dirCtrlScan',
              parent=self.panelFrame, pos=wxPoint(10, 27), size=wxSize(540,
              376),
              style=wxDIRCTRL_SELECT_FIRST | wxSUNKEN_BORDER | wxDIRCTRL_3D_INTERNAL)

        self.buttonScan = wxButton(id=wxID_WXMAINFRAMEBUTTONSCAN, label='&Scan',
              name='buttonScan', parent=self.panelFrame, pos=wxPoint(-85, 10),
              size=wxSize(75, 23), style=0)
        self.buttonScan.SetDefault()
        EVT_BUTTON(self.buttonScan, wxID_WXMAINFRAMEBUTTONSCAN,
              self.OnScanButton)

        self.buttonClose = wxButton(id=wxID_WXMAINFRAMEBUTTONCLOSE,
              label='&Close', name='buttonClose', parent=self.panelFrame,
              pos=wxPoint(10, 10), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.buttonClose, wxID_WXMAINFRAMEBUTTONCLOSE,
              self.OnButtonClose)

        self._init_coll_toolBar_Tools(self.toolBar)

        ##self._init_sizers()

    def __init__(self, parent, config):
        self.config = None
        self.config = config


        self._init_ctrls(parent)

        # we need to set controls heights to 0 and reinit sizers
        # to overcome boa sizers bug
        self.dirCtrlScan.SetSize((-1, 0))
        self.panelFrame.SetSize((-1, 0))        
        self._init_sizers()
        self.flexGridSizerPanel.AddSizer(self.gridSizerButtons, flag = wxGROW)

        # set window icons
        icons = wxIconBundle()
        icons.AddIconFromFile('img/FrameIcon.ico', wxBITMAP_TYPE_ICO)
        self.SetIcons(icons)
        
        self._UpdateState()

    def OnFileExit(self, event):
        self.Close()

    def OnToolsPreferences(self, event):
        wxDialogPreferences.Configure(self, self.config)        
        self._UpdateState()

    def OnHelpAbout(self, event):
        dlg = wxDialogAbout.create(self, self.config)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def _IsConfigured(self):
        if self.config.Get('ClamAV', 'ClamScan') == '' or \
            self.config.Get('ClamAV', 'FreshClam') == '' or \
            self.config.Get('ClamAV', 'Database') == '' :
            return False
        else:
            return True


    def _UpdateState(self):
        # disable Run Command button if the configuration is invalid
        enabled = self._IsConfigured()        
        self.buttonScan.Enable(enabled)
        self.toolBar.EnableTool(wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE, enabled)    

    def OnScanButton(self, event):
        path = self.dirCtrlScan.GetPath().replace('\\', '/').rstrip('/')
        wxDialogStatus.Scan(self, self.config, path)        

    def OnToolsUpdate(self, event):
        wxDialogStatus.UpdateVirDB(self, self.config)

    def OnButtonClose(self, event):
        self.Close()

