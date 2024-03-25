from IPython.display import display, HTML, Image, clear_output
import time
import random
from time import sleep
from ipywidgets import Output
from bs4 import BeautifulSoup
from google.oauth2 import service_account
import pandas as pd
import gspread
import requests
import json
import os
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
import matplotlib.pyplot as plt

os.environ["GOOGLE_JSON"] = json.dumps({
    "type": "service_account", 
    "project_id": "bios0030-memory", 
    "private_key_id": "2f51c5f763dfcd6086159b1940fcf255a765c940", 
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCPCLtQlHB6eq2f\nTLEH6UDVQyi2/+n1Ptn0Ggc/mpD6uod0rvVNwNd7+IWO/y/wYV21/JNIYYEh1eEG\nivX5/m1vsMJFjjV+Y2saFhwhlnjDZuex1pxIseA7RvcGQ9OCCcyw9EULH0g/YVta\nh0bz3a5DpXe3sNh63yjBi7mlMJpaB7XDBoJPUY2hLdyCoLXjZjBlcKevoWTvzMAG\nOHHqnNAKFN2Gu84sSMny4quLZFsyjxrDNVZrYoE1UFi281U0SAHEusPv1rgvOEMH\nyx7wOwZEim+5PSyNRFTVRLRJTb9oOGGkVG63PP9IdKwOm+4qMPHNSDFBDs04MQkI\n/EY1Pjd5AgMBAAECggEAQaE5Ca1CuwBFYD25US7236P0L5vXRv9y1G2I++c5NMKX\n2rNYvTeJ6ElNRyLSZVLXw+RD1EdhEBxqJy1l1jKnFkOdsHqjEv4dK5gPil3XxZkX\nIOOfTD/J6okSWZ6PkzBZ6qv6bjMJXIOYfj5qEQWbq1BmUTPk8OQqeDxbj29ws3P8\njouRyJN/7gNFUg+EogbEcMZ4ej3Cf5saNbo5mDzZXgYenr5uG77jTdVc391uaDqT\nETLpJx4vSON2xplxWBxlhY6HkHt0uz1VZ6QNda5xuLls6NogbqCM32rzcwiHB8th\nGtpWQG+W4Hshff7cbkHsqKaLTaShIfmHH3K6d6IMbQKBgQDDdZyOHDBafF43A+WF\nQWy8kunmN3G/4Gvw2aUiIn6agSpoPohTX3smJku3gQTbMChBKuJqqlIFYd58u+A+\n+92FjhEyOI7tUEUGfctEtyOFeiXGF/+e65nBYDrZTPpyItal8vJGsK8e9HAuD58X\nmdLw6/kWUde03/BwDEMuAxnsHwKBgQC7VjT5OtK86rT4yQTFpJN4ENooQpf1g9vk\n/IGcKHdp5FoRq6BL5j2fMieg++O3TAHFOZKFGheoKXj/B2ziZVnLQkPyPzF6Qxty\ngR3EVFFa8rOvZBKpUYgnJxfgtOZkYa9DfBh7e3eWCqJCPaz9RbqlBsYYKoKXiPwV\nKSVmZRjpZwKBgAI7GWpV0Ad4W+rs1HXM5VzRoHHMODQkb5b0JPpawm8pAj7mV8/7\nywAId9zEUDXgOtVjk+n7v6voDg4GZuzRGxonIPMdyiPTQrZsQSGrpXAkkMHODFDY\nB405d/J6+nDLDQAf4bwE0DreN1mPPBWc39d4GgOzM28RD0F4IlwoFOepAoGAIbIj\n3SBjf2+IFaeyoAo2LEZ7tvojcxnAl7ODbJ8qu3VDbiI8tuo280eGMUKddv7I4ry0\nShSjZK/w/45KW353ZEQLDKupLqCbc0EeJY41A/LbtxR89s+fectiVBy1xCB98dmE\nXdGbdPV8sgV99CByrfRF9VrQGomdLgE0pPJSRMkCgYEAicVfI90YlaycH0JSw4Pw\nRUMAUY7KUEACYf6iL3gvgbnxf7K9OoNr2s2GcRpo8ObGmoZsJCaZokmj4Kwqg/26\nXIC8dcMwRSMmxV0haB9rtpvCZbB0ZGn5hFYfP+cOrOnZQ5ANSTgoAiNXGq8mCDcW\n+uOAOl124Lhl7M6rsdp467o=\n-----END PRIVATE KEY-----\n", 
    "client_email": "bios0030-memory@bios0030-memory.iam.gserviceaccount.com", 
    "client_id": "106146065497408016680", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth", 
    "token_uri": "https://oauth2.googleapis.com/token", 
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", 
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bios0030-memory%40bios0030-memory.iam.gserviceaccount.com", 
    "universe_domain": "googleapis.com"})

