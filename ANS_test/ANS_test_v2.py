#Necessary installations to run the test
#Incooperation of google sheets to code
from IPython.display import display, HTML, Image, clear_output
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json 
import time
import random
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
from google.oauth2 import service_account
import gspread
import os
import matplotlib.pyplot as plt
import numpy as np
#Creation of google environment 
os.environ["GOOGLE_JSON"] = json.dumps({
    "type": "service_account",
    "project_id": "ans-test-416912",
    "private_key_id": "d0ced6a15f908cbe0bac5338042cbd9e29c71ebf",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCXShd2p+8Zgtxj\nOM6omQ03A6wyOOEo3XTFuH/jbtYk0mXqnoWYBgP+sPOHm/diSPyWd1JrBhHymH/u\n6xySaSJw+KYks+Sh1j5x5PRFgxh72zPEJ+uMo2jHLBWI3eG8CRtvoxQQKxa3nABN\nkg3f2il3ar5kwfvJUVj8EPTiC0acKaXP6fl6i4Z8dAvdqdT/j1N0h+/Iltj73z2B\nTQM+vF1I59/cVolLRi0pD71t/ga2xyi1sR8I9JF7+/IyEkYoQGk/lGaw4wKvgoD3\nCy8N856hMTdyNZh4KR2Ng5tCs7tVT5V2Tk5dqrbMM66PKzfZ7fhAHt8V/K6Uzj8y\ncOABQUSJAgMBAAECggEAAkM4R9zh12m0ulKni4+zagTW6s7dNi9er1TPq9L05qrT\nXZ+Gi7QeU+0pTThEyj5hca4h6EoYU16avjPbsuhZ3KLpWC/tDcsOlsU37oC0CWkp\nNGgs7obkmqLzBP+dgEKKG6CunIHKdo9BlWdnZ/dDKr8ozwi0J2n9KNLnmKhWw1/Z\nrzSNMx3TUZ3wQaH/+yC3kL/faHU+m9ImtjoCA0YmZ+gc4xSnycVoYUg2Tp5UsbNc\nGqln6FK0suIe3QMpZXpZyUKCbAKgZaeluIPsVnTx65ppFm3Sg/1FNpOsYNReOgJu\nZSH5eBlCXvWp0jQQ2DPKPMcJdtPESoCKQzyFzyGpQQKBgQDPGSRY8tvUypRPOtDM\n4i+i9n4z5dflwINZLhG6aHJQtm6cbYQKR+MEHza5VpJg6JK1UJ70bLoZss6un8CK\nTgzep8D5JjkRSaYCr2i8EDwJxPAU5j2nzXr5CgLZEGkAElkeWBOIpnKKI0S1YqTQ\nPMDeZSmvtYahWWfPeWxv7i3vQQKBgQC7A161vZVD8bu5vpCm6xNOSw59/rgC2oUN\nuSL/G4cWlJ+lp9DuPAwcjLaMUHRp86v2zQ4ZkrKs6jtm3Opby6QDXXhrrO65yeLL\nWqGbJd3gygPmrY4bWvmS8IO9ycBJFnQn5Skl4VeXM40/RfSVDnchvRw8PkhgrXyi\nQZxwbRBLSQKBgCOXX47F1g/g7NIc+otrh+JK2G+U3aDHkAtAhp1xm8vRPns1uw6F\nQjeQIbiCb0+mSKhOfbLmCKmn+Cs8mztppH6Td++ZqQ8WiChH+wjvBVJsfRIqa4gu\nIScxmEGzt0fi31v+qQTADkk9PG6r0EVVW5Qc8KgY21VZZyTZ6k/mMBDBAoGAT692\n6q+2a3YUTGgT0Nv3pPO8YBlqJOUhrqBFdjgvjoKTqA1irDBv5LZcjls1z3OhwY7M\nRD9K3P0NhJ37SlPyNfDc/9x2+Dk65vVeSPKQoVjS4rbvB17zWxYavIK76SilI960\ncsya+vVfaSeQuPap8nlXD6BmTLN/mM+mLg161OkCgYBnr6KOWjSp1gwfdCbBSzKC\nGhN1afTT5NDVDOeBRGpDGTRuhREuiY7tzpZanOmbJl7ZFIhc049JIgUP72yn+1ho\nMDhsklM49canLEeBZM9qKZe6ltFx8kJrrFCwhsh+6JorNpYlsXKZICAC0bMRdJsn\nUdRLdd+TpmuDFHe2pM4Kqw==\n-----END PRIVATE KEY-----\n",
    "client_email": "ans-test-responses@ans-test-416912.iam.gserviceaccount.com",
    "client_id": "116855767855578680791",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/ans-test-responses%40ans-test 416912.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}) 
    
