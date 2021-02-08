f_dict = {}

for feature in feature_cols:
    f_list = [f for f in feature_cols if f != feature]
    X_train2 = X_train[f_list]
    X_test2 = X_test[f_list]

    # building decision tree model
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train2, y_train)
    y_pred = clf.predict(X_test2)

    # evaluating model
    f_dict[feature] = metrics.accuracy_score(y_test, y_pred)

small_features = ["usercompany", "noguest", "performancecheck", "irrelevantcheck", "externalcheck", "worktime", "personinmeeting", "userfullname"]
X_train3 = X_train[small_features]
X_test3 = X_test[small_features]

clf = DecisionTreeClassifier()
clf = clf.fit(X_train3, y_train)
y_pred = clf.predict(X_test3)

print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))

