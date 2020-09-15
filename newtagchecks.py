import datetime
import re
from nltk import word_tokenize

from sner import Ner
tagger = Ner(host = "localhost", port = 9199)

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
    if meeting["companyname"]:
        alternate_list = company_dict[meeting["companyname"]]
        for alternate in alternate_list:
            if str(alternate).lower() in str(meeting["title"]).lower():
                return 1
    return 0

#creates a dictonary of company titles including some alternative spellings
def create_company_dict(meeting_list):
    company_dic = {}
    for company_name in list(set([meeting["companyname"] for meeting in meeting_list])):
        company_dic[company_name] = [company_name, \
                                     company_name.strip(" "),\
                                     ''.join(ch for ch in company_name if ch.isupper()),\
                                     ''.join(ch[0] for ch in company_name.split(" ") if ch)]
        # put variations of company name into dictionary 
        # includes: original name; delete spaces; only capital letters; only initials 
    if "" in company_dic: del company_dic[""]
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

#returns 1 if the meeting title only contains the user's first name
def first_name_only(meeting):
    user_names = word_tokenize(meeting["username"])
    if word_in_title(user_names[0], meeting) and not word_in_title(user_names[1], meeting):
        return 1
    else:
        return 0



#returns 1 if brackets follow a person - kinda works at getting e.g. Jane (Multiplii) but people use it also for Jane (Task)
def brackets_following_person(meeting):
    title = and_sub(meeting["title"])
    for (word, entity) in tagger.tag(title):
        if entity == "PERSON":
            start_index = title.index(word) + len(word)
            if start_index >= len(title)-2:
                return 0
            elif title[start_index] == "(" or title[start_index+1] == "(":
                return 1
    return 0

#returns 1 if "and" between two people - works pretty well at identifying external meetings
def and_between_persons(meeting):
    entities = tagger.tag(meeting["title"])
    for index in range(len(entities)):
        if entities[index][0] == "and":
            if index > 0 and index < len(entities)-1:
                if entities[index-1][1] == "PERSON" and entities[index+1][1] == "PERSON":
                    return 1
    return 0

#checks if 2 person entities follow each other
def firstname_and_surname(meeting):
    title = meeting["title"]
    title = and_sub(title)
    title = lower_keywords(title)
    entities = tagger.tag(title)
    for index in range(len(entities)-1):
        if entities[index][1] == "PERSON" and entities[index+1][1] == "PERSON":
            return 1
    return 0

        


and_symbols_list = ["&","//", "/", "<>", "< >", " x "]

def and_sub(title):
    and_title = title
    for symbol in and_symbols_list:
        while symbol in str(and_title).lower():
            and_title = replace_with(and_title, symbol, " and ")
    return and_title
        
def replace_with(string, target, replacement):
    if target not in string:
        return string
    else:
        start_index = string.find(target)
        length = len(target)
        return string[0:start_index] + replacement + string[start_index + length:]

#replace with but finds the target regardless of its captilization  !! Currently will also lower parts of words
def lower_word(string, word):
    length = len(word)
    start_list = [m.start() for m in re.finditer(word, string.lower())]
    for start_index in start_list:
        string = string[0:start_index] + word + string[start_index + length:]
    return string

#checks if the meeting only contains persons on their own -- pretty good at working out if the meetings are one to one
def only_firstname(meeting):
    if person_in_meeting(meeting) == 1 and firstname_and_surname(meeting) == 0:
        return 1
    else:
        return 0
    

#evaluates the word list
def evaluate_wordlist(meeting_list, word_list, correct_tag):
    word_dict = {}
    for word in word_list:
        total = 0
        correct = 0
        for meeting in meeting_list:
            if word_in_title(word, meeting):
                total +=1
                if meeting["tag"] == correct_tag:
                    correct += 1
        word_dict[word] = [total, correct, total - correct]
    return word_dict


# deal with number of guests (empty & '<' sign) 
def no_guest_range(meeting):
    if not meeting['noguest']:
        return 0
    return int(''.join(ch for ch in meeting['noguest'] if ch.isdigit()))
                




#checks if there is at least one person tag in the meeting
def person_in_meeting(meeting):
    title = lower_keywords(meeting["title"])
    title = and_sub(title)
    entities = tagger.tag(title)
    for (word, entity) in entities:
        if entity == "PERSON":
            return 1
    return 0

#lowers any word in our word list
def lower_keywords(title):
    for keyword in all_keywords:
        if keyword in title.lower() and keyword not in title:
            title = lower_word(title, keyword)
    return title

teamspirit_keywords = ["lunch hangout", "book club", "fika", "chin-wag", "team meet", "team call", "drinks", "learn"]
project_keywords = ["standup", "session", "demo","leads", "leadership", "sync",
                    "discussion", "plan", "onboarding", "delivery", "updates",
                    "update", "intro", "introduction", "checkin", "check in",
                    "catchup", "catch up","status", "workshop", "planning",
                    "handover","department", "alignment", "follow up"]
#check these words poss add fu or f/u
time_keywords = ["biweekly", "weekly", "daily", "monthly"]
broadcast_keywords = ["conference", "panel", "forum", "seminar", "summit", "committee",
                      "presentation","all hands","q & a","company", "company wide"]
one_to_one_keywords = ["catchup", "catch up", "chat","1 – 1", "1-1", "1:1",
                       "one to one", "1 on 1", "one on one"]
performance_keywords = ["review", "okr", "orks", "tracker", "feedback", "progress review", "salary review"]
irrelevant_keywords = ["reminder", "buffer", "break", "annual leave", "busy", "office hours",
                       "prep", "preparation", "cancel", "clear", "draft", "placeholder",
                       "offline", "block", "blocked", "dnb", "to do", "todo", "ooo",
                       "leave work", "edit", "edited", "hold", "birthday", "travel", "a/l",
                       "webinar"]
irrelevant_keywords2 = ["meditation", "work out", "haircut",  "yoga", "whiskey",
                        "donate", "clean", "run", "tennis", "workout"]
external_keywords = ["call with", "zoom"]

all_keywords = teamspirit_keywords + project_keywords + time_keywords + broadcast_keywords + one_to_one_keywords + performance_keywords + irrelevant_keywords + irrelevant_keywords2 + external_keywords

all_keywords += ["meet", "phone"]





             
            
