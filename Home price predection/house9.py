import pandas as pd
df = pd.read_csv("Home price predection/House Price Prediction Dataset.csv")
print(df.head())
df.info()
print(df.columns)
X = df[
    [
        "Area",
        "Bedrooms",
        "Bathrooms",
        "Floors",
        "YearBuilt"
    ]
]
y = df["Price"]
print(X.head())
print(y.head())
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=40
)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(predictions[:5])
print(y_test.head())