#set the variable filename for the path of your csv file
filename = "input_files/New Tagged Full.csv"

import pickle

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

#opens classifier
with open("multipli_classifier.pkl", "rb") as fid:
    clf_loaded = pickle.load(fid)

#read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize',
			 'teamsize', 'starttime', 'endtime', 'lastsync', 'meetingtitle', 'noguest', 'tag']
calendar_data = pd.read_csv(filename, header=0, names=col_names)
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


y_pred = clf_loaded.predict(X)
