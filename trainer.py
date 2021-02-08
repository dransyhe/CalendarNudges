#imports modules for inputting + cleaning data
import pandas as pd
from cleaner import *
#pd.options.mode.chained_assignment = None

#imports modules for features
from feature_functions import *
from features import *

#imports modules for machine learning
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

#imports modules for visualizing the decision tree
import matplotlib.pyplot as plt
from sklearn import tree

#imports pickle for saving classifier
import pickle

#read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize',
			 'teamsize', 'starttime', 'endtime', 'lastsync', 'meetingtitle', 'noguest', 'tag']
calendar_data = pd.read_csv("input_files/New Tagged Full.csv", header=0, names=col_names)
calendar_data = calendar_data.astype(str)

#generates a meeting_list and company_dict from the calendar_data dataframe
meeting_list = meeting_list_generator(calendar_data)
company_dict = create_company_dict(meeting_list)

#generates a dataframe including all of our features
feature_df = feature_creator(meeting_list, company_dict)

#select which features to use in the ml model
feature_cols = ["noguest", "userfullname", "workday", "worktime", "usercompany", "bracketsafterperson",
                 "andbetweenpersons", "firstnameandsurname", "personinmeeting", "teamspiritcheck",
                 "projectcheck", "timekeywordscheck", "onetoonecheck", "broadcastcheck", "performancecheck", "irrelevantcheck",
                 "externalcheck"]

#creates an imputer for dealing with missing number of guests currently using mean
imp = SimpleImputer(missing_values = np.nan, strategy = "mean")
X = feature_df[feature_cols]
X = imp.fit_transform(X)

#manual  tags
y = calendar_data.tag

# splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#creates decision tree classifier
clf = DecisionTreeClassifier(max_depth = 10)
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))

#saves classifier
with open("multipli_classifier.pkl", "wb") as fid:
    pickle.dump(clf,fid)



