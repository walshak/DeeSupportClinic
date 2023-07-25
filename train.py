# Import the libraries for model training and evaluation
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
# Load the sample data
data = pd.read_csv("sample_data.csv")

# Prepare the data for training
X = data.drop(columns=['Diabetes_Neuropathy'])
y = data['Diabetes_Neuropathy']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=47)

# Train the Naive Bayes classifier
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Save the trained model using joblib
joblib.dump(classifier, 'naive_bayes_model.joblib')

# Evaluate the model on the test set
y_pred = classifier.predict(X_test)

# Calculate accuracy and other metrics
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the accuracy and other metrics
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
print("Confusion Matrix:")
print(conf_matrix)