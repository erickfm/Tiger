import time

import pandas as pd
import streamlit as st
from Tiger.functions import login, logout, page_config, create_client, get_data, post_data, clear_multi, \
    get_daily_attendance, get_attendance_options, remove_attendance, app_update, drop_duplicates

page_config('Attendance')
organization, name, authentication_status, username, authenticator = login()
if authentication_status:
    col_l, col_r = st.columns([1, 3])
    date = col_l.date_input('Date')
    with st.spinner('Loading...'):
        students = get_data(organization, 'Students')
        classes = get_data(organization, 'Classes')
        classes = classes[classes['date'] == date]
        attendance = get_daily_attendance(organization, date).set_index('student_id', drop=False).sort_values('last_name')
    class_names = sorted(set(classes['class_name']))
    class_name = col_r.selectbox('Class', class_names)
    try:
        class_id = attendance[attendance['class_name'] == class_name]['class_id'].iloc[0]
        class_attendance = attendance[(attendance['class_id'] == class_id)]
    except IndexError:
        if class_name in class_names:
            class_id = classes[classes['class_name'] == class_name]['class_id'].iloc[0]
            class_attendance = pd.DataFrame(
                [{'student_id': '', 'last_name': '', 'first_name': '', 'belt': ''}]).set_index('student_id', drop=False)
        else:
            st.info(f'No classes scheduled for {date}. Add a class in [Calendar](http://localhost:8501/Calendar)')
            st.stop()
            exit()
    st.dataframe(
        class_attendance[['last_name', 'first_name', 'belt']],
        use_container_width=True
    )
    add_attendants_tab, remove_attendants_tab, = st.tabs(['Add', 'Remove'])
    with add_attendants_tab:
        form = st.form('attendance_form_a')
        col_fl, col_fr = form.columns([10, 1])
        options = get_attendance_options(students, class_attendance, True)
        attending = col_fl.multiselect('Students', options)
        attending_ids = [int(i.split('(')[1].split(')')[0]) for i in attending]
        col_fr.write('# ')
        if col_fr.form_submit_button('Add'):
            data = pd.DataFrame([{'class_id': class_id, 'date': date, 'student_id': student_id} for student_id in attending_ids])
            post_data(data, organization, table_name='Attendance')
            app_update()
    with remove_attendants_tab:
        form = st.form('attendance_form_r')
        col_fl, col_fr = form.columns([13, 2])
        options = get_attendance_options(students, class_attendance, False)
        attending = col_fl.multiselect('Students', options)
        attending_ids = [int(i.split('(')[1].split(')')[0]) for i in attending]
        col_fr.write('# ')
        if col_fr.form_submit_button('Remove'):
            remove_attendance(date, class_id, attending_ids, organization, table_name='Attendance')
            app_update()
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')

# data = [
#   {
#     "class_id": 1,
#     "date": "2023-06-12",
#     "student_id": 1
#   },
#   {
#     "class_id": 1,
#     "date": "2023-06-12",
#     "student_id": 2
#   },
#   {
#     "class_id": 2,
#     "date": "2023-06-11",
#     "student_id": 3
#   },
#   {
#     "class_id": 2,
#     "date": "2023-06-11",
#     "student_id": 4
#   },
#   {
#     "class_id": 3,
#     "date": "2023-06-10",
#     "student_id": 5
#   },
#   {
#     "class_id": 3,
#     "date": "2023-06-10",
#     "student_id": 6
#   },
#   {
#     "class_id": 4,
#     "date": "2023-06-09",
#     "student_id": 7
#   },
#   {
#     "class_id": 4,
#     "date": "2023-06-09",
#     "student_id": 8
#   },
#   {
#     "class_id": 5,
#     "date": "2023-06-08",
#     "student_id": 9
#   },
#   {
#     "class_id": 5,
#     "date": "2023-06-08",
#     "student_id": 10
#   },
#   {
#     "class_id": 1,
#     "date": "2023-06-19",
#     "student_id": 1
#   },
#   {
#     "class_id": 1,
#     "date": "2023-06-19",
#     "student_id": 2
#   },
#   {
#     "class_id": 2,
#     "date": "2023-06-26",
#     "student_id": 3
#   },
#   {
#     "class_id": 2,
#     "date": "2023-06-26",
#     "student_id": 4
#   },
#   {
#     "class_id": 3,
#     "date": "2023-06-17",
#     "student_id": 5
#   },
#   {
#     "class_id": 3,
#     "date": "2023-06-17",
#     "student_id": 6
#   },
#   {
#     "class_id": 4,
#     "date": "2023-06-24",
#     "student_id": 7
#   },
#   {
#     "class_id": 4,
#     "date": "2023-06-24",
#     "student_id": 8
#   },
#   {
#     "class_id": 6,
#     "date": "2023-06-18",
#     "student_id": 9
#   },
#   {
#     "class_id": 6,
#     "date": "2023-06-18",
#     "student_id": 10
#   },
#   {
#     "class_id": 7,
#     "date": "2023-06-18",
#     "student_id": 1
#   },
#   {
#     "class_id": 7,
#     "date": "2023-06-18",
#     "student_id": 2
#   }
# ]
#
#
# table = 'Attendance'
# o_data = [
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-12"
#   },
#   {
#     "class_id": 2,
#     "class_name": "Intermediate Taekwondo",
#     "date": "2023-06-11"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-10"
#   },
#   {
#     "class_id": 4,
#     "class_name": "Children's Taekwondo",
#     "date": "2023-06-09"
#   },
#   {
#     "class_id": 5,
#     "class_name": "Women's Self-Defense",
#     "date": "2023-06-08"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-19"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-26"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-17"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-24"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-12"
#   },
#   {
#     "class_id": 2,
#     "class_name": "Intermediate Taekwondo",
#     "date": "2023-06-11"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-10"
#   },
#   {
#     "class_id": 4,
#     "class_name": "Children's Taekwondo",
#     "date": "2023-06-09"
#   },
#   {
#     "class_id": 5,
#     "class_name": "Women's Self-Defense",
#     "date": "2023-06-08"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-19"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-26"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-17"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-24"
#   },
#   {
#     "class_id": 6,
#     "class_name": "Sparring Class",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 7,
#     "class_name": "Cardio Kickboxing",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 4,
#     "class_name": "Children's Taekwondo",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 5,
#     "class_name": "Women's Self-Defense",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 3,
#     "class_name": "Advanced Taekwondo",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 6,
#     "class_name": "Sparring Class",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 7,
#     "class_name": "Cardio Kickboxing",
#     "date": "2023-06-18"
#   },
#   {
#     "class_id": 1,
#     "class_name": "Beginner Taekwondo",
#     "date": "2023-06-18"
#   }
# ]
# df = pd.DataFrame(data)
# st.write(df)
#
# f = st.form('hi')
# if f.form_submit_button('Submit'):
#     post_data(df, organization, table)
