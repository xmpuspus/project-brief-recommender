import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title('Project Brief Recommender')
st.write('Based on project brief category IDs, recommend the top project brief closest to the description.')


n_briefs = st.sidebar.slider('Number of Recommended Briefs', 1, 20, 10)

# Read Data
brief_data = pd.read_csv('briefs.csv')


# Clean nulls
b_clean = brief_data.fillna(0)

# Category IDs need to be strings, not numeric
b_clean['primary_category_id'] = b_clean['primary_category_id'].astype(str)
b_clean['secondary_category_id'] = b_clean['secondary_category_id'].astype(str)

# Get dummies
df = pd.get_dummies(b_clean[['primary_category_id', 'secondary_category_id']])

# Primary Category
pc_values = pd.Series(b_clean['primary_category_id'].unique()).str.strip()
pc_dummies = pd.get_dummies(pc_values)

pc_sample = st.sidebar.selectbox("Primary Category ID", pc_values.values.tolist())
pc_sample_dummies = pc_dummies.loc[np.where(pc_values.values == str(pc_sample))[0]].values.tolist()[0]


# Secondary Category
# Primary Category
sc_values = pd.Series(b_clean['secondary_category_id'].unique()).str.strip()
sc_dummies = pd.get_dummies(sc_values)

sc_sample = st.sidebar.selectbox("Secondary Category ID", sc_values.values.tolist())
sc_sample_dummies = sc_dummies.loc[np.where(sc_values.values == str(sc_sample))[0]].values.tolist()[0]

# concatenate to single input
sample = pc_sample_dummies + sc_sample_dummies
new_input = pd.DataFrame([sample])


# Get similarity scores 
scores = df.dot(new_input.T.values)

# Connect back to brief id
new_df = b_clean[['brief_id']]
new_df['new_scores'] = scores

# Get back top n briefs from highest to lowest scores
top_n_brief_scores = new_df.sort_values('new_scores', ascending=False)[:n_briefs]

# get list only
list_briefs = top_n_brief_scores.brief_id.values.tolist()

st.write(f'List of recommended briefs are {list_briefs}')



