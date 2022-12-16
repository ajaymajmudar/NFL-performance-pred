# NFL Player Production Prediction: From College to the Combine to Success

## Introduction
Every year, the National Football League (NFL) hosts a draft combine for over 300 college players who have declared for the NFL draft. At this combine, players are able to showcase their skills through a variety of physical tests. This event is very important because it allows NFL teams to evaluate players based on numerous metrics in a controlled environment. Teams use the combine, on top of a player’s college stats, to try to predict professional performance. These evaluations on players can win championships or sink a franchise. 

## Problem Description

From our initial analysis and reference research, we believe there is information to be gained from combine data in predicting a player’s success in terms of production in the NFL. However, our research also points to potential shortcomings in single statistics correlating to player production, or to certain positions being more predictable than others[2]. Different models and approaches will shed light on which features might be most informative, as well as which techniques might prove more robust in predicting successful players.


Our project goal is to build models that are fed from NFL combine data in order to extract insights used to accurately project a player’s production in the NFL. We plan to use various metrics from the combine including 40 yard dash time, bench press, vertical leap ability, and much more. These player models will look at player production, which we will define based on Pro Football Reference’s Approximate Value statistic - which assigns a singular number as a player’s valuation - and will also include performance in relevant key stats (ex: sacks for defense players, rushing yards for RB) by player position. Approximate Value and performance will be based upon the performance of a player for their career value. We will investigate how career statistics could inform the selection process to see if certain Combine metrics can predict player value and performance.


The key question is can we utilize physical measurables to reliably identify players who will perform at a high level?


