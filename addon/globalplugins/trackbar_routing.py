#globalplugins/trackbar_routing.py
import globalPluginHandler
from NVDAObjects.IAccessible import IAccessible
import config
import braille
import winUser
import os
import sys
import api

TBM_GETRANGEMIN = winUser.WM_USER+1
TBM_GETRANGEMAX = winUser.WM_USER+2
TBM_SETPOS = winUser.WM_USER+5
TBM_SETPOSNOTIFY = winUser.WM_USER+34
WM_HSCROLL = 0x0114
WM_VSCROLL = 0x0115
SB_THUMBPOSITION = 4
SB_THUMBTRACK = 5
winver = int(str(sys.getwindowsversion()[0])+str(sys.getwindowsversion()[1]))
class trackbar(IAccessible):
	__gestures = {
		'br('+config.conf['braille']['display']+'):route': 'setvalue'
	}
	def script_setvalue(self, gesture):
		hwnd = self.windowHandle
		cur = winUser.sendMessage(hwnd, TBM_GETPOS, 0, 0)
		max = winUser.sendMessage(hwnd, TBM_GETRANGEMAX, 0, 0)
		min = winUser.sendMessage(hwnd, TBM_GETRANGEMIN, 0, 0)
		newpos = ((gesture.routingIndex * (max - min)) / (braille.handler.displaySize -1)) + min
		if winver >= 61:
			winUser.sendMessage(hwnd, TBM_SETPOSNOTIFY, -1, int(newpos))
		else:
			winUser.sendMessage(hwnd, TBM_SETPOS, -1, int(newpos))
			winUser.sendMessage(api.getForegroundObject().windowHandle,WM_HSCROLL,winUser.MAKELONG(SB_THUMBTRACK,cur),hwnd)
			winUser.sendMessage(api.getForegroundObject().windowHandle,WM_HSCROLL,winUser.MAKELONG(SB_THUMBPOSITION,newpos),hwnd)
			winUser.sendMessage(api.getForegroundObject().windowHandle,WM_VSCROLL,winUser.MAKELONG(SB_THUMBTRACK,cur),hwnd)
			winUser.sendMessage(api.getForegroundObject().windowHandle,WM_VSCROLL,winUser.MAKELONG(SB_THUMBPOSITION,newpos),hwnd)
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_SLIDER:
			clsList.insert(0, trackbar)