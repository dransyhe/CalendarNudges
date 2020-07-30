import datetime
import re


#corrects the start time in a datetime object with the correct timezone
def dates_and_times_corrector(meeting):
    start_datetime = start_datetime_corrector(meeting["starttime"])
    if meeting["timezone"][1] == "+":
        time_change = int(re.findall(r"\d+", meeting["timezone"])[0])
    elif meeting["timezone"][1] == "-":
        time_change = -int(re.findall(r"\d+", meeting["timezone"])[0])
    else:
        time_change = 0
    start_datetime = start_datetime + datetime.timedelta(hours = time_change)
    meeting["starttime"] = start_datetime
    return meeting    

#converts the starttime string into a datetime object
def start_datetime_corrector(start_string):
    start_year = int(start_string[0:4])
    start_month = int(start_string[5:7])
    start_day = int(start_string[8:10])
    start_hour = int(start_string[11:13])
    start_minute = int(start_string[14:16])
    return datetime.datetime(start_year, start_month, start_day,start_hour,start_minute)
    
#returns 1 if the users full name is included in the meeting title
def users_fullname(meeting):
    if str(meeting["username"]).lower() in str(meeting["title"]).lower():
        return 1
    else:
        return 0

#returns 1 if the meeting occurs on a nonworkday
def not_workday(meeting):
    if meeting["starttime"].isocalendar()[2] >= 6:
        return 1
    else:
        return 0

#returns 1 if the meeting does not occur on work time
def not_worktime(meeting):
    if meeting["starttime"].time() < datetime.time(6) or meeting["starttime"].time() > datetime.time(21):
        return 1
    else:
        return 0

#returns 1 if the user's company is in the title
def user_company_in_title(meeting, company_dict):
    alternate_list = company_dict[meeting["companyname"]]
    for alternate in alternate_list:
        if str(alternate).lower() in str(meeting["title"]).lower():
            return 1
    return 0

#creates a dictonary of company titles including some alternative spellings
def create_company_dict(meeting_list):
    company_dic = {}
    for company_name in list(set([meeting["companyname"] for meeting in meeting_list])):
        company_dic[company_name] = [company_name]
    company_dic["People Collective"] = company_dic["People Collective"] +["PC"]
    company_dic["Grant Tree"] = company_dic["Grant Tree"] + ["GrantTree"]
    company_dic["BECO Capital"] = company_dic["BECO Capital"] + ["BECO"]
    company_dic["Shaper Impact Capital"] =  company_dic["Shaper Impact Capital"] + ["SIC"]
    return company_dic

#checks in a word is included in the meeting title
def word_in_title(word, meeting):
    return word.lower() in str(meeting["title"]).lower()

#returns 1 if any word in word_list is included in the meeting title
def word_list_check(word_list, meeting):
    for word in word_list:
        if word_in_title(word,meeting):
            return 1
    return 0

