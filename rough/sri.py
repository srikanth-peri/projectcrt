

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the data
data = pd.read_csv("card.csv")

# Check for missing values
print(data.isnull().sum())

# Count the transaction types
type_counts = data["type"].value_counts()
transactions = type_counts.index
quantity = type_counts.values

# Plot the distribution of transaction types
figure = px.pie(data, 
             values=quantity, 
             names=transactions, hole=0.5, 
             title="Distribution of Transaction Type")
figure.show()

# Encode the 'type' column
data['type_encoded'] = data['type'].astype('category').cat.codes

# Calculate and print correlation with 'isFraud'
correlation = data.select_dtypes(include=['number']).corr()
print(correlation["isFraud"].sort_values(ascending=False))

# Map transaction types to numerical values
data["type"] = data["type"].map({"CASH_OUT": 1, "PAYMENT": 2, 
                                 "CASH_IN": 3, "TRANSFER": 4,
                                 "DEBIT": 5})

# Map 'isFraud' to binary values
data["isFraud"] = data["isFraud"].map({0: 0, 1: 1})

print(data.head())

# Define features and target variable
X = np.array(data[["type", "amount", "oldbalanceOrg", "newbalanceOrig"]])
y = np.array(data["isFraud"])

# Impute missing values in the features
imputer = SimpleImputer(strategy='most_frequent')
X = imputer.fit_transform(X)

# Impute missing values in the target variable
imputer_y = SimpleImputer(strategy='most_frequent')
y = imputer_y.fit_transform(y.reshape(-1, 1)).ravel()  # Reshape and flatten

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Train the Decision Tree model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate the model
score = model.score(X_test, y_test)
print(f"Model accuracy: {score * 100:.2f}%")

# Save the trained model to a file
joblib.dump(model, 'fraud_detection_model.pkl')