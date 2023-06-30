import streamlit as st
from Tiger.constants import client_info
from Tiger.functions import login, logout, page_config, drop_duplicates

page_config('Account')
academy, name, authentication_status, username, authenticator = login()
if authentication_status:
    st.write('### Account Info')
    form = st.form('form')
    form.text_input('Name', name)
    form.text_input('Academy', client_info[academy])
    if form.form_submit_button('Save'):
        st.success('Account settings updated')
    st.write('---')
    st.write('### Logout')
    logout(authenticator, 'main')
    st.write('# ')
    if username == 'erickm':
        with st.expander('Admin Tools'):
            st.write('### Drop Duplicates')
            form = st.form('drop form')
            organizations = form.multiselect('Organizations',['OjaiTKD'])
            table_names = form.multiselect('Tables',['Attendance', 'Classes', 'Contacts', 'Cycles', 'Events', 'Ranks', 'Students'])
            if form.form_submit_button('Submit'):
                for organization in organizations:
                    for table_name in table_names:
                        drop_duplicates(organization, table_name)
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
