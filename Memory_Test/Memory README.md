# Memory Test Code (Group 6)

This test starts by asking for some information from the respondent for data analysis. 
The test itself has 3 levels in total, in increasing difficulty.
For each level, the respondent will have 15 seconds to observe a picture.
After 15 seconds, they will then have to answer 5 questions about the picture.
Once all 3 levels are completed, they are asked to provide consent for uploading their data to our repository.

V2.0.0 Updates:
- Functions are stored in a Python code file and is imported into Notebook to run test
- Users are asked to provide consent to data collection before test starts, rather than after completing the test
- User responses to each individual question are uploaded to Google Forms
- “Press enter to continue” commands were changed to buttons
- User results (scores and time taken to the complete test) are compared to mean results from previous responses
- Comparison of results is visualised through a scatter plot
- Word bank of colours and objects in each grid was provided to minimise misspelling and misinterpretation effects
- One of the questions (“How many different fruits were there in the picture?”) in level 3 was changed as the answer could be derived from the word bank
- Full test was split into multiple functions: one for the main test, one for result comparison, and one for plotting the scatter graph
