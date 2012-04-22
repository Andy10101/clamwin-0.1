//-----------------------------------------------------------------------------
// Name:        ShellExtImpl.cpp
// Product:     ClamWin Antivirus
//
// Author:      Alex Cherney [alex at cher dot id dot au]
//
// Created:     2004/19/03
// Copyright:   Copyright Alex Cherney (c) 2004
// Licence:     
//   This program is free software; you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation; either version 2 of the License, or
//   (at your option) any later version.
// 
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
// 
//   You should have received a copy of the GNU General Public License
//   along with this program; if not, write to the Free Software
//   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

//-----------------------------------------------------------------------------

#include <windows.h>
#include <tchar.h>
#include <stdio.h>
#include <shlobj.h>
#include "ShellExt.h"
#define ResultFromShort(i)  ResultFromScode(MAKE_SCODE(SEVERITY_SUCCESS, 0, (USHORT)(i)))


extern HINSTANCE	g_hmodThisDll;	// Handle to this DLL itself.

//
//  FUNCTION: CShellExt::Initialize(LPCITEMIDLIST, LPDATAOBJECT, HKEY)
//
//  PURPOSE: Called by the shell when initializing a context menu or property
//           sheet extension.
//
//  PARAMETERS:
//    pIDFolder - Specifies the parent folder
//    pDataObj  - Spefifies the set of items selected in that folder.
//    hRegKey   - Specifies the type of the focused item in the selection.
//
//  RETURN VALUE:
//
//    NOERROR in all cases.
//
//  COMMENTS:   Note that at the time this function is called, we don't know 
//              (or care) what type of shell extension is being initialized.  
//              It could be a context menu or a property sheet.
//

STDMETHODIMP CShellExt::Initialize(LPCITEMIDLIST pIDFolder,
                                   LPDATAOBJECT pDataObj,
                                   HKEY hRegKey)
{
	HRESULT hres = E_FAIL;
	STGMEDIUM medium;
	FORMATETC fmte = {CF_HDROP, NULL, DVASPECT_CONTENT, -1, TYMED_HGLOBAL};
	
	
	// Initialize can be called more than once
	if (m_pDataObj)
		m_pDataObj->Release();
	
	// duplicate the object pointer and registry handle
	if (pDataObj)
	{
		m_pDataObj = pDataObj;
		pDataObj->AddRef();
	}
	
	// use the given IDataObject to get a list of filenames (CF_HDROP)
	hres = pDataObj->GetData(&fmte, &medium);
	
	if(FAILED(hres))
		return E_FAIL;
	
	// find out how many files the user selected
	if(DragQueryFile((HDROP)medium.hGlobal, (UINT)-1, NULL, 0) == 1)
		DragQueryFile((HDROP)medium.hGlobal, 0, m_szFile, sizeof(m_szFile));
	
	::ReleaseStgMedium(&medium);
	
	return NOERROR;
}


//
//  FUNCTION: CShellExt::QueryContextMenu(HMENU, UINT, UINT, UINT, UINT)
//
//  PURPOSE: Called by the shell just before the context menu is displayed.
//           This is where you add your specific menu items.
//
//  PARAMETERS:
//    hMenu      - Handle to the context menu
//    indexMenu  - Index of where to begin inserting menu items
//    idCmdFirst - Lowest value for new menu ID's
//    idCmtLast  - Highest value for new menu ID's
//    uFlags     - Specifies the context of the menu event
//
//  RETURN VALUE:
//
//
//  COMMENTS:
//
// The menu text
STDMETHODIMP CShellExt::QueryContextMenu(HMENU hMenu,UINT indexMenu,UINT idCmdFirst,UINT idCmdLast,UINT uFlags)
{
	
	UINT			idCmd = idCmdFirst;
	HRESULT		hr = E_INVALIDARG;
	
	// Seperator
	::InsertMenu(hMenu, indexMenu++, MF_SEPARATOR|MF_BYPOSITION, 0, NULL);
	::InsertMenu(hMenu, indexMenu++, MF_STRING|MF_BYPOSITION, idCmd++, _T("Scan For Viruses With ClamWin"));
	// Seperator
	::InsertMenu(hMenu, indexMenu++, MF_SEPARATOR|MF_BYPOSITION, 0, NULL);
	
	return ResultFromShort(idCmd-idCmdFirst);	//Must return number of menu
	//items we added.
}

