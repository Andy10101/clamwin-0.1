#!/bin/bash
CVSROOT=anonymous@cvs.sourceforge.net:/cvsroot/clamav
THISDIR=/cygdrive/l/Projects/ClamWin
cd $THISDIR
/bin/cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/clamav -z9 co clamav-devel
cd $THISDIR/clamav-devel
/bin/sh ./configure --disable-clamav
/bin/make --makefile $THISDIR/clamav-devel/Makefile

