import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
#from sklearn.ensemble import BaggingClassifier
import checks

# visualise the decision tree
import matplotlib.pyplot as plt
from sklearn import tree 



# read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize', \
			 'teamsize', 'starttime', 'lastsync', 'meetingtitle', 'noguest', 'relevance'] 
calendar_data = pd.read_csv("input_files/input2.csv", header=0, names=col_names)


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
    meeting = checks.dates_and_times_corrector(meeting)
    meeting_list += [meeting]

#defines keyword and irrelevant word lists as well as a dictonary of user companyies
keyWords = ["meeting","discussion", "team", "1:1"]
irreWords = ["block", "busy", "hold", "offline", "office hours", "lunch", "dinner", "edited", "cancel", "leave work"]
company_dict = checks.create_company_dict(meeting_list)


#create empty lists for each of the features
key = []
irr = []
worktime = []
workday = []
users_fullname = []
company_title = []

#populates the feature lists
for meeting in meeting_list:
    key.append(checks.word_list_check(keyWords,meeting))
    irr.append(checks.word_list_check(irreWords, meeting))
    worktime.append(checks.not_worktime(meeting))
    workday.append(checks.not_workday(meeting))
    users_fullname.append(checks.users_fullname(meeting))
    company_title.append(checks.user_company_in_title(meeting,company_dict))

calendar_data['keyword'] = key
calendar_data['irreword'] = irr
calendar_data['not worktime'] = worktime
calendar_data['not workday'] = workday
calendar_data['users fullname'] = users_fullname
calendar_data['company title'] = company_title

#feature selection
feature_cols = ['noguest', 'keyword', 'irreword', 'not worktime', 'not workday', 'users fullname', 'company title']
X = calendar_data[feature_cols]
y = calendar_data.relevance

# splitting data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# building decision tree model 
clf = DecisionTreeClassifier(criterion="entropy", max_depth=10)  # the parameters can be adjusted to improve accuracy
                                                                 # "criterion" : optional (default=”gini”) : gini, entropy
                                                                 # "splitter" : string, optional (default=”best”) : best, random 
                                                                 # "max_depth" : int or None, optional (default=None): int or None
"""
# Use of bagging to optimise -- parameters to be discussed
clf = BaggingClassifier(dclf, n_estimators = 10, max_samples = 0.5, max_features = 0.5, \
                        bootstrap = True, bootstrap_features = True, oob_score = True, \
                        warm_start = False, random_state = 0)
"""
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)



# evaluating model 
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# visualise the decision tree 
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=1000)
tree.plot_tree(clf,
               feature_names = feature_cols, 
               class_names=["y","n"],
               filled = True);
fig.savefig('decisiontree.png')











