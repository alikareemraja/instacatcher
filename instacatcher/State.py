#!/bin/python
"""
State of the application.
"""
from datetime import datetime
import pickle

class State(object):
    def __init__(self):
        # Set variables
        self.nbrOfPosts = 1      # how many posts should be downloaded
        self.usrOfPosts = ""     # instagram user name of influencer
        self.influencer_list = []
        self.getStories = False
        self.timeFrom = datetime.strptime("1900-01-01", '%Y-%m-%d').date()  # lower bound for time interval downloads
        self.timeTo = datetime.today().date()                               # upper bound for time interval downloads
        self.isDate = True

def Save(object):
    with open('instacatcher_state.pkl', 'wb') as output:
        pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)

def Load():
        try:
                with open('instacatcher_state.pkl', 'rb') as input:
                        object = pickle.load(input)
                        return object;
        except:
                return State();