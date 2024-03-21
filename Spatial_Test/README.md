# Spatial reasoning test (Group06)

The spatial reasoning test measures user's ability to rotate images using imagination. It will display a 3D image followed by a series of 2D images and ask user to select the image that cannot be made by rotating the 3D image. User input is recorded using buttons and counter and time taken is recorded using time installation package. The time taken, number of questions answered correctly as well as the percentage of correct answers and demographic data is uploaded to Google Forms if the user gives their consent to it.

Update 1: on 02.03.2024, version 1.2
Reproducible randomness added to the test
New images now used to display 2D projections side by side
Notebook connected to Google Spreadsheets through Google Spreadsheet API
Two functions added to allow users to compare their results to average results
A function that checks if the username had been used previously added

Update 2: on 13.03.2024, version 1.2.1
Bug that caused comparison function to not work properly fixed
Only one comparison function is now used for all users to reduce lines of code
Consent form separated into two functions that are called upon in the main test
A graphical representation of user results added to the comparison function

Update 3: on 21.03.2024, version 1.3
In the main test code: descriptions added to  the consent forms 1 and 2, modified visual representation of user results with axis switched.
The main test code conversted to a python file, which is called upon in the version 1.3 Notebook
