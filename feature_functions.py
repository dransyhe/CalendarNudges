import datetime
import re
import numpy as np
from nltk import word_tokenize
import pandas as pd

#for the named entity recoginition
from sner import Ner
tagger = Ner(host = "localhost", port = 9199)

#checks if the user's full name is included in the meeting title, if either username or title blank returns 0
def users_fullname(meeting):
    if pd.isnull(meeting["username"]) or pd.isnull(meeting["title"]):
        return 0
    if str(meeting["username"]).lower() in str(meeting["title"]).lower():
        return 1
    else:
        return 0

# returns 1 if the meeting occurs on a nonworkday, returns 0 if the starttime is blank
def not_workday(meeting):
    if pd.isnull(meeting["starttime"]):
        return 0
    if meeting["starttime"].isocalendar()[2] >= 6:
        return 1
    else:
        return 0

# returns 1 if the meeting does not occur on work time, returns 0 if the starttime is blank
def not_worktime(meeting):
    if pd.isnull(meeting["starttime"]):
        return 0
    if meeting["starttime"].time() < datetime.time(6) or meeting["starttime"].time() > datetime.time(21):
        return 1
    else:
        return 0

# checks in a word is included in the meeting title, returns 0 if the meeting title is blank
def word_in_title(word, meeting):
    if pd.isnull(meeting["title"]):
        return 0
    return word.lower() in str(meeting["title"]).lower()


# returns 1 if any word in word_list is included in the meeting title
def word_list_check(word_list, meeting):
    for word in word_list:
        if word_in_title(word, meeting):
            return 1
    return 0


# returns 1 if the meeting title only contains the user's first name, returns 0 if either title or username is blank
def first_name_only(meeting):
    if pd.isnull(meeting["username"]) or pd.isnull(meeting["title"]):
        return 0
    user_names = word_tokenize(meeting["username"])
    if word_in_title(user_names[0], meeting) and not word_in_title(user_names[1], meeting):
        return 1
    else:
        return 0


# returns 1 if brackets follow a person - kinda works at getting e.g. Jane (Multiplii) but people use it also for Jane (Task)
def brackets_following_person(meeting):
    if pd.isnull(meeting["title"]):
        return 0
    title = and_sub(meeting["title"])
    for (word, entity) in tagger.tag(title):
        if entity == "PERSON":
            start_index = title.index(word) + len(word)
            if start_index >= len(title) - 2:
                return 0
            elif title[start_index] == "(" or title[start_index + 1] == "(":
                return 1
    return 0


# returns 1 if "and" between two people - works pretty well at identifying external meetings
def and_between_persons(meeting):
    if pd.isnull(meeting["title"]):
        return 0
    entities = tagger.tag(meeting["title"])
    for index in range(len(entities)):
        if entities[index][0] == "and":
            if index > 0 and index < len(entities) - 1:
                if entities[index - 1][1] == "PERSON" and entities[index + 1][1] == "PERSON":
                    return 1
    return 0


# checks if 2 person entities follow each other
def firstname_and_surname(meeting):
    if pd.isnull(meeting["title"]):
        return 0
    title = meeting["title"]
    title = and_sub(title)
    title = lower_keywords(title)
    entities = tagger.tag(title)
    for index in range(len(entities) - 1):
        if entities[index][1] == "PERSON" and entities[index + 1][1] == "PERSON":
            return 1
    return 0

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


# replace with but finds the target regardless of its captilization  !! Currently will also lower parts of words
def lower_word(string, word):
    length = len(word)
    start_list = [m.start() for m in re.finditer(word, string.lower())]
    for start_index in start_list:
        string = string[0:start_index] + word + string[start_index + length:]
    return string


# checks if the meeting only contains persons on their own -- pretty good at working out if the meetings are one to one
def only_firstname(meeting):
    if person_in_meeting(meeting) == 1 and firstname_and_surname(meeting) == 0:
        return 1
    else:
        return 0

# checks if there is at least one person tag in the meeting
def person_in_meeting(meeting):
    if pd.isnull(meeting["title"]):
        return 0
    title = lower_keywords(meeting["title"])
    title = and_sub(title)
    entities = tagger.tag(title)
    for (word, entity) in entities:
        if entity == "PERSON":
            return 1
    return 0


# lowers any word in our word list
def lower_keywords(title):
    for keyword in all_keywords:
        if keyword in title.lower() and keyword not in title:
            title = lower_word(title, keyword)
    return title


# returns 1 if the user's company is in the title
def user_company_in_title(meeting, company_dict):
    if not pd.isnull(meeting["companyname"]) and  pd.isnull(meeting["title"]):
        alternate_list = company_dict[meeting["companyname"]]
        for alternate in alternate_list:
            if str(alternate).lower() in str(meeting["title"]).lower():
                return 1
    return 0


# creates a dictonary of company titles including some alternative spellings
def create_company_dict(meeting_list):
    company_dic = {}
    for company_name in list(set([meeting["companyname"] for meeting in meeting_list if not pd.isnull(meeting["companyname"])])):
        company_dic[company_name] = [company_name, \
                                     company_name.strip(" "), \
                                     ''.join(ch for ch in company_name if ch.isupper()), \
                                     ''.join(ch[0] for ch in company_name.split(" ") if ch)]
        # put variations of company name into dictionary
        # includes: original name; delete spaces; only capital letters; only initials
    return company_dic


and_symbols_list = ["&", "//", "/", "<>", "< >", " x "]
teamspirit_keywords = ["lunch hangout", "book club", "fika", "chin-wag", "team meet", "team call", "drinks", "learn"]
project_keywords = ["standup", "session", "demo", "leads", "leadership", "sync",
                    "discussion", "plan", "onboarding", "delivery", "updates",
                    "update", "intro", "introduction", "checkin", "check in",
                    "catchup", "catch up", "status", "workshop", "planning",
                    "handover", "department", "alignment", "follow up"]
# check these words poss add fu or f/u
time_keywords = ["biweekly", "weekly", "daily", "monthly"]
broadcast_keywords = ["conference", "panel", "forum", "seminar", "summit", "committee",
                      "presentation", "all hands", "q & a", "company", "company wide"]
one_to_one_keywords = ["catchup", "catch up", "chat", "1 – 1", "1-1", "1:1",
                       "one to one", "1 on 1", "one on one"]
performance_keywords = ["review", "okr", "orks", "tracker", "feedback", "progress review", "salary review"]
irrelevant_keywords = ["reminder", "buffer", "break", "annual leave", "busy", "office hours",
                       "prep", "preparation", "cancel", "clear", "draft", "placeholder",
                       "offline", "block", "blocked", "dnb", "to do", "todo", "ooo",
                       "leave work", "edit", "edited", "hold", "birthday", "travel", "a/l",
                       "webinar"]
irrelevant_keywords2 = ["meditation", "work out", "haircut", "yoga", "whiskey",
                        "donate", "clean", "run", "tennis", "workout"]
irrelevant_keywords_all = irrelevant_keywords + irrelevant_keywords2
external_keywords = ["call with", "zoom"]

all_keywords = teamspirit_keywords + project_keywords + time_keywords + broadcast_keywords + one_to_one_keywords + performance_keywords + irrelevant_keywords + irrelevant_keywords2 + external_keywords

all_keywords += ["meet", "phone"]







