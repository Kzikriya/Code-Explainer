import streamlit as st
import google.generativeai as genai

# App UI
st.set_page_config(page_title="Code Sage", page_icon="🧠", layout="wide")
st.title("🧠 Code Sage - AI Code Explainer")
st.markdown("Understand, explain, and improve your code with AI assistance")

# API key input
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
if not api_key:
    st.info("👈 Please enter your Gemini API key in the sidebar to continue")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Invalid API key. Please check your API key and try again.")
    st.stop()

# Layout
tab1, tab2, tab3 = st.tabs(["Explain Code", "Debug Code", "Code Conversion"])

with tab1:
    st.subheader("Code Explanation")
    code_input = st.text_area(
        "Paste your code here:",
        height=200,
        placeholder="def example_function():\n    print('Hello World')"
    )
    
    detail_level = st.radio(
        "Explanation detail:",
        ["Simple Overview", "Line-by-Line", "Comprehensive Analysis"],
        horizontal=True
    )
    
    if st.button("Explain Code", key="explain"):
        if code_input:
            with st.spinner("Analyzing your code..."):
                prompt = f"""
                Provide a {detail_level.lower()} explanation of this code:
                {code_input}
                
                Explain what the code does, how it works, and any important concepts.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("Code Explanation:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error("Error in code analysis. Please try again.")
        else:
            st.warning("Please enter some code to analyze.")

with tab2:
    st.subheader("Debug Code")
    debug_code = st.text_area(
        "Paste code with issues:",
        height=150,
        placeholder="Code that isn't working as expected",
        key="debug_input"
    )
    
    issue_desc = st.text_input("Describe the issue (optional):")
    
    if st.button("Debug Code", key="debug"):
        if debug_code:
            with st.spinner("Looking for issues..."):
                prompt = f"""
                Analyze this code for issues and problems:
                {debug_code}
                
                The user reports: {issue_desc if issue_desc else 'No specific issue described'}
                
                Identify any bugs, errors, or potential improvements.
                Provide fixed code and explanation of changes.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("Debug Analysis:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error("Error in debugging. Please try again.")
        else:
            st.warning("Please enter some code to debug.")

with tab3:
    st.subheader("Code Conversion")
    convert_code = st.text_area(
        "Paste code to convert:",
        height=150,
        placeholder="Code to convert to another language",
        key="convert_input"
    )
    
    target_language = st.selectbox(
        "Convert to:",
        ["Python", "JavaScript", "Java", "C++", "PHP", "Ruby"]
    )
    
    if st.button("Convert Code", key="convert"):
        if convert_code:
            with st.spinner(f"Converting to {target_language}..."):
                prompt = f"""
                Convert this code to {target_language}:
                {convert_code}
                
                Provide the complete converted code and briefly explain any major changes needed.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success(f"Code converted to {target_language}:")
                    st.code(response.text, language=target_language.lower())
                except Exception as e:
                    st.error("Error in code conversion. Please try again.")
        else:
            st.warning("Please enter some code to convert.")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini • Code Sage © 2023")