#!/bin/python
"""
Hello World, but with more meat.
"""

import wx
import wx.adv
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
from instacatcher.Login import Login
from instacatcher.Dashboard import Dashboard
from instacatcher.DataAccess.Download_Progress import Download_Progress

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
        #st = wx.StaticText(pnl, label="InstaCatcher 1.0", pos=(25,25))
        # box.Add(st, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        #font = st.GetFont()
        #font.PointSize += 10
        #font = font.Bold()
        #st.SetFont(font)

        # INFLUENCER NAME TXT FIELD
        t2 = wx.StaticText(pnl, -1, pos=(25, 80), size=(150, 30), label="User Name: ")
        self.usrSelector = wx.TextCtrl(pnl,value=self.state.usrOfPosts, pos=(180, 80), size=(150, 30))
        self.usrSelector.Bind(wx.EVT_TEXT, self.OnKeyTypedUsr)
        add = wx.Button(pnl, label="Add", pos=(190,110), size=(60,25))
        emptybtn = wx.Button(pnl, label="Empty", pos=(250,110), size=(60,25))
        self.Bind(wx.EVT_BUTTON, self.adduser, add)
        self.Bind(wx.EVT_BUTTON, self.empty, emptybtn)
        # box.Add(t2, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
 
        #self.text = wx.TextCtrl(pnl,style = wx.TE_MULTILINE) 
        self.listbox = wx.ListBox(pnl, pos =(365, 80),size = (160,200), choices = self.state.influencer_list, style = wx.LB_SINGLE)

        # GET STORIES
        t1 = wx.StaticText(pnl, -1,pos=(25,150), size = (150,30), label="Get Stories")
        self.storiesSelector = wx.CheckBox(pnl, pos=(50,165), size = (20,20))
        self.storiesSelector.Bind(wx.EVT_CHECKBOX,self.OnClickStories)
        if self.state.getStories == True:
            self.storiesSelector.SetValue(self.state.getStories)
        
        # SAVE DOCS
        """ doclabel = wx.StaticText(pnl, -1,pos=(130,150), size = (150,30), label="Create Docs")
        self.docsSelector = wx.CheckBox(pnl, pos=(160,165), size = (20,20))
        self.docsSelector.Bind(wx.EVT_CHECKBOX,self.OnClickDocs) """
        self.state.createDocs = True
        """ if self.state.createDocs == True:
            self.docsSelector.SetValue(self.state.createDocs) """

        # GET POSTS
        t1 = wx.StaticText(pnl, -1,pos=(230,150), size = (150,30), label="Get Posts")
        self.postsSelector = wx.CheckBox(pnl, pos=(250,165), size = (20,20))
        self.postsSelector.Bind(wx.EVT_CHECKBOX,self.OnClickPosts)
        if self.state.savePosts == True:
            self.postsSelector.SetValue(self.state.savePosts)

        # DATE FROM FIELD
        t3 = wx.StaticText(pnl, -1, pos=(25, 210), size=(150, 30), label="Start Date:")
        #self.datefromSelector = wx.TextCtrl(pnl, value = self.state.timeFrom.strftime("%Y-%m-%d"),  pos=(180, 310), size=(150, 30))
        self.datefromSelector = wx.adv.DatePickerCtrl(pnl, -1, dt=self.state.timeFrom, pos=(180, 210), size=(150, 30), style=wx.adv.DP_DEFAULT|wx.adv.DP_SHOWCENTURY, validator=wx.Validator(), name="start_date")
        self.datefromSelector.Bind(wx.adv.EVT_DATE_CHANGED, self.OnKeyTypedDateFrom)

        t4 = wx.StaticText(pnl, -1, pos=(25, 260), size=(150, 30), label="End Date:")
        #self.datetoSelector = wx.TextCtrl(pnl, value = self.state.timeTo.strftime("%Y-%m-%d") , pos=(180, 360), size=(150, 30))
        self.datetoSelector = wx.adv.DatePickerCtrl(pnl, -1, dt=self.state.timeTo, pos=(180, 260), size=(150, 30), style=wx.adv.DP_DEFAULT|wx.adv.DP_SHOWCENTURY, validator=wx.Validator(), name="end_date")
        self.datetoSelector.Bind(wx.adv.EVT_DATE_CHANGED, self.OnKeyTypedDateTo)

        lbl = wx.StaticText(pnl, label="Type in the name of the Influencer and optionally select the number of posts and date restricitons. Read instructions for more details.", pos=(25, 5), size=(350, 100))
        lbl.Wrap(350)
        
        self.dbtn = wx.Button(pnl, label="Download", pos=(25,400), size=(120,30))
        self.Bind(wx.EVT_BUTTON, self.action, self.dbtn)

        lbl.Wrap(350)
        

        self.analytics_button = wx.Button(pnl, label="Analytics Dashboard", pos=(330,400), size=(180,30))
        self.Bind(wx.EVT_BUTTON, self.analytics, self.analytics_button)
        
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
        
        #loginWindow = Login(self, title="Login", state=state)
        self.login_button = wx.Button(pnl, label="Login", pos=(450,20), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.login, self.login_button)
        #loginWindow.Show()

        # And indicate we don't have a worker thread yet
        self.worker = []

    def action(self,event):
        
        State.Save(self.state);
        downloader = Download_Progress(self, "Download", self.state)
        downloader.Show()
        downloader.run();
        self.SetStatusText('Downloading Data')
        btn = event.GetEventObject()
        btn.Disable()
        

    def analytics(self,event):
        dashboardWindow = Dashboard(self, title="Dashboard", state=self.state)
        dashboardWindow.Show()

    def login(self, event):
        loginWindow = Login(self, title="Login", state=self.state)
        loginWindow.Show()

    def OnKeyTypedNbr(self, event):
        try:
            self.state.nbrOfPosts = int(event.GetString())
        except:
            self.nbrSelector.SetValue("")
            self.state.nbrOfPosts = 1

    def OnClickStories(self, event):
        checkbox = event.GetEventObject()
        self.state.getStories = checkbox.GetValue()


    def OnClickPosts(self, event):
        
        checkbox = event.GetEventObject()
        self.state.savePosts = checkbox.GetValue()

    def OnClickDocs(self, event):

        checkbox = event.GetEventObject()
        self.state.createDocs = checkbox.GetValue()


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
            datefrom = event.GetEventObject()
            self.state.timeFrom =  self._wxdate2pydate(datefrom.GetValue()) #datetime.strptime(datefrom.GetValue(), '%m/%d/%Y').date();
            self.state.isDate = True

        except ValueError as ve:
            print('ValueError Raised:', ve)
            self.state.isDate = False

    def OnKeyTypedDateTo(self, event):
        try:
            dateto = event.GetEventObject()
            self.state.timeTo = self._wxdate2pydate(dateto.GetValue()) #datetime.strptime(dateto.GetValue(), '%m/%d/%Y').date();
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

    def _wxdate2pydate(self, date):
        import datetime
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:
            return None