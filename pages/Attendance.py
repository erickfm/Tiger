import streamlit as st
from Tiger.functions import login, logout, page_config, create_client, get_students

page_config('Attendance')
academy, name, authentication_status, username, authenticator = login()
if authentication_status:
    df = get_students()

    st.multiselect()
    logout(authenticator)
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
