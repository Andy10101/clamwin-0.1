#-----------------------------------------------------------------------------
# Name:        Addin.py
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
import sys, os
import warnings
import traceback
import _winreg

# *sigh* - this is for the binary installer, and for the sake of one line
# that is implicit anyway, I gave up
import encodings

try:
    True, False
except NameError:
    # Maintain compatibility with Python 2.2
    True, False = 1, 0
    
import locale
locale.setlocale(locale.LC_NUMERIC, "C")

    
from win32com import universal
from win32com.server.exception import COMException
from win32com.client import gencache, DispatchWithEvents, Dispatch
import pythoncom
from win32com.client import constants, getevents




# win32com generally checks the gencache is up to date (typelib hasn't
# changed, makepy hasn't changed, etc), but when frozen we dont want to
# do this - not just for perf, but because they don't always exist!
bValidateGencache = not hasattr(sys, "frozen")


# Support for COM objects we use.
gencache.EnsureModule('{00062FFF-0000-0000-C000-000000000046}', 0, 9, 0, bForDemand=True) # Outlook 9
gencache.EnsureModule('{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}', 0, 2, 1, bForDemand=True) # Office 9

# We the "Addin Designer" typelib for its constants
gencache.EnsureModule('{AC0714F2-3D04-11D1-AE7D-00A0C90F26F4}', 0, 1, 0,
                        bForDemand=True, bValidateFile=bValidateGencache)


# ... and also for its _IDTExtensibility2 vtable interface.
universal.RegisterInterfaces('{AC0714F2-3D04-11D1-AE7D-00A0C90F26F4}', 0, 1, 0, ["_IDTExtensibility2"])

class ButtonEvent:
    def OnClick(self, button, cancel):
        import win32ui # Possible, but not necessary, to use a Pythonwin GUI
        win32ui.MessageBox("Hello from Python")
        return cancel

class FolderEvent:
    def OnItemAdd(self, item):
        try:
            print "An item was added to the inbox with subject:", item.Subject
        except AttributeError:
            print "An item was added to the inbox, but it has no subject! - ", repr(item)


class OutlookAddin:
    _com_interfaces_ = ['_IDTExtensibility2']
    _public_methods_ = []
    _reg_clsctx_ = pythoncom.CLSCTX_INPROC_SERVER
    _reg_clsid_ = "{BD0BB9CD-7A10-4312-BECD-A55647377EB2}"
    _reg_progid_ = "ClamWin.OutlookAddin"
    _reg_policy_spec_ = "win32com.server.policy.EventHandlerPolicy"
    def OnConnection(self, application, connectMode, addin, custom):
        print "OnConnection", application, connectMode, addin, custom
        # ActiveExplorer may be none when started without a UI (eg, WinCE synchronisation)
        activeExplorer = application.ActiveExplorer()
        if activeExplorer is not None:
            bars = activeExplorer.CommandBars
            toolbar = bars.Item("Standard")
            item = toolbar.Controls.Add(Type=constants.msoControlButton, Temporary=True)
            # Hook events for the item
            item = self.toolbarButton = DispatchWithEvents(item, ButtonEvent)
            item.Caption="Python"
            item.TooltipText = "Click for Python"
            item.Enabled = True

        # And now, for the sake of demonstration, setup a hook for all new messages
        inbox = application.Session.GetDefaultFolder(constants.olFolderInbox)
        self.inboxItems = DispatchWithEvents(inbox.Items, FolderEvent)

    def OnDisconnection(self, mode, custom):
        print "OnDisconnection"
    def OnAddInsUpdate(self, custom):
        print "OnAddInsUpdate", custom
    def OnStartupComplete(self, custom):
        print "OnStartupComplete", custom
    def OnBeginShutdown(self, custom):
        print "OnBeginShutdown", custom

        
def _DoRegister(klass, root):
    key = _winreg.CreateKey(root,
                            "Software\\Microsoft\\Office\\Outlook\\Addins")
    subkey = _winreg.CreateKey(key, klass._reg_progid_)
    _winreg.SetValueEx(subkey, "CommandLineSafe", 0, _winreg.REG_DWORD, 0)
    _winreg.SetValueEx(subkey, "LoadBehavior", 0, _winreg.REG_DWORD, 3)
    _winreg.SetValueEx(subkey, "Description", 0, _winreg.REG_SZ, "Clam Antivirus Outlook Plugin")
    _winreg.SetValueEx(subkey, "FriendlyName", 0, _winreg.REG_SZ, "ClamWin")


