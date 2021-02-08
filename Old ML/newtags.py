import pandas as pd
from newtagchecks import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import time


#read the input data file in CSV

pd.options.display.max_rows
pd.set_option('display.max_rows', None)

col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize',
			 'teamsize', 'starttime','endtime', 'lastsync', 'meetingtitle', 'noguest', 'tag']
calendar_data = pd.read_csv("../input_files/New Tagged 3.csv", header=0, names=col_names)





#creates lists of username, companyname, title, noguests, timezone and startime
calendar_data.username = calendar_data.username.astype(str)
usernames_list = calendar_data.username.values.tolist()

calendar_data.companyname = calendar_data.companyname.astype(str)
companyname_list =  calendar_data.companyname.values.tolist()

calendar_data.meetingtitle = calendar_data.meetingtitle.astype(str)
titles_list = calendar_data.meetingtitle.values.tolist()

calendar_data.noguest = calendar_data.noguest.astype(str)
noguest_list = calendar_data.noguest.values.tolist()

calendar_data.timezone = calendar_data.timezone.astype(str)
timezone_list = calendar_data.timezone.values.tolist()

calendar_data.starttime = calendar_data.starttime.astype(str)
starttime_list = calendar_data.starttime.values.tolist()

calendar_data.tag = calendar_data.tag.astype(str)
tag_list = calendar_data.tag.values.tolist()

calendar_data.endtime = calendar_data.endtime.astype(str)
endtime_list = calendar_data.endtime.values.tolist()

#creates a list of dictonaries each representing a meeting and converts the starttime into a datetime object
meeting_list = []
for i in range(len(usernames_list)):
    meeting = {}
    meeting['username'] = usernames_list[i]
    meeting['companyname'] = companyname_list[i]
    meeting['title'] = titles_list[i]
    meeting['noguest'] = noguest_list[i]
    meeting['timezone'] = timezone_list[i]
    meeting['starttime'] = starttime_list[i]
    meeting['endtime'] = endtime_list[i]
    meeting['tag'] = tag_list[i]
    meeting = dates_and_times_corrector(meeting)
    meeting_list += [meeting]

company_dict = create_company_dict(meeting_list)

#creates empty lists for each of the features
userfullname = []
workday = []
worktime = []
duration = []
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
noguestrange = [] 

#populates the feature list
for meeting in meeting_list:
    userfullname.append(users_fullname(meeting))
    workday.append(not_workday(meeting))
    worktime.append(not_worktime(meeting))
    duration.append(len_duration(meeting))
    usercompany.append(user_company_in_title(meeting, company_dict))
    onlyuserfirst.append(first_name_only(meeting))
    bracketsafterperson.append(brackets_following_person(meeting))
    andbetweenpersons.append(and_between_persons(meeting))
    firstnameandsurname.append(firstname_and_surname(meeting))
    personinmeeting.append(person_in_meeting(meeting))
    teamspiritcheck.append(word_list_check(teamspirit_keywords,meeting))
    projectcheck.append(word_list_check(project_keywords,meeting))
    timekeywordscheck.append(word_list_check(time_keywords,meeting))
    onetoonecheck.append(word_list_check(time_keywords,meeting))
    broadcastcheck.append(word_list_check(broadcast_keywords,meeting))
    performancecheck.append(word_list_check(performance_keywords, meeting))
    irrelevantcheck.append(word_list_check(irrelevant_keywords,meeting))
    externalcheck.append(word_list_check(external_keywords, meeting))
    noguestrange.append(no_guest_range(meeting)) 

calendar_data["userfullname"] = userfullname
calendar_data["workday"] = workday
calendar_data["worktime"] = worktime
calendar_data["duration"]= duration
calendar_data["usercompany"] = usercompany
#calendar_data["onlyuserfirst"] = onlyuserfirst
calendar_data["bracketsafterperson"] = bracketsafterperson
calendar_data["andbetweenpersons"] = andbetweenpersons
calendar_data["firstnameandsurname"] = firstnameandsurname
#calendar_data["onlyfirstname"] = onlyfirstname
calendar_data["personinmeeting"] = personinmeeting
calendar_data["teamspiritcheck"] = teamspiritcheck
calendar_data["projectcheck"] = projectcheck
calendar_data["timekeywordscheck"] = timekeywordscheck
calendar_data["onetoonecheck"] = onetoonecheck
calendar_data["broadcastcheck"] = broadcastcheck
calendar_data["performancecheck"] = performancecheck
calendar_data["irrelevantcheck"] = irrelevantcheck
calendar_data["externalcheck"] = externalcheck
calendar_data["noguestrange"] = noguestrange


feature_cols = ["noguestrange", "userfullname", "workday", "worktime","duration", "usercompany", "bracketsafterperson",
                 "andbetweenpersons", "firstnameandsurname", "personinmeeting", "teamspiritcheck",
                 "projectcheck", "timekeywordscheck", "onetoonecheck", "broadcastcheck", "performancecheck", "irrelevantcheck",
                 "externalcheck"]
#Currently the two first name ones aren't working not sure why??

X = calendar_data[feature_cols]

#manual  tags
y = calendar_data.tag

# splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# building decision tree model
clf = DecisionTreeClassifier(criterion="entropy", max_depth=10)   # can tune the parameters
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)


# evaluating model
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

end = time.perf_counter()
print(end)


