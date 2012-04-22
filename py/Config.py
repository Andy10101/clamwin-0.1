
#-----------------------------------------------------------------------------
# Name:        Config.py
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
import ConfigParser
import binascii
import sys

CONFIG_EVENT='Global\\ClamWinConfigUpdateEvent01'

class Settings(object):    
    def __init__(self, filename):        
        self._filename = filename	
        self._settings = {
        'ClamAV':
        [0, {'ClamScan': '', 'FreshClam': '', 'Database': '',
             'RemoveInfected': '0', 'ScanRecursive': '1', 'Priority': 'Normal'}],
        'Proxy':
        [0, {'Host': '', 'Port': '3128', 'User':'',
             'Password': ''}], 
        'Updates':
        [0, {'Enable': '1', 'Frequency': 'Daily', 'Time': '10:00:00', 'WeekDay': '2'}], 
        }

    def Read(self):                
        try:
            conf = ConfigParser.ConfigParser()
            conf.read(self._filename)
        except ConfigParser.Error:
            return False

        ret = True
        for sect in self._settings:
            for name in self._settings[sect][1]:
                try:                    
                    val = conf.get(section = sect, option = name)
                except ConfigParser.Error:
                    ret = False			
                else:
                    if self._settings[sect][0]: # is binary?
                        val = binascii.a2b_hex(val)
                    self._settings[sect][1][name] = val
        return ret

    def Write(self):        
        try:
            conf = ConfigParser.ConfigParser()
            for sect in self._settings:
                if not conf.has_section(sect):
                    conf.add_section(sect)
                    for name in self._settings[sect][1]:	                        
                        val = self._settings[sect][1][name]
                        if self._settings[sect][0]: # is binary?
                            val = binascii.b2a_hex(val)
                        conf.set(sect, option = name, value = val)
            conf.write(file(self._filename, 'w'))
        except ConfigParser.Error:
            return False
        else:
            if sys.platform.startswith("win"):
                import win32event, win32api
                # raise the event so other programs can reload config
                hEvent = None
                try:
                    hEvent = win32event.CreateEvent(None, True, False, CONFIG_EVENT);
                    win32event.PulseEvent(hEvent)
                    win32api.CloseHandle(hEvent)                    
                except win32api.error, e:
                    if hEvent is not None:
                        win32api.CloseHandle(hEvent)
                    print "Event Failed", str(e)
            return True

    
    def Get(self, sect, name):
        value = self._settings[sect][1][name]
        if(value is None):
            return ""
        return value
        
    
    def Set(self, sect, name, val):
        if val is None:
            val = ''
        if not self._settings.has_key(sect) or \
            not self._settings[sect][1].has_key(name):
            raise AttributeError('Internal Error. No such attribute: '+ sect + ': ' + name)
        else:
            self._settings[sect][1][name] = val
            
        