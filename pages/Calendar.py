import streamlit as st
from Tiger.functions import login, logout, page_config

page_config('Events')
academy, name, authentication_status, username, authenticator = login()
if authentication_status:
    st.write(f'Welcome *{name}*')
    st.title('Some content')
    logout(authenticator)
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
