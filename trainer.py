#imports modules for inputting + cleaning data
import pandas as pd
from cleaner import *
#pd.options.mode.chained_assignment = None

#imports modules for features
from feature_functions import *

#imports modules for machine learning
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

#imports modules for visualizing the decision tree
import matplotlib.pyplot as plt
from sklearn import tree

#read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize',
			 'teamsize', 'starttime', 'endtime', 'lastsync', 'meetingtitle', 'noguest', 'tag']
calendar_data = pd.read_csv("input_files/New Tagged 3.csv", header=0, names=col_names)
calendar_data = calendar_data.astype(str)

meeting_list = meeting_list_generator(calendar_data)
company_dict = create_company_dict(meeting_list)

