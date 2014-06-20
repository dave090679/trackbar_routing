#globalplugins/trackbar_routing.py#A part of NonVisual Desktop Access (NVDA)#Copyright (C) 2006-2012 NVDA Contributors#This file is covered by the GNU General Public License.#See the file COPYING for more details.
import globalPluginHandlerimport controlTypes
from NVDAObjects.IAccessible import IAccessible
import config
import braille
import winUser
import os
import sys
import api
from  NVDAObjects.UIA import UIAimport UIAHandlerTBM_GETPOS = winUser.WM_USER
TBM_GETRANGEMIN = winUser.WM_USER+1
TBM_GETRANGEMAX = winUser.WM_USER+2
TBM_SETPOS = winUser.WM_USER+5
TBM_SETPOSNOTIFY = winUser.WM_USER+34
WM_HSCROLL = 0x0114
WM_VSCROLL = 0x0115
SB_THUMBPOSITION = 4
SB_THUMBTRACK = 5
winver = int(str(sys.getwindowsversion()[0])+str(sys.getwindowsversion()[1]))
class uia_trackbar(UIA):	__gestures = {		'br('+config.conf['braille']['display']+'):route': 'setvalue'	}	def script_setvalue(self, gesture):		hwnd = self.windowHandle		cur = self.UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_RangeValueValuePropertyId) 		max = self.UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_RangeValueMaximumPropertyId) 		min = self.UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_RangeValueMinimumPropertyId) 		newpos = ((gesture.routingIndex * (max - min)) / (braille.handler.displaySize -1)) + min		self.UIAElement.GetCurrentPattern(UIAHandler.UIA_RangeValuePatternId).QueryInterface(UIAHandler.IUIAutomationRangeValuePattern).SetValue(newpos)class trackbar(IAccessible):
	__gestures = {
		'br('+config.conf['braille']['display']+'):route': 'setvalue'
	}
	def script_setvalue(self, gesture):
		hwnd = self.windowHandle
		cur = winUser.sendMessage(hwnd, TBM_GETPOS, 0, 0)
		max = winUser.sendMessage(hwnd, TBM_GETRANGEMAX, 0, 0)
		min = winUser.sendMessage(hwnd, TBM_GETRANGEMIN, 0, 0)		newpos = ((gesture.routingIndex * (max - min)) / (braille.handler.displaySize -1)) + min
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
		if (obj.role == controlTypes.ROLE_SLIDER and isinstance(obj, IAccessible)):
			clsList.insert(0, trackbar)
		elif (obj.role == controlTypes.ROLE_SLIDER and isinstance(obj, UIA)):			clsList.insert(0, uia_trackbar)