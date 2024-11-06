# Law helper
Law Helper is a web application designed to assist users in identifying the most relevant criminal offenses
from the penal code based on the description provided by the user. The application employs a TF-IDF (Term Frequency-Inverse Document Frequency)
model to analyze text and match the most suitable legal articles.

## Stack
In this project I used HTML/CSS, Python with Flask and I test my TF-IDF Model in Jupyter Lab.

## Features
**Crime Matching**: Users input a description of an offense, and the application returns the most relevant articles from the penal code.

**TF-IDF Model**: Advanced text analysis using TF-IDF ensures precise matching of offenses. Before this stemming is applied. It is based on polish law and penal code, so stemming is on polish language.

**User-Friendly Interface**: A simple and intuitive interface allows for easy input and retrieval of results.

## How It Works
1. Input Description: Users enter a description of the offense in a text field.

   ![Zrzut ekranu 2024-11-06 130318](https://github.com/user-attachments/assets/eff61b84-1ed7-434e-a330-b92a263a83cb)

2. Data Processing: The TF-IDF model analyzes the input text for word frequency in relation to defined offenses.


3. Output: The application returns a list of the most relevant penal code article based on the input description and the penalty.

  ![Zrzut ekranu 2024-11-06 130336](https://github.com/user-attachments/assets/9717991d-65d4-45e8-b619-64c5a9fa2450)

   
