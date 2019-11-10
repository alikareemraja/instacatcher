import wx
import wx.adv


class Login(wx.Frame):

    def __init__(self, parent, title, state):
        
        super(Login, self).__init__(parent, title = title,size = (350,200))

        self.state = state;

        # create a panel in the frame
        pnl = wx.Panel(self)
        
        # INFLUENCER NAME TXT FIELD
        username_label = wx.StaticText(pnl, -1, pos=(25, 20), size=(150, 30), label="User Name: ")
        self.login_user_ctrl = wx.TextCtrl(pnl,value=self.state.login_user, pos=(180, 20), size=(150, 30))
        self.login_user_ctrl.Bind(wx.EVT_TEXT, self.login_user_ctrl_function)

        # INFLUENCER NAME TXT FIELD
        password_label = wx.StaticText(pnl, -1, pos=(25, 60), size=(150, 30), label="Password: ")
        self.login_pass_ctrl = wx.TextCtrl(pnl,value=self.state.login_password, pos=(180, 60), size=(150, 30))
        self.login_pass_ctrl.Bind(wx.EVT_TEXT, self.login_pass_ctrl_function)

        self.login_button = wx.Button(pnl, label="Login", pos=(220,100), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.login, self.login_button)


    def login_user_ctrl_function(self, event):
        self.state.login_user = event.GetString()


    def login_pass_ctrl_function(self, event):
        self.state.login_password = event.GetString()

    def login(self, event):
        self.Close()