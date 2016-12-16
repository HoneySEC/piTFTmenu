#!/usr/bin/env python
import sys, os, time, subprocess, commands, pygame, socket, fcntl, struct
from pygame.locals import *
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
pygame.font.init()
pygame.display.init()
#pygame.mouse.set_visible(0)

TYPE_NONE=0
TYPE_PROC=1
TYPE_CMD=2
TYPE_SVC=3

CurrentPage=1
MaxPages=3

class _Button:
    def __init__(self, ButtonText, ButtonCmd, CommandType):
		self.ButtonText = ButtonText
		self.ButtonCmd = ButtonCmd
		self.CommandType = CommandType
		
# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(BtnNumber, text, colour):
	if BtnNumber == 1:
		xpo = 30
		ypo = 105 
		height = 55 
		width = 210
	elif BtnNumber == 2:
		xpo = 260
		ypo = 105 
		height = 55 
		width = 210
	elif BtnNumber == 3:
		xpo = 30
		ypo = 180 
		height = 55 
		width = 210
	elif BtnNumber == 4:
		xpo = 260
		ypo = 180 
		height = 55 
		width = 210
	elif BtnNumber == 5:
		xpo = 30
		ypo = 255 
		height = 55 
		width = 210
	elif BtnNumber == 6:
		xpo = 260
		ypo = 255 
		height = 55 
		width = 100
	elif BtnNumber == 7:
		xpo = 370
		ypo = 255 
		height = 55 
		width = 100
	pygame.draw.rect(screen, colour, (xpo-10,ypo-10,width,height),3)
	pygame.draw.rect(screen, colour, (xpo-9,ypo-9,width-1,height-1),1)
	pygame.draw.rect(screen, colour, (xpo-8,ypo-8,width-2,height-2),1)
	font=pygame.font.Font(None,42)
	label=font.render(str(text), 1, (colour))
	screen.blit(label,(xpo,ypo))

