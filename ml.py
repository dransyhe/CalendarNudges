import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
from nltk.tokenize.stanford import StanfordTokenizer 


# read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize', \
			 'teamsize', 'starttime', 'lastsync', 'meetingtitle', 'noguest', 'relevance'] 
calendar_data = pd.read_csv("input.csv", header=None, names=col_names)

# tokenise the meetingtitle 
tk = StanfordTokenizer() 
# LATER: feature engineering for meetingtitle 

# feature selection
feature_cols = ['jobrole', 'companysize', 'teamsize', 'meetingtitle', 'noguest'] 
X = calendar_data[feature_cols] 
y = calendar_data.relevance 

# splitting data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# building decision tree model 
clf = DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)

# evaluating model 
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

""" 
Optimising Decision Tree model
criterion : optional (default=”gini”) : gini, entropy
splitter : string, optional (default=”best”) : best, random 
max_depth : int or None, optional (default=None): int or None

clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
""" 

"""
Use of ensembles:

"Bagging":
from sklearn.ensemble import BaggingClassifier
bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
"""

"""
Using other models:

"Naive Bayes":
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

"Random Forest":
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=1000, n_features=4, \
						   n_informative=2, n_redundant=0, \
						   random_state=0, shuffle=False)
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)
print(clf.predict([[0, 0, 0, 0]])) 
"""

