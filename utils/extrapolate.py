import pickle

import numpy as np
import pandas as pd

from utils.utils import convert_topicTags_to_tags_array

def predict_question_rating(question: dict):
    with open('data/gradient_boosting_model.pkl', 'rb') as file:
        loaded_gb_model = pickle.load(file)

    with open('data/preprocessing_objects.pkl', 'rb') as file:
        ordinal_encoder, scaler, feature_cols, tag_list, emphasized_tags = pickle.load(file)

    input_data = {
        'total_acs': question["total_acs"],
        'total_submitted': question["total_submitted"],
        'tags': convert_topicTags_to_tags_array(question["topicTags"]),
        'difficulty': question["difficulty"]
    }

    input_data['acceptance_rate'] = input_data['total_acs'] / input_data['total_submitted']

    # Log transform total_acs, total_submitted, and acceptance_rate
    input_data['log_total_acs'] = np.log1p(input_data['total_acs'])
    input_data['log_total_submitted'] = np.log1p(input_data['total_submitted'])
    input_data['log_acceptance_rate'] = np.log1p(input_data['acceptance_rate'])

    # Ordinal encoding for difficulty
    input_df = pd.DataFrame([input_data])
    input_df['difficulty_encoded'] = ordinal_encoder.transform(input_df[['difficulty']])

    # Add binary features for emphasized tags in the input data
    for tag in tag_list:
        input_df[f'tag_{tag}_freq'] = 0
        if tag in input_data['tags']:
            input_df[f'tag_{tag}_freq'] = 1
        if tag in emphasized_tags:
            input_df[f'emphasized_tag_{tag}'] = 10 if tag in input_data['tags'] else 0  # Boost binary feature

    # Ensure input_df has the same feature columns
    input_df = input_df[feature_cols]

    # Standardize input features
    input_scaled = scaler.transform(input_df)

    # Convert scaled input back to DataFrame with feature names
    input_scaled_df = pd.DataFrame(input_scaled, columns=feature_cols)

    # Predict using the loaded Gradient Boosting model
    gb_pred = loaded_gb_model.predict(input_scaled_df)

    return gb_pred[0]