# load spreadsheet containing test responses
google_json = os.environ["GOOGLE_JSON"]
service_account_info = json.loads(google_json)
credentials = service_account.Credentials.from_service_account_info(service_account_info)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds_with_scope = credentials.with_scopes(scope)
client = gspread.authorize(creds_with_scope)
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1nBjOO330Pljrm61nOuOqchG6JB7hHSNY58XlyrqkwMw/edit?usp=drive_link') #memory response 1.0 spreadsheet
worksheet = spreadsheet.get_worksheet(0)
records_data = worksheet.get_all_records()
spreadsheet_df = pd.DataFrame.from_dict(records_data)
spreadsheet_df

def send_to_google_form(data_dict, form_url):
    """
    This function allows test responses to be sent to a Google Form. 
    """
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

# lists of questions and answers
lev1 = [
    ("What object was in the top left corner?", "triangle"),
    ("What colour was the circle?", "purple"),
    ("What object was in blue?", "square"),
    ("What colour was the star?", "pink"),
    ("What object was above the star?", "circle")
]

lev2 = [
    ("What object was in the centre?", "pentagon"),
    ("What colour was the object in the bottom right corner?", "red"),
    ("What object was beside the arrow?", "rectangle"),
    ("What object was orange in colour?", "heart"),
    ("What colour was the object below the star?", "white")
]

lev3 = [
    ("What object was next to the heart?", "cherry"),
    ("What colour was the object next to the peach?", "green"),
    ("What object was in the bottom left corner?", "apple"),
    ("The peach was located to the __ of the star. (Options: top, bottom, left, right)", "left"),
    ("What object was to the left of the object in pink?", "circle")
] 

