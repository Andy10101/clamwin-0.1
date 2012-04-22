rem @echo off
rem call winenv.bat
set CYGWINDIR=d:\cygwin
set THISDIR=l:\Projects\ClamWin
set ISTOOLDIR=D:\Program Files\ISTool 4
set MINGWDIR=D:\mingw
set MINGW_MAKE=mingw32-make.exe

if not "%1"=="ALL" goto _short
rem build cygwin part of it
call %CYGWINDIR%\bin\bash --login "%thisdir%\build.sh"
if not "%ERRORLEVEL%"=="0" goto ERROR  
build py2exe binaries
:_short 
cd Setup\py2exe
call python setup_all.py 
if not "%ERRORLEVEL%"=="0" goto ERROR  
rem build ExplorerShell
cd ..\..\cpp
set OLD_PATH=%PATH%
set PATH=%MINGWDIR%\bin
call %MINGW_MAKE% -f ExplorerShell.mk all
if not "%ERRORLEVEL%"=="0" goto ERROR  
set PATH=%OLDPATH%
cd ..\
rem build setup
call "%ISTOOLDIR%\ISTool.exe" -compile "%THISDIR%\Setup\Setup.iss"
if not "%ERRORLEVEL%"=="0" goto ERROR  

goto END

:ERROR
@echo an error occured
pause

:end

