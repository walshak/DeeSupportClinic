# data_preparation.py

import random
import pandas as pd

def generate_synthetic_data(num_samples):
    data = {
        'Age': [random.randint(25, 75) for _ in range(num_samples)],
        'Gender': [random.choice(['Male', 'Female']) for _ in range(num_samples)],
        'BMI': [round(random.uniform(18.5, 40.0), 2) for _ in range(num_samples)],
        'Fasting_Blood_Sugar': [random.randint(70, 120) for _ in range(num_samples)],  # Represented in mg/dL
        'Blood_Pressure': [f"{random.randint(100, 160)}/{random.randint(60, 100)}" for _ in range(num_samples)],
        'Family_History_of_Diabetes': [random.choice(['Yes', 'No']) for _ in range(num_samples)],
        'Smoking_Status': [random.choice(['Non-smoker', 'Former smoker', 'Current smoker']) for _ in range(num_samples)],
        'Physical_Activity_Level': [random.choice(['Low', 'Moderate', 'High']) for _ in range(num_samples)],
        'Numbness_in_Extremities': [random.choice(['Yes', 'No']) for _ in range(num_samples)],
        'Blurred_Vision': [random.choice(['Yes', 'No']) for _ in range(num_samples)],
        'Diabetes_Neuropathy': [random.choice([0, 1]) for _ in range(num_samples)],  # Target variable
    }
    return pd.DataFrame(data)

def preprocess_blood_pressure(df):
    df['Systolic_BP'] = df['Blood_Pressure'].apply(lambda x: int(x.split('/')[0]))
    df['Diastolic_BP'] = df['Blood_Pressure'].apply(lambda x: int(x.split('/')[1]))
    df.drop(columns=['Blood_Pressure'], inplace=True)
    return df

if __name__ == "__main__":
    num_samples = 50
    df = generate_synthetic_data(num_samples)

    # Map categorical features to numerical values
    categorical_mapping = {
        'Gender': {'Male': 0, 'Female': 1},
        'Family_History_of_Diabetes': {'No': 0, 'Yes': 1},
        'Smoking_Status': {'Non-smoker': 0, 'Former smoker': 1, 'Current smoker': 2},
        'Physical_Activity_Level': {'Low': 0, 'Moderate': 1, 'High': 2},
        'Numbness_in_Extremities': {'No': 0, 'Yes': 1},
        'Blurred_Vision': {'No': 0, 'Yes': 1}
    }

    df.replace(categorical_mapping, inplace=True)
    df = preprocess_blood_pressure(df)

    df.to_csv("sample_data.csv", index=False)
