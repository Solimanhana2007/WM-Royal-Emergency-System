import pandas as pd
from sklearn.model_selection import train_test_split 
df = pd.read_csv("mail_data.csv")
print(df.head())
print(df["Category"].value_counts())

X = df["Message"]
y = df["Category"]
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model.fit(X_train, y_train) 
predictions = model.predict(X_test)
print(predictions[:10])
predictions = model.predict(X_test)
print(y_test.head())
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("Classification Report:")
print(classification_report(y_test, predictions))
