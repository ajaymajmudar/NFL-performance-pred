
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import *
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
import numpy as np


player_dataset = pd.read_csv("Player_Dataset_With_Averages.csv")

player_dataset.describe()

draft_df  = pd.read_csv("draft_AV_table_60_21_College.csv")

total_player_with_av = pd.merge(player_dataset, draft_df, left_on = ["name", "position", "college"], right_on = ["Player", "Pos", "College/Univ"], how='left')

total_player_with_av["Missing"] = total_player_with_av["Player"].isna()

total_player_with_av.describe()

print(np.sum(total_player_with_av["Missing"]), np.count_nonzero(total_player_with_av["Missing"]), total_player_with_av["Missing"].size)

# Load Dataset 
input = total_player_with_av
#features_cav=['season_played', 'Age', 'Pick', 'passing_touchdowns', 'defense_tackles', 'receiving_yards', 'defense_sacks', 'defense_interceptions', 'rushing_yards', 'weights', 'rushing_attempts', 'Rnd', 'receiving_yards_average', 'receiving_touchdowns', 'age', 'hands', 'rushing_touchdowns', 'receiving_receptions', 'passing_sacks_yards_lost', 'passing_rating', 'passing_yards', 'passing_interceptions', 'heights', 'passing_attempts', 'rushing_touchdowns_average', 'punt_return_yards', 'receiving_touchdowns_average', 'passing_sacks_average', 'passing_touchdowns_average', 'field_goal_makes_average', 'defense_tackle_assists', 'passing_sacks', 'punt_return_attempts_average', 'passing_completions']
#features_dav= ['season_played', 'Age', 'Pick', 'defense_tackles', 'receiving_yards_average', 'defense_sacks', 'passing_sacks_yards_lost', 'defense_interceptions', 'weights', 'rushing_yards', 'rushing_attempts', 'Rnd', 'receiving_yards', 'hands', 'age', 'passing_interceptions', 'passing_yards', 'passing_rating', 'rushing_yards_average', 'receiving targets', 'receiving_touchdowns', 'passing_touchdowns_average', 'passing_sacks_average', 'passing_touchdowns', '3_cone', 'vertical', 'defense_tackle_assists', 'defense_sacks_average', 'heights', 'passing_completions', 'defense_interceptions_average', 'receiving_touchdowns_average']

input.to_csv("merge_with_average.csv")

features_cav = ["age", "40_dash", "vertical", "broad", '3_cone', "DrAV"]

print(input.shape, "Before")

input_cav= input[input[features_cav].notnull().all(axis=1)]

print(input_cav.shape, "After")

input_cav["TopAV"] = np.where(input_cav["DrAV"] >= 25, 1, 0)

final_features = ["age", "40_dash", "vertical", "broad", '3_cone']

X=input_cav[final_features]
#print(input_cav)

y = input_cav['TopAV']
#print(X)


X.head()

##Validation

Xval=X.values

print(Xval)
print(len(Xval))
yval=y.values
print(yval)
print(len(yval))
X_train, X_validation, Y_train, Y_validation = train_test_split(Xval, yval, test_size=0.20, random_state=1)


##Model

model=LogisticRegression(solver='liblinear',multi_class='ovr')
kfold = StratifiedKFold(n_splits=5, random_state=1, shuffle=True)
cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')

print(cv_results)

model = model.fit(X_train, Y_train)

ypred = model.predict(X_validation)
confusionMatrix = confusion_matrix(Y_validation,ypred)

model.score(X_validation, Y_validation)

r2_score(yval,ypred)
print(r2_score)

##Metrics
#accuracy score
acc = klearn.metrics.accuracy_score(yval, ypred, normalize = True)

#ROC score
roc = sklearn.metrics.roc_auc_score(yval, Y_train)

#precision, recall, f1
f1 = sklearn.metrics.f1_score(yval, ypred)
prec = sklearn.metrics.precision_score(yval, ypred)
recall = sklearn.metrics.recall_score(yval, ypred)

#print plot
#https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic.html