# Note that Addins can be registered either in HKEY_CURRENT_USER or
# HKEY_LOCAL_MACHINE.  If the former, then:
# * Only available for the user that installed the addin.
# * Appears in the 'COM Addins' list, and can be removed by the user.
# If HKEY_LOCAL_MACHINE:
# * Available for every user who uses the machine.  This is useful for site
#   admins, so it works with "roaming profiles" as users move around.
# * Does not appear in 'COM Addins', and thus can not be disabled by the user.

# Note that if the addin is registered in both places, it acts as if it is
# only installed in HKLM - ie, does not appear in the addins list.
# For this reason, the addin can be registered in HKEY_LOCAL_MACHINE
# by executing 'regsvr32 /i:hkey_local_machine outlook_addin.dll'
# (or 'python addin.py hkey_local_machine' for source code users.
# Note to Binary Builders: You need py2exe dated 8-Dec-03+ for this to work.

# Called when "regsvr32 /i:whatever" is used.  We support 'hkey_local_machine'
def DllInstall(bInstall, cmdline):
    klass = OutlookAddin
    if bInstall and cmdline.lower().find('hkey_local_machine')>=0:
        # Unregister the old installation, if one exists.
        DllUnregisterServer()
        # Don't catch exceptions here - if it fails, the Dll registration
        # must fail.
        _DoRegister(klass, _winreg.HKEY_LOCAL_MACHINE)
        print "Registration (in HKEY_LOCAL_MACHINE) complete."

def DllRegisterServer():
    klass = OutlookAddin
    # *sigh* - we used to *also* register in HKLM, but as above, this makes
    # things work like we are *only* installed in HKLM.  Thus, we explicitly
    # remove the HKLM registration here (but it can be re-added - see the
    # notes above.)
    try:
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,
                          "Software\\Microsoft\\Office\\Outlook\\Addins\\" \
                          + klass._reg_progid_)
    except WindowsError:
        pass
    _DoRegister(klass, _winreg.HKEY_CURRENT_USER)
    print "Registration complete."

def DllUnregisterServer():
    klass = OutlookAddin
    # Try to remove the HKLM version.
    try:
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,
                          "Software\\Microsoft\\Office\\Outlook\\Addins\\" \
                          + klass._reg_progid_)
    except WindowsError:
        pass
    # and again for current user.
    try:
        _winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
                          "Software\\Microsoft\\Office\\Outlook\\Addins\\" \
                          + klass._reg_progid_)
    except WindowsError:
        pass

if __name__ == '__main__':
    # woohoo - here is a wicked hack.  If we are a frozen .EXE, then we are
    # a mini "registration" utility.  However, we still want to register the
    # DLL, *not* us.  Pretend we are frozen in that DLL.
    # NOTE: This is only needed due to problems with Inno Setup unregistering
    # our DLL the 'normal' way, but then being unable to remove the files as
    # they are in use (presumably by Inno doing the unregister!).  If this
    # problem ever goes away, so will the need for this to be frozen as
    # an executable.  In all cases other than as above, 'regsvr32 dll_name'
    # is still the preferred way of registering our binary.
    if hasattr(sys, "frozen"):
        sys.frozendllhandle = win32api.LoadLibrary("otlook_addin.dll")
        sys.frozen = "dll"
        # Without this, com registration will look at class.__module__, and
        # get all confused about the module name holding our class in the DLL
        OutlookAddin._reg_class_spec_ = "addin.OutlookAddin"
        # And continue doing the registration with our hacked environment.
    import win32com.server.register
    win32com.server.register.UseCommandLine(OutlookAddin)
    # todo - later win32all versions of  UseCommandLine support
    # finalize_register and finalize_unregister keyword args, passing the
    # functions.
    # (But DllInstall may get support in UseCommandLine later, so let's
    # wait and see)
    if "--unregister" in sys.argv:
        DllUnregisterServer()
    else:
        DllRegisterServer()
        # Support 'hkey_local_machine' on the commandline, to work in
        # the same way as 'regsvr32 /i:hkey_local_machine' does.
        # regsvr32 calls it after DllRegisterServer, (and our registration
        # logic relies on that) so we will too.
        for a in sys.argv[1:]:
            if a.lower()=='hkey_local_machine':
                DllInstall(True, 'hkey_local_machine')
        

