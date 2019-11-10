import wx
import wx.adv
import wx.lib.scrolledpanel
from instacatcher.State import State 
import instacatcher.DataAccess.InstaLoaderThread as Thread


class Download_Progress(wx.Frame):
    
    def __init__(self, parent, title, state):
        
        super(Download_Progress, self).__init__(parent, title = title,size = (300,400))
        self.abbu = parent
        self.state = state;

        # create a panel in the frame
        #pnl = wx.Panel(self)
        self.pnl = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(300,400), style=wx.SIMPLE_BORDER)
        self.pnl.SetupScrolling()

        #self.cancel_button = wx.Button(self.pnl, label="Cancel", pos=(160,320), size=(120,30))
        #self.Bind(wx.EVT_BUTTON, self.cancel, self.cancel_button)
                

        y_position = 50
        self.progress_bars = []
        for influencer in self.state.influencer_list:
            doclabel = wx.StaticText(self.pnl, -1,pos=(10,y_position), size = (100,30), label=influencer)
            txt = wx.StaticText(self.pnl, -1,pos=(110,y_position), size = (150,30), label="In Progress - 0 Items")
            self.progress_bars.append(txt)
            y_position = y_position + 30
            # Set up event handler for any worker thread results

        
    def run(self):

        if self.state.login_user == "" and self.state.login_password == "":
            message = wx.MessageDialog(self.pnl, "Please provide your instagram credentials!", caption=wx.MessageBoxCaptionStr,
              style=wx.OK|wx.CENTRE, pos=wx.DefaultPosition) 
            message.ShowModal()
            self.Close()
            self.abbu.dbtn.Enable()
            return

        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        print("Starting download")
        self.worker = []
        index = 0;
        for influencer in self.state.influencer_list:
            self.worker.append(Thread.InstaLoaderThread(self.progress_bars[index],self.state, influencer))
            index = index + 1

    def cancel(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if len(self.worker) > 0:
            for worker in self.worker:
                worker.abort()

    def OnResult(self, event):
        """Show Result status."""
        self.SetLabel(event.data)            
        