import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
#from nltk.tokenize.stanford import StanfordTokenizer 
import checks


# read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize', \
			 'teamsize', 'starttime', 'lastsync', 'meetingtitle', 'noguest', 'relevance'] 
calendar_data = pd.read_csv(r'C:\Users\Issy H\Documents\Machine learning\CalendarNudges-master(2)\input2.csv', header=0, names=col_names)


#creates lists of username, companyname, title, noguests, timezone and startime
calendar_data.username = calendar_data.username.astype(str)
usernames_list = calendar_data.username.values.tolist()

calendar_data.companyname = calendar_data.companyname.astype(str)
companyname_list =  calendar_data.companyname.values.tolist()

calendar_data.meetingtitle = calendar_data.meetingtitle.astype(str)
titles_list = calendar_data.meetingtitle.values.tolist()

calendar_data.noguest = calendar_data.noguest.astype(int)
noguest_list = calendar_data.noguest.values.tolist()

calendar_data.timezone = calendar_data.timezone.astype(str)
timezone_list = calendar_data.timezone.values.tolist()

calendar_data.starttime = calendar_data.starttime.astype(str)
starttime_list = calendar_data.starttime.values.tolist()

#calendar_data_endtime = calendar_data.endtime.astype(str)
#endtime_list = calendar_data.endtime.values.tolist()



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
    #meeting['endtime']=endtime_list[i]
    meeting = checks.dates_and_times_corrector(meeting)
    meeting_list += [meeting]

#Yu he code included 



#defines keyword and irrelevant word lists as well as a dictonary of user companyies
keyWords = ["meeting","discussion", "team", "1:1", "1-1", "weekly", "monthly", "update", "All Hands Meeting", "Bi-Weekly"]
irreWords = ["block", "busy", "hold", "offline", "office hours", "lunch", "dinner", "edited", "cancel", "leave work"]
company_dict = checks.create_company_dict(meeting_list)


#create empty lists for each of the features
key = []
irr = []
worktime = []
workday = []
users_fullname = []
company_title = []
#duration = []


#populates the feature lists
for meeting in meeting_list:
    key.append(checks.word_list_check(keyWords,meeting))
    irr.append(checks.word_list_check(irreWords, meeting))
    worktime.append(checks.not_worktime(meeting))
    workday.append(checks.not_workday(meeting))
    users_fullname.append(checks.users_fullname(meeting))
    company_title.append(checks.user_company_in_title(meeting,company_dict))
    #add meeting length as feature
    #duration.append(checks.long_duration(meeting))

calendar_data['keyword'] = key
calendar_data['irreword'] = irr
calendar_data['not worktime'] = worktime
calendar_data['not workday'] = workday
calendar_data['users fullname'] = users_fullname
calendar_data['company title'] = company_title
#calendar_data['duartion'] = duration

#feature selection
feature_cols = ['noguest', 'keyword', 'irreword', 'not worktime', 'not workday', 'users fullname', 'company title']#add duration 
X = calendar_data[feature_cols]
#manual relevance tags 
y = calendar_data.relevance

# splitting data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# building decision tree model 
clf = DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)


# evaluating model 
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))






