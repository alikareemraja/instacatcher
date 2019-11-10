#!/bin/python
"""
Hello World, but with more meat.
"""

import wx
import instaloader
import os
from datetime import datetime
import sys
from docx import Document
from docx.shared import Inches
import xlsxwriter
import calendar
import regex
import emoji
import instacatcher.Application as UI
import instacatcher.State as State




if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.

    
    try:
        state = State.Load();
        app = wx.App()
        frm = UI.Application(None, title='InstaCatcher', state= state)
        frm.Show()
        app.MainLoop()
        
    except:
        wx.MessageDialog(None, "Something went wrong!", caption="Oops!",
              style=wx.OK, pos=wx.DefaultPosition)