def main_test():
    """
    This test starts by asking for some information from the respondent for data analysis. 
    The test itself has 3 levels in total, in increasing difficulty.
    For each level, the respondent will have 15 seconds to observe a picture.
    After 15 seconds, they will then have to answer 5 questions about the picture.
    Upon completion of the test, results are sent to a Google Form.
    """
    
    # dictionary for saving responses
    results_dict = {
        "id": [],
        "gender": [],
        "age": [],
        "substance": [],
        "lev1_answers": [],
        "counter1": [],
        "lev2_answers": [],
        "counter2": [],
        "lev3_answers": [],
        "counter3": [],
        "final_score": [],
        "time_taken1": [],
        "time_taken2": [],
        "time_taken3": [],
        "total_time": [],
    }

    display(HTML("<h4>Thank you for your participation! Your data will be uploaded.</h4>"))
    time.sleep(1)
    display(HTML("<h4>Please contact a.fedorec@ucl.ac.uk</h4>"))
    time.sleep(1)
    display(HTML("<h4>If you have any questions or concerns regarding the stored results.</h4>"))
    time.sleep(5)
    clear_output()

    # collection of personal information
    display(HTML("<h4>Please enter an anonymised ID:</h4>"))
    time.sleep(1)
    display(HTML("<h5>To generate an anonymous 4-letter unique user identifier please enter:</h5>"))
    time.sleep(1)
    display(HTML("<h5>- Two letters based on the initials (first and last name) of a childhood friend</h5>"))
    time.sleep(1)
    display(HTML("<h5>- Two letters based on the initials (first and last name) of a favourite actor/actress</h5>"))
    time.sleep(1)
    display(HTML("<h5>E.g. If your friend was called Charlie Brown and film star was Tom Cruise</h5>"))
    time.sleep(1)
    display(HTML("<h5>Then your unique identifier would be CBTC</h5>"))
    time.sleep(1)
    display(HTML("<h5>Note: Please use the same ID for all Group 6 cognitive tests</h5>"))
    ans1 = text_input("> ")
    display(HTML("<h4>Please enter your gender:</h4>"))
    ans2 = text_input("> ")
    display(HTML("<h4>Please enter your age (in numbers):</h4>"))
    ans3 = text_input("> ")
    display(HTML("<h4>Have you consumed any substances (Eg. caffeine, alcohol, or drugs) in the last 12 hours that might affect your cognitive abilities?</h4>"))
    time.sleep(1)
    display(HTML("<h5>Please enter 'yes' or 'no'. If yes, please specify. Enter '-' if you would prefer not to disclose this information.</h5>"))
    ans4 = text_input("> ")
    btn3 = widgets.Button(description="Click me to continue")
    btn3.on_click(register_btn_event)
    display(btn3)
    wait_for_event()
    clear_output(wait=False)

    # explanation of test
    display(HTML("<h4>There will be 3 levels in total</h4>"))
    time.sleep(1)
    display(HTML("<h4>For each level, you will have 15 seconds to commit a picture to memory</h4>"))
    time.sleep(1)
    display(HTML("<h4>You will then answer 5 questions about the picture</h4>"))
    time.sleep(1)
    display(HTML("<h4>Please read all the questions carefully and type all your answers in lowercase</h4>"))
    time.sleep(1)

    btn4 = widgets.Button(description="Click me to start")
    btn4.on_click(register_btn_event)
    display(btn4)
    wait_for_event()
    clear_output(wait=False)

    # start of level 1
    level1 = Image("memory1.png", width = 400) # for level 1 picture
    wordlist1 = Image("word_list1.png", width = 800)
    out1 = Output() # for countdown timer
    display(level1) 
    display(out1) 

    counter1 = 0 # to keep track of scores in each separate level

    # displaying countdown timer
    for i in range (15, -1, -1):
        out1.clear_output(wait=True)
        with out1: display(HTML(f"<h4>Time remaining: {i} seconds</h4>"))
        time.sleep(1)
    clear_output(wait=False)

    # randomise questions
    lev1_ques = lev1.copy()
    random.seed(1)
    random.shuffle(lev1_ques)

    start_time1 = time.time() # to keep track of time taken to answer questions
    lev1_ans = [] # to keep track of each individual answer

    # start of questions
    for question, correct_ans in lev1_ques:
        display(wordlist1) # display list of objects and colours
        display(HTML(f"<h4>{question}</h4>"))
        answer = text_input("> ")
        lev1_ans.append(answer)
        if answer == correct_ans:
            display(HTML("<h4>Correct!</h4>"))
            time.sleep(2)
            clear_output(wait=False)
            counter1 += 1
        else:
            display(HTML(f"<h4>Sorry! The answer is {correct_ans!r}, not {answer!r}</h4>"))
            time.sleep(2)
            clear_output(wait=False)

    end_time1 = time.time()
    time_taken1 = end_time1 - start_time1 # calculate total time taken for level 1

    display(HTML("<h4>Congratulations! You have completed Level 1</h4>"))
    time.sleep(1)

    # start of level 2
    display(HTML("<h4>Welcome to Level 2</h4>"))
    time.sleep(1)

    display(btn4)
    wait_for_event()
    clear_output(wait=False)

    level2 = Image("memory2.png", width = 400)
    wordlist2 = Image("word_list2.png", width = 800)
    display(level2)
    display(out1)

    counter2 = 0

    for i in range (15, -1, -1):
        out1.clear_output(wait=True)
        with out1: display(HTML(f"<h4>Time remaining: {i} seconds</h4>"))
        time.sleep(1)
    clear_output(wait=False)

    lev2_ques = lev2.copy()
    random.seed(1)
    random.shuffle(lev2_ques)

    start_time2 = time.time()
    lev2_ans = []

    for question, correct_ans in lev2_ques:
        display(wordlist2)
        display(HTML(f"<h4>{question}</h4>"))
        answer = text_input("> ")
        lev2_ans.append(answer)
        if answer == correct_ans:
            display(HTML("<h4>Correct!</h4>"))
            time.sleep(2)
            clear_output(wait=False)
            counter2 += 1
        else:
            display(HTML(f"<h4>Sorry! The answer is {correct_ans!r}, not {answer!r}</h4>"))
            time.sleep(2)
            clear_output(wait=False)

    end_time2 = time.time()
    time_taken2 = end_time2 - start_time2

    display(HTML("<h4>Congratulations! You have completed Level 2</h4>"))
    time.sleep(1)

    # start of level 3
    level3 = Image("memorypic3.png", width = 400)
    wordlist3 = Image("word_list3.png", width = 800)
    
    display(HTML("<h4>Welcome to Level 3</h4>"))
    time.sleep(1)

    display(btn4)
    wait_for_event()
    clear_output(wait=False)

    display(level3)
    display(out1)

    counter3 = 0

    for i in range (15, -1, -1):
        out1.clear_output(wait=True)
        with out1: display(HTML(f"<h4>Time remaining: {i} seconds</h4>"))
        time.sleep(1)
    clear_output(wait=False)
    
    lev3_ques = lev3.copy()
    random.seed(1)
    random.shuffle(lev3_ques)

    start_time3 = time.time()
    lev3_ans = []

    for question, correct_ans in lev3_ques:
        display(wordlist3)
        display(HTML(f"<h4>{question}</h4>"))
        answer = text_input("> ")
        lev3_ans.append(answer)
        if answer == correct_ans:
            display(HTML("<h4>Correct!</h4>"))
            time.sleep(2)
            clear_output(wait=False)
            counter3 += 1
        else:
            display(HTML(f"<h4>Sorry! The answer is {correct_ans!r}, not {answer!r}</h4>"))
            time.sleep(2)
            clear_output(wait=False)

    end_time3 = time.time()
    time_taken3 = end_time3 - start_time3
    
    # calculate total time taken and final score across all three levels
    total_time = time_taken1 + time_taken2 + time_taken3
    final_score = counter1 + counter2 + counter3

    # responses are added to result dictionary
    results_dict["id"].append(ans1)
    results_dict["gender"].append(ans2)
    results_dict["age"].append(ans3)
    results_dict["substance"].append(ans4)
    results_dict["lev1_answers"].append(lev1_ans)
    results_dict["counter1"].append(counter1)
    results_dict["lev2_answers"].append(lev2_ans)
    results_dict["counter2"].append(counter2)
    results_dict["lev3_answers"].append(lev3_ans)
    results_dict["counter3"].append(counter3)
    results_dict["final_score"].append(final_score)
    results_dict["time_taken1"].append(time_taken1)
    results_dict["time_taken2"].append(time_taken2)
    results_dict["time_taken3"].append(time_taken3)
    results_dict["total_time"].append(total_time)

    # results are uploaded to Google Form
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLScRVOFAri5zqvY2SQyOptEvTkXmeukUxcjXwE_p-uysQV-kKw/viewform?usp=sf_link"
    send_to_google_form(results_dict, form_url)

    # returns respondent ID, final score, and total time taken for further comparison to mean results
    return ans1, total_time, final_score 

