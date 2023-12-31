# -*- coding: utf-8 -*-
"""MedicalCostAnaylsis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12-hXiSs6X3tj1rt0_baTggV_giGNw5ER
"""

import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
from scipy.stats import shapiro
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV

insurance = pd.read_csv("/content/insurance.csv")

df = insurance.copy()

insurance.head()

insurance.shape

df.info() # you can see the type of datas below

# Now decribe all column

df["age"].describe().T

df["sex"].describe().T

df["bmi"].describe().T

df["children"].describe().T

df["smoker"].describe().T

df["region"].describe().T

df["charges"].describe().T

# Making graphic about frequency of bmi
sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.hist(insurance["bmi"], bins=40,edgecolor = "Purple")
plt.title("Bmi-Frequency Graph")
plt.xlabel("Bmi")
plt.ylabel("Frequency")
plt.show()

median_bmi =np.median(insurance["bmi"])
print("Median of bmi is: ",median_bmi)

sns.set(rc={"figure.figsize":(9,6)})
sns.boxplot(x=insurance["bmi"])
plt.xlabel("Bmi")
plt.title("Box graph of Bmi")
plt.show()

df.duplicated().sum
df[df.duplicated()]

# We gonna take all featres and convert easy to use
# Gonna focus connection between Sex-Smoker and Region
features = df.select_dtypes("object").columns.to_list()
sns.set(rc={"figure.figsize":(9,6)})
i=1
for all_features in features:
  plt.title(f"{all_features.capitalize()}-Count Graph")
  sns.countplot(df,x = all_features)
  plt.show()

sns.set(rc={"figure.figsize":(9,6)})
sns.barplot(x="smoker",y="charges",data=insurance)
plt.title("Smoke-Charges Graph")

print("Sex,Smoker and Region - Charge graphs about affect")
for all_features in features:
  print(all_features.capitalize())
  print(f"{all_features.capitalize()}-charge affect")
  print(df.groupby(all_features).agg(min_charges=("charges","min"),mean_charges= ("charges","mean"),max_charges= ("charges","max")))

  sns.boxplot(df,x = all_features,y = "charges")
  plt.show()

df.info()

sns.set(rc={"figure.figsize":(9,6)})
sns.countplot(x = "region",data=insurance, hue = "smoker")
plt.title("Regio,Smoker-People Graph")

sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.title("Sex-Bmi Graph")
sns.barplot(x="sex",y="bmi",data=insurance)
plt.xlabel("Sex")
plt.ylabel("Bmi")
plt.show()

insurance.head()

sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.title("Smoker-Charges Graph")
sns.barplot(x="smoker",y="charges",data=insurance)
plt.xlabel("Smoker")
plt.ylabel("Charges")
plt.show()

sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.scatter(insurance["age"], insurance["bmi"], alpha = 0.4)
plt.title("Age-Bmi Graph")
plt.xlabel("Age")
plt.ylabel("Bmi")
plt.show()

sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.scatter(insurance["bmi"], insurance["children"], alpha=0.5)
plt.title("Bmi-Child Population Graph")
plt.xlabel("Bmi")
plt.ylabel("Child Population")
plt.show()

sns.set(rc={"figure.figsize":(9,6)})
plt.figure(figsize=(9,6))
plt.scatter(insurance["bmi"], insurance["charges"], alpha = 0.4)
plt.title("Age-Bmi Graph")
plt.xlabel("Bmi")
plt.ylabel("Charges")
plt.show()

sns.set(rc={"figure.figsize":(9,6)})
sns.barplot(x="region", y="bmi", data=insurance, hue="smoker")
plt.title("Region,Smoker-Bmi Graph")
plt.xlabel("Region")
plt.ylabel("Bmi")
plt.show()

"""Data Preprocessing"""

encoded_data = insurance.copy()

encoded_data = pd.get_dummies(encoded_data, columns=["sex", "smoker", "region"], drop_first=True)
print(encoded_data.head())

encoded_data_num = encoded_data.copy()
encoded_data_num = encoded_data_num.astype(int)
print(encoded_data_num.head())

encoded_data_num.head()

X = encoded_data_num.drop("charges", axis=1)  # Bağımsız değişkenler
y = encoded_data_num["charges"]  # Hedef değişken
# Veriyi train ve test setlere ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#outlier variable?
z_scores = stats.zscore(df["bmi"])
threshold = 3
outliers = abs(z_scores) > threshold
outlier_val = df["bmi"][outliers]
print("Outlier values:", outlier_val)

clean_df = df[~outliers]
encode_df = pd.get_dummies(clean_df, columns=["region", "smoker", "sex"], prefix=["region", "smoker", "sex"])

X = encode_df.drop("charges", axis=1)
y = encode_df["charges"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Model Selection"""

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(encode_df.drop("charges", axis=1))
scaled_df = pd.DataFrame(X_scaled, columns=encode_df.drop("charges", axis=1).columns)

def crossval(model):
    scores = cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv=10)
    forest_reg_rmse_scores = np.sqrt(-scores)
    print("cv : ")
    return forest_reg_rmse_scores.mean()

linear_regressor = LinearRegression()
linear_model = linear_regressor.fit(X_train,y_train)
linear_pred = linear_regressor.predict(X_test)
crossval(linear_model)

encoded_data_num.head()

decision_tree_regressor = DecisionTreeRegressor()
decision_tree_regression_model = DecisionTreeRegressor(max_depth=3, random_state=42)
decision_tree_regression_model = decision_tree_regressor.fit(X_train, y_train)
decision_tree_regression_pred = decision_tree_regression_model.predict(X_test)
crossval(decision_tree_regression_model)

"""Hyper-parameter Optimization"""

param_grid = [
    { "n_estimators": [30, 40, 50, 60, 70, 80], "max_depth": [1, 3, 5, 7, 9] },
    { "bootstrap": [False], "n_estimators": [3, 8], "max_depth": [1, 3, 5, 7, 9]}
]

random_forest_regressor = RandomForestRegressor(random_state=38)
forest_grid_search = GridSearchCV(random_forest_regressor, param_grid, cv=6, scoring='neg_mean_squared_error', refit=True)
forest_grid_search.fit(X_scaled, y)
forest_grid_search.best_params_

"""Model Evaluation"""

all_of_the_best_model = forest_grid_search.best_estimator_
y_pred = all_of_the_best_model.predict(X_scaled)

mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)
r2 = r2_score(y, y_pred)

final_scores = [mse,mae,r2]
final_scores_labels = ["mse","mae","r2"]

for i,j in zip(final_scores,final_scores_labels):
    print(f"{j} : {i}")