#Function that allows user to see how their result compares to the mean (needs testing)
def compare_to_mean(elapsed_time, num_correct):
    '''
    Compare to mean function takes in the return of the ans_test() function for the user and compares it to the mean of returns of the previous users.
    Arguments: username/ID from google forms
    Returns: Comparison of percentage of correct answers and time taken to the mean values for these variables as an HTML message for the user
    '''
    google_json = os.environ["GOOGLE_JSON"]
    service_account_info = json.loads(google_json)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_with_scope = credentials.with_scopes(scope)
    client = gspread.authorize(creds_with_scope)
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1jlGqKvzAmFnNpNvvL6jF3m0knTq_bBhSQvJPRdR8nhs/edit?usp=sharing')
    worksheet = spreadsheet.get_worksheet(0)
    records_data = worksheet.get_all_records()
    spreadsheet_df = pd.DataFrame.from_dict(records_data)
    style = f'font-size: 20px'
    mean_correct = spreadsheet_df['Correct proportion'].mean()
    mean_time = spreadsheet_df['Time'].mean()
    compare_correct = round((round(num_correct/64, 2) - mean_correct)/mean_correct * 100, 2)
    compare_time = round((elapsed_time - mean_time)/mean_time * 100, 2)
    if compare_correct > 0:
        compare_correct = compare_correct
        if compare_time >0:
            compare_time = compare_time
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_correct}% better than average. <br> It took you {compare_time}% more than average.</span>')
        else:
            compare_time = compare_time * -1
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_correct}% better than average. <br> It took you {compare_time}% less than average.</span>') 
    else:
        compare_correct = compare_correct * -1
        if compare_time >0:
            compare_time = compare_time
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_correct}% worse than average. <br> It took you {compare_time}% more than average.</span>')
        else:
            compare_time = compare_time * -1
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_correct}% worse than average. <br> It took you {compare_time}% less than average.</span>') 
    return display(html_comparison)

#Comparison of results visualised through a scatter plot
def comparison_plot(ID, time, score, mean_time, mean_score):
    """
    This function visualises respondents' results in comparison to mean results in a scatter plot. 
    Mean score and mean time taken are plotted as dotted horizontal and vertical lines. 
    """
    # plot all previous responses
    plt.figure(figsize=(6, 4))
    plt.scatter(spreadsheet_df["total_time"], spreadsheet_df["final_score"], color="silver", label="All Responses")

    # plot mean score and mean time as reference lines
    plt.axvline(x=mean_time, color="pink", linestyle="--", label="Mean Time")
    plt.axhline(y=mean_score, color="khaki", linestyle="--", label="Mean Score")

    # plot respondent's results as comparison
    plt.scatter(time, score, color="royalblue", label=ID)

    # add labels and legend
    plt.xlabel("Total Time (s)")
    plt.ylabel("Final Score")
    plt.title("Individual Results vs. Mean Results")
    plt.legend()

    # show plot
    plt.grid(True)
    plt.show()

    return

# Function to check the username 
def check_username():
    '''
    This function asks the user to input a username and checks if the username already exists in the Google Sheet for the spatial test.
    If the username exists, it displays a message asking the user to make another username and produces a line for re-input.
    If the username does not exist, it returns the new username.
    Returns: original username.
    '''
    while True:  # Loop to allow for re-input if username is taken
        ans1 = text_input("")  # Corrected variable name for input
        google_json = os.environ["GOOGLE_JSON"]
        # Ensure the JSON is decoded to a string if it's in bytes
        if isinstance(google_json, bytes):
            google_json = google_json.decode('utf-8')
        # Ensure the JSON string is converted to a dictionary
        if isinstance(google_json, str):
            google_json = json.loads(google_json)
            credentials = service_account.Credentials.from_service_account_info(google_json)
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds_with_scope = credentials.with_scopes(scope)
            client = gspread.authorize(creds_with_scope)
            spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1jlGqKvzAmFnNpNvvL6jF3m0knTq_bBhSQvJPRdR8nhs/edit?usp=sharing')
            worksheet = spreadsheet.get_worksheet(0)
            records_data = worksheet.get_all_records()
            spreadsheet_df = pd.DataFrame.from_dict(records_data)
            style = f'font-size: 20px'
            if ans1 in spreadsheet_df['ID'].values:
                display(HTML(f'<span style="{style}">This username is already taken. <br> Please choose another one. </span>'))
            else:
                display(HTML(f'<span style="{style}">Username added successfully!</span>'))
                return ans1  # Exit the function after successful addition

        
