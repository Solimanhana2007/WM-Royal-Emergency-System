import pandas as pd
df = pd.read_csv("bank_transactions.pyse12.csv")
print("--------------HEAD---------------")
print(df.head())
print("------------SHAPE-----------------")
print(df.shape)
print("-------------INFO----------------")
print(df.info())
print("------------ISNULL-----------------")
print(df.isnull().sum())
print("-------------DUPLICATED----------------")
print(df.duplicated().sum())
print("------------CUSTOMER IDs-----------------")
print(df["CustomerID"].nunique())
print("------------CUSTOMER IDs HEAD-----------------")
print(df["CustomerID"].value_counts().head(10))
print("------------CUSTOMER transactions----------------")
transaction_counts = df["CustomerID"].value_counts()
print(transaction_counts.describe())
print("-------------GROUPBY----------------")
print(df.groupby("CustomerID")["TransactionAmount (INR)"].sum().head(10))

print("-------------FEATURES----------------")

total_spent = df.groupby("CustomerID")["TransactionAmount (INR)"].sum()

average_spent = df.groupby("CustomerID")["TransactionAmount (INR)"].mean()

transaction_counts = df["CustomerID"].value_counts()

avg_balance = df.groupby("CustomerID")["CustAccountBalance"].mean()


customer_data = pd.DataFrame({
    "TotalSpent": total_spent,
    "AverageSpent": average_spent,
    "TransactionCount": transaction_counts,
    "AvgAccountBalance": avg_balance
})

print(customer_data.head())