	# Project: ExplorerShell
CPP  = g++.exe
CC   = gcc.exe
WINDRES = windres.exe
RES  = ExplorerShell_private.res
OBJ  = ./Build/ShellExt.o ./Build/ShellExtImpl.o $(RES)
LINKOBJ  = ./Build/ShellExt.o ./Build/ShellExtImpl.o $(RES)
LIBS =  -L"$(MINGWDIR)/lib" --no-export-all-symbols --add-stdcall-alias $(MINGWDIR)/lib/libole32.a $(MINGWDIR)/lib/libuuid.a 
INCS =  -I"$(MINGWDIR)/include" 
CXXINCS =  -I"$(MINGWDIR)/include/c++"  -I"$(MINGWDIR)/include/c++/mingw32"  -I"$(MINGWDIR)/include/c++/backward"  -I"$(MINGWDIR)/include" 
BIN  = Build/ExplorerShell.dll
CXXFLAGS = $(CXXINCS)  -O3
CFLAGS = $(INCS)-DBUILDING_DLL=1   -O3

.PHONY: all all-before all-after clean clean-custom

all: all-before Build/ExplorerShell.dll all-after


clean: clean-custom
	rm -f $(OBJ) $(BIN)
	
all-before:
	$(shell mkdir ".\Build")
	

DLLWRAP=dllwrap.exe
DEFFILE=./Build/libExplorerShell.def
STATICLIB=./Build/libExplorerShell.a

	    
$(BIN): $(LINKOBJ)
	$(DLLWRAP) --output-def $(DEFFILE) --driver-name c++ --implib $(STATICLIB) $(LINKOBJ) $(LIBS) -o $(BIN)

./Build/ShellExt.o: ShellExt.cpp
	$(CPP) -c ShellExt.cpp -o ./Build/ShellExt.o $(CXXFLAGS)

./Build/ShellExtImpl.o: ShellExtImpl.cpp
	$(CPP) -c ShellExtImpl.cpp -o ./Build/ShellExtImpl.o $(CXXFLAGS)

ExplorerShell_private.res: ExplorerShell_private.rc 
	$(WINDRES) -i ExplorerShell_private.rc -I rc -o ExplorerShell_private.res -O coff 