#Copied function for sending responses to google form from the week 6 documents
def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

#Copied function for making buttons from the week 6 documents (buttons fix)

event_info = {
    'type': '',
    'description': '',
    'time': -1
}

def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info

def register_btn_event(btn):
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

def register_text_input_event(text_input):
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    return

def text_input(prompt=None):
    text_input = widgets.Text(description=prompt, style= {'description_width': 'initial'})
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text_input.on_submit(register_text_input_event)
    display(text_input)
    event = wait_for_event(timeout=10)
    text_input.disabled = True
    return event['description']

# Image production using Image installation
test1 = Image("test_10 VS 9.png", width=450)
test2 = Image("test_12 VS 16.png", width=450)
test3 = Image("test_12 VS 9.png", width=450)
test4 = Image("test_14 VS 12.png", width=450)
test5 = Image("test_15 VS 20.png", width=450)
test6 = Image("test_18 VS 16.png", width=450)
test7 = Image("test_18 VS 21.png", width=450)
test8 = Image("test_20 VS 18.png", width=450)
test9 = Image("test_10 VS 9 (2).png", width=450)
test10 = Image("test_12 VS 16 (2).png", width=450)
test11 = Image("test_12 VS 9 (2).png", width=450)
test12 = Image("test_14 VS 12 (2).png", width=450)
test13 = Image("test_15 VS 20 (2).png", width=450)
test14 = Image("test_18 VS 16 (2).png", width=450)
test15 = Image("test_18 VS 21 (2).png", width=450)
test16 = Image("test_20 VS 18 (2).png", width=450)
test17 = Image("test_10 VS 9 (3).png", width=450)
test18 = Image("test_12 VS 16 (3).png", width=450)
test19 = Image("test_12 VS 9 (3).png", width=450)
test20 = Image("test_14 VS 12 (3).png", width=450)
test21 = Image("test_15 VS 20 (3).png", width=450)
test22 = Image("test_18 VS 16 (3).png", width=450)
test23 = Image("test_18 VS 21 (3).png", width=450)
test24 = Image("test_20 VS 18 (3).png", width=450)
test25 = Image("test_10 VS 9 (4).png", width=450)
test26 = Image("test_12 VS 16 (4).png", width=450)
test27 = Image("test_12 VS 9 (4).png", width=450)
test28 = Image("test_14 VS 12 (4).png", width=450)
test29 = Image("test_15 VS 20 (4).png", width=450)
test30 = Image("test_18 VS 16 (4).png", width=450)
test31 = Image("test_18 VS 21 (4).png", width=450)
test32 = Image("test_20 VS 18 (4).png", width=450)
test33 = Image("test_10 VS 9 (5).png", width=450)
test34 = Image("test_12 VS 16 (5).png", width=450)
test35 = Image("test_12 VS 9 (5).png", width=450)
test36 = Image("test_14 VS 12 (5).png", width=450)
test37 = Image("test_15 VS 20 (5).png", width=450)
test38 = Image("test_18 VS 16 (5).png", width=450)
test39 = Image("test_18 VS 21 (5).png", width=450)
test40 = Image("test_20 VS 18 (5).png", width=450)
test41 = Image("test_10 VS 9 (6).png", width=450)
test42 = Image("test_12 VS 16 (6).png", width=450)
test43 = Image("test_12 VS 9 (6).png", width=450)
test44 = Image("test_14 VS 12 (6).png", width=450)
test45 = Image("test_15 VS 20 (6).png", width=450)
test46 = Image("test_18 VS 16 (6).png", width=450)
test47 = Image("test_18 VS 21 (6).png", width=450)
test48 = Image("test_20 VS 18 (6).png", width=450)
test49 = Image("test_10 VS 9 (7).png", width=450)
test50 = Image("test_12 VS 16 (7).png", width=450)
test51 = Image("test_12 VS 9 (7).png", width=450)
test52 = Image("test_14 VS 12 (7).png", width=450)
test53 = Image("test_15 VS 20 (7).png", width=450)
test54 = Image("test_18 VS 16 (7).png", width=450)
test55 = Image("test_18 VS 21 (7).png", width=450)
test56 = Image("test_20 VS 18 (7).png", width=450)
test57 = Image("test_10 VS 9 (8).png", width=450)
test58 = Image("test_12 VS 16 (8).png", width=450)
test59 = Image("test_12 VS 9 (8).png", width=450)
test60 = Image("test_14 VS 12 (8).png", width=450)
test61 = Image("test_15 VS 20 (8).png", width=450)
test62 = Image("test_18 VS 16 (8).png", width=450)
test63 = Image("test_18 VS 21 (8).png", width=450)
test64 = Image("test_20 VS 18 (8).png", width=450)

