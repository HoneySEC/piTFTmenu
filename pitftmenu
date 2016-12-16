#!/bin/bash

exectty=$(/usr/bin/tty)
if [ "$exectty" == "/dev/tty1" ]; then
	#export FRAMEBUFFER=/dev/fb1
	export FRAMEBUFFER=/dev/fb0
	export APPDIR=$(/bin/pwd)
	startpage="pitftmenu.py"
	/usr/bin/env python $APPDIR$"/pitftmenu.py"
fi
