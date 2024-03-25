from sklearn.utils import shuffle
from IPython.display import display, HTML, Image, clear_output
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import json 
import time
import gspread
import random
from google.oauth2 import service_account
import os
import ipywidgets as widgets
from jupyter_ui_poll import ui_events

os.environ["GOOGLE_JSON"] = json.dumps({
    "type": "service_account",
    "project_id": "spatial-reasoning-415622",
    "private_key_id": "1ad3846f6fdf518a0577eda565b8f5a7ce3f5ae1",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDCnv0ceRzIEKzh
vuaZXtaPnbKfNHeaQHlMH/4OfjrH4P46bZ26bE+OwPMGQV18h+cj3Lbn6db7mm4U
7jzz5zu0iMWXuCgOtfrsnP01NljipkaNRdcM7tVwr7I2B58e/xmOFS7D4clp7KKi
IIatl2RUZPZClYFN0WhypWyjk8QuulgmrspzrcO1xG/rklvST//3b71laM+l5V30
icU3yRydhPEmAAE8ek2WbcpF4dyeVabPFRkNDfio/wfB5pfLGWLo1RSKesoz+HaI
y1CZueuCnZrce2o2USnLzvMeqn0BUWSSKtyp6MqGCmpY2MaB+9/29Bj9KVDMRVAA
Zown3HSZAgMBAAECggEACmIiHelGRFRDbP3a3rblGp9uvri1Ytjqv8l7K/nHGA/k
cGiVwDL0IakgriZBnxm/FrY5WfErY5wPIHW/ccHV+SFM7XXJSVOjMgmEJtkh7+Gw
JOxjd1CsuYjeKKzKbARvMBnoN1IuBUU3PhAfL1bC5w/F5bKFRgoUmP1DaQzCrD10
EjWIdzSEx6nfCRFQfHTFTvqt4zA/V385kOwRRnpIXnCSuyPAUGy/9K/7GMDa0DGV
IBZ5p7bj0RrKVamanKQm9XjgtaycVP5ycTp+WRZPq6F3iOpacNz/ScR33lhpDrxq
xzx+k0ynE2/Q3NCTgjI76mQJA6aAH5RMyVCWCFl7MwKBgQDfoS5np7qHK7W30coD
uzlOAk0IEzc9Z3Av2XYG/1K/mOtv7PyCPcJR1OO8Sa4nYfs6arVLedjgmoUNSiOX
NCTljor1yg0MTQu4dYGWbKxYKeQr9isb0t9a3INHKPU/TpvhJ/q7q7iMPGws/gf0
iHuVR31p1XWRTD4YTE4IUkQyuwKBgQDeyt25P1b+lcwwEdmCY6djKKTcD+L4uoR6
Rr2gYbciWwkS1XpK440Dqv5NCy2gStuNnqWYxbkjChNe2bq1c7gBf6RFvES9hz9f
GeszH38UBzAtc/63qEWvP9niTL3QfE+0kXLOT3prmg3MjkqErNN+XeeNwUWTDVdA
qgBUB2rSuwKBgAH8ZnMZNDjbFIQLYuXhlcKxlomJ0iXDc2WZYsjxH4UAEKcvzZZC
giVD5LnZVaiX4ClGpVGERX7JIIFbtTE0j1dSir1gC/md/Yqn0HzLfkRSKuqRBxT6
LG2cI7ZQEM19HzlCp6FfBwaHytYjc2Kii6Zpuh1kfeTKboq8sry0LlLdAoGABku9
UErV7oPVLVaTyvd993NilUVtqJG8xKfTHAEm57Wi4AFgX1Vm2r+uSAcU1v7GjY36
KAMOZEsYmQmWGSKYBJLS1ZWoa6Kyy8EzwFIXiT1awy4P+Kisr3MieR6qDoY0ymmB
0Qq17ux/j1RGDtHDeEK3FG5txOYPnSgwsi8zeZkCgYEAqH6h6DD1PDKbFkuAozGK
RhtDXaMtAeDNGBlT8t6zoDlpVKLWZSVb3SyJ+OpA72ScDrRf2HbVcxkokSU33cAq
+nnnKMgwSs4a0/+dLMZnYWuAfXI7/e2n3piE8itzKXBYOo8ojhdZ9BTeU7bolsW2
xsRoUPhFQ9bJNNaR44ySEfs=
-----END PRIVATE KEY-----""",
    "client_email": "spatial-reasoning-test@spatial-reasoning-415622.iam.gserviceaccount.com",
    "client_id": "108672995315883551832",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/spatial-reasoning-test%40spatial-reasoning-415622.iam.gserviceaccount.com"
})
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

#Function that allows user to see how their result compares to the mean
def compare_to_mean(time, grade):
    '''
    This function is designed to provide feedback to users who have declined to submit their answers through Google Forms. 
    It compares the time it took for the user to complete the test and grade as percentage of correct answers with their respective averages from previous users, who consented to submit their answers through Google Forms. 
    The comparison results are then presented to the user in an HTML formatted message, showing how their performance and time taken to complete the test compare to the average. 

    The function extracts data from a Google Sheets document, stored in the environment in Jupyter Notebook, which contains records of previous users' grades and times. 
    It calculates the mean grade and mean time from this data, and then compares the user's grade and time to these mean values. 
    The comparison is expressed as a percentage difference from the mean, and the message is tailored to indicate whether the user's performance and time are better or worse than average.

    Takes in:
    - time (float): The time it took for the user to complete the test.
    - grade (float): The grade as percentage of correct answers the user achieved on the test.

    Returns:
    - An HTML formatted message displayed to the user, displaying how their test performance and time taken compare to the respective averages.
    '''
    google_json = os.environ["GOOGLE_JSON"]
    service_account_info = json.loads(google_json)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_with_scope = credentials.with_scopes(scope)
    client = gspread.authorize(creds_with_scope)
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1F8JrCifa0gcvj4trM3fU39NTBn3q0gL2F_-cpBjhqsA/edit?usp=sharing')
    worksheet = spreadsheet.get_worksheet(0)
    records_data = worksheet.get_all_records()
    spreadsheet_df = pd.DataFrame.from_dict(records_data)
    style = f'font-size: 20px'
    mean_grade = spreadsheet_df['Grade'].mean()
    mean_time = spreadsheet_df['Time'].mean()
    compare_grade = round((grade - mean_grade)/mean_grade * 100, 2)
    compare_time = round((time - mean_time)/mean_time * 100, 2)
    if compare_grade > 0:
        compare_grade = compare_grade
        if compare_time >0:
            compare_time = compare_time
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_grade}% better than average. <br> It took you {compare_time}% more than average.</span>')
        else:
            compare_time = compare_time * -1
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_grade}% better than average. <br> It took you {compare_time}% less than average.</span>') 
    else:
        compare_grade = compare_grade * -1
        if compare_time >0:
            compare_time = compare_time
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_grade}% worse than average. <br> It took you {compare_time}% more than average.</span>')
        else:
            compare_time = compare_time * -1
            html_comparison = HTML(f'<span style ="{style}"> Your score for the test is by {compare_grade}% worse than average. <br> It took you {compare_time}% less than average.</span>') 
    plt.figure(figsize=(6, 4))
    plt.scatter(spreadsheet_df['Time'], spreadsheet_df['Grade'], color='silver', label='All Responses')

    # plot mean score and mean time as reference lines
    plt.axvline(y=mean_grade, color='khaki', linestyle='--', label='Mean Score')
    plt.axhline(x=mean_time, color='peachpuff', linestyle='--', label='Mean Time')

    # plot individual's results as comparison
    plt.scatter(grade, time, color='royalblue', label= 'Your Result')

    # add labels and legend
    plt.ylabel('Final Score')
    plt.xlabel('Total Time (s)')
    plt.title('Individual Results vs. Mean Results')
    plt.legend()

        # show plot
    plt.grid(True)
    plt.show()
    return display(html_comparison)

def check_username():
    """
    This function asks the user to input a username and checks if the username already exists in the Google Sheet for the spatial test.
    If the username exists, it displays a message asking the user to make another username and produces a line for re-input.
    If the username does not exist, it returns the new username.
    
    The function uses the Google Sheets API to access and manipulate the spreadsheet data. 
    It uses the `gspread` library to authorize and interact with the Google Spreadsheet and `pandas` to handle the data.
    
    The function contains an infinite loop with a conditional return statement for successful username addition.
    This means it will keep running until a unique username is entered by the user.
    The function is required for the subsequent execution of compare_to_mean_consented() function to avoid errors due to the same username.
    """
    while True:  # Loop to allow for re-input if username is taken
        ans1 = text_input("") 
        google_json = os.environ["GOOGLE_JSON"]
        if isinstance(google_json, bytes):
            google_json = google_json.decode('utf-8')
        if isinstance(google_json, str):
            google_json = json.loads(google_json)
        credentials = service_account.Credentials.from_service_account_info(google_json)
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds_with_scope = credentials.with_scopes(scope)
        client = gspread.authorize(creds_with_scope)
        spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1F8JrCifa0gcvj4trM3fU39NTBn3q0gL2F_-cpBjhqsA/edit?usp=sharing')
        worksheet = spreadsheet.get_worksheet(0)
        records_data = worksheet.get_all_records()
        spreadsheet_df = pd.DataFrame.from_dict(records_data)
        style = f'font-size: 20px'
        if ans1 in spreadsheet_df['Username/ID'].values:
            display(HTML(f'<span style="{style}">This username is already taken. <br> Please choose another one. </span>'))
        else:
            display(HTML(f'<span style="{style}">Username added successfully!</span>'))
            return ans1  

#Images of 3D cubes and their 2D options uploaded to code
#All images were created with the cubes function and screenshoted
cubes1_0 = Image('cubes1.png', width = 600)
cubes2_0 = Image('cubes2.png', width = 600)
cubes3_0 = Image('cubes3.png', width = 600)
cubes4_0 = Image('cubes4.png', width = 600)
cubes5_0 = Image('cubes5.png', width = 600)
cubes6_0 =Image('cubes6.png', width = 600)
cubes7_0 = Image('cubes7.png', width = 600)
cubes8_0 = Image('cubes8.png', width = 600)
cubes9_0 = Image('cubes9.png', width = 600)
cubes10_0 = Image('cubes10.png', width = 600)
cubes11_0 = Image('cubes11_0.png', width = 600)

#Created a dictionary with 3D cubes, their 2D options and correct answer as string
cube_dict = dict(task1 =  [cubes1_0, 'd'], 
                 task2 = [cubes2_0, 'c'], 
                 task3 = [cubes3_0, 'b'], 
                 task4 = [cubes4_0, 'a'], 
                 task5 = [cubes5_0, 'a'], 
                 task6 = [cubes6_0, 'd'], 
                 task7 = [cubes7_0, 'a'], 
                 task8 = [cubes8_0, 'b'], 
                 task9 = [cubes9_0, 'c'], 
                 task10 = [cubes10_0, 'd'],
                 task11 = [cubes11_0,'a'])

#Dictionary converted into a pandas dataframe to make displaying image data possible
df_cubes = pd.DataFrame(data=cube_dict)
df_cubes = df_cubes.fillna(' ').T

def consent_form_1():
     """
    This function displays a consent form to the user asking their permission to upload their response data. 
    It is the first part of the full consent form
    The function presents the user with two buttons: 'Yes' and 'No'. 
    - If the user clicks 'Yes', a message is displayed confirming that their answers will be uploaded to Google Forms, and the consent variable increases by 1.
    - If the user clicks 'No', a message is displayed telling them that their answers will not be uploaded.
    Returns: consent (int): A variable with value that depends on the user clicking 'Yes' (1) or 'No' (2).
    """
    style = f'font-size: 20px'
    consent = 0
    display(HTML(f'<span style ="{style}">Please read: <br> We wish to record your response data <br> to an anonymised public data repository. <br> Your data will be used for educational teaching purposes <br> practising data analysis and visualisation. <br>  <br> Please click   yes   in the box below if you consent to the upload.</span>'))
    btn1 = widgets.Button(description="Yes")
    btn2 = widgets.Button(description="No")
    btn1.on_click(register_btn_event) 
    btn2.on_click(register_btn_event)
    panel = widgets.HBox([btn1, btn2])
    display(panel)
    consent_result = wait_for_event(timeout=10)
    clear_output()
    if consent_result['description']=="Yes":
        display(HTML(f'<span style ="{style}">Your answers will be uploaded to Google Forms</span>'))
        consent += 1
    else:
        display(HTML(f'<span style ="{style}">Your answers will not be uploaded to Google Forms</span>'))
        consent = 0
    return consent

def consent_form_2(consent, ans1, ans2, ans3, ans4, counter, grade, time_taken):
    """
    This function continues consent_form_1 and processes user data for a consent form. It collects information
    from the user that was given during the spatial test. If the user consents, their data is appended to a dictionary and then sent to a
    Google Form. An HTML message is displayed to the user, thanking them for their
    participation. The message is different depending on whether the user had consented (1) or not (0).

    Parameters:
    - consent (int): Taken from the consent form 1. Indicates whether the user had consented (1) or not (0).
    - ans1 (str): The user's username.
    - ans2 (str): The user's gender.
    - ans3 (str): The user's age.
    - ans4 (str): Information about substances the user might have taken.
    - counter (int): Number of user's correct answers.
    - grade (float): Percentage of correct answers given by the user.
    - time_taken (float): The time taken by the user to complete the test.
    Returns: None.
    """
    spatial_data_dict = {'Username/ID': [],
                     'Gender': [],
                     'Age': [],
                     'Substances': [],
                     'Counter': [],
                     'Grade': [],
                     'Time': []}
    style = f'font-size: 20px'
    if consent == 1:
        spatial_data_dict["Username/ID"].append(ans1)
        spatial_data_dict["Gender"].append(ans2)
        spatial_data_dict["Age"].append(ans3)
        spatial_data_dict["Substances"].append(ans4)
        spatial_data_dict["Counter"].append(counter)
        spatial_data_dict["Grade"].append(grade)
        spatial_data_dict["Time"].append(time_taken)

        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdcW_Nc5bJeod4imAMLwxwrSdc0zuT546wPN2wwiXc7kFLRSg/viewform?usp=sf_link"
        display(HTML(f'<span style ="{style}"> Thanks for your participation. <br> Please contact a.fedorec@ucl.ac.uk <br> If you have any questions or concerns <br> regarding the stored results.</span>'))

        send_to_google_form(spatial_data_dict, form_url)
    else:
        display(HTML(f'<span style ="{style}"> We hope you enjoyed the test.</span>'))
    return

def spatial_test(df_cubes):  #the function takes in a pandas dataframe with 3D cube, its 2D answer options and correct answers
    '''
    This function conducts a spatial reasoning test using a series of images contained within a pandas DataFrame. 
    Users are shown a 3D cube and must select which of the provided 2D projections cannot be made by rotating the 3D figure in space. 
    The test measures the accuracy of the participant's answers (as a percentage) and the time taken to complete the test. 
    Prior to starting, users are asked for consent to upload their anonymized results for educational purposes. 
    Users are also asked to input demographic information and whether they have consumed any substances that could affect cognitive performance. 
    The function utilizes IPython display tools and widgets for interactive buttons for answer selection and text inputs for demographic and substance information. 
    Results are optionally uploaded to a Spatial Reasoning Test Google Form if given the user's consent. 
    The participant's performance is compared to an average, and feedback is provided.

    Arguments:
    - df_cubes: A pandas DataFrame containing the images for the spatial reasoning test: the 3D cube images, 2D answer options, and the correct answers.

    Returns:
    - An HTML message displaying the participant's percentage of correct answers and the time taken to complete the test.
    '''
    style = f'font-size: 20px' 
    shuffled_df = shuffle(df_cubes, random_state=1)
    consent = consent_form_1()
    id_instructions = HTML(f"<span style ='{style}'>Enter your anonymised ID <br> To generate an anonymous 4-letter unique user identifier please enter: <br> - two letters based on the initials (first and last name) of a childhood friend <br> - two letters based on the initials (first and last name) of a favourite actor / actress <br> e.g. if your friend was called Charlie Brown and film star was Tom Cruise <br> then your unique identifier would be CBTC <br> Or just enter four random letters if you had no childhood friends and don't care about actors. </span>")
    display(id_instructions)
    display(HTML(f'<span style ="{style}">Please use the same ID for all Group 6 cognitive tests. <br> Please type in your ID: </span>'))
    ans1 = check_username()
    clear_output()
    display(HTML(f'<span style ="{style}">Please type in your gender:</span>'))
    ans2 = text_input('')
    clear_output()
    display(HTML(f'<span style ="{style}">Please type in your age:</span>'))
    ans3 = text_input('')
    clear_output()
    display(HTML(f'<span style ="{style}">Have you consumed any substances (Eg. alcohol, caffeine or drugs) in the last 12 hours that might affect your cognitive abilities?</span>'))
    display(HTML("<span>Note: Please enter 'yes/no', <br> if yes, please specify <br> or press enter if you would prefer not to disclose this information.</span>"))
    ans4 = text_input('') 
    clear_output()
    counter = 0 #counter for correct answers
    #displays wellcome message
    display(HTML(f'<span style = "{style}">In this test you will need to choose an option, displaying a 2D projection which cannot be made by rotating a given 3D figure in space. <br> There will be 11 questions. <br> Click the button with your answer underneath the options. </span>'))
    start_time = time.time()
    for i in range(11): #loop iterates over rows in dataframe
        task = shuffled_df[0][i] #attribute a variable to a 3D cube in dataframe
        display(task) #The following lines display the image of 3D cube followed by options, which are annotated by letters
        btn1 = widgets.Button(description='a')
        btn2 = widgets.Button(description='b')
        btn3 = widgets.Button(description='c')
        btn4 = widgets.Button(description='d')
        btn1.on_click(register_btn_event) 
        btn2.on_click(register_btn_event) 
        btn3.on_click(register_btn_event) 
        btn4.on_click(register_btn_event) 
        panel = widgets.HBox([btn1, btn2, btn3, btn4])
        display(panel)
        ans = wait_for_event(timeout=200)
        clear_output()
        if ans['description'] == shuffled_df[1][i]: #attribute correct answer to string variable in dataframe
            display(HTML(f'<span style ="{style}">You are correct!</span>'))
            time.sleep(2)
            clear_output(wait = False)
            counter +=1
        else: 
            display(HTML(f'<span style ="{style}">Your answer is wrong. <br> The correct answer is "{shuffled_df[1][i]}".</span>'))
            time.sleep(5)
            clear_output(wait = False)
            counter +=0
        clear_output()   
    grade = round(counter/11 * 100, 2) #final result calculates percentage of correct answers and rounds them to 2 significant figures
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    html_outro = HTML(f'<span style = "{style}"> Your result is {grade}%. <br> It took you {time_taken} seconds.</span>')
    consent_form_2(consent, ans1, ans2, ans3, ans4, counter, grade, time_taken)
    compare_to_mean(time_taken, grade)
    return display(html_outro) #Result displayed as % of correct answers
spatial_test(df_cubes)