#!/bin/python
"""
Hello World, but with more meat.
"""


import instaloader
import os
import wx
from datetime import datetime
import sys
from docx import Document
from docx.shared import Inches
import xlsxwriter
import calendar
import regex
import emoji
from threading import *

class InstaLoaderThread(Thread):
    
    """Worker Thread Class."""
    def __init__(self, application_window, state, influencer_list):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.influencer_list = influencer_list;
        self._application_window = application_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.state = state;
        self.start()
    

    def run(self):

        
        for username in self.influencer_list:
            
            L = instaloader.Instaloader()

            self.post_folder = username + '_posts';
            self.stories_folder = username + '_stories';

            auth = L.login("ali.kareem.raja","r3s3tpassw0rD1!")

            try: # try to load user profile; else give error console text
                self.profile = instaloader.Profile.from_username(L.context, username)  #self.state.usrOfPosts
            except:
                self._application_window.SetStatusText('User does not exist. Try different User name.')
                return

            if self.state.isDate == False:
                self._application_window.SetStatusText('Date format is not recognized. Please change to correct format.')
                return

            excelData = []


            # pre-check if everyting is in order with the time interval
            if self.state.nbrOfPosts == 1: # if nbrOfPosts has not changed -> just focus on time intervall
                if self.state.timeFrom != datetime.strptime("1900-01-01", '%Y-%m-%d').date():
                    self.state.nbrOfPosts = 99999

            if self.state.timeFrom > datetime.today().date(): # lower bound needs to be earlier than today
                self.state.timeFrom = datetime.strptime("1900-01-01", '%Y-%m-%d').date()

            if self.state.timeFrom > self.state.timeTo: # lower bound needs to be earlier than upper bound
                self.state.timeFrom = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
                if self.state.timeTo <= datetime.strptime("1900-01-01", '%Y-%m-%d').date():
                    self.state.timeTo = datetime.today().date()


            stories = L.get_stories([self.profile.userid]) 
            
            storiesExcelData = []
            
            for story in stories:
                    for item in story.get_items():
                        storiesExcelData.append([item.date_local, calendar.day_name[item.date_local.weekday()], item.owner_profile.followers, "Video" if item.is_video == True else "Photo"])                    
                        L.download_storyitem(item, self.stories_folder)

                    
            """Load Posts:"""
            self._application_window.SetStatusText('Loading posts...')
            posts = self.profile.get_posts()

            # counter variable for looping through posts
            i = 0
        
            for post in posts: # iterate through each post
                while i < self.state.nbrOfPosts:

                    if self._want_abort:
                        # Use a result of None to acknowledge the abort (of
                        # course you can use whatever you'd like or even
                        # a separate event type)
                        return
                    
                    if post.date_utc.date() >= self.state.timeFrom and post.date_utc.date() <= self.state.timeTo:
                        i += 1
                    else:
                        post = (next(posts))
                        if post.date_utc.date() < self.state.timeFrom:
                            i += 10000
                            post = (next(posts))
                        continue

                    trueFalse = False
                    try:
                        trueFalse = L.download_post(post, self.post_folder)
                    except:
                        trueFalse = False

                    #if trueFalse:
                        #self._application_window.SetStatusText('Downloaded post: ' + post.caption)
                    #else:
                        #self._application_window.SetStatusText('/!\ Error downloading posts.')
                        

                    postTime = post.date_utc
                    fileName = self._application_window.getDate(postTime)

                    project_path = os.path.dirname(sys.modules['__main__'].__file__)
                    #script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
                    rel_path = "{0}/{1}.txt".format(self.post_folder,fileName)
                    abs_file_path = os.path.join(project_path, rel_path)

                    try:
                        caption = open(abs_file_path, 'r+').read()
                    except:
                        print("Image has no caption.")


                    """Catch information for Excel Sheet:"""
                    postWeekday = calendar.day_name[postTime.weekday()]

                    followers = 0
                    try:
                        followers = self.profile.followers
                    except:
                        followers = 1
                        print("Error catching FOLLOWERS of Influencer. FOLLOWERS set to 1.")

                    capLength = 0
                    capEmoticons = 0
                    cap = post.caption
                    
                    if cap != None:
                        capLength = len(cap)
                        data = regex.findall(r'\X', cap)
                        for word in data:
                            if any(char in emoji.UNICODE_EMOJI for char in word):
                                capEmoticons += 1
                    else:
                        capLength = 0
                        capEmoticons = 0

                    capHashtags = 0
                    try:
                        hashtags = post.caption_hashtags
                        capHashtags = len(hashtags)
                    except:
                        capHashtags = 0
                        print("Hashtags could not be fetched")


                    likes = 0
                    try:
                        likes = post.likes
                    except:
                        likes = 0
                        print("Error catching LIKES of Influencer.")

                    likesPerFollower = likes / followers



                    """Erstelle .docx Dokument:"""
                    document = Document()

                    # Überschrift erstellen:
                    mediaType=""
                    if post.is_video:
                        mediaType="Video (Dauer: %s Sek.)" % str(post.video_duration)
                    else:
                        mediaType="Foto"

                    document.add_heading('{0} von {1} am {2}:'.format(mediaType,self.post_folder,fileName), level=1)
                    document.add_paragraph('Information caught at %s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    if os.path.exists('{0}/{1}.jpg'.format(self.post_folder,fileName)):
                        document.add_picture('{0}/{1}.jpg'.format(self.post_folder,fileName), width=Inches(2.5))
                    else:
                        counter = 1
                        while os.path.exists('{0}/{1}_{2}.jpg'.format(self.post_folder,fileName,counter)):
                            document.add_picture('{0}/{1}_{2}.jpg'.format(self.post_folder,fileName,counter), width=Inches(2.5))
                            counter += 1

                    mediaTypeExcel = post.typename
                    if mediaTypeExcel == "GraphSidecar":
                        sidecars = post.get_sidecar_nodes()
                        counter = 0
                        for _ in sidecars:
                            counter += 1
                        mediaTypeExcel = "Fotoserie (%s)" % str(counter)
                    else:
                        mediaTypeExcel = mediaType

                    # Likes:
                    document.add_heading('%s Likes' % str(post.likes), level=3)

                    # Bildunterschrift:
                    document.add_heading('Caption:', level=3)
                    document.add_paragraph(caption)

                    # Iterate over all comments of current post
                    document.add_heading('%s Comments:' % str(post.comments), level=3)
                    r = document.add_paragraph()
                    comments = post.get_comments()


                    likesPerFollower = likes / followers

                    com0To1 = 0
                    com1To3 = 0
                    com3To12 = 0
                    com12To24 = 0
                    com24To48 = 0
                    comRest = 0
                    comEmoticonCounter = 0


                    for com in comments:
                        q = document.add_paragraph()
                        q.add_run("%s: " % str(getattr(com, 'created_at_utc'))).bold
                        q.add_run(com.text)

                        # check time difference of each comment to post
                        comTime = getattr(com, 'created_at_utc')
                        timeDifference = (comTime - postTime).total_seconds()

                        if timeDifference <= 3600:
                            com0To1 += 1
                        elif timeDifference <= 10800:
                            com1To3 +=1
                        elif timeDifference <= 43200:
                            com3To12 += 1
                        elif timeDifference <= 86400:
                            com12To24 += 1
                        elif timeDifference <= 172800:
                            com24To48 += 1
                        else:
                            comRest += 1

                        data = regex.findall(r'\X', getattr(com, 'text'))
                        for word in data:
                            if any(char in emoji.UNICODE_EMOJI for char in word):
                                comEmoticonCounter += 1

                        # capHashtags = 0

                    comCount = post.comments
                    comAnswers = comCount - (com0To1 + com1To3 + com3To12 + com12To24 + com24To48 + comRest)
                    comPerFollower = comCount / followers

                    if comCount != 0:
                        comEmoticonAverage = comEmoticonCounter / comCount
                    else:
                        comEmoticonAverage = 0

                    """Create EXCEL Data and store to Array"""
                    dataPoint = [postTime, postWeekday, followers, mediaTypeExcel, capLength, capEmoticons, capHashtags, likes, likesPerFollower, comCount, comPerFollower, com0To1, com1To3, com3To12, com12To24, com24To48, comRest, comAnswers, comEmoticonAverage]
                    excelData.append(dataPoint)

                    """Create folder if not existent:"""
                    try:
                        os.mkdir("data_%s" % username)
                        print("Directory data_", username, " created.")
                    except:
                        print("Directory data_", username, " already exists.")

                    document.save('data_{0}/{1}.docx'.format(username,fileName))
                    try:
                        post = (next(posts))
                    except:
                        print("No more posts to iterate.")
                        self._application_window.SetStatusText('Download Finished')
                        break;

            """Create and built Excel Sheet:"""
            fileNameExcel = datetime.now().strftime("%Y_%m_%d_%H_%M")
            workbook = xlsxwriter.Workbook('data_{0}/{1}.xlsx'.format(username,fileNameExcel), {'constant_memory': True})
            worksheet = workbook.add_worksheet()

            bold = workbook.add_format({'bold': 1})
            bold = workbook.add_format({'bold': 2})
            date_format = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm'})
            merge_format = workbook.add_format({'align': 'center'})

            #create header
            worksheet.write('A1', 'PostTime', bold)
            worksheet.write('B1', 'Weekday', bold)
            worksheet.write('C1', 'Followers', bold)
            worksheet.write('D1', 'MediaType', bold)

            worksheet.merge_range('E1:G1', 'Caption', merge_format)
            worksheet.merge_range('H1:I1', 'Likes', merge_format)
            worksheet.merge_range('J1:S1', 'Comments', merge_format)
            worksheet.write('E2', 'Length', bold)
            worksheet.write('F2', 'Emojis', bold)
            worksheet.write('G2', 'Hashtags', bold)
            worksheet.write('H2', 'Count', bold)
            worksheet.write('I2', 'per Follower', bold)
            worksheet.write('J2', 'Count', bold)
            worksheet.write('K2', 'per Follower', bold)
            worksheet.write('L2', '0-1 h', bold)
            worksheet.write('M2', '1-3 h', bold)
            worksheet.write('N2', '3-12 h', bold)
            worksheet.write('O2', '12-24 h', bold)
            worksheet.write('P2', '24-48 h', bold)
            worksheet.write('Q2', 'Rest', bold)
            worksheet.write('R2', 'Comment Answers', bold)
            worksheet.write('S2', 'Emojis p. Comment', bold)

            row = 2
            col = 0

            for element in excelData:
                
                worksheet.write_string(row, col, str(element[0]))   # postTime
                worksheet.write_string(row, col + 1, element[1])    # postWeekday
                worksheet.write_number(row, col + 2, element[2])    # followers
                worksheet.write_string(row, col + 3, element[3])    # mediaType
                worksheet.write_number(row, col + 4, element[4])    # capLength
                worksheet.write_number(row, col + 5, element[5])    # capEmoticons
                worksheet.write_number(row, col + 6, element[6])    # capHashtags
                worksheet.write_number(row, col + 7, element[7])    # likes
                worksheet.write_number(row, col + 8, element[8])    # likesPerFollower
                worksheet.write_number(row, col + 9, element[9])    # comCount
                worksheet.write_number(row, col + 10, element[10])  # comPerFollower
                worksheet.write_number(row, col + 11, element[11])  # com0To1
                worksheet.write_number(row, col + 12, element[12])  # com1To3
                worksheet.write_number(row, col + 13, element[13])  # com3To12
                worksheet.write_number(row, col + 14, element[14])  # com12To24
                worksheet.write_number(row, col + 15, element[15])  # com24To48
                worksheet.write_number(row, col + 16, element[16])  # comRest
                worksheet.write_number(row, col + 17, element[17])  # comAnswers
                worksheet.write_number(row, col + 18, element[18])  # comEmoticonAverage

                row += 1

            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 1})
            bold = workbook.add_format({'bold': 2})
            date_format = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm'})
            merge_format = workbook.add_format({'align': 'center'})
            
            #create header
            worksheet.write('A1', 'PostTime', bold)
            worksheet.write('B1', 'Weekday', bold)
            worksheet.write('C1', 'Followers', bold)
            worksheet.write('D1', 'MediaType', bold)

            row = 2
            col = 0

            for element in storiesExcelData:
                
                worksheet.write_string(row, col, str(element[0]))   # postTime
                worksheet.write_string(row, col + 1, element[1])    # postWeekday
                worksheet.write_number(row, col + 2, element[2])    # followers
                worksheet.write_string(row, col + 3, element[3])    # mediaType

                row += 1



            workbook.close()


            # Set Status Text if finished sucessfully
            print("Excel written for " + username)
        self._application_window.SetStatusText('Finished sucessfully.')                            
   

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1