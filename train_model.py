import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

encoder=LabelEncoder()
encoders = {}

df=pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
print(df.head(5))
df.drop(
    ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"],
    axis=1,
    inplace=True
)
print(df.info())

# now we have to encode this text into numbers so the model can understand
object_columns = df.select_dtypes(include=["object", "string"]).columns

# for column in object_columns:
#     df[column] = encoder.fit_transform(df[column])

# print(df.head())
# Encode categorical columns

object_columns = df.select_dtypes(include=["object"]).columns

for column in object_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column])

    encoders[column] = encoder

print(df.head())

#Training and Testing - Splitting the data
# Features (Input)
X = df.drop("Attrition", axis=1)

# Target (Output)
y = df["Attrition"]

print("X Shape:", X.shape)
print("y Shape:", y.shape)

# Split the data into Training and Testing sets

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)

#model implementation
# Create Model
model = LogisticRegression(max_iter=5000)


# Train Model
model.fit(X_train, y_train)

print("Model Trained Successfully!")

# Make Predictions
y_pred = model.predict(X_test)

# print("Predictions:")
# print(y_pred)
# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)

# print("Accuracy:", accuracy)
print(f"Accuracy: {accuracy*100:.2f}%")

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# joblib.dump(encoder, "label_encoder.pkl")
joblib.dump(encoders, "encoders.pkl")
print("Encoders Saved Successfully!")

# Save Model
joblib.dump(model, "employee_attrition_model.pkl")

print("Model Saved Successfully!")


#lets compare this with other model to improve this 

# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier

# #logistic 
# lr_model = LogisticRegression(max_iter=1000)
# lr_model.fit(X_train, y_train)
# lr_pred = lr_model.predict(X_test)
# print("Logistic Regression :", accuracy_score(y_test, lr_pred))
# print(classification_report(y_test, lr_pred))

# #Decision Tree
# dt_model = DecisionTreeClassifier(random_state=42)
# dt_model.fit(X_train, y_train)
# dt_pred = dt_model.predict(X_test)
# print("Decision Tree :", accuracy_score(y_test, dt_pred))
# print(classification_report(y_test, dt_pred))

# #random forest
# rf_model = RandomForestClassifier(random_state=42)
# rf_model.fit(X_train, y_train)
# rf_pred = rf_model.predict(X_test)
# print("Random Forest :", accuracy_score(y_test, rf_pred))
# print(classification_report(y_test, rf_pred))

# #Gradient Booster
# gb_model = GradientBoostingClassifier(random_state=42)
# gb_model.fit(X_train, y_train)
# gb_pred = gb_model.predict(X_test)
# print("Gradient Boosting :", accuracy_score(y_test, gb_pred))
# print(classification_report(y_test, gb_pred))




