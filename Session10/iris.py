import pandas as pd
df = pd.read_csv("Session10/IRIS.csv")
print(df.head())
X = df[[
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
]]
y=df["species"]
print(X.head())
print(y.head())
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=30
)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(y_pred)
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print(accuracy)