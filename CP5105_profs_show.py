import streamlit as st
import pandas as pd
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Professor Profile Viewer",
    page_icon="👨‍🏫",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache the CSV data"""
    try:
        df = pd.read_csv('CP5125_profs.csv')
        return df
    except FileNotFoundError:
        st.error("CSV file not found. Please make sure 'CP5125_profs.csv' is in the same directory.")
        return None

def display_image(image_path, width=200):
    """Display image with error handling"""
    try:
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.image(image, width=width)
        else:
            st.write("📷 Image not found")
    except Exception:
        st.write("📷 Unable to load image")

def main():
    st.title("👨‍🏫 Professor Profile Viewer")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Professor selection
    prof_names = df['name'].tolist()
    
    # Initialize session state for current index
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    
    # Navigation buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("⬅️ Prev"):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
    with col2:
        if st.button("➡️ Next"):
            if st.session_state.current_index < len(prof_names) - 1:
                st.session_state.current_index += 1

    # Footer info
    st.sidebar.markdown("---")
    st.sidebar.write(f"Showing {st.session_state.current_index + 1} of {len(prof_names)} professors")
    for i,name in enumerate(prof_names):
        if st.sidebar.button(name,key=f"prof_{i}"):
            st.session_state.current_index = i
    
    
    # Display current professor info
    current_prof = df.iloc[st.session_state.current_index]
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Photo")
        display_image(current_prof['photo'], width=250)
        
        st.subheader("Contact Info")
        st.write(f"**Office:** {current_prof['office_location']}")
        st.write(f"**Phone:** {current_prof['phone_number']}")
        
        if pd.notna(current_prof['profile_website_link']):
            st.write(f"**Website:** [Profile Link]({current_prof['profile_website_link']})")

        if pd.notna(current_prof['CP5105_project']):
            
            st.markdown("### 🔬 **CP5105 Project** ⭐") 
            projects = current_prof['CP5105_project'].split('\n')
            for project in projects:
                if project.strip():
                    #st.write(f"• {project.strip()}")
                    st.markdown(f"• **<span style='color:orange'>{project.strip()}</span>**", unsafe_allow_html=True)
        
    with col2:
        st.subheader(f"{current_prof['name']}")
        st.write(f"*{current_prof['title']}*")
        
        # Education
        if pd.notna(current_prof['education']):
            st.subheader("Education")
            education_lines = current_prof['education'].split('\n')
            for line in education_lines:
                if line.strip():
                    st.write(f"• {line.strip()}")
        
        # Profile/Bio
        if pd.notna(current_prof['profile']):
            st.subheader("Profile")
            st.write(current_prof['profile'])
        
        # Research Areas
        if pd.notna(current_prof['research_areas']):
            st.subheader("Research Areas")
            st.write(current_prof['research_areas'])
        
        # Research Interests
        if pd.notna(current_prof['research_interests']):
            st.subheader("Research Interests")
            interests = current_prof['research_interests'].split('\n')
            for interest in interests:
                if interest.strip():
                    st.write(f"• {interest.strip()}")
    
    # Additional sections in expandable format
    if pd.notna(current_prof['selected_publications']):
        with st.expander("📚 Selected Publications"):
            publications = current_prof['selected_publications'].split('\n')
            for pub in publications:
                if pub.strip():
                    st.write(f"• {pub.strip()}")
    
    if pd.notna(current_prof['award_and_honors']):
        with st.expander("🏆 Awards and Honors"):
            awards = current_prof['award_and_honors'].split('\n')
            for award in awards:
                if award.strip():
                    st.write(f"• {award.strip()}")
    
    if pd.notna(current_prof['courses_taught']):
        with st.expander("📖 Courses Taught"):
            courses = current_prof['courses_taught'].split('\n')
            for course in courses:
                if course.strip():
                    st.write(f"• {course.strip()}")
    
    

    

if __name__ == "__main__":
    main()