import numpy as np
import pandas as pd
import pickle
# import matplotlib.pyplot as plt

from utils.utils import convert_topicTags_to_tags_array

def predict_question_rating(question: dict, model_type='ridge'):
    # Load the appropriate model
    model_filename = 'data/ridge_model.pkl' if model_type == 'ridge' else 'data/lasso_model.pkl'
    with open(model_filename, 'rb') as file:
        loaded_model = pickle.load(file)

    # Load preprocessing objects
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
            input_df[f'emphasized_tag_{tag}'] = 10 if tag in input_data['tags'] else 0

    # Ensure input_df has the same feature columns
    missing_cols = set(feature_cols) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0

    input_df = input_df[feature_cols]

    # Standardize input features
    input_scaled = scaler.transform(input_df)

    # Convert scaled input back to DataFrame with feature names
    input_scaled_df = pd.DataFrame(input_scaled, columns=feature_cols)

    # Predict using the loaded model
    prediction = loaded_model.predict(input_scaled_df)

    return prediction[0]