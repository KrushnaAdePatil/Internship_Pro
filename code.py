import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load Data
dataset_path = 'Netflix_dashboard_dataset.csv'
df = pd.read_csv(dataset_path)

# 2. Calculate Viewer Retention Score
df['viewer_retention_score'] = (df['total_watch_hours_millions'] * 1000) / df['monthly_active_viewers_thousands']

# 3. Build Content-Based Recommendation Engine
# Fill NA values to prevent TF-IDF crashes
df['listed_in'] = df['listed_in'].fillna('')
df['type'] = df['type'].fillna('')
df['language'] = df['language'].fillna('')
df['combined_features'] = df['listed_in'] + " " + df['type'] + " " + df['language']

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Helper function to get top recommendation title
def get_top_recommendation(idx):
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_recommendation_idx = sim_scores[1][0]  # First item is itself, so take the 2nd
    return df.iloc[top_recommendation_idx]['title']

# 4. Map ML Recommendations directly into the dataset
df['recommended_next_watch'] = [get_top_recommendation(i) for i in range(len(df))]

# 5. NEW: Add Retention Campaign Segmentation Rules
def assign_campaign_segment(score):
    if score < 50:
        return 'Tier 1: At-Risk (Send Loyalty Discount / 20% Off)'
    elif score <= 100:
        return 'Tier 2: Steady (Send In-App Reminder & Recommendation)'
    else:
        return 'Tier 3: Super-Fan (Send VIP Early Access / Preview)'

df['retention_campaign_segment'] = df['viewer_retention_score'].apply(assign_campaign_segment)

# 6. Save Updated Dataset for Power BI
output_path = 'Netflix_with_Retention.csv'
df.to_csv(output_path, index=False)

print("Success! 'Netflix_with_Retention.csv' updated.")

# --- Test Recommendation Function ---
def recommend(title):
    if title not in df['title'].values:
        return f"Title '{title}' not found."
    idx = df[df['title'] == title].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    show_indices = [i[0] for i in sim_scores]
    return df[['title', 'listed_in', 'retention_campaign_segment', 'recommended_next_watch']].iloc[show_indices]

print("\nSample Campaign Output for 'Stranger Things':")
print(recommend('Stranger Things'))