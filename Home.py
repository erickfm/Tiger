import pandas as pd
import streamlit as st


from Tiger.functions import login, logout, page_config, create_client, run_query

page_config(home=True)
academy, name, authentication_status, username, authenticator = login()
if authentication_status:
    st.write(f'Welcome *{name}*')
    st.title('Some content')
    logout(authenticator)
elif authentication_status is None:
    pass
elif not authentication_status:
    st.error('Username/password is incorrect')



# data = [
#     {"student_id": 1, "first_name": "John", "last_name": "Doe", "address": "123 Main St", "city": "Anytown", "state": "California", "zip_code": "12345", "phone_number": "555-123-4567", "email": "john.doe@example.com", "rank_id": 1, "belt": "Black", "birthdate": "1990-05-15", "equipment_size": "Large", "belt_size": "42", "start_date": "2021-01-01"},
#     {"student_id": 2, "first_name": "Jane", "last_name": "Smith", "address": "456 Elm St", "city": "Otherville", "state": "New York", "zip_code": "54321", "phone_number": "555-987-6543", "email": "jane.smith@example.com", "rank_id": 2, "belt": "Blue", "birthdate": "1985-09-10", "equipment_size": "Medium", "belt_size": "38", "start_date": "2022-03-15"},
#     {"student_id": 3, "first_name": "Michael", "last_name": "Johnson", "address": "789 Oak Ave", "city": "Smalltown", "state": "Texas", "zip_code": "98765", "phone_number": "555-555-5555", "email": "michael.johnson@example.com", "rank_id": 1, "belt": "Black", "birthdate": "1992-12-03", "equipment_size": "Large", "belt_size": "40", "start_date": "2020-07-10"},
#     {"student_id": 4, "first_name": "Emily", "last_name": "Davis", "address": "321 Pine St", "city": "Sometown", "state": "Florida", "zip_code": "54321", "phone_number": "555-456-7890", "email": "emily.davis@example.com", "rank_id": 3, "belt": "Purple", "birthdate": "1993-08-20", "equipment_size": "Medium", "belt_size": "36", "start_date": "2023-02-05"},
#     {"student_id": 5, "first_name": "David", "last_name": "Wilson", "address": "567 Oak St", "city": "Metropolis", "state": "California", "zip_code": "98765", "phone_number": "555-789-1234", "email": "david.wilson@example.com", "rank_id": 2, "belt": "Blue", "birthdate": "1991-06-25", "equipment_size": "Large", "belt_size": "42", "start_date": "2021-04-10"},
#     {"student_id": 6, "first_name": "Sarah", "last_name": "Johnson", "address": "890 Maple Ave", "city": "Villageton", "state": "Texas", "zip_code": "67890", "phone_number": "555-222-3333", "email": "sarah.johnson@example.com", "rank_id": 2, "belt": "Blue", "birthdate": "1994-02-12", "equipment_size": "Medium", "belt_size": "39", "start_date": "2022-09-20"},
#     {"student_id": 7, "first_name": "Daniel", "last_name": "Anderson", "address": "234 Cedar St", "city": "Cityville", "state": "Florida", "zip_code": "54321", "phone_number": "555-444-5555", "email": "daniel.anderson@example.com", "rank_id": 1, "belt": "Black", "birthdate": "1988-11-30", "equipment_size": "Large", "belt_size": "40", "start_date": "2020-03-10"},
#     {"student_id": 8, "first_name": "Jessica", "last_name": "Brown", "address": "456 Pine St", "city": "Townsville", "state": "California", "zip_code": "78901", "phone_number": "555-666-7777", "email": "jessica.brown@example.com", "rank_id": 3, "belt": "Purple", "birthdate": "1995-07-18", "equipment_size": "Medium", "belt_size": "37", "start_date": "2023-01-05"},
#     {"student_id": 9, "first_name": "Andrew", "last_name": "Wilson", "address": "678 Elm St", "city": "Metroville", "state": "New York", "zip_code": "56789", "phone_number": "555-888-9999", "email": "andrew.wilson@example.com", "rank_id": 2, "belt": "Blue", "birthdate": "1992-04-05", "equipment_size": "Large", "belt_size": "43", "start_date": "2021-07-15"},
#     {"student_id": 10, "first_name": "Olivia", "last_name": "Thomas", "address": "901 Oak Ave", "city": "Citytown", "state": "Texas", "zip_code": "34567", "phone_number": "555-111-2222", "email": "olivia.thomas@example.com", "rank_id": 1, "belt": "Black", "birthdate": "1989-09-28", "equipment_size": "Large", "belt_size": "41", "start_date": "2020-12-01"}
# ]
#
# import io
# from google.cloud import bigquery
# buf = io.StringIO()
#
#
# df = pd.DataFrame(data)
# st.write(df)
#
#
# df.info(buf=buf, verbose=True)
# s = buf.getvalue()
#
# st.code(s)
#
#
# table_id = 'tiger-389322.OjaiTKD.Students'
# job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV
# )
# job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
# job.result()
# table = client.get_table(table_id)  # Make an API request.
# st.write(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")
