#!/bin/python
"""
State of the application.
"""
from datetime import datetime
import pickle

class State(object):
    def __init__(self):
        # Set variables
        self.login_user = ""
        self.login_password = ""
        self.usrOfPosts = ""     # instagram user name of influencer
        self.influencer_list = []
        self.getStories = False
        self.createDocs = False
        self.savePosts = False
        self.timeFrom = datetime.today().date()  # lower bound for time interval downloads
        self.timeTo = datetime.today().date()                               # upper bound for time interval downloads
        self.isDate = True

def Save(object):
        with open('instacatcher_state.pkl', 'wb') as output:
                pickle.dump(object, output, pickle.DEFAULT_PROTOCOL)

def Load():
        try:
                with open('instacatcher_state.pkl', 'rb') as input:
                        object = pickle.load(input)
                        return object;
        except:
                return State();