test_blank = Image("Blank.jpg", width=450) 

# Define the correct answers for each task
answers = dict( 
    task1 = [test1, 'Left'],
    task2 =[test2, 'Right'],
    task3 =[test3,'Left'],
    task4 =[test4, 'Left'],
    task5 =[test5, 'Right'],
    task6 =[test6, 'Left'],
    task7 =[test7, 'Right'],
    task8 =[test8, 'Left'],
    task9 =[test9, 'Left'],
    task10 =[test10,'Right'],
    task11 =[test11, 'Left'],
    task12 =[test12, 'Left'],
    task13 =[test13, 'Right'],
    task14 =[test14, 'Left'],
    task15 =[test15,'Right'],
    task16 =[test16, 'Left'],
    task17 =[test17, 'Left'],
    task18 =[test18, 'Right'],
    task19 =[test19, 'Left'],
    task20 =[test20, 'Left'],
    task21 =[test21,'Right'],
    task22 =[test22, 'Left'],
    task23 =[test23, 'Right'],
    task24 =[test24, 'Left'],
    task25 =[test25, 'Left'],
    task26 =[test26, 'Right'],
    task27 =[test27, 'Left'],
    task28 =[test28, 'Left'],
    task29 =[test29, 'Right'],
    task30 =[test30, 'Left'], 
    task31 =[test31, 'Right'], 
    task32 =[test32, 'Left'],
    task33 =[test33, 'Left'],
    task34 =[test34, 'Right'],
    task35 =[test35, 'Left'],
    task36 =[test36, 'Left'],
    task37 =[test37, 'Right'],
    task38 =[test38, 'Left'],
    task39 =[test39, 'Right'],
    task40 =[test40, 'Left'],
    task41 =[test41, 'Left'],
    task42 =[test42, 'Right'],
    task43 =[test43, 'Left'],
    task44 =[test44, 'Left'],
    task45 =[test45, 'Right'],
    task46 =[test46, 'Left'], 
    task47 =[test47, 'Right'],
    task48 =[test48, 'Left'],
    task49 =[test49, 'Left'],
    task50 =[test50, 'Right'],
    task51 =[test51, 'Left'], 
    task52 =[test52, 'Left'],
    task53 =[test53, 'Right'], 
    task54 =[test54, 'Left'],
    task55 =[test55, 'Right'],
    task56 =[test56, 'Left'],
    task57 =[test57, 'Left'],
    task58 =[test58, 'Right'],
    task59 =[test59, 'Left'], 
    task60 =[test60, 'Left'], 
    task61 =[test61, 'Right'],
    task62 =[test62, 'Left'], 
    task63 =[test63, 'Right'],
    task64 =[test64, 'Left'])
    

#Create a dataframe for the images and correct answers
df_ans = pd.DataFrame(data=answers)
df_ans = df_ans.fillna(' ').T

