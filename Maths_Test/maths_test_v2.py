# This imports everything necessary for this code to run
import time
from IPython.display import display,Image, HTML, clear_output
import ipywidgets as widgets
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json 
from jupyter_ui_poll import ui_events
import gspread 
from oauth2client.service_account import ServiceAccountCredentials 
from google.oauth2 import service_account
import gspread
import json
import os
import matplotlib.pyplot as plt
import numpy as np

#This ode imports my data from google sheets and converts it onto a pandas dataframe
google_json = r"""
{
  "type": "service_account",
  "project_id": "maths-ability-test",
  "private_key_id": "e890da2538f47fe0b498eb63e7776456febf755c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDPrj1gLHhI3Kv4\nTQLUKwllE/9dDxE6QmtkhErxSChNJcDvVYP4AcPyMj3PwZ8Fiv1k78REd/Wzv1Us\ngxyx7VsbBQMBOQNZC/Cmv7i38wY3X1fzWi8o9OmTLdxx7EWGfbpSQ0cIkywoVynO\n2IX0W8BPDNtVuKZRQt85jEvTUyGLsW/QzPxAhggFXSvEr1wVmMjClEQNj9V08fb+\n2m3iK3A3bfemHuN+IkwrUjI7l3/rrKOYJlCSQq6NT54sAKTZVVHClF+N2YVy4Kko\nJs1Tk/X2HuO6MlXC0yj78RXk0eUMngLQWBg2I8VAxoAz13LpVOVItPV3/GfBW+QZ\nfGGuIVXXAgMBAAECggEAE2P6WQtt46eu6s0N8Y9fHi/izOaGPkFLU6RCdwq8sI9Q\n10fNvY80o11rhgVW+qaCiDUWxynIKBM6OaC4QiieNASgxjFzjZHe00LdVVd8ghkF\n1jPaaWGMmXBTv9NGnosIpXugmz1ahx20SprOzwTuDLNvmy5VYQr0WqQtxDpjzG4G\npCfPCN3+eBGCRMkJfWasm8u06CqlIBOlSGrNZbDqxv2DH+g9UQvGydylLDxkmKwk\n1OD3+0SstFSaVB33UG8OW+ChyHn0TfqnjVTidtiDtC0E3CwkJz//9A71imo5n0By\noZ2pYGV5nDLYnzfIqjSCWlGUBRA6BerhqGftWSZ0aQKBgQDuzCV86VKxcgSpC0QB\n0SZiEzpCUU1B2OtqViwM7mYY3qlnpVzIMytob4lVY0qRkcRCa1xL4SKaqQ9hjNYp\nsB/J8QoOpwxY9ANmIHTQIZYBNjoN4XJKLJ4lnA/3MiLJxTyvOkfg1sIG4DLdCv8/\na9XIMuDnyk5SXoq/LRbyvHuVcwKBgQDepD5FCJZ6QoSNAP1PXxcSHOjESEPcgEFm\nH971iUhliIiQRzz45BVlRpTQ7SdI7ORCLEDstZ3Bw/tYfzCyXnO1dyGSFDSakjyL\nSHDGG3wSQe9AUEc0572k3M7anRsgvVDDlLZZ2AD5gaaOHOdvRo6yCCaKqQabV3uw\nb/2avnKFDQKBgQC8XWx0y9ffAQGMFsbeaAzO8DvUdC1s858/khnNWYBPvdQDXf2C\nLlrfVpwOLvRzP3iArA9yC3Uwaosnd+C3oaZxtSEpzbt/r3u+43tBcjzRV+UTbfKp\nb+iP4jr10yZ94oer8V0hjkYfBlsY4cPWU0mfUgL21C5T6x+nDfo8H1Gc4QKBgQDB\nHByWrBg4+zEVTGJqUcQlBcYvWa7itqwC9Gni9qxAxOgOnHuaNdsI+OtjPA/zBOYH\nL3Mw3WZ0BpUf8VI/pAUgxK/tkHEAEQ9KkA6hBn3bKC1ozziz/r1THeKdY99/yjUf\nLwHrc5uEzpu0cAWdUsm6Sa+EXY9Jddvm8Xw6mC2kkQKBgQC4HMl7KwNYCTT+r5IQ\n8uFpTzB7lAggCwzw2s+v6p+dBASPepZwZG1o063Dn3iiJ28r4LrKO2CA+q9tm5Wh\nNJQ9Pl4PGOvoTdsCUS/sn64T4Aia0vZkdZPijQMgdNThJF1lShJ1piq4aazz3AF1\n3eS7+boUKFrSx8mQn14+5eMN4g==\n-----END PRIVATE KEY-----\n",
  "client_email": "maths-test@maths-ability-test.iam.gserviceaccount.com",
  "client_id": "104379896158258427149",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/maths-test%40maths-ability-test.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

# Created credentials object from the service account credential json
service_account_info = json.loads(google_json)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Assign API scope to credentials so it has permission to interdace
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_with_scope = credentials.with_scopes(scope)

client = gspread.authorize(creds_with_scope)

spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1gLQzRUIP4c4cI7_-fA60wzbeT71GRrz6B1avRnUfz0w/edit?resourcekey#gid=1737581509')

worksheet = spreadsheet.get_worksheet(0)

# Get all records from the sheet
records_data = worksheet.get_all_records()

# Convert records to DataFrame and display
records_df = pd.DataFrame.from_dict(records_data)

# These functions were provided allowing data to be sent to google forms and for buttons to function
def send_to_google_form(data_dict, form_url):
    ''' 
    Helper function to upload information to a corresponding google form 
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
    event = wait_for_event(timeout=60)
    text_input.disabled = True
    return event['description']

# This function displays information about the tests and to count down time until questions begin
def countdown(timer):
    """
    Countdown function to display information about the test and a timer till the questions 
    are displayed
    Arguments: timer(the duration of the countdown in seconds)
    Returns: none
    """
    while timer:
        intro_to_test = f"""Welcome to the Maths Ability Test <br>
        This test will begin by asking questions about yourself <br>
        Then you will be asked maths questions <br> 
        This test starts in: {timer} seconds"""
        display(HTML(f"<h3>{intro_to_test}</h3>"))
        time.sleep(1)
        timer -= 1
        clear_output(wait=True)

    clear_output(wait=True)

# This cell contains a function to gain consent from the user if they are happy to have their data uploaded to google sheets
def data_consent():
    """
    data_consent function asks whether the user consents to having their data uploaded to google sheets. The consent is given on not given by a using pressing a button
    Arguments: none
    Returns: consent (if the user consents to the data upload, 1 is added to consent, if they do not consent, consent remains 0
    """
    consent = 0
    btn1 = widgets.Button(description="Yes")
    btn2 = widgets.Button(description="No")
    
    btn1.on_click(register_btn_event)
    btn2.on_click(register_btn_event)
    
    # To give the user the option of not uploading their scores and answers, there is a button and the score is only uploaded if they click yes
    data_consent_info = """
    Please read: <br>
    We wish to store you response data to an anonymised public data repository. Your
    data will be used for educational teaching purposes practising data analysis and
    visualisation. <br>
    Please press yes if you consent to your data being uploaded"""
    display(HTML(f"<h3>{data_consent_info}</h3>"))

    # Displays th buttons
    panel = widgets.HBox([btn1, btn2])
    display(panel)
    
    result = wait_for_event()
    if result['description'] == "Yes":
        consent += 1
    else:
        consent = 0
    clear_output(wait=False)
    return consent

# This function asks the user questions about themselves, these answers are necessary for the data analysis
def introduction_questions():
    """
    This function asks the user for their ID, age, gender, any substances they have taken
    Arguments: none
    Returns: user_id1 (the id of the user), ans11 (the users age), ans21 (the users gender), ans31 (the substances a user has taken) 
    """
    # Instructions for how the user should set their ID
    id_instructions = """
    Enter your anomised ID <br>
    To generate an anonymous 4-letter unique user identifier please enter: <br>
    Two letters based on the initials of a chldhood friend <br> Two initials based on a favourite actor/ actress <br>
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise, then your unique identifier would be CBTC <br>
    This should be the same as what is used for other tests done for group 6"""
    display(HTML(f"<h3>{id_instructions}</h3>"))
    user_id1 = text_input("> ")
    clear_output(wait=True)

    # Questions about the user to use the data collected for analysis
    display(HTML("<h3>What is your age?</h3>"))
    ans11 = text_input("> ")
    clear_output(wait=True)
    
    display(HTML("<h3>What is your gender?</h3>"))
    ans21 = text_input("> ")
    clear_output(wait=True)
    
    display(HTML("<h3>Have you consumed any substances (Eg. caffeine, alcohol, or drugs) in the last 12 hours that might affect your cognitive abilities?</h3>"))
    display(HTML("<h3>Note: Please enter 'yes' or 'no'. If yes please specify. Press enter if you would prefer not to disclose this information.</h3>"))
    ans31 = text_input("> ")
    clear_output(wait=True)

    return user_id1, ans11, ans21, ans31 # Returns the users answers so they can be collects and uploaded to google forms

# This function contains an introduction to the test and instructions about what type of numbers to put into the questions
def countdown_intro(timer):
    """
    Countdown function to display information about the test and a timer till the questions 
    are displayed
    Arguments: timer(the duration of the countdown in seconds)
    Returns: none
    """
    while timer:
        intro_2 = f"""This part of the test will ask you maths questions <br>
        There are 3 levels to complete, each with 5 questions <br>
        Each question has 3 attempts <br>
        Each correct answer gains 2 points, each incorrect answer loses 1 point <br>
        Please enter whole numbers only <br>
        This test starts in: {timer} seconds"""
        display(HTML(f"<h3>{intro_2}</h3>"))
        time.sleep(1)
        timer -= 1
        clear_output(wait=True)

    clear_output(wait=True)

# The following three functions are for the three different levels in the test. 
# Each functions displays the equations then allows the user to enter their answers
# Each question has 3 attempts, with each correct answer gaining a point, and each incorrect answer loosing a point

def addition_questions(number_one, number_two):
    """
    This asks the user 5 addition questions and allows the user to input the answer
    Arguments: number_one (the first number in the question, number_two (the second number
    in the question)
    Returns: a tuple containing time_taken (the time taken to answer each question, counter_add 
    (the score of the user) and incorrect_answers_add (the number of incorrect answers)
    """
    
    # To define the inital values as 0
    counter_add = 0
    incorrect_answers_add = 0

    # The formula for how the coreect answer is calculated
    correct_answer = int(number_one) + int(number_two)

    # Loop so each question has 3 attempts. If the user gets a question wrong, they loose an attempt
    # This loop will run till the user answers correctly or runs out of attempts
    attempts = 3
    while attempts >= 0:
        # These display the questions. Each number and operator is displayed for a short period of time then disappears
        display(HTML(f"<span style='font-size: 90px;'>{number_one}</span>"))
        time.sleep(2)
        clear_output()

        display(HTML("<span style='font-size: 90px;'>+</span>"))
        time.sleep(1)
        clear_output(wait=True)

        display(HTML(f"<span style='font-size: 90px;'>{number_two}</span>"))

        # Starts the timer
        start_time=time.time()

        # Allows the user to input their answer
        display(HTML("<h3>Enter the answer: </h3>"))
        user_answer = int(text_input("> "))
        if user_answer == correct_answer: # If the answer is correct this code runs
            display(HTML("<h3>Well done!</h3>"))
            time. sleep(1)
            counter_add += 2 # The user gains two points when correct
            break # If the user answers correctly the loop is broken 
        elif attempts>1: # This code runs if the user is incorrect but still has attempts left
            attempts -= 1 # Lowers the number of attempts
            counter_add -=1 # Lowers the number of attempts
            incorrect_answers_add += 1 # Increases the number incorrect
            display(HTML("<h3>Incorrect answer!</h3>"))
            display(HTML(f"<h3>You have {attempts} attempts left.</h3>"))
            time.sleep(2)
            clear_output(wait=True)
        else: # If the user runs out of attempts, the correct answer is displayed
            display(HTML(f"<h3>Incorrect answer! The correct answer was: {correct_answer}</h3>"))
            counter_add -=1 # Lowers the number of attempts
            incorrect_answers_add += 1 # Increases the number incorrect
            time.sleep(2)
            clear_output(wait=True)
            break

    # Ends the timer
    end_time = time.time()

    #Calculates the time taken per question
    time_taken = end_time - start_time

    return time_taken, counter_add, incorrect_answers_add

def mixed_questions(number_three, number_four, number_five):
    """
    This asks the user 5 questions involving multiplication and addition and allows the user to input the answer
    Arguments: number_three (the third number in the question), number_four (the fourth number
    in the question), number_five (the fifth number if the question)
    Returns: a tuple containing time_taken2 (the time taken to answer each question, counter 
    (the score of the user) and incorrect_answers_add (the number of incorrect answers)
    """

    # Defines the initial values as 0
    counter_mixed = 0
    incorrect_answers_mixed = 0

    # Defines how the correct answer for these questions is calculated
    correct_answer = int(number_three) * int(number_four) +int(number_five)

    attempts = 3 # Gives each question 3 attempts
    while attempts >= 0: # So the loop only runs when there are greater than or equal to zero attempts
        # Displays each number and operator for short periods of time before being cleared
        display(HTML(f"<span style='font-size: 90px;'>{number_three}</span>"))
        time.sleep(2)
        clear_output()

        display(HTML("<span style='font-size: 90px;'>x</span>"))
        time.sleep(1)
        clear_output(wait=True)

        display(HTML(f"<span style='font-size: 90px;'>{number_four}</span>"))
        time.sleep(2)
        clear_output(wait=True)

        display(HTML("<span style='font-size: 90px;'>+</span>"))
        time.sleep(1)
        clear_output(wait=True)

        display(HTML(f"<span style='font-size: 90px;'>{number_five}</span>"))

        # Starts the timer
        start_time=time.time()

        display(HTML("<h3>Enter the answer: </h3>"))
        user_answer = int(text_input("> ")) # To allow the user to enter their answer
        if user_answer == correct_answer: # If the user is correct, this code runs
            display(HTML("<h3>Well done!</h3>"))
            time.sleep(1)
            counter_mixed += 2 # User gains points if they answer correctly, then the loop breakks 
            break
        elif attempts>1: # If the loser get the questions wrong but still has attempters left
            attempts -= 1 # Looses an attempt
            counter_mixed -=1 # Looses a point
            incorrect_answers_mixed += 1 # Adds to the score of incorrect answers
            display(HTML("<h3>Incorrect answer!</h3>"))
            display(HTML(f"<h3>You have {attempts} attempts left.</h3>"))
            time.sleep(2)
            clear_output(wait=True)
        else: # If the user runs out of attempts the correct answer is displayed
            display(HTML(f"<h3>Incorrect answer! \nThe correct answer was: {correct_answer}</h3>"))
            counter_mixed -=1 # Looses a point
            incorrect_answers_mixed += 1 # Adds to the score of incorrect answers
            time.sleep(2)
            clear_output(wait=True)
            break

    # Stops the clock running
    end_time = time.time()

    # Calculates the time taken per question
    time_taken2 = end_time - start_time

    return time_taken2, counter_mixed, incorrect_answers_mixed

def mixed_questions2(number_six, number_seven, number_eight):
    """
    This asks the user 5 questions involving division and addition and allows the user to input the answer
    Arguments: number_six (the sixth number in the question), number_seven (the seventh number
    in the question), number_eigth (the eigth number if the question)
    Returns: a tuple containing time_taken3 (the time taken to answer each question, counter 
    (the score of the user) and incorrect_answers_add (the number of incorrect answers)
    """
    
    # Defines the initial values as 0
    counter_mixed2 = 0
    incorrect_answers_mixed2 = 0

    # Defines how these questions are answered
    correct_answer = int(number_six) / int(number_seven) + int(number_eight)

    # Loop to display the questions and allow the user to answer when they have attempts left
    attempts = 3
    while attempts >= 0:
        # Displays the numbers and operators used in these questions 
        display(HTML(f"<span style='font-size: 90px;'>{number_six}</span>"))
        time.sleep(2)
        clear_output()

        display(HTML("<span style='font-size: 90px;'>&divide;</span>"))
        time.sleep(1)
        clear_output(wait=True)

        display(HTML(f"<span style='font-size: 90px;'>{number_seven}</span>"))
        time.sleep(2)
        clear_output(wait=True)

        display(HTML("<span style='font-size: 90px;'>+</span>"))
        time.sleep(1)
        clear_output(wait=True)

        display(HTML(f"<span style='font-size: 90px;'>{number_eight}</span>"))

        # Starts the timer
        start_time=time.time()

        display(HTML("<h3>Enter the answer: </h3>"))
        user_answer = int(text_input("> ")) # To allow the user to answer
        if user_answer == correct_answer: # If the answer is correct, this code runs
            display(HTML("<h3>Well done!</h3>"))
            time. sleep(1)
            counter_mixed2 += 2 # The score increases when correct answer is given
            break
        elif attempts>1: # If the answer is wrong, this code runs
            attempts -= 1 # Lowers the numbers of attempts
            counter_mixed2 -=1 # Lowers the score
            incorrect_answers_mixed2 += 1 # Increases the number of incorrect answers
            display(HTML("<h3>Incorrect answer!</h3>"))
            display(HTML(f"<h3>You have {attempts} attempts left.</h3>"))
            time.sleep(2)
            clear_output(wait=True)
        else: # If the answer is wrong and the user has run out of attempts
            display(HTML(f"<h3>Incorrect answer! The correct answer was: {correct_answer}</h3>"))
            counter_mixed2 -=1 # Lowers the score
            incorrect_answers_mixed2 += 1 # Increases the number of incorrect attempts
            time.sleep(2)
            clear_output(wait=True)
            break

    # Stops the timer
    end_time = time.time()

    # Calculates the time taken per questions
    time_taken3 = end_time - start_time

    return time_taken3, counter_mixed2, incorrect_answers_mixed2 

# This function compares number of correct answers and time taken to the mean values for these variables as an HTML message for the user
def compare_to_sheets(counter):
    '''
    Compare to mean function takes in the return of the spatial_test() function for the user and compares it to the mean of returns of the previous users.
    Arguments: score (the score the user achieved)
    Returns: none
    '''
    global records_df
    records_df['counter'] = records_df['counter'].replace('', np.nan).astype(float, errors='ignore')
    records_df = records_df.dropna(subset=['counter'])
    
    median_grade = records_df['counter'].astype(int).median()
    user_score= counter
    display(HTML(f"<h3>Median score is {median_grade}</h3>"))
    time.sleep(2)
    
    # Count the frequency of each value in the column
    #value_counts = records_df['counter'].value_counts().sort_index()

    plt.figure(figsize=(10, 4))
    records_df.boxplot(column='counter', vert=False)  # Set vert=False to switch the scores to the x-axis
    
    # Add an extra dot at value 10
    plt.scatter(x=counter, y=1, color='red', zorder=5)  # zorder ensures the dot is plotted on top of the box plot
    
    # Add labels and title
    plt.title('Box plot of scores, red dot is your score')
    plt.xlabel('Score')
    plt.xlim(0,30)
    
    # Show the plot
    plt.show()

# This function allows the test to run. The test only runs if the user consents to upload of the data
# It contains data dictionary for the users answers to be added to, the numbers used in the test
def maths_ability_test():
    """
    This function condusts the maths ability test.
    This function starts the maths test after a countdown and if the user has consented to participate.
    If the user consents, it sets up a dictionary to store the user's results and conducts the test.
    The test consists of addition, multiplication and division questions with varying difficulty levels.
    The user's answers, time taken, and scores are recorded in the data dictionary.
    After the test, the results are displayed to the user and uploaded to a Google Form.
    If the user does not consent the test does not take place
    Arguments: none
    Returns: none
    """
    
    timer = 5
    countdown(timer)
    
    consent1 = data_consent()
    # Sets up the dictionary with empty lists, so the users results can be added to them
    data_dict = {
    'id': [],
    'age': [],
    'gender': [],
    'substance': [],
    'addition time': [],
    'addition score': [],
    'addition incorrect': [],
    'mixed time': [],
    'mixed score': [],
    'mixed incorrect': [],
    'mixed 2 time': [],
    'mixed 2 score': [],
    'mixed 2 incorrect': [],
    'average time': [],
    'counter': [],
    'total incorrect': []
    }

    user_id, ans1, ans2, ans3 = introduction_questions()

    timer = 8
    countdown_intro(timer)

    # The numbers that I use in my questions, the numbers get harder through each section as the questions progress
    numbers_list = ['12', '13', '49', '36', '127']
    numbers_list2 = ['11', '54', '65', '87', '52']
    numbers_list3 = ['5', '11', '9', '14', '23']
    numbers_list4 = ['7', '4', '12', '7', '11']
    numbers_list5 = ['6', '12', '13', '34', '7']
    numbers_list6 = ['18', '45', '56', '87', '135']
    numbers_list7 = ['6', '9', '7', '3', '5']
    numbers_list8 = ['33', '46', '52', '16', '46']
    
    # Puts all the types of questions into a list, so they can be shuffled
    question_functions = [addition_questions, mixed_questions, mixed_questions2]
    
    # Shuffle the list to randomize the order of question types
    random.seed(1)  
    random.shuffle(question_functions)
    
    total_time = 0
    total_time2 = 0
    total_time3 = 0
    total_counter_add = 0
    total_counter_mixed = 0
    total_counter_mixed2 = 0
    total_incorrect_answers = 0
    counter = 0
    
    # Loop to go through the different types of questions in a random order
    for func in question_functions:
        clear_output(wait=True)
        if func == addition_questions: # This code is run when addition questions are called on
            for num_one, num_two in zip(numbers_list, numbers_list2): # Takes numbers from numbers list one and numbers list 2
                clear_output(wait=True)
                time_taken, counter_add, incorrect_answers_add = addition_questions(num_one, num_two)
                total_time += time_taken # Adds together the time for each question in this question
                total_counter_add += counter_add # Adds to the score for addition questions
                total_incorrect_answers += incorrect_answers_add # Adds to total number of incorrect numbers
        elif func == mixed_questions: # This code is run when mixed questions are called on
            for num_three, num_four, num_five in zip(numbers_list3, numbers_list4, numbers_list5): # Uses numbers from list 3, 4, 5
                clear_output(wait=True)
                time_taken2, counter_mixed, incorrect_answers_mixed = mixed_questions(num_three, num_four, num_five)
                total_time2 += time_taken2 # Adds together the time for each question in this question
                total_counter_mixed += counter_mixed # Adds to the score for mixed questions
                total_incorrect_answers += incorrect_answers_mixed # Adds to total number of incorrect numbers
        elif func == mixed_questions2: # This code is run when mixed questions 2 are called on
            for num_six, num_seven, num_eight in zip(numbers_list6, numbers_list7, numbers_list8): # Uses numbers from list 6, 7, 8
                clear_output(wait=True)
                time_taken3, counter_mixed2, incorrect_answers_mixed2 = mixed_questions2(num_six, num_seven, num_eight)
                total_time3 += time_taken3 # Adds together the time for each question in this question
                total_counter_mixed2 += counter_mixed2 # Adds to the score for mixed questions 2
                total_incorrect_answers += incorrect_answers_mixed2  # Adds to total number of incorrect numbers
    
    clear_output(wait=True)
    
    average_time = (int(total_time) + int(total_time2) + int(total_time3)) / 15 # Calculates thr average time per question
    counter = total_counter_add + total_counter_mixed + total_counter_mixed2 # Calculates the total score

    # These display to  the user their score and time
    display(HTML(f"<h3>The average time to answer each question is: {average_time:.2f}</h3>"))
    time.sleep(2)
    display(HTML(f"<h3>Your final score is: {counter}/30</h3>"))
    time.sleep(2)

    compare_to_sheets(counter)
    if consent1 == 1:
        # This dictionary stores the users answers, so they can be uploaded to google sheets
        data_dict['id'].append(user_id)
        data_dict['age'].append(ans1)
        data_dict['gender'].append(ans2)
        data_dict['substance'].append(ans3)
        data_dict['addition time'].append(total_time)
        data_dict['addition score'].append(total_counter_add)
        data_dict['mixed time'].append(total_time2)
        data_dict['mixed incorrect'].append(incorrect_answers_mixed)
        data_dict['mixed 2 time'].append(total_time3)
        data_dict['mixed 2 score'].append(total_counter_mixed2)
        data_dict['mixed 2 incorrect'].append(incorrect_answers_mixed2)
        data_dict['average time'].append(average_time)
        data_dict['counter'].append(counter)
        data_dict['total incorrect'].append(total_incorrect_answers)
        form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfvTT-Bj4nQfALiUdBo-zcydTC9uHH3XecY4ReK4_tBJf9HQQ/viewform?usp=sf_link'
        send_to_google_form(data_dict, form_url)
        display(HTML(f'<h3> Thanks for your participation. <br> Please contact a.fedorec@ucl.ac.uk <br> If you have any questions or concerns regarding the stored results.<h3>'))
    else:
        display(HTML("<h3>Thanks for taking this test. <br>Your data has not been upladed to google forms</h3>"))

maths_ability_test()