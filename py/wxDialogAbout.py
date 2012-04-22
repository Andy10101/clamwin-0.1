#-----------------------------------------------------------------------------
#Boa:Dialog:wxAboutDlg

#-----------------------------------------------------------------------------
# Name:        wxDialogAbout.py
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
from wxPython.lib.stattext import wxGenStaticText
from wxPython.html import *
import Process
import os

def create(parent, config):
    return wxAboutDlg(parent, config)

[wxID_WXABOUTDLG, wxID_WXABOUTDLGBUTTONOK, 
 wxID_WXABOUTDLGGENSTATICTEXTCLAMAV2, wxID_WXABOUTDLGSTATICBITMAP1, 
 wxID_WXABOUTDLGSTATICBITMAPPYTHON, wxID_WXABOUTDLGSTATICBITMAPWXPYTHON, 
 wxID_WXABOUTDLGSTATICBITMAPWXWIDGETS, wxID_WXABOUTDLGSTATICLINE1, 
 wxID_WXABOUTDLGSTATICTEXTBUILTON, wxID_WXABOUTDLGSTATICTEXTCLAMAV1, 
 wxID_WXABOUTDLGSTATICTEXTCLAMVER, wxID_WXABOUTDLGSTATICTEXTFREESW, 
 wxID_WXABOUTDLGSTATICTEXTNAME, wxID_WXABOUTDLGSTATICTEXTWINCLAMVER, 
] = map(lambda _init_ctrls: wxNewId(), range(14))


