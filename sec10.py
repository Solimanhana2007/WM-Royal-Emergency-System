from sklearn.neighbors import KNeighborsClassifier

X_train = [
    [8, 95],
    [7, 90],
    [6, 85],
    [3, 50],
    [2, 40],
    [1, 20]
]

y_train = [
    "Pass",
    "Pass",
    "Pass",
    "Fail",
    "Fail",
    "Fail"
]

model = KNeighborsClassifier(n_neighbors=1)

model.fit(X_train, y_train)

student = [[5,80]]

prediction = model.predict(student)

print(prediction)