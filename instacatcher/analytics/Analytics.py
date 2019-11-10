import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import wx

class Analytics():

    def __init__(self, parent, state):
        self.state = state
        #self.pnl = wx.Panel(self)

    def transform_columns(self, dataframe):
        dataframe.rename(columns={ 'Caption' : 'Caption_Length' , 'Unnamed: 5' : 'Caption_Emojis', 'Unnamed: 6' : 'Caption_Hashtags', 'Likes': 'Likes_Count', 'Unnamed: 8':'per Follower', 'Comments':'Comments_Count', 'Unnamed: 10' : 'Comments_per Follower', 'Unnamed: 11' : 'Comments_0-1 h', 'Unnamed: 12': 'Comments_1-3 h', 'Unnamed: 13' : 'Comments_3-12 h', 'Unnamed: 14' : 'Comments_12-24 h', 'Unnamed: 15' : 'Comments_24-48 h', 'Unnamed: 16' : 'Comments_Rest', 'Unnamed: 17' : 'Comments_Comment Answers', 'Unnamed: 18': 'Comments_Emojis p. Comment'}, 
                    inplace=True)
        dataframe = dataframe.drop(dataframe.index[0])
        
        dataframe['PostTime'] = pd.to_datetime(dataframe['PostTime'])
        dataframe['Followers'] = pd.to_numeric(dataframe['Followers'])
        dataframe['Caption_Length'] = pd.to_numeric(dataframe['Caption_Length'])
        dataframe['Caption_Emojis'] = pd.to_numeric(dataframe['Caption_Emojis'])
        dataframe['Caption_Hashtags'] = pd.to_numeric(dataframe['Caption_Hashtags'])
        dataframe['Likes_Count'] = pd.to_numeric(dataframe['Likes_Count'])
        dataframe['per Follower'] = pd.to_numeric(dataframe['per Follower'])
        dataframe['Comments_Count'] = pd.to_numeric(dataframe['Comments_Count'])
        dataframe['Comments_per Follower'] = pd.to_numeric(dataframe['Comments_per Follower'])
        dataframe['Comments_0-1 h'] = pd.to_numeric(dataframe['Comments_0-1 h'])
        dataframe['Comments_1-3 h'] = pd.to_numeric(dataframe['Comments_1-3 h'])
        dataframe['Comments_3-12 h'] = pd.to_numeric(dataframe['Comments_3-12 h'])
        dataframe['Comments_12-24 h'] = pd.to_numeric(dataframe['Comments_12-24 h'])
        dataframe['Comments_24-48 h'] = pd.to_numeric(dataframe['Comments_24-48 h'])
        dataframe['Comments_Rest'] = pd.to_numeric(dataframe['Comments_Rest'])
        dataframe['Comments_Comment Answers'] = pd.to_numeric(dataframe['Comments_Comment Answers'])
        dataframe['Comments_Emojis p. Comment'] = pd.to_numeric(dataframe['Comments_Emojis p. Comment'])

        return dataframe

    def open_excel(self,username):
        if os.path.exists('data_{0}/{1}.xlsx'.format(username,username)):
            project_path = os.path.dirname(sys.modules['__main__'].__file__)
            #script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
            rel_path = "data_{0}/{1}.xlsx".format(username, username)
            abs_file_path = os.path.join(project_path, rel_path)
            return  pd.read_excel (abs_file_path)
        print("Unable to open excel")

    def create_linechart(self, username, x_axis, y_axis):
        try:
            df = self.open_excel(username)
            df = self.transform_columns(df)
            df.plot(kind='line',x=x_axis,y=y_axis,color='red')
            plt.show()
        except:
            raise Exception("The two axes are incompatible for this chart type. Try another combination.")
        

    def create_scatterchart(self, username, x_axis, y_axis):
        try:
            df = self.open_excel(username)
            df = self.transform_columns(df)
            df.plot(kind='scatter',x=x_axis,y=y_axis,color='red')
            plt.show()
        except:
            raise Exception("The two axes are incompatible for this chart type. Try another combination.")

    def do(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        df = pd.read_excel (dir_path + '/170qm.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'

        df = self.rename_columns(df)
        df = df.drop(df.index[0])
        df['PostTime'] = pd.to_datetime(df['PostTime'])
        df['Caption_Emojis'] = pd.to_numeric(df['Caption_Emojis'])
        df['Likes_Count'] = pd.to_numeric(df['Likes_Count'])
        print(list(df.columns))
        print (df["Caption_Emojis"])


        df.plot(kind='scatter',x='Likes_Count',y='Caption_Emojis',color='red')
        #plt.show()    

        df.plot(kind='line',x='PostTime',y='Followers',color='red')
        #plt.show()

        weekday_group = df.groupby("Weekday").count()["Likes_Count"].reset_index(name="count")
        print(weekday_group)
        weekday_group.plot(kind='bar', x='Weekday', y='count', align='center', alpha=0.5)
        #plt.show()




        #y_pos = np.arange(len(df['Weekday']))
        #performance = df['Likes_Count']

        #plt.bar(y_pos, performance, align='center', alpha=0.5)
        #plt.xticks(y_pos, df['Weekday'])
        #plt.ylabel('Usage')
        #plt.title('Programming language usage')

        #plt.show()