class wxAboutDlg(wxDialog):
    def _GotoInternetUrl(self, url):
        try:
            import webbrowser
        except ImportError:
            wxMessageBox('Please point your browser at: %s' % url)
        else:
            webbrowser.open(url)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxDialog.__init__(self, id=wxID_WXABOUTDLG, name='wxAboutDlg',
              parent=prnt, pos=wxPoint(398, 301), size=wxSize(386, 318),
              style=wxDEFAULT_DIALOG_STYLE, title='About ClamWin')
        self.SetClientSize(wxSize(378, 291))
        self.SetBackgroundColour(wxColour(255, 255, 255))
        self.SetAutoLayout(false)
        self.SetToolTipString('About ClamWin')
        EVT_CHAR_HOOK(self, self._OnCharHook)

        self.buttonOK = wxButton(id=wxID_WXABOUTDLGBUTTONOK, label='OK',
              name='buttonOK', parent=self, pos=wxPoint(153, 254),
              size=wxSize(71, 23), style=0)
        EVT_BUTTON(self.buttonOK, wxID_WXABOUTDLGBUTTONOK, self.OnOK)

        self.staticTextName = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTNAME,
              label='ClamWin Antivirus', name='staticTextName', parent=self,
              pos=wxPoint(106, 9), size=wxSize(140, 19), style=0)
        self.staticTextName.SetFont(wxFont(12, wxSWISS, wxNORMAL, wxBOLD,False))

        self.staticTextFreeSW = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTFREESW,
              label='This program is free software', name='staticTextFreeSW',
              parent=self, pos=wxPoint(10, 145), size=wxSize(248, 17), style=0)

        self.staticTextClamVer = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTCLAMVER,
              label='ClamAV Version gets here', name='staticTextClamVer',
              parent=self, pos=wxPoint(10, 105), size=wxSize(254, 31), style=0)

        self.staticTextBuiltOn = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTBUILTON,
              label='This program is built on:', name='staticTextBuiltOn',
              parent=self, pos=wxPoint(10, 176), size=wxSize(361, 18), style=0)

        self.staticLine1 = wxStaticLine(id=wxID_WXABOUTDLGSTATICLINE1,
              name='staticLine1', parent=self, pos=wxPoint(-2, 167),
              size=wxSize(381, 2), style=0)

        self.staticBitmap1 = wxStaticBitmap(bitmap=wxBitmap('img/Clam.png',
              wxBITMAP_TYPE_PNG), id=wxID_WXABOUTDLGSTATICBITMAP1,
              name='staticBitmap1', parent=self, pos=wxPoint(272, 44),
              size=wxSize(100, 100), style=0)
        self.staticBitmap1.SetToolTipString('Clam Antivirus Homepage')
        self.staticBitmap1.SetCursor(wxStockCursor(wxCURSOR_HAND))
        EVT_LEFT_DOWN(self.staticBitmap1, self._OnClamAVHomePage)

        self.staticBitmapPython = wxStaticBitmap(bitmap=wxBitmap('img/PythonPowered.gif',
              wxBITMAP_TYPE_GIF), id=wxID_WXABOUTDLGSTATICBITMAPPYTHON,
              name='staticBitmapPython', parent=self, pos=wxPoint(8, 199),
              size=wxSize(110, 44), style=0)
        self.staticBitmapPython.SetToolTipString('Python Homepage')
        self.staticBitmapPython.SetCursor(wxStockCursor(wxCURSOR_HAND))
        EVT_LEFT_DOWN(self.staticBitmapPython, self._OnPythonHomepage)

        self.staticBitmapWxPython = wxStaticBitmap(bitmap=wxBitmap('img/wxPyButton.png',
              wxBITMAP_TYPE_PNG), id=wxID_WXABOUTDLGSTATICBITMAPWXPYTHON,
              name='staticBitmapWxPython', parent=self, pos=wxPoint(123, 199),
              size=wxSize(99, 43), style=0)
        self.staticBitmapWxPython.SetToolTipString('wxPython Homepage')
        self.staticBitmapWxPython.SetCursor(wxStockCursor(wxCURSOR_HAND))
        EVT_LEFT_DOWN(self.staticBitmapWxPython, self._OnwxPythonHomepage)

        self.staticBitmapWxWidgets = wxStaticBitmap(bitmap=wxBitmap('img/wxWidgButton.png',
              wxBITMAP_TYPE_PNG), id=wxID_WXABOUTDLGSTATICBITMAPWXWIDGETS,
              name='staticBitmapWxWidgets', parent=self, pos=wxPoint(228, 199),
              size=wxSize(144, 43), style=0)
        self.staticBitmapWxWidgets.SetToolTipString('wxWidgets Homepage')
        self.staticBitmapWxWidgets.SetCursor(wxStockCursor(wxCURSOR_HAND))
        EVT_LEFT_DOWN(self.staticBitmapWxWidgets, self._OnwxWindowsHomepage)

        self.staticTextWinClamVer = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTWINCLAMVER,
              label='Version 0.1c', name='staticTextWinClamVer', parent=self,
              pos=wxPoint(140, 33), size=wxSize(78, 16), style=0)
        self.staticTextWinClamVer.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxBOLD,
              False))

        self.staticTextClamAV1 = wxStaticText(id=wxID_WXABOUTDLGSTATICTEXTCLAMAV1,
              label='Virus Protection is provided by:',
              name='staticTextClamAV1', parent=self, pos=wxPoint(10, 59),
              size=wxSize(180, 16), style=0)
        self.staticTextClamAV1.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxNORMAL,
              False))

        self.genStaticTextClamAV2 = wxGenStaticText(ID=wxID_WXABOUTDLGGENSTATICTEXTCLAMAV2,
              label='Clam Antivirus <www.clamav.net>',
              name='genStaticTextClamAV2', parent=self, pos=wxPoint(10, 81),
              size=wxSize(196, 16), style=0)
        self.genStaticTextClamAV2.SetForegroundColour(wxColour(0, 0, 255))
        self.genStaticTextClamAV2.SetFont(wxFont(10, wxSWISS, wxNORMAL,
              wxNORMAL, False))
        self.genStaticTextClamAV2.SetCursor(wxStockCursor(wxCURSOR_HAND))

    def __init__(self, parent,  config=None):
        self._init_ctrls(parent)
        self. config = config
        self._SetClamVersion()
        self.SetDefaultItem(self.buttonOK)
        self.buttonOK.SetDefault()
        self.staticTextClamVer.SetSize(wxSize(255, 36));

    def OnOK(self, event):
        self.EndModal(wxID_OK)

    def _OnCharHook(self, event):
        if event.GetKeyCode() == WXK_ESCAPE:
            self.EndModal(wxID_CANCEL)
        event.Skip()

    def _OnClamAVHomePage(self, event):
        self._GotoInternetUrl('http://www.clamav.net')

    def _OnPythonHomepage(self, event):
        self._GotoInternetUrl('http://www.python.org')

    def _OnwxPythonHomepage(self, event):
        self._GotoInternetUrl('http://www.wxpython.org')

    def _OnwxWindowsHomepage(self, event):
        self._GotoInternetUrl('http://www.wxwidgets.org')
        
    def _SetClamVersion(self):
        if self.config is None: 
            return
        if not os.path.exists(self.config.Get('ClamAV', 'ClamScan')):
            ver  = 'Could not locate ClamScan executable'
        else:    
            cmd = '"' + self.config.Get('ClamAV', 'ClamScan')  + '" --stdout --version'
            proc = None
            try:
                proc = Process.ProcessOpen(cmd)
                proc.wait()
                ver = proc.stdout.readline()            
            except:
                ver = 'Unable to retrieve ClamAV version'        
            if proc is not None:
                proc.close()        
        self.staticTextClamVer.SetLabel(ver)

    
            
        