BOOL CShellExt::Scan(HWND hwnd)
{
    DWORD len = _tcslen(m_szFile);
    if(!len)
    {
        MessageBox(hwnd, _T("Error: Unable to retrieve Path."), _T("ClamWin"), MB_OK | MB_ICONERROR);
        return FALSE;
    }
    // remove last slash
    if(m_szFile[len-1] == _T('\\'))
        m_szFile[len-1] = _T('\0');
    
    DWORD dwType, cbData;
    TCHAR szCmd[MAX_PATH];
    TCHAR szClamWinPath[MAX_PATH] = _T("");
    
    // get path to ClamWin
    // Try registry first
    HKEY hKey;
    if (ERROR_SUCCESS == RegOpenKeyEx(HKEY_LOCAL_MACHINE, _T("Software\\ClamWin"), 0, KEY_READ, &hKey))
    {
        cbData = sizeof(szClamWinPath);
        RegQueryValueEx(hKey, _T("Path"), NULL, &dwType, (PBYTE)szClamWinPath, &cbData);
    }
    if(!_tcslen(szClamWinPath))
    {
        // could not retrieve from registry    
        // try in the same folder as the shell extension
        TCHAR szModule[MAX_PATH];
        if(GetModuleFileName(NULL, szModule, sizeof(szModule)))
        {
            // get folder name    
            _tsplitpath(szModule, NULL, szClamWinPath, NULL, NULL);            
        }
    }
    len = _tcslen(szClamWinPath);
    if(!len)
    {
        MessageBox(hwnd, _T("Error: Unable to retrieve path to ClamWin. Please reinstall ClamWin"), _T("ClamWin"), MB_OK | MB_ICONERROR);
        return FALSE;
    }
    // remove trailing slash
    if(szClamWinPath[len-1] == _T('\\'))
        szClamWinPath[len-1] = _T('\0');    
    
    _stprintf(szCmd, _T("\"%s\\%s\" --mode=scanner --path=\"%s\""), 
                szClamWinPath, _T("ClamWin.exe"), m_szFile);
        
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory( &si, sizeof(si) );
    si.cb = sizeof(si);

    ZeroMemory( &pi, sizeof(pi) );

    // Start the child process. 
    if( !CreateProcess( NULL, // No module name (use command line). 
        szCmd,            // Command line. 
        NULL,             // Process handle not inheritable. 
        NULL,             // Thread handle not inheritable. 
        FALSE,            // Set handle inheritance to FALSE. 
        0,                // No creation flags. 
        NULL,             // Use parent's environment block. 
        NULL,             // Use parent's starting directory. 
        &si,              // Pointer to STARTUPINFO structure.
        &pi )             // Pointer to PROCESS_INFORMATION structure.
    )    
    {
        TCHAR szMsg[MAX_PATH*2];
        _stprintf(szMsg, "Error: Unable to execute command %s.", szCmd);
        MessageBox(hwnd, szMsg, "ClamWin", MB_OK | MB_ICONERROR);        
        return FALSE;
    }

    // Close process and thread handles. 
    CloseHandle( pi.hProcess );
    CloseHandle( pi.hThread );
    
    return TRUE;        
}
//
//  FUNCTION: CShellExt::InvokeCommand(LPCMINVOKECOMMANDINFO)
//
//  PURPOSE: Called by the shell after the user has selected on of the
//           menu items that was added in QueryContextMenu().
//
//  PARAMETERS:
//    lpcmi - Pointer to an CMINVOKECOMMANDINFO structure
//
//  RETURN VALUE: HRESULT code signifying success or failure;NOERROR if no error
//
//
//  COMMENTS:
//
STDMETHODIMP CShellExt::InvokeCommand(LPCMINVOKECOMMANDINFO lpcmi)
{
	HRESULT			hr = E_INVALIDARG;
	
	//If HIWORD(lpcmi->lpVerb) then we have been called programmatically
	//and lpVerb is a command that should be invoked.  Otherwise, the shell
	//has called us, and LOWORD(lpcmi->lpVerb) is the menu ID the user has
	//selected.  Actually, it's (menu ID - idCmdFirst) from QueryContextMenu().
	if (!HIWORD(lpcmi->lpVerb))
	{
		UINT idCmd = LOWORD(lpcmi->lpVerb);		
		switch (idCmd)
		{
		case 0:
		    Scan(lpcmi->hwnd);		    
			break;
		}
		hr = NOERROR;
	}
	return hr;
}


//
//  FUNCTION: CShellExt::GetCommandString(UINT idCmd,UINT uFlags,UINT FAR *reserved,LPSTR pszName,UINT cchMax)
//
//  PURPOSE: Called by the shell to retreive the cononical command name
//			 or help text for a menu item added by a context menu extension handler
//
//  PARAMETERS:
//	  idCmd - Menu item ID offset
//    uFlags - Value specifying the type of information to retreive
//    *reserved - Pointer to reserved value
//    pszName - Pointer to buffer to receive name string or help text
//    cchMax - Buffer size
//
//  RETURN VALUE: HRESULT code signifying success or failure;NOERROR if no error
//
//
//  COMMENTS:
//
STDMETHODIMP CShellExt::GetCommandString(UINT idCmd,UINT uFlags,UINT FAR *reserved,LPTSTR pszName,UINT cchMax)
{
	
	switch (idCmd)
	{
	case 0:	
		_tcsncpy(pszName, _T("ClamWin Antivirus"), cchMax);
		break;
   }
	return NOERROR;
}