# Get Your External IP Address
def get_ip(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ip_msg = ifname + ': ' +socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
	except Exception:
		ip_msg = ifname + ': Not connected' 
		pass
	return ip_msg

# define function that checks for touch location
def on_touch():
	# get the position that was touched
	touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#  x_min                 x_max   y_min                y_max
	if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
		# button 1 event
		button(1)
	elif 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
		# button 2 event
		button(2)
	elif 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
		# button 3 event
		button(3)
	elif 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
		# button 4 event
		button(4)
	elif 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
		# button 5 event
		button(5)
	elif 260 <= touch_pos[0] <= 360 and 255 <= touch_pos[1] <=310:
		# button 6 event
		button(6)
	elif 370 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
		# button 7 event
		button(7)

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def check_service(srvc):
	try:
		check = "/usr/sbin/service " + srvc + " status"
		status = run_cmd(check)
		if ("is running" in status) or ("active (running)") in status:
			return True
		else:
			return False
	except:
		return False
	
def toggle_service(srvc):
	check = "/usr/sbin/service " + srvc + " status"
	start = "/usr/sbin/service " + srvc + " start"
	stop = "/usr/sbin/service " + srvc + " stop"
	status = run_cmd(check)
	if ("is running" in status) or ("active (running)") in status:
		run_cmd(stop)
		return False
	else:
		run_cmd(start)
		return True

def DrawScreen(page):
	# colors    R    G    B
	white    = (255, 255, 255)
	tron_whi = (189, 254, 255)
	red      = (255,   0,   0)
	green    = (  0, 255,   0)
	blue     = (  0,   0, 255)
	tron_blu = (  0, 219, 232)
	black    = (  0,   0,   0)
	cyan     = ( 50, 255, 255)
	magenta  = (255,   0, 255)
	yellow   = (255, 255,   0)
	tron_yel = (255, 218,  10)
	orange   = (255, 127,   0)
	tron_ora = (255, 202,   0)

	# Tron theme blue
	tron_regular = tron_blu
	tron_light   = tron_whi
	tron_inverse = tron_yel

	# Background Color
	screen.fill(black)

	# Outer Border
	pygame.draw.rect(screen, tron_regular, (0,0,479,319),8)
	pygame.draw.rect(screen, tron_light, (2,2,479-4,319-4),2)

	Sc_Button[page,6] = _Button("  <<<", "", TYPE_NONE)
	Sc_Button[page,7] = _Button("  >>>", "", TYPE_NONE)
	
	# Buttons and labels
	make_label(str(CurrentPage)+"/"+str(MaxPages), 430, 10, 32, tron_light)
	
	make_label(get_ip('eth0'), 32, 10, 32, tron_inverse)
	make_label(get_ip('wlan0'), 32, 35, 32, tron_inverse)
	make_label(get_ip('wlan1'), 32, 60, 32, tron_inverse)
	
	#Buttons
	for i in range(1, 6):
		colour = tron_light
		if Sc_Button[page,i].CommandType == TYPE_SVC:
			if check_service(Sc_Button[page,i].ButtonCmd):
				colour=green
			else:
				colour=red
		make_button(i, Sc_Button[page,i].ButtonText, colour)
		
	#Page change buttons
	for i in range(6, 8):
		make_button(i, Sc_Button[page,i].ButtonText, tron_ora)
	
# Define each button press action
def button(number):
	global CurrentPage,MaxPages
	if CurrentPage==1 and number == 3:
		# exit
		pygame.quit()
		process = subprocess.call("setterm -term linux -back default -fore white -clear all", shell=True)
		sys.exit()
	if CurrentPage==1 and number == 5:
		pygame.display.quit()
		pygame.quit()
		sys.exit()
	if number == 6:
		# Previous page
		CurrentPage = CurrentPage - 1
		if CurrentPage == 0:
			CurrentPage = MaxPages
		DrawScreen(CurrentPage)
	if number == 7:
        # next page
		CurrentPage = CurrentPage + 1
		if CurrentPage > MaxPages:
			CurrentPage = 1
		DrawScreen(CurrentPage)
	else:	
		if Sc_Button[CurrentPage, number].CommandType == TYPE_PROC:
			pygame.quit()
			process = subprocess.call(Sc_Button[CurrentPage, number].ButtonCmd, shell=True)
			os.execv(__file__, sys.argv)
			sys.exit()
		elif Sc_Button[CurrentPage, number].CommandType == TYPE_CMD:
			pygame.quit()
			run_cmd(Sc_Button[CurrentPage, number].ButtonCmd)
			os.execv(__file__, sys.argv)
		elif Sc_Button[CurrentPage, number].CommandType == TYPE_SVC:
			toggle_service(Sc_Button[CurrentPage, number].ButtonCmd)
			DrawScreen(CurrentPage)

Sc_Button = {}
#Page 1
Sc_Button[1,1] = _Button("    X on TFT", "/usr/bin/sudo FRAMEBUFFER=/dev/fb1 startx", TYPE_CMD)
Sc_Button[1,2] = _Button("   X on HDMI", "/usr/bin/sudo FRAMEBUFFER=/dev/fb0 startx", TYPE_CMD)
Sc_Button[1,3] = _Button("    Shutdown", "/sbin/poweroff", TYPE_CMD)
Sc_Button[1,4] = _Button("      Reboot", "/sbin/reboot", TYPE_PROC)
Sc_Button[1,5] = _Button("        Exit", "", TYPE_NONE)
#Page 2
Sc_Button[2,1] = _Button("  FTP Server", "vsftpd", TYPE_SVC)
Sc_Button[2,2] = _Button("  WWW Server", "apache2", TYPE_SVC)
Sc_Button[2,3] = _Button("     OpenVAS", "openvas-manager", TYPE_SVC)
Sc_Button[2,4] = _Button("            ", "", TYPE_NONE)
Sc_Button[2,5] = _Button("       MySQL", "mysql", TYPE_SVC)
#Page 3
Sc_Button[3,1] = _Button("    Terminal", "setterm -term linux -back default -fore white -clear all", TYPE_PROC)
Sc_Button[3,2] = _Button("      Kismet", "/usr/bin/kismet", TYPE_CMD)
Sc_Button[3,3] = _Button("            ", "", TYPE_NONE)
Sc_Button[3,4] = _Button("            ", "", TYPE_NONE)
Sc_Button[3,5] = _Button("            ", "", TYPE_NONE)
#3
#make_button(" WWW Server", 30, 105, 55, 210, green)
#make_button("   FTP Server", 260, 105, 55, 210, green)
#make_button("   FTP Server", 260, 105, 55, 210, tron_light)
#make_button("  VNC-Server",  30, 180, 55, 210, green)
#make_button("  VNC-Server", 30, 180, 55, 210, tron_light)
#make_button("    Metasploit ", 260, 180, 55, 210, tron_light)
#make_button("      MySQL", 30, 105, 55, 210, green)
#make_button("    OpenVAS", 260, 180, 55, 210, green)

#set size of the screen
size = width, height = 480, 320
screen = pygame.display.set_mode(size)

DrawScreen(1)

#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            on_touch()
        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
    ## Reduce CPU utilisation
    time.sleep(0.1)

