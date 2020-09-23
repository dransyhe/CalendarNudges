import pandas as pd
import datetime
import re
import numpy as np


def meeting_list_generator(calendar_data):

    #creates lists of the usernames, companynames, title, no guests, timezone, starttime, endtime, tag from calendar_data dataframe
    usernames_list = calendar_data.username.values.tolist()
    companyname_list = calendar_data.companyname.values.tolist()
    titles_list = calendar_data.meetingtitle.values.tolist()
    noguest_list = calendar_data.noguest.values.tolist()
    timezone_list = calendar_data.timezone.values.tolist()
    starttime_list = calendar_data.starttime.values.tolist()
    endtime_list = calendar_data.starttime.values.tolist()
    tag_list = calendar_data.tag.values.tolist()

    #creates meeting_list which is a list of dictonaries each representing a meeting
    meeting_list = []
    for i in range(len(usernames_list)):
        meeting = {}
        meeting['username'] = check_empty(usernames_list[i])
        meeting['companyname'] = check_empty(companyname_list[i])
        meeting['title'] = check_empty(titles_list[i])
        meeting['noguest'] = check_num(noguest_list[i])
        meeting['timezone'] = timezone_list[i]
        meeting['starttime'] = starttime_list[i]
        meeting["endtime"] = endtime_list[i]
        meeting['tag'] = tag_list[i]
        meeting = dates_and_times_corrector(meeting)
        meeting_list += [meeting]

    return meeting_list


#converts a string to integer unless the string is not an integer then returns np.nan
def check_num(string):
    try:
        return int(string)
    except ValueError:
        return np.nan

#check if the string is empty then will return np.nan if it is empty
def check_empty(string):
    if string != "":
        return string
    else:
        return np.nan


#corrects the start time in a datetime object with the correct timezone
def dates_and_times_corrector(meeting):

    #converts start and end strings into datetime objects
    start_datetime = start_datetime_corrector(meeting["starttime"])
    end_datetime = start_datetime_corrector(meeting["endtime"])

    #finds the timechange of the datetime due to the timezone
    if meeting["timezone"] == "":
        time_change = 0
    elif meeting["timezone"][1] == "+":
        time_change = int(re.findall(r"\d+", meeting["timezone"])[0])
    elif meeting["timezone"][1] == "-":
        time_change = -int(re.findall(r"\d+", meeting["timezone"])[0])
    else:
        time_change = 0

    #changes the datetime by the timezone
    if type(start_datetime) == datetime.datetime:
        start_datetime = start_datetime + datetime.timedelta(hours = time_change)
    if type(end_datetime) == datetime.datetime:
        end_datetime = end_datetime + datetime.timedelta(hours = time_change)

    #updates the meeting
    meeting["starttime"] = start_datetime
    meeting["endtime"] = end_datetime
    return meeting

#converts the starttime string into a datetime object
def start_datetime_corrector(start_string):
    #will return np.nan if the string is not in the expected format
    try:
        start_year = int(start_string[0:4])
        start_month = int(start_string[5:7])
        start_day = int(start_string[8:10])
        start_hour = int(start_string[11:13])
        start_minute = int(start_string[14:16])
        return datetime.datetime(start_year, start_month, start_day,start_hour,start_minute)
    except ValueError:
        return np.nan