def compare_to_mean(score, time):
    """
    This function compares respondent's final score and total time taken to complete the test to the mean results.
    Mean results are calculated from previous responses. 
    """
    # calculates mean results from previous responses 
    mean_score = spreadsheet_df["final_score"].mean()
    mean_time = spreadsheet_df["total_time"].mean()
    # then compares current respondent's results to the mean
    compare_score = round((score - mean_score)/mean_score * 100, 2)
    compare_time = round((time - mean_time)/mean_time * 100, 2)
    # display comparison output
    if compare_score > 0:
        compare_score = compare_score
        html_score = HTML(f'<h4>Your score is {compare_score}% above average</h4>')
        if compare_time > 0:
            compare_time = compare_time
            html_time = HTML(f'<h4>It took you {compare_time}% more time than average</h4>')
        else:
            compare_time = compare_time * -1
            html_time = HTML(f'<h4>It took you {compare_time}% less time than average</h4>') 
    else:
        compare_score = compare_score * -1
        html_score = HTML(f'<h4>Your score is {compare_score}% below average</h4>')
        if compare_time > 0:
            compare_time = compare_time
            html_time = HTML(f'<h4>It took you {compare_time}% more time than average</h4>')
        else:
            compare_time = compare_time * -1
            html_time = HTML(f'<h4>It took you {compare_time}% less time than average</h4>') 

    # returns comparison output and mean results for display
    return html_score, html_time, mean_score, mean_time

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

