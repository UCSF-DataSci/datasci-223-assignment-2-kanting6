#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # FIX: Added error handling for file not found
        print(f"Error: File not found at {filepath}")
        return []
    except json.JSONDecodeError:
        # FIX: Added error handling for JSON parsing errors
        print("Error: Failed to parse JSON file.")
        return []

def clean_patient_data(patients):
    """
    Clean patient data by:
    - Capitalizing names
    - Converting ages to integers
    - Filtering out patients under 18
    - Removing duplicates
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        list: Cleaned list of patient dictionaries
    """
    cleaned_patients = []
    seen_records = set()

    for patient in patients:
        # FIX: Corrected key 'nage' to 'name'
        patient['name'] = patient['name'].title()

        try:
            # FIX: Convert age to integer and handle invalid values
            patient['age'] = int(patient['age'])
        except (ValueError, TypeError):
            patient['age'] = 0

        # FIX: Corrected logic to filter patients under 18
        if patient['age'] < 18:
            continue

        # FIX: Avoid duplicate entries by using a set to track records
        record_tuple = (patient['name'], patient['age'], patient['gender'], patient['diagnosis'])
        if record_tuple not in seen_records:
            seen_records.add(record_tuple)
            cleaned_patients.append(patient)

    return cleaned_patients

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    patients = load_patient_data(data_path)

    if not patients:
        # FIX: Added check for empty or invalid patient data
        print("No patient data to process.")
        return

    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)

    if not cleaned_patients:
        # FIX: Added check for no cleaned patients
        print("No valid patients found after cleaning.")
        return

    # Print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        print(f"Name: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}, Diagnosis: {patient['diagnosis']}")

    return cleaned_patients

if __name__ == "__main__":
    main()
