import time
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from google.oauth2 import service_account
from google.cloud import bigquery


@st.cache_resource
def create_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    return client


@st.cache_data(ttl=600)
def run_query(query):
    client = create_client()
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


def page_config(title='', preset='default', home=False):
    if preset == 'default':
        st.set_page_config(page_title="Tiger", page_icon="🐯", layout="wide")
        if home:
            st.write('# 🐯 Tiger')
        else:
            st.write(f'# 🐯 {title}')


def login(location='sidebar', config_path='Tiger/config.yaml'):
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login('Login', location=location)
    academy = config['credentials']['usernames'][username]['academy']
    time.sleep(.1)
    return academy, name, authentication_status, username, authenticator


def logout(authenticator, location='sidebar'):
    authenticator.logout('Logout', location=location)
    time.sleep(.1)
    return 1


def get_students():
    with st.spinner('Gathering student details...'):
        client = create_client()
        sql = """
            select distinct *
            from `tiger-389322.OjaiTKD.Students`
        """
        df = client.query(sql).to_dataframe()
    return df