def dot_comparison_task(df_ans): 
    '''The function runs the ANS test, which measures the ability to quickly detect which image has more dots/objects.
    The function displays an image with two sets of dots for 0.75s followed by a blank image and asks the user to click on the button that represents the side with more dots.
    The function records the number of correct answers (num_correct) and time taken to complete the test.
    Then the function uploads the results to the Google Form if it has the user's agreement.
    The function returns the number of correct answers and time taken as an HTML output.'''
    
    # Style for HTML text
    style = f'font-size: 20px'
    random.seed(1)
    # Create a dictionary for Google Forms
    ans_data_dict = {'ID': [],
                     'Gender': [],
                     'Age': [],
                     'Substances': [],
                     'Correct': [],
                     'Correct proportion': [],
                     'Time': []
                    }
    num_correct = 0 
    display(HTML(f'<span style ="{style}">Welcome to the ANS test!</span>'))
    time.sleep(1)
    # The following 4 questions ask the user for demographic information
    display(HTML(f'<span style ="{style}">Please read: <br>  <br> We wish to record your response data <br> to an anonymised public data repository. <br> Your data will be used for educational teaching purposes <br> practising data analysis and visualisation. <br>  <br> Please click   yes   in the box below if you consent to the upload.</span>'))
    btn1 = widgets.Button(description="Yes")
    btn2 = widgets.Button(description="No")
    btn1.on_click(register_btn_event) 
    btn2.on_click(register_btn_event)
    panel = widgets.HBox([btn1, btn2])
    display(panel)
    consent_result = wait_for_event(timeout=200)
    clear_output()
    id_instructions = HTML(f"<span style ='{style}'>Enter your anonymised ID <br> To generate an anonymous 4-letter unique user identifier please enter: <br> - two letters based on the initials (first and last name) of a childhood friend <br> - two letters based on the initials (first and last name) of a favourite actor / actress <br> e.g. if your friend was called Charlie Brown and the film star was Tom Cruise <br> then your unique identifier would be CBTC</span>")
    display(id_instructions)
    time.sleep(3)
    clear_output(wait=True)
    display(HTML(f'<span style ="{style}">Please use the same ID for all Group 6 cognitive tests. <br> Please type in your ID: </span>'))
    ans1 = check_username()
    time.sleep(0.5)
    clear_output(wait=True)
    display(HTML(f'<span style ="{style}">Please type in your gender:</span>'))
    ans2 = text_input('')
    time.sleep(0.5)
    clear_output(wait=True)
    display(HTML(f'<span style ="{style}">Please type in your age:</span>'))
    ans3 = text_input('')
    time.sleep(0.5)
    clear_output(wait=True)
    display(HTML(f'<span style ="{style}">Have you consumed any substances (Eg. alcohol or drugs) in the last 12 hours that might affect your cognitive abilities?</span>'))
    ans4 = text_input('') 
    time.sleep(0.5)
    clear_output(wait=True)
    display(HTML(f'<span style = "{style}">In this test, you will need to choose the side with more dots (left or right). <br> You will have 0.75s to look at the image and 3s to answer. <br> There will be 64 questions. <br> Click the buttons to answer the question. </span>'))
    start_time = time.time()
    time.sleep(5)
    
    for i in range(64):  # Perform sixty-four blocks
        display(df_ans[0][i])
        time.sleep(0.75)
        clear_output(wait=True) 
        display(test_blank)
        response_start_time = time.time()
        # Ask for user input
        display(HTML(f'<span style ="{style}">Which side has more dots? (left/right):</span>'))
        btn1 = widgets.Button(description='Left')
        btn2 = widgets.Button(description='Right')
        btn1.on_click(register_btn_event) 
        btn2.on_click(register_btn_event)
        panel = widgets.HBox([btn1, btn2])
        display(panel)
        response = wait_for_event(timeout=3)
        clear_output()
        response_time = time.time() - response_start_time

        # Check if the response is valid and within the time limit
        if response_time <= 3.0:
            # Check if the user's answer is correct
            if response['description'] == df_ans[1][i]:
                num_correct +=1
                display(HTML(f'<span style ="{style}">Correct!</span>'))
                time.sleep(0.5)
                clear_output(wait=False)
            else:
                display(HTML(f'<span style ="{style}">Incorrect!</span>'))
                time.sleep(0.5)
                clear_output(wait=False)
        else:
            display(HTML(f'<span style ="{style}">No response detected or time exceeded.</span>'))
            time.sleep(0.5)
            clear_output(wait=False)
           
        time.sleep(0.5)
        clear_output(wait=True) 
    
    end_time = time.time() 
    elapsed_time = round(end_time - start_time, 2)  # Calculate total time taken
    html_out = HTML(f'<span style ="{style}">Time taken to complete the test: {elapsed_time} seconds. <br> Number of correct answers: {num_correct}.</span>')
    if consent_result['description'] == "Yes":
        ans_data_dict["ID"].append(ans1)
        ans_data_dict["Gender"].append(ans2)
        ans_data_dict["Age"].append(ans3)
        ans_data_dict["Substances"].append(ans4)
        ans_data_dict["Time"].append(str(elapsed_time))
        ans_data_dict["Correct"].append(str(num_correct))
        ans_data_dict["Correct proportion"].append(str(round(num_correct/64, 2)))
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdXvUjero2yh_CFCymqVlydVmTAKmLFHJQyy4MXZ4wbEl6FEw/viewform?usp=sf_link"
        display(HTML(f'<span style ="{style}"> Thanks for your participation. <br> Please contact a.fedorec@ucl.ac.uk <br> If you have any questions or concerns <br> regarding the stored results.</span>'))
        send_to_google_form(ans_data_dict, form_url)
    else:
        display(HTML(f'<span style ="{style}"> No problem, we hope you enjoyed the test.</span>'))
    compare_to_mean(elapsed_time, num_correct)
    return display(html_out)  # Showing the user their result

dot_comparison_task(df_ans)



