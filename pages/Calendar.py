import pandas as pd
import streamlit as st
from Tiger.functions import login, logout, page_config, get_data

from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event

from datetime import timedelta

page_config('Calendar')
organization, name, authentication_status, username, authenticator = login()
if authentication_status:
    week_tab, add_tab, remove_tab = st.tabs(['Weekly Schedule', 'Add', 'Remove'])
    with week_tab:
        classes = get_data(organization, 'Classes')
        events = get_data(organization, 'Events')
        cycles = get_data(organization, 'Cycles')
        selected_date = st.date_input('Date', key='display')
        if selected_date.weekday() == 6:
            start_date = selected_date
        else:
            idx = (selected_date.weekday() + 1) % 7
            start_date = selected_date - timedelta(idx)
        end_date = start_date + timedelta(days=6)
        calendar_config = data.CalendarConfig(dates=f'{start_date} - {end_date}', hours='8:00 - 20:00')
        calendar_events = []
        for event in classes.iloc:
            calendar_events.append(Event(event['class_name'], day=event['date'], start='9:00', end='19:00'))
        for event in events.iloc:
            calendar_events.append(Event(event['class_name'], day=event['date'], start='9:00', end='19:00'))
        for event in cycles.iloc:
            calendar_events.append(Event(event['class_name'], day=event['date'], start='9:00', end='19:00'))
        data.validate_config(calendar_config)
        data.validate_events(calendar_events, calendar_config)
        calendar = Calendar.build(calendar_config)
        calendar.add_events(calendar_events)
        calendar.save("cal.png")
        st.image('cal.png')
    with add_tab:
        # form = st.form('add_form')
        l_col, r_col = st.columns([1,1])
        event_name = l_col.text_input('Name')
        is_class = st.selectbox('Type', ['Class', 'Event', 'Cycle'])
        recurring = st.checkbox('Recurring')
        if recurring:
            frequency = l_col.selectbox('Frequency', ['Daily', 'Weekly', 'Monthly', 'Annually'])
            start_date = r_col.date_input('Start Date')
            end_date = r_col.date_input('End Date')
        else:
            event_date = r_col.date_input('Date')
        if st.button('Add'):
            if recurring:
                st.success(f'{event_name}{recurring}{frequency}{start_date}{end_date}')
            else:
                st.success(f'{event_name}{recurring}{event_date}')


    with remove_tab:
        pass
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
