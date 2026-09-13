import streamlit as st
import pandas as pd
import altair as alt

# Set page config for a premium, wide look
st.set_page_config(
    page_title="Netflix AI & Retention Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix-like aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #141414;
        color: #ffffff;
    }
    .stSelectbox label, .stMetric label {
        color: #e50914 !important;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #e50914;
    }
    .css-1d391kg {
        background-color: #000000;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('Netflix_with_Retention.csv')

try:
    df = load_data()
except Exception as e:
    df = pd.DataFrame() # Fallback
    st.error(f"Error loading data: {e}\n\nMake sure to run `python code.py` first to generate 'Netflix_with_Retention.csv'!")

if not df.empty:
    # Sidebar navigation
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Dashboard Overview", "AI Recommendations", "Retention Segmentation"])

    st.sidebar.markdown('---')
    st.sidebar.info("This is an advanced viewer retention and content recommendation system.")

    if menu == "Dashboard Overview":
        st.title("🎥 Netflix AI & Retention Dashboard")
        st.markdown("Monitor high-level metrics across the platform.")

        # Interactive filter
        type_filter = st.selectbox("Filter by Type:", ["All", "Movie", "TV Show"])
        filtered_df = df if type_filter == "All" else df[df['type'] == type_filter]
        
        # Top KPIs
        tot_shows = len(filtered_df)
        avg_retention = filtered_df['viewer_retention_score'].mean()
        tot_watch_hours = filtered_df['total_watch_hours_millions'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Titles Available", f"{tot_shows:,}")
        col2.metric("Avg Retention Score", f"{avg_retention:.1f}")
        col3.metric("Total Watch Hours (M)", f"{tot_watch_hours:,.0f}")

        st.markdown("### 📊 Top Content by Viewer Retention")
        # Sort and show top 10
        top_retention = filtered_df.sort_values(by='viewer_retention_score', ascending=False).head(10)
        
        # Display as a clean chart
        chart = alt.Chart(top_retention).mark_bar(color="#e50914").encode(
            x=alt.X('viewer_retention_score', title="Retention Score"),
            y=alt.Y('title', sort='-x', title="Title"),
            tooltip=['title', 'viewer_retention_score', 'retention_campaign_segment']
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

        st.markdown("### 🔍 Dataset Explorer")
        st.dataframe(filtered_df[['title', 'type', 'language', 'viewer_retention_score', 'retention_campaign_segment']].head(50), use_container_width=True)

    elif menu == "AI Recommendations":
        st.title("🤖 AI Content Recommendation Engine")
        st.markdown("Our NLP algorithm suggests content based on genres, type, and language similarities.")

        # Allow user to pick a title
        all_titles = sorted(df['title'].tolist())
        selected_title = st.selectbox("Select a Netflix Title you liked:", all_titles)

        if selected_title:
            row = df[df['title'] == selected_title].iloc[0]
            st.write(f"**You selected:** {selected_title} ({row['type']})")
            st.write(f"**Match Tags:** {row['listed_in']}")
            
            st.markdown("### 🎯 Recommended Next Watch")
            recommended = str(row['recommended_next_watch'])
            rec_titles = recommended.split('|')
            
            cols = st.columns(len(rec_titles))
            for i, rec_title in enumerate(rec_titles):
                with cols[i]:
                    st.success(f"**{rec_title}**")
                    # Fetch details of recommended
                    rec_row = df[df['title'] == rec_title]
                    if not rec_row.empty:
                        rec_row = rec_row.iloc[0]
                        st.caption(f"{rec_row['type']} • {rec_row['language']}")
                        st.write(f"*{rec_row['listed_in']}*")

    elif menu == "Retention Segmentation":
        st.title("📈 Viewer Retention Segments")
        st.markdown("Automated segmentation pipeline categorizing users based on engagement scores.")

        segments = df['retention_campaign_segment'].value_counts().reset_index()
        segments.columns = ['Segment', 'Count']
        
        # Pie chart using Altair
        pie = alt.Chart(segments).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Segment", type="nominal", scale=alt.Scale(scheme='reds')),
            tooltip=['Segment', 'Count']
        ).properties(height=400, title="Campaign Distribution")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.altair_chart(pie, use_container_width=True)
        with col2:
            st.markdown("### Segment Action Plan")
            st.write("- **Tier 1 (At-Risk):** Target with high loyalty discounts (e.g., 20% off) to prevent churn.")
            st.write("- **Tier 2 (Steady):** Use in-app notifications recommending next-best-watch to increase watch hours.")
            st.write("- **Tier 3 (Super-Fan):** Engage with VIP offerings, early premieres, or merchandise.")
            
            st.dataframe(segments, use_container_width=True)