def memory_test(): 
    """
    The full test starts by asking for respondents to provide consent to data collection.
    If consent is not given, the test does not run. 
    Once consent is given, the main test runs, which consists of 3 levels. 
    
    some information from the respondent for data analysis. 
    The test itself has 3 levels in total, in increasing difficulty.
    For each level, the respondent will have 15 seconds to observe a picture.
    After 15 seconds, they will then have to answer 5 questions about the picture.
    Once all 3 levels are completed, they are asked to provide consent for uploading their data to our repository.
    """

    # start of test asking for respondent information
    display(HTML("<h3>Welcome to the Memory Test!</h3>"))
    time.sleep(2)

    data_consent_info = """DATA CONSENT INFORMATION: <br>

    Please read: <br>

    We wish to record your response data to an anonymised public data repository. <br>
    Your data will be used for educational teaching purposes, practising data analysis and visualisation. <br>
    Please select 'yes' in the box below if you consent to the upload."""

    display(HTML(f"<h4>{data_consent_info}</h4>"))
    
    btn1 = widgets.Button(description="Yes")
    btn2 = widgets.Button(description="No")
    
    btn1.on_click(register_btn_event) 
    btn2.on_click(register_btn_event)

    panel = widgets.HBox([btn1, btn2])
    display(panel)

    consent_result = wait_for_event()
    clear_output(wait=False)

    # test runs if consent is given 
    if consent_result['description']=="Yes":

        # main_test function is called
        ans1, total_time, final_score = main_test() 
        # comparison of respondent results to mean results
        html_score, html_time, mean_score, mean_time = compare_to_mean(final_score, total_time)

        # test results are displayed to respondent
        display(HTML("<h4>Thank you for taking the test! Your results have been uploaded.</h4>"))
        time.sleep(1)
        display(HTML(f"<h4>Your final score is: {final_score}/15</h4>"))
        time.sleep(1)
        display(HTML(f"<h4>The total time taken was: {total_time:.2f} seconds</h4>"))
        time.sleep(1)
        display(html_score)
        time.sleep(1)
        display(html_time)
        time.sleep(1)

        # comparison plot is displayed
        comparison_plot(ans1, total_time, final_score, mean_time, mean_score)

    # test does not run if respondent did not consent to data collection
    else:
        display(HTML("<h4>No problem! Feel free to give the test a try if you change your mind.</h4>"))

    return 

memory_test()