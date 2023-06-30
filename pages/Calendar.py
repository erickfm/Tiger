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

    classes = get_data(organization, 'Classes')
    events = get_data(organization, 'Events')
    cycles = get_data(organization, 'Cycles')
    selected_date = st.date_input('Date')
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

    #     [
    #     Event('Planning', day='2019-09-23', start='11:00', end='13:00'),
    #     Event('Class', day='2019-09-23', start='10:00', end='14:00'),
    #     Event('Class', day='2019-09-23', start='5:00', end='23:00'),
    #     Event('Class', day='2019-09-23', start='5:00', end='23:00'),
    #     Event('Demo', day='2019-09-27', start='15:00', end='16:00'),
    #     Event('Retrospective', day='2019-09-27', start='17:00', end='18:00'),
    # ]

    data.validate_config(calendar_config)
    data.validate_events(calendar_events, calendar_config)

    calendar = Calendar.build(calendar_config)
    calendar.add_events(calendar_events)
    calendar.save("cal.png")
    st.image('cal.png')
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