## Data Collection:
We collected our NFL Combine data from a [Kaggle](https://www.kaggle.com/toddsteussie/nfl-play-statistics-dataset-2004-to-present)Dataset, NFL Player Data from another [Kaggle](https://www.kaggle.com/zynicide/nfl-football-player-stats) dataset, and collected the Career Values that were scraped from ProFootball Reference.

### Data Cleaning - Combine and Player Statistics:
In order to combine the NFL combine dataset with the NFL game dataset, there were multiple steps that were taken. First, names were attempted to be matched between the two datasets, and from there a singular new row was created, with reference to the player id in one dataset and the player id in the other dataset. An issue that arose with this was the presence of name duplicates, but this was handled by cross-referencing the name with the college the player attended. Doing this step then created a row representing a player that was in both datasets, and an id to easily access info about the player from each dataset.


Next, the NFL combine stats and cumulative game stats were added for each player. For the players, any game they appeared in was added up together and then averaged by the number of games they played, in order to both obtain career stats and career average stats. Additionally, by investigating the first game and last game the player played in that dataset, the seasons played for the player were determined. Then lastly, in order to be able to identify when a player was drafted so that we could scrape to find the appropriate approximate value for the player, the draft year was searched and added to the dataset for each player.


So, after combining the player game dataset and the combined dataset, we had one cumulative dataset which consisted of the player name, the reference ids in both original datasets, the seasons they played, career total and average stats, combine values, the college players, and the year they were drafted.


### Data Cleaning - Labels and Scraping Approximate Values:
To define and evaluate our model, we wanted to use an aggregate measure that encompassed a player’s production throughout their career. To do this, we relied on the Approximate Value statistic from Pro Football Reference, a website that compiles a myriad of statistics on the NFL. 


We scraped data from the draft pages in this website using pandas (which leverages Beautiful Soup). To do this, we iterated through every draft from 1960 until the present and collected a player’s name, draft year, university, career approximate value and draft approximate value.This was a larger range than our other data sources, and encompassed nearly 20,000 players.


We created labels for our model by finding the median Career Approximate Value from our player sample (which included more players than we had combine statistics for), which had a value of 9. Using this value, we then labeled the players as above or below the median, and proceeded to train our model to classify players as such. The reasoning here being that we want to pick players who on balance are better than others.


When the combine values for each player were loaded in, there were plenty of players with NaN as their Combine measurements for certain tests, which would hurt our ability to predict their success. Therefore, we filled the empty fields with the average for the position. This was the best way to approach this issue since, if we dropped players with NaN Combine values, we would lose a massive part of our dataset. And since the importance of the player would still be captured in his real life measured combine values, the average value replacing the empty sections would not hurt the estimation on whether that player was good or bad based on his actual combine performance. Therefore, each player was lumped into categories for what position they belong to (Ex. LB, QB, RB, WR, etc…) and then averages for all players in that position group were taken (ignoring the players in the position with a nan for that test when taking the average), and these values were used to fill in the empty combine measurements. This way, we could run our predictive and exploratory models using these stats without dropping a massive part of our dataset.

### Methods - Data Pre-processing:
Our combined dataset including career stats and draft combine data consisted of 87 features. 

For target labels, we had two options:
  * Career AV: Approximate value of a player throughout his career
  * Draft AV: Approximate value of a player for the team that drafted him

Backward selection: We ran forward and backward selection on our data. However, since the data is correlated and backward selection wasn’t too expensive to run, we decided to focus on the features outputted from backward selection.

### Methods - Analytical:
Supervised:
  -  Logistic Regression: Classifier of Approximate Values split into categories (histogram)
  - By Position Logistic
  - Linear Regression Attempt
Unsupervised:
  - K-means clustering: to help find patterns in the data

### Feature Selection:
Backward selection was run on a merged combine and draft Approximate Value data set, i.e. Approximate Value (AV) for a player on the team they were originally drafted to, as well as on a merged combine and career Approximate Value data set. These approximate values come from the Pro-Football Reference statistic that calculates the approximate value a player provides in their career.


Initially, running backward selection with the two target variables and 0.05 significance level, the method chose around 35 features. In this case our model had an R squared value of 0.67. We have decided that looking at Career AV made more sense, because the point of the draft is to get the player that can potentially be the most valuable to your team long term. We have also looked at just the features from draft combine data. In this analysis, the five significant features that we have found as a result of backwards elimination were 40 dash, 3 cone, age, vertical, and broad.

| Description of Selection Method Used  | Selected Features |
| ------------- | ------------- |
| Features selected by forward selection for career AV using only draft combine data  | 40_dash, Age, weights, heights  |
| Features selected by backward selection for career AV using only draft combine data  | heights, weights, Age, broad  |
| Features selected by forward selection for draft AV using only draft combine data  | 40_dash, 3_cone, Age, shuttle, vertical, broad  |
| Features selected by backward selection for draft AV using only draft combine data  | Age, 40_dash, vertical, broad, 3_cone  |

### Logistic Regression - Results:
The significant features from backward feature selection above - age, 40 yard dash time, vertical jump, broad jump, 3 cone drill - were run through a logistic regression supervised learning model to classify players. Approximate Values were categorized based on a representation of our data as a histogram, not factoring in players who don’t have an Approximate Value. We decided on a binary classification of a player being in the top half of his peers based on the career Approximate Value. The median career Approximate Value was 9. Using logistic regression, we determined that with approximately 60% accuracy a player in the top half of the average career Approximate Values could be predicted based on the above selected features. This analysis can prove to be very valuable because if NFL teams want to attempt and predict which players will have the most valuable careers, then they can place an emphasis on these metrics at the draft combine.


According to the model screenshots below, the accuracy to which we could predict a player’s performance was around 60%. This is a decent score to start off with, but we believed this could be improved greatly. 

!["Model Results"](Data_Cleaning/images/model_results.png)


In order to determine the success of our features on predicting whether a player was good or not, we plotted each feature vs the probability that the player with that feature value was a good player. To reiterate, the features we selected were age, 40-yard dash times (a test of speed), vertical jump (a test of jumping ability), broad jump ( a test of explosiveness), and 3 cone drill (a test of agility).

First, we investigated the age of the players. Most players were drafted from the range of 20-24 years old, which makes sense due to this being the time most people finish up college and are ready to enter into the pros. However, there were definitely some outliers, such as Brandon Weeden, a quarterback who went through the NFL combine at age 28. As can be seen, there is a very noticeable correlation between the age that a player was drafted and the probability that they are a good player. The younger the player is, the better the player is likely to be. This makes sense as the more talented a player is, the more likely they are to leave college early and at a younger age, and enter the NFL.

!["Age vs Prob"](Data_Cleaning/images/age.png)

Next, we investigated the 40 yard dash. The trend for the 40 yard dash time is harder to see, but there is a very slight downward trend in the data where the probability of a player being considered good decreases as a player’s 40 yard dash time is slower. This makes sense as well since the faster a player is (since that is what this test inherently measures), the more likely they will be to get open and outrun other players, and therefore the more likely they are to be successful.

!["40 Dash vs Prob"](Data_Cleaning/images/40yard.png)

The third feature under investigation was vertical jump. This feature also has a noticeable correlation where the higher the vertical jump, the more likely a player is to be considered good. However, there is a large block of players in the middle, between a vertical of 30 and 40, where it is hard to determine a correlation between the vertical jump and the probability of success for the player. Therefore, while there is a loose noticeable trend for this test, it is not as strong as for the 40 yard dash or the age of the player.

!["Vertical vs Prob"](Data_Cleaning/images/vertical_plot.png)

The fourth feature under investigation was the broad jump. As shown in the first plot, we had a pretty significant outlier where a certain player had a broad jump of 8 inches. This was affecting the regression fit of the broad jump in predicting player success and additionally was skewing the plot in a way where actionable items could not be read from it. So, we removed this outlier data point, and replotted the broad jump among all the players in the second plot shown above. Here, once again a trend can be noticed that the higher broad jump results in a player more likely to be considered successful. However, while this trend is definitely noticeable for a broad jump less than 100 inches (that a player is unlikely to be successful) and for a broad jump higher than 125 inches (that a player is likely to be successful), the middle horde of players between 100 and 125 inches makes a less convincing case that broad jump is a solid estimate of the likelihood of player success. From this plot, it appears that extreme broad jump values are good estimates of player success, while intermediate values do not add much information.

!["Broad with Outlier"](Data_Cleaning/images/broad_w_outlier.png)
!["Broad vs Prob"](Data_Cleaning/images/broad_plot.png)

The last feature under investigation was the 3 cone drill. As can be seen, there is not really any clear correlation between the 3 cone drill and the probability of player success. No matter whether the score was high or low, there was a pretty even spread of players with the same score that had a high and low probability of being good, which doesn’t provide us with much new information.

!["3 Cone vs Prob"](Data_Cleaning/images/3conedrill.png)

!["Coefficients"](Data_Cleaning/images/coef.png)

Above are the coefficient scores for the features age, 40 yard dash, vertical jump, broad jump, 3-cone drill, and bench press respectively. Bench press was added as an extra investigative measure in addition to the features obtained from forward and backwards selection, but it was determined not to be too significant, which is why it was not brought up under discussion. The above scores represent the given features in order. First was age, then 40 yard dash, then vertical jump, followed by broad jump, and then lastly 3-cone drill. Looking at the absolute value of the weights, with a weight closer to 1 being more preferable, it makes sense that age and 40 yard dash provided the best prediction for player success based on the graphs seen above. However, with a score of around 0.35, they still are not great estimates for player success. The broad jump and vertical jump did not serve as good estimates at all of player success, and this may be due to the fact that while those tests were good at estimating player success at the extremes, they were poor in the middle section of the data since those plots consisted of a horde of player data in the middle. And then lastly, the 3 cone drill had a relatively decent score, in comparison to the other features, which is interesting to note since from the plot it did not appear as if the graph provided any clear prediction of player success. From this analysis, it appears as if age and the 40 yard dash time are the two most important features in predicting the likelihood of player success. 

!["Model Metrics"](Data_Cleaning/images/metrics.png)

According to the results, our accuracy score was around 60%, but the R2 score was low. We believe that the R2 score is low because using one model for players of different positions does not produce an accurate model. Our precision score is 0.56, which means 0.56 of all positive-predicted data points are true positives. Our recall value is a striking 0.27, meaning that the model predicts only 0.27 percent of good players as good players, while most of them are predicted as bad. Based on these precision and recall scores, the F1-score we get is 0.36. 

!["AUC Plot"](Data_Cleaning/images/auc_plot.png)

The ROC-AUC performance metric essentially measures the portion of classes classified correctly. ROC is a probability curve, and AUC measures the degree to which the model can separate between the two classes - above the median career Approximate Value and below the median career Approximate Value. This plot graphs the tradeoffs between the true positive rate and the false positive rate. An AUC value of 0.5 indicates that the model lacks class separation, so since our model has an AUC score of 0.61, this means that while our model recognizes the difference between classes in some cases but not in most situations. 

!["Recall Confusion Matrix"](Data_Cleaning/images/confusion_matrix.png)

The confusion matrix looks at true positives, (where the predicted values matched the actual values) false positives, (predicted that the player was above the career Approximate Value median but was not) true negatives (predicted that the player was not above the median career Approximate Value and the player was not) and false negatives (predicted that the player was not above the median career Approximate Value but the player actually was). 


Given the recall values, we can see that the model classifies 85% of players labeled as bad (0) correctly. On the other hand, the recall for good players (1) is only 27%. This means that our model fails to predict a lot of good players accurately. 

### Logistic Regression - Analysis:
In analyzing the logistic regression model, we saw that the model is biased towards labeling players as bad, i.e. 0 or below the median. One reason for this is that some positions naturally have lower approximate values, just because not all positions are of equal importance in football, and our model just labels these players as bad, even if their value is good for their position. 


This leads into our next point that AV’s are relative to position, meaning that a comparison between players in different positions creates inaccuracy. Different positions inherently have different Combine results that matter to them. For example, for a wide receiver and a running back, speed and agility are very important because they will get the football and have to make a move to get open/break tackles. Therefore, items such as the 40 yd dash or the 3 cone drill would be important. However, for a player such as offensive or defensive lineman, the bench press will be far more important as their role is to stand strong and make sure the other lineman does not move past them/they can move past the other player. 


Our predictive model is not accurate enough to be used in a practical sense in its current state. We have considered improvements including additional work to pull in Approximate Values for players who were missing this measure, add additional measures to the selected Combine features that we used for our logistic regression model and even could add Wonderlic, a cognitive test, scores to our data set. Moreover, one issue with our model is that with the binary classification, there were more instances with a zero classification, i.e. with Approximate Values below the career median. We decided to institute positional analysis in our models as our next step to see if those new positionally specific features will produce a better model regarding approximate career value. 

### Logistic Regression By Position - Results:
As mentioned in the analysis of our initial logistic regression model, our data set contains more instances of players with a 0 binary classification of their Approximate Value, i.e. the player’s AV falls below the median. Therefore, we hypothesized that low recall of our model, 27% for correctly classifying a player as having an AV above the median, was partially due to disparity among positions. Some positions naturally have a lower median AV and aren’t as comparable to positions such as quarterback which generally has a higher median AV in proportion to its importance on the field. Additionally, certain combine metrics are more relevant to one position than to another. The chart below is representative of our data set and displays career Approximate Values by position on a dual axis with the prevalence of data points at our disposal of each position. This shows that the average AV’s are not uniform for each position. For these reasons, we decided to run a logistic regression model through subsets of our data, split by positions, and try to achieve higher accuracy in prediction. 

!["Position vs AV"](Data_Cleaning/images/Postion_vs_Av.png)

Our predictive model again classified players as 0 or 1, i.e. below the position’s respective median or above it respectively. Median values were recalculated per position. The same four features from the initial feature selection were used in the logistic regression by position models - age, 40 yard dash, vertical, broad and 3 cone drill. The three main positions analyzed below are quarterback, defensive back and wide receiver. 

The median AV for a quarterback (QB) is 8. Our results in the chart to the right show a recall of 61% in classifying a QB as below median AV and 67% classifying above 8 AV. Our precision score is 0.64, which means 64% of all positive-predicted data points are true positives based on our ground truth values. The f-score from the precision and recall score is around 0.65, where a score of 1 is 100% correct classification. This means our model is a little bit better than a baseline model which guesses the same classification for each data point that would result in an f-1 score of around 0.5.

!["QB Stats"](Data_Cleaning/images/qb_logit_score.png)

The ROC-AUC chart shows an AUC value of 0.69, which is better than our first, more general iteration of the logistic regression model which resulted in a 0.61 AUC value. The ROC curve represents the separability of our data from the red line, a.k.a. a baseline model which has a 50/50 chance of correct classifications. Our model is 38% better than this baseline model

!["QB ROC"](Data_Cleaning/images/auc_plot_qb.png)

The median career AV for a wide receiver (WR) is 7. On running the logistic regression model on the wide receivers in our data set, precision remained close to that of the original model, .61. Recall also sat at 50% correct classification of WR’s under the 7 AV and  71% over the median. The f-score, from precision and recall, is 60%, which is only 20% better than a baseline, coin toss model. 

!["wr Stats"](Data_Cleaning/images/wr_logit_score.png)

The ROC plot is similar to that of our original model, slightly better with an area under the curve of 0.64 compared to 0.61 and slightly worse than the AUC of the QB model, 0.69. 0.64 indicates that while our model recognizes the separability of the two classes in our data, it does not correctly identify a significant majority of defensive backs as above or below the median career AV. 

!["wr ROC"](Data_Cleaning/images/auc_plot_wr.png)

Lastly, defensive backs (DB) have a median career AV of 12. This model only achieved an accuracy of 57%, i.e. 57% of players were correctly categorized as above or below the median AV, according to the five key Combine features, compared to their ground truth labels. 

!["db Stats"](Data_Cleaning/images/db_logit_score.png)

The AUC value in the ROC chart for defensive backs is the lowest of the general, quarterback and wide receiver models. An AUC of 0.59 is only marginally better than the baseline. As evidenced by the shape of the blue curve in the plot, it lies pretty close to the red line and does not separate itself significantly at any point in the chart. 

!["db ROC"](Data_Cleaning/images/auc_plot_db.png)

### Logistic Regression By Position - Analysis:
Since AV is calculated relative to a player’s position, it made sense to do another iteration of the logistic regression model on each position separately. However, the logistic regression models separated by position had low recall and accuracy scores, with the quarterback model reaching the highest accuracy of 64%. Since the quarterback position is arguably the most important on the field, quarterbacks are generally held to a higher standard with less variability among them, also evidenced in our data set. We believe this is the primary reason why the quarterback model had the highest accuracy, compared to the general model and the other position specific models. 


The same features were used from our original feature selection in the position specific models; re-running feature selection for each position could lend additional accuracy to these models. Splitting by position did help alleviate some of our issues with the model having a preference for predicting players as below median as it spread out the zero instances more evenly over positions. However, this was still a problem, and in the future, we would look into a way to oversample the 1, above the median, instances. 


Adding more features to our dataset, such as Wonderlic cognitive scores and college statistics would make our model more accurate. When looking to draft players, coaches look at college statistics, not just the Combine, so this would be more accurate to reality, but also indicates that the Combine alone can’t accurately predict whether a player will perform above or below the median NFL player for their drafted team. 

### Linear Regression By Position - Results:
We also implemented a linear regression model on our data set split by player position. As the logistic regression models for quarterbacks and wide receivers were the most accurate, those are also the main two models we focused on for linear regression. The wide receiver model focused on age, 40 yard dash and arm length as independent variables to predict a WR’s Approximate Value.

!["WR Lin Reg"](Data_Cleaning/images/wr_lin_reg.png)

R2 measures the strength of the relationship between the selected features and AV, an R2 value of .058 is very low and indicates that the model doesn’t do a good job of explaining variation of AV from the mean; only 5.8% of AV variation can be explained by the independent variables. As can also be seen in the image to the right, according to the Jarque-Bera test and the Kurtosis measure, it is very unlikely that the data is normally distributed. Another important measure is the F-statistic, the probability of the F-statistic should be close to zero to indicate significance of the data and reject the null hypothesis, which states that the independent variables do not have a significant effect on the dependent variable. While the value in the table to the right appears relatively low, it should be much closer to zero to suggest significance. This is essentially saying that the model with the three independent variables, age, 40 yard dash and arm length, isn’t significantly different than a model with no independent variables. The OLS Regression results also give the coefficient value for each independent variable. A large absolute value for the coefficient is better, and the sign of the coefficient indicates the direction of the independent variable’s effect. Here, the 40-yard dash has the highest impact, and lower times indicate higher Approximate Values.

The regression plots from the 40-yard dash are shown below. In these plots, while we see that the fitted line does follow the very general shape of the observed data points, it isn’t a direct or close relationship. The standardized residuals plot shows the difference between observed and predicted points, and here, while there is no clear pattern, the residuals aren’t evenly distributed as high or low predictions and are not clustered, meaning that while 40-yard dash is the best indicator for a wide receiver’s AV from the three tested independent variables, it still isn’t an accurate predictor. 40-yard dash, by itself, can’t predict a wide receiver’s AV.

!["WR 40 Dash"](Data_Cleaning/images/wr_dash_plots.png)

The regression plots for arm length prediction of Approximate Value are also below. Arm length had the lowest coefficient score. The shape of the data below corroborates this point. The range of arm lengths is pretty narrow and most fall along 31.75 inches, these stacked data points are hard to fit a regression line to and don’t provide much additional information to a wide receiver’s Approximate Value.

!["WR Arm"](Data_Cleaning/images/wr_arm_plots.png)

Lastly, for the wide receiver model, the independent variable age’s regression plots are below. The partial regression plot shows a line of best fit that very loosely follows the shape of the data. From the residuals plot, we don’t see any trends in the data, indicating a lack of room for improvement in fitting a regression line to this model. Additionally, the CCPR plot takes into account the other independent variables. Since the line of best fit barely changes, this shows that age doesn’t have a strong impact on the Approximate Values of wide receivers.

!["WR Age"](Data_Cleaning/images/wr_age_plots.png)

The results from the linear regression model for quarterbacks are shown to the right. Age, bench and 40 yard dash were the three independent variables tested in this model. The R2 value for this model was 0.182. This indicates that 18.2% of the variation in Approximate Values of a quarterback can be explained by the independent variables. This is not a high or good R2 by any means, but it is better than that of the wide receiver model. Again, we see using the Jarque-Bera test that there is a very slim chance that the data is normally distributed. The Omnibus value not being close to 1 also indicates that the errors are not normally distributed. The probability of the F-statistic should be close to zero to indicate significant data and reject the null hypothesis. While the value in the table to the right is low, especially relative to the F-statistic in the wide receiver model. However, this is still not as close to zero as we would like it to be. On a more positive note, the Durbin-Watson test produces a value between 1 and 2, which implies that the variance of errors is constant. According to the coefficient values for the independent variables, 40 yard dash has the highest impact  followed by age, both of which have inverse relationships with Approximate Value.

!["qb Lin Reg"](Data_Cleaning/images/qb_lin_reg.png)

The regression plot for the 40-yard dash is shown here. In accordance with the magnitude of its coefficient, the regression line generally follows the spread of the data. Additionally, in the residuals plot, the standardized residuals are somewhat clustered around the center of the graph. Since there is no clear pattern in these data points, there isn’t any easily discernible room for improvement in this linear regression model.

!["qb 40 Dash"](Data_Cleaning/images/qb_dash_plots.png)

The regression plots for age are shown below. Age has an inverse relationship with Approximate Value. As in the case of the 40-yard dash, the regression line does fit the general shape of the data. In the residuals versus age plot, we don’t see a trend in the data points, which doesn’t suggest additional room for improvement in the model. 

!["qb age"](Data_Cleaning/images/qb_age_plots.png)

Lastly, the least impactful independent variable on Approximate Value was bench press ability. The regression plots for which are below. In this case, the majority of data points all seem to fall along the same point, making it difficult to accurately fit a regression line. The residuals don’t have a true trend line. Clearly, the bench press feature isn’t best suited for a linear regression model.

!["qb bench"](Data_Cleaning/images/qb_bench_plots.png)

### Linear Regression By Position - Analysis:
The quarterback linear regression model performed better than the wide receiver model, with an R2 of .182 versus .058, but neither of these models are good at assigning continuous Approximate Values to players based on Combine features. For both models, the 40-yard dash was most impactful, based on its coefficient. It makes sense that the quarterback model would perform better than the wide receiver model. Quarterbacks hold a very important position on the field and as such are held to a higher standard. This leads to lower variability among QB Combine, and likely performance as well, statistics. We saw this in our data set as well. 
Both models had incredibly high condition numbers, 973 (QB) and 2280 (WR), meaning that the matrices are ill-conditioned, and there are collinearity errors. Comparatively, the QB model seems to have less correlation in our data. The heat maps shown below exhibit this. We can tell from these images that the wide receiver data would be more difficult to separate. Correlation adds error to linear regression models, and we can attribute some of the poor prediction in both models to the lack of independence in Combine features. This is also the reason, analytically, that the quarterback model performed better than the wide receiver model.

!["qb heat"](Data_Cleaning/images/qb_heatmap.png)
!["wr heat"](Data_Cleaning/images/wr_heatmap.png)

### K-means Model - Results:
After implementing the supervised regression models, we decided to see if we could find better correlations and results with an unsupervised method. K-means clustering is a reasonable approach for this because we were able to perform clustering of the players based on their NFL Combine statistics. We believe positional clustering would be an important aspect to look at to gain information about players and see if players who do cluster well together have similar Combine measurements. We analyzed the clusters through 4 ways: F-measures, Silhouette score, Distortion score, Davies-Bouldin Index. The plots below show the respective clustering for each method. F-measures peaked at clustering of 4 clusters, Distortion score produced a clustering of 4 through a visual elbow method analysis, and Silhouette score and Davies-Bouldin Index indicated that the lowest number of clusters resulted in the best score. Based on visual inspection, we decided to go with 4 clusters. 

!["F vs Cluster"](Data_Cleaning/images/FmeasuresVClusters.png)
!["Sill vs Cluster"](Data_Cleaning/images/SillhoutteVClusters.png)
!["Distortion vs Cluster"](Data_Cleaning/images/DistortionVClusters.png)
!["DB vs Cluster"](Data_Cleaning/images/DaviesBouldinVClusters.png)

When running our model with 4 clusters, it was very clear that weight was a divider in the clusters, and it served as the only significant divider. This can clearly be shown in the plots below as the groups evenly divided when weights were used as the x axis, but with vertical as an x axis the clustering is not so clear.

!["Weight Clusters"](Data_Cleaning/images/WeightsV40dash.png)
!["Vertical Clusters"](Data_Cleaning/images/40dashVVertical.png)

Positions that play against each other in the actual game (WR against DB) also clustered very well together. Through our plots below we show a player positional analysis of strong cluster correlation. There is a cluster of offensive linemen (Center (C), Guard (G), and Tackle (T)) which has over 50% of the players in that position in that cluster to show a strong correlation. There is another cluster of Defensive Ends (DE). Another cluster of Defensive Back (DB), Kicker (K), and Wide Receiver (WR). A final cluster is a variety of positions such as Fullback (FB), Linebacker (LB), Punter (P), Quarterback (QB), Running back (RB), Tight End (TE).

!["12 Pos"](Data_Cleaning/images/posRecallClusters12.png)
!["13 Pos"](Data_Cleaning/images/posRecallClusters34.png)

### K-means Model - Analysis:
Positions that play against each other in the actual game (WR against DB) also clustered very well together. Through our plots below we show a player positional analysis of strong cluster correlation. There is a cluster of offensive linemen (Center (C), Guard (G), and Tackle (T)) which has over 50% of the players in that position in that cluster to show a strong correlation. There is another cluster of Defensive Ends (DE). Another cluster of Defensive Back (DB), Kicker (K), and Wide Receiver (WR). A final cluster is a variety of positions such as Fullback (FB), Linebacker (LB), Punter (P), Quarterback (QB), Running back (RB), Tight End (TE). 

### Comparison of Models:
Comparing our initial logistic regression attempt with the logistic regressions done on subsets based on player positions, we see that while models for quarterbacks and wide receivers have done better, the model for defensive backs has done worse than the model for the entire data. From this fact, one may speculate that the draft combine is better for identifying promising offensive players than identifying defensive ones. We can only definitively say that while splitting by position helped marginally, it did not make our model good at predicting a player’s AV category. Going forward, we would take steps to redo feature selection for each position as well and run logistic regression using these new, position specific features.


One problem that we mentioned about the initial logistic regression method was the low recall score of 0.27. We thought that this may be because average career approximate values changed from position to position. Looking at specific positions seems to have in fact helped with that problem. For QBs, for instance, the model’s recall score has risen to 0.61, for WRs to 0.50, and for DBs to 0.52. The recall score is not much lower than other metrics for any of these models. We believe that this problem has remained due to the fact that Approximate Value is calculated more on a performance basis that, as have seen, can’t reliably be predicted by the Combine. Also, there still remains the issue of bias towards categorizing a player as below the median AV.


The linear regression models we ran were not accurate and failed to appropriately fit a line to the data. At the same time however, the residuals plots did not have any clear trends, indicating that our linear regression models were fitted as best as possible for the given independent variables. Linear regression was done by position, and we highlighted the quarterback and wide receiver models. The quarterback model performed best, for an R2 value of 18%. Our results also showed that the independent variables were insignificant, meaning that the model didn’t perform better compared to one without independent variables. The logistic regression models seem to have been more successful than the linear regression models, but neither were good discrete nor continuous classifiers.


From the supervised models, we decided to run the K-means algorithm on the draft Combine data which showed that when players are separated into 4 clusters, there are strong trends between clusters and player positions. Since Combine features were unsuccessful in predicting Approximate Values, we pivoted to looking into whatever significant and useful insights could be pulled from the data. The K-means model provided information that NFL teams can use to understand if a player is playing in the best possible position and to allocate talent appropriate across positions, especially for generalized or cross functional players.

### Conclusion
Across all of our models and most positions, the 40-yard dash and age were the two most prevalent features to predict Approximate Value. In the linear and logistic regression models, 40 yard dash and age were the most impactful independent features for the continuous and for the binary classifications. Despite their relative significance, neither of these features, even combined with more features in the logistic model, could predict a player’s AV better than 64% in the logistic regression for quarterbacks model; 64% isn’t impressive compared to a baseline model having 50% accuracy, essentially a coin toss. 


The linear and logistic regression models did perform better when split into player positions as we predicted after running a logistic regression model on the entire dataset. This is in part due to the fact that players with zero instances, i.e. below the median Approximate Value, were no longer as heavily represented in the dataset and were spread across multiple, separate data sets. At the end of the day, Approximate Value could not be reliably predicted from either of these models. Approximate Value is calculated from a holistic, performance based stance, and it appears that there aren’t any quick shortcuts in the Combine data that can predict AV.


The logical next steps would be to see if Combine stats could predict player production at a more granular level - i.e. investigating position specific measures such as pass completion percentage for quarterbacks. These could have a more direct correlation to biometrics and tested physical ability. We could also re-run the position specific linear and logistic regression models after performing feature selection for each position. However, the median approximate values and the key statistics across positions do not differ that greatly, especially if only considering offensive or defensive players. We do not expect that this would improve the models to the extent that they could be reliably used by coaches. 


After analyzing these supervised methods, the K-Means model was able to extract useful information from Combine data, albeit unrelated to Approximate Value. We found that clusters of Combine features did contain differentiable player positions. This can be used to determine the best fit of position for players to most effectively allocate skill and resources.


All in all, we have discovered that the NFL Combine data is not as useful as many may believe it to be when it comes to predicting player performance. The scores and metrics that our models provided us did not have a significant correlation with player performance. We discovered that there was some potential use for the model when it came to clustering players based on their metrics, and this can be helpful for grouping players into their ideal positions. 


## References
Ellinger, B. (2020, June 11). NFL drafting efficiency, 2010-2019. Football Outsiders. Retrieved October 5, 2021, from https://www.footballoutsiders.com/stat-analysis/2020/nfl-drafting-efficiency-2010-2019.

Patankar, A., & Monga, A. J. (n.d.). Projecting NFL quarterback readiness final.Projecting NFL Quarterback Readiness. Retrieved October 4, 2021, from http://cs229.stanford.edu/proj2017/final-reports/5231213.pdf.

Kuzmits, F. E., & Adams, A. J. (2008). The NFL combine: Does it predict performance in the National Football League? Journal of Strength and Conditioning Research, 22(6), 1721–1727. https://doi.org/10.1519/jsc.0b013e318185f09d

Robinson, J., Forbes, C., & Rowe-Anderson, H. (n.d.). Predicting a NFL Wide Receiver's Draft-ability. Retrieved October 4, 2021, from https://github.gatech.edu/pages/jrobinson339/MLGroup49Project.github.io/.

Langaroudi, M., & Yamaghani, M. (n.d.). Home Browse Journal Info Guide for Authors Submit Manuscript Reviewers Contact Us Sports Result Prediction Based on Machine >Learning and Computational Intelligence Approaches: A Survey. Journal of Advances in Computer Engineering and Technology, 5(1), 27–36. </p>
Wheeler, K. (n.d.). Predicting NBA Player Performance. Retrieved October 4, 2021, from https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.278.4919&rep=rep1&type=pdf.

Yang, J. W., Hodax, J. D., Machan, J. T., Krill, M. K., Lemme, N. J., Durand, W. M., Hoffman, J. T., Hewett, T. E., & Owens, B. D. (2019). Factors affecting return to play after primary achilles tendon tear: A cohort of NFL players. Orthopaedic Journal of Sports Medicine, 7(3), 232596711983013. https://doi.org/10.1177/2325967119830139 

Martins, B. G. P. (2019, February 6). Predicting the risk of injury of professional football players with machine learning. Handle Proxy. Retrieved October 4, 2021, from http://hdl.handle.net/10362/62419. 

Ruiz-Pérez, I., López-Valenciano, A., Hernández-Sánchez, S., Puerta-Callejón, J. M., De Ste Croix, M., Sainz de Baranda, P., & Ayala, F. (1AD, January 1). A field-based approach to determine soft tissue injury risk in elite futsal using novel Machine Learning Techniques. Frontiers in Psychology. Retrieved October 4, 2021, from https://www.frontiersin.org/articles/10.3389/fpsyg.2021.610210/full.

Ige, Oluwabukun. Logistic Regression in SciKit Learn, A step by step Process Retrieved November 16, 2021, from https://medium.com/@oluwabukunmige/logistic-regression-in-scikit-learn-a-step-by-step-process-32f546241f32