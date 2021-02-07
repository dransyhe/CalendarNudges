from feature_functions import *
import pandas as pd

def feature_creator(meeting_list, company_dict):

    # creates empty lists for each of the features
    userfullname = []
    workday = []
    worktime = []
    usercompany = []
    onlyuserfirst = []
    bracketsafterperson = []
    andbetweenpersons = []
    firstnameandsurname = []
    onlyfirstname = []
    personinmeeting = []
    teamspiritcheck = []
    projectcheck = []
    timekeywordscheck = []
    onetoonecheck = []
    broadcastcheck = []
    performancecheck = []
    irrelevantcheck = []
    externalcheck = []
    noguest = []

    # populates the feature list
    for meeting in meeting_list:
        userfullname.append(users_fullname(meeting))
        workday.append(not_workday(meeting))
        worktime.append(not_worktime(meeting))
        usercompany.append(user_company_in_title(meeting, company_dict))
        onlyuserfirst.append(first_name_only(meeting))
        bracketsafterperson.append(brackets_following_person(meeting))
        andbetweenpersons.append(and_between_persons(meeting))
        firstnameandsurname.append(firstname_and_surname(meeting))
        onlyfirstname.append(only_firstname(meeting))
        personinmeeting.append(person_in_meeting(meeting))
        teamspiritcheck.append(word_list_check(teamspirit_keywords, meeting))
        projectcheck.append(word_list_check(project_keywords, meeting))
        timekeywordscheck.append(word_list_check(time_keywords, meeting))
        onetoonecheck.append(word_list_check(time_keywords, meeting))
        broadcastcheck.append(word_list_check(broadcast_keywords, meeting))
        performancecheck.append(word_list_check(performance_keywords, meeting))
        irrelevantcheck.append(word_list_check(irrelevant_keywords_all, meeting))
        externalcheck.append(word_list_check(external_keywords, meeting))
        noguest.append(meeting["noguest"])

    feature_df = pd.DataFrame()

    feature_df["userfullname"] = userfullname
    feature_df["workday"] = workday
    feature_df["worktime"] = worktime
    feature_df["usercompany"] = usercompany
    feature_df["onlyuserfirst"] = onlyuserfirst
    feature_df["bracketsafterperson"] = bracketsafterperson
    feature_df["andbetweenpersons"] = andbetweenpersons
    feature_df["firstnameandsurname"] = firstnameandsurname
    feature_df["onlyfirstname"] = onlyfirstname
    feature_df["personinmeeting"] = personinmeeting
    feature_df["teamspiritcheck"] = teamspiritcheck
    feature_df["projectcheck"] = projectcheck
    feature_df["timekeywordscheck"] = timekeywordscheck
    feature_df["onetoonecheck"] = onetoonecheck
    feature_df["broadcastcheck"] = broadcastcheck
    feature_df["performancecheck"] = performancecheck
    feature_df["irrelevantcheck"] = irrelevantcheck
    feature_df["externalcheck"] = externalcheck
    feature_df["noguest"] = noguest

    return feature_df





