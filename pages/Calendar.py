import streamlit as st
from Tiger.functions import login, logout, page_config

from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event



page_config('Calendar')
academy, name, authentication_status, username, authenticator = login()
if authentication_status:


    config = data.CalendarConfig(
        lang='en',
        dates='Su - Sa',
        legend=False,
    )
    events = [
        Event('Planning', day='2019-09-23', start='11:00', end='13:00'),
        Event('Class', day='2019-09-23', start='10:00', end='14:00'),
        Event('Class', day='2019-09-23', start='5:00', end='23:00'),
        Event('Class', day='2019-09-23', start='5:00', end='23:00'),
        Event('Demo', day='2019-09-27', start='15:00', end='16:00'),
        Event('Retrospective', day='2019-09-27', start='17:00', end='18:00'),
    ]

    data.validate_config(config)
    data.validate_events(events, config)

    calendar = Calendar.build(config)
    calendar.add_events(events)
    calendar.save("sprint_23.png")
    st.image('sprint_23.png')
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')
