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
import instacatcher.DataAccess.InstaLoaderThread as Thread
import instacatcher.State as State

class Application(wx.Frame):



    # Set variables
    nbrOfPosts = 1      # how many posts should be downloaded
    usrOfPosts = ""     # instagram user name of influencer

    timeFrom = datetime.strptime("1900-01-01", '%Y-%m-%d').date()  # lower bound for time interval downloads
    timeTo = datetime.today().date()                               # upper bound for time interval downloads
    isDate = True                                                  # bool if both inputs are actually date format

    def __init__(self, parent, title, state):
        # ensure the parent's __init__ is called
        super(Application, self).__init__(parent, title = title,size = (550,530))

        self.state = state;

        # create a panel in the frame
        pnl = wx.Panel(self)
        # box = wx.BoxSizer(wx.VERTICAL)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="InstaCatcher 1.0", pos=(25,25))
        # box.Add(st, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # INFLUENCER NAME TXT FIELD
        t2 = wx.StaticText(pnl, -1, pos=(25, 140), size=(150, 30), label="User Name: ")
        self.usrSelector = wx.TextCtrl(pnl,value=self.state.usrOfPosts, pos=(180, 140), size=(150, 30))
        self.usrSelector.Bind(wx.EVT_TEXT, self.OnKeyTypedUsr)
        add = wx.Button(pnl, label="Add", pos=(190,170), size=(60,25))
        emptybtn = wx.Button(pnl, label="Empty", pos=(250,170), size=(60,25))
        self.Bind(wx.EVT_BUTTON, self.adduser, add)
        self.Bind(wx.EVT_BUTTON, self.empty, emptybtn)
        # box.Add(t2, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
 
        #self.text = wx.TextCtrl(pnl,style = wx.TE_MULTILINE) 
        self.listbox = wx.ListBox(pnl, pos =(405, 140),size = (120,-1), choices = self.state.influencer_list, style = wx.LB_SINGLE)

        # NUMBER OF POSTS TXT FIELD
        t1 = wx.StaticText(pnl, -1,pos=(25,210), size = (150,30), label="Number of Posts: ")
        self.nbrSelector = wx.TextCtrl(pnl,value= str(self.state.nbrOfPosts), pos=(180,210), size = (150,30))
        self.nbrSelector.Bind(wx.EVT_TEXT,self.OnKeyTypedNbr)
        # box.Add(t1, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        # GET STORIES
        t1 = wx.StaticText(pnl, -1,pos=(25,260), size = (150,30), label="Get Stories")
        self.nbrSelector = wx.CheckBox(pnl, pos=(180,260), size = (150,30))
        self.nbrSelector.Bind(wx.EVT_TEXT,self.OnClickStories)
        if self.state.getStories == True:
            self.nbrSelector.SetValue(self.getStories)

        # DATE FROM FIELD
        t3 = wx.StaticText(pnl, -1, pos=(25, 310), size=(150, 30), label="From YYYY-MM-DD:")
        self.datefromSelector = wx.TextCtrl(pnl, value = self.state.timeFrom.strftime("%Y-%m-%d"),  pos=(180, 310), size=(150, 30))
        self.datefromSelector.Bind(wx.EVT_TEXT, self.OnKeyTypedDateFrom)

        t4 = wx.StaticText(pnl, -1, pos=(25, 360), size=(150, 30), label="To YYYY-MM-DD:")
        self.datetoSelector = wx.TextCtrl(pnl, value = self.state.timeTo.strftime("%Y-%m-%d") , pos=(180, 360), size=(150, 30))
        self.datetoSelector.Bind(wx.EVT_TEXT, self.OnKeyTypedDateTo)

        lbl = wx.StaticText(pnl, label="Type in the name of the Influencer and optionally select the number of posts and date restricitons. Read instructions for more details.", pos=(25, 65), size=(350, 100))
        lbl.Wrap(350)
        btn = wx.Button(pnl, label="Download", pos=(25,400), size=(150,50))
        self.Bind(wx.EVT_BUTTON, self.action, btn)

        lbl.Wrap(350)
        cancel = wx.Button(pnl, label="Cancel", pos=(225,400), size=(150,50))
        self.Bind(wx.EVT_BUTTON, self.cancel, cancel)
        # box.Add(lbl, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        # box.Add(btn, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()

        # resize panel
        # pnl.SetSizer(box)
        self.Centre()
        self.Show()

        # And indicate we don't have a worker thread yet
        self.worker = []

    def action(self,event):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        State.Save(self.state);
        self.SetStatusText('Downloading Data')
        for influencer in self.state.influencer_list:
            self.worker.append(Thread.InstaLoaderThread(self,self.state, influencer))
            btn = event.GetEventObject()
            btn.Disable()
            

    def cancel(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker.count > 0:
            for worker in self.worker:
                worker.abort()


    def OnKeyTypedNbr(self, event):
        try:
            self.state.nbrOfPosts = int(event.GetString())
        except:
            self.nbrSelector.SetValue("")
            self.state.nbrOfPosts = 1

    def OnClickStories(self, event):
        self.state.getStories = event.IsChecked


    def OnKeyTypedUsr(self, event):
        self.state.usrOfPosts = event.GetString()

    def adduser(self, event):
        self.state.influencer_list.append(self.state.usrOfPosts)
        self.listbox.Append(self.state.usrOfPosts)
        #self.state.usrOfPosts = event.GetString()
        #self.usrOfPosts = event.GetString()

    def empty(self, event):
        self.listbox.Clear();
        self.state.influencer_list = [];
        #self.state.usrOfPosts = event.GetString()
        #self.usrOfPosts = event.GetString()

    def OnKeyTypedDateFrom(self, event):
        try:
            timeStr = str(event.GetString())
            self.state.timeFrom = datetime.strptime(timeStr, '%Y-%m-%d').date()
            print("Time succesfully converted and stored!")
            self.state.isDate = True

        except ValueError as ve:
            print('ValueError Raised:', ve)
            self.state.isDate = False

    def OnKeyTypedDateTo(self, event):
        try:
            timeStr = str(event.GetString())
            self.state.timeTo = datetime.strptime(timeStr, '%Y-%m-%d').date()
            print("Time succesfully converted and stored!")
            self.state.isDate = True
            
        except ValueError as ve:
            print('ValueError Raised:', ve)
            self.state.isDate = False

    def makeMenuBar(self):
        

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        
        State.Save(self.state);
        self.Close(True)


    def OnHello(self, event):
       
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):

        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)