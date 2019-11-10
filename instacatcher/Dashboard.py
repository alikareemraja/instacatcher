import wx
import wx.adv
from instacatcher.analytics.Analytics import Analytics

class Dashboard(wx.Frame):

    def __init__(self, parent, title, state):
        
        super(Dashboard, self).__init__(parent, title = title,size = (790,530))

        self.state = state;
        # create a panel in the frame
        self.pnl = wx.Panel(self)

        t1 = wx.StaticText(self.pnl, -1,pos=(605,16), size = (150,30), label="Users:")
        self.users_listbox = wx.ListBox(self.pnl, pos =(605, 35),size = (160,200), choices = self.state.influencer_list, style = wx.LB_SINGLE)

        columns = ['PostTime', 'Followers', 'Caption_Length', 'Caption_Emojis', 'Caption_Hashtags', 'Likes_Count', 'per Follower', 'Comments_Count', 'Comments_per Follower', 'Comments_0-1 h', 'Comments_1-3 h', 'Comments_3-12 h', 'Comments_12-24 h', 'Comments_24-48 h', 'Comments_Rest', 'Comments_Comment Answers', 'Comments_Emojis p. Comment']
        groupby = ['Weekday', 'Year', 'MediaType']

        charts_box = wx.StaticBox(self.pnl, wx.ID_ANY,size=(550,450), label="Charts")
        
        self.y_axis_control = wx.RadioBox(charts_box, -1, label="Y-Axis", pos=(270,10) ,
         choices=columns, majorDimension=0, style=wx.RA_SPECIFY_ROWS,
         validator=wx.DefaultValidator)
         #self.y_axis_control.Wrap(250)

        self.x_axis_control = wx.RadioBox(charts_box, -1, label="X-Axis", pos=(10,10),
         choices=columns, majorDimension=0, style=wx.RA_SPECIFY_ROWS,
         validator=wx.DefaultValidator)

        linechart_button = wx.Button(charts_box, label="Line Chart", pos=(25,400), size=(120,30))
        self.Bind(wx.EVT_BUTTON, self.generate_linechart, linechart_button)

        scatterchart_button = wx.Button(charts_box, label="Scatter Chart", pos=(150,400), size=(120,30))
        self.Bind(wx.EVT_BUTTON, self.generate_scatterchart, scatterchart_button)
    

    def generate_linechart(self,event):
        try:
            analytics = Analytics(self.pnl, self.state)
            user = self.users_listbox.GetString(self.users_listbox.GetSelection())
            y_axis = self.y_axis_control.StringSelection
            x_axis = self.x_axis_control.StringSelection
            analytics.create_linechart(user, x_axis, y_axis)
        
        except:
            msg = wx.MessageDialog(self.pnl, "The two axes are incompatible for this chart type. Try another combination.", caption="Oops!",
              style=wx.OK, pos=wx.DefaultPosition)
            msg.ShowModal()

    def generate_scatterchart(self,event):
        try:
            analytics = Analytics(self.pnl, self.state)
            user = self.users_listbox.GetString(self.users_listbox.GetSelection())
            y_axis = self.y_axis_control.StringSelection
            x_axis = self.x_axis_control.StringSelection
            analytics.create_scatterchart(user, x_axis, y_axis)
        except:
            msg = wx.MessageDialog(self.pnl, "The two axes are incompatible for this chart type. Try another combination.", caption="Oops!",
              style=wx.OK, pos=wx.DefaultPosition)
            msg.ShowModal()