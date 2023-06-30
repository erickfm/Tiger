import time
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from google.oauth2 import service_account
from google.cloud import bigquery


def page_config(title='', preset='default', home=False):
    if preset == 'default':
        st.set_page_config(page_title="Tiger", page_icon="🐯", layout="centered")
        if home:
            st.write('## 🐯 Tiger')
        else:
            st.write(f'## 🐯 {title}')


def login(location='main', config_path='Tiger/config.yaml'):
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
    organization = config['credentials']['usernames'][username]['organization']
    time.sleep(.1)
    return organization, name, authentication_status, username, authenticator


def logout(authenticator, location='main'):
    authenticator.logout('Logout', location=location)
    time.sleep(.1)
    return 1


@st.cache_resource
def create_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    return client


@st.cache_data(ttl=600, show_spinner=False)
def get_data(organization, table):
    client = create_client()
    sql = f"""
    select distinct *
    from `tiger-389322.{organization}.{table}`
    """
    df = client.query(sql).to_dataframe()
    return df


@st.cache_data(ttl=600, show_spinner=False)
def get_daily_attendance(organization, date):
    client = create_client()
    sql = f"""
    with att as (
        select distinct *
        from `tiger-389322.{organization}.Attendance`),
        stu as (
        select distinct *
        from `tiger-389322.{organization}.Students`),
        cla as (
        select class_id, class_name
        from `tiger-389322.{organization}.Classes`)
    select distinct * 
    from att
    join stu on att.student_id = stu.student_id
    join cla on att.class_id = cla.class_id
    where att.date = '{date}'
    """
    # st.code(sql)
    df = client.query(sql).to_dataframe()
    return df


def post_data(data, organization, table_name):
    st.write(data)
    with st.spinner(f'Updating {table_name}...'):
        client = create_client()
        table_id = f'tiger-389322.{organization}.{table_name}'
        job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV)
        job = client.load_table_from_dataframe(data, table_id, job_config=job_config)
        job.result()
        table = client.get_table(table_id)
    return table
    # st.success(f"Loaded {len(data)} rows and {len(data.columns)} columns to {table_id}")


def sql_array(input_list):
    if len(input_list)>1:
        return tuple(input_list)
    else:
        return f'({input_list[0]})'


def remove_attendance(date, class_id, student_ids, organization, table_name):
    with st.spinner(f'Removing data...'):
        client = create_client()
        sql = f"""
        delete from tiger-389322.{organization}.{table_name}
        where date = '{date}' and
        class_id = {class_id} and
        student_id in {sql_array(student_ids)}
        """
        # st.code(sql)
        df = client.query(sql).to_dataframe()
    return df


def clear_multi():
    time.sleep(5)
    st.session_state['multi'] = []


def drop_duplicates(organization, table_name):
    with st.spinner(f'Dropping duplicates on {organization}.{table_name}...'):
        client = create_client()
        sql = f"""
        create or replace table tiger-389322.{organization}.Temp as (select distinct * from tiger-389322.{organization}.{table_name});
        create or replace table tiger-389322.{organization}.{table_name} as (select * from tiger-389322.{organization}.Temp);
        drop table tiger-389322.{organization}.Temp;
        """
        df = client.query(sql).to_dataframe()
        st.success(f'Duplicates dropped on {organization}.{table_name}')
    return df


def get_attendance_options(students, class_attendance, adding):
    options = sorted(set(
        students['last_name'] + ', ' + students['first_name'] + ' (' + [str(i) for i in students['student_id']] + ')'))
    already_attending = sorted(set(
        class_attendance['last_name'] + ', ' + class_attendance['first_name'] + ' (' + [str(i) for i in
                                                                                        class_attendance[
                                                                                            'student_id']] + ')'))
    if adding:
        options = [i for i in options if i not in already_attending]
    else:
        options = [i for i in options if i in already_attending]
    return options


def app_update():
    # time.sleep(.5)
    st.cache_data.clear()
    st.experimental_rerun()
