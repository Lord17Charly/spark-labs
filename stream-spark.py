import streamlit as st
import requests
import pandas as pd
import json

def post_spark_job(user, repo, job, token):
    # Define the API endpoint
    url = f'https://api.github.com/repos/{user}/{repo}/dispatches'
    
    # Define the data to be sent in the POST request
    payload = {
      "event_type": job
    }

    headers = {
      'Authorization': f'Bearer {token}',
      'Accept': 'application/vnd.github.v3+json',
      'Content-type': 'application/json'
    }

    st.write("🔁 Dispatching Spark job to GitHub Actions...")
    st.write(f"URL: {url}")
    st.write(f"Payload: {payload}")
    
    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Display the response in the app
    st.write("🔽 GitHub Response:")
    st.write(response)
    if response.status_code == 204:
        st.success("✅ Spark job dispatched successfully.")
    else:
        st.error(f"❌ Error dispatching job: {response.text}")


def get_spark_results(url_results):
    st.write("🔁 Getting results from:")
    st.write(url_results)
    response = requests.get(url_results)

    st.write("🔽 Response:")
    st.write(response)

    if response.status_code == 200:
        try:
            data = response.json()
            st.success("✅ JSON Loaded successfully!")
            st.json(data)
        except Exception:
            st.warning("⚠️ Could not parse JSON. Showing raw text:")
            st.text(response.text)
    else:
        st.error(f"❌ Failed to fetch results: {response.status_code}")


# STREAMLIT UI
st.title("✨ Spark & Streamlit Controller")

# Section: Dispatch Spark Job
st.header("🚀 spark-submit Job")

github_user  = st.text_input('GitHub User', value='adsoftsito')
github_repo  = st.text_input('GitHub Repo', value='bigdata')
spark_job    = st.text_input('Spark Event Name', value='spark')
github_token = st.text_input('GitHub Token', value='***', type='password')

if st.button("📤 POST spark-submit"):
    post_spark_job(github_user, github_repo, spark_job, github_token)


# Section: Read Spark Job Results
st.header("📥 spark-submit Results")

url_results = st.text_input('URL to results (JSON)', value='https://raw.githubusercontent.com/...')

if st.button("📥 GET spark results"):
    get_spark_results(url_results)
