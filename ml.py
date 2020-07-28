import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
#from nltk.tokenize.stanford import StanfordTokenizer 


# read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize', \
			 'teamsize', 'starttime', 'lastsync', 'meetingtitle', 'noguest', 'relevance'] 
calendar_data = pd.read_csv("input.csv", header=None, names=col_names)

# tokenise the meetingtitle and checks if contain keywords, irrelevantwords 
keyWords = ["meeting", "panel", "discussion", "session", "webinar", "team"]
irreWords = ["block", "busy", "hold", "offline", "office hours", "lunch", "dinner", "edited", "cancel", "leave work"]
#tk = StanfordTokenizer() 
calendar_data.meetingtitle = calendar_data.meetingtitle.astype(str)
titles = calendar_data['meetingtitle'].values.tolist()
key = []
irre = [] 
acr = [] 
for i in range(len(titles)): 
	#words = list(tk.tokenize(titles[i])) 
	keyword_f = False
	irreword_f = False 
	"""for j in range(len(words)):
		if words[j] in keyWords:
			keyword_f = True 
		elif words[j] in irreWords:
			irreword_f = True """
	if ("<>" in titles[i]) or ("< >" in titles[i]):
		accrosscompany = True
	else:
		accrosscompany = False
	titles[i] = titles[i].lower()
	for keyword in keyWords:
		if keyword in titles[i]:
			keyword_f = True
			break
	for irreword in irreWords:
		if irreword in titles[i]:
			irreword_f = True 
			break 
	key.append(keyword_f)
	irre.append(irreword_f)
	acr.append(accrosscompany)
#calendar_data['keyword', 'irreword', 'accrosscompany'] = results 
calendar_data['keyword'] = key
calendar_data['irreword'] = irre 
calendar_data['accrosscompany'] = acr 



# feature selection
#feature_cols = ['companysize', 'teamsize', 'noguest', 'keyword', 'irreword', 'accrosscompany'] 
feature_cols = ['noguest', 'keyword', 'irreword', 'accrosscompany'] 
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


