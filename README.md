# Law helper
Law Helper is a web application designed to assist users in identifying the most relevant criminal offenses
from the penal code based on the description provided by the user. The application employs a TF-IDF (Term Frequency-Inverse Document Frequency)
model to analyze text and match the most suitable legal articles. This is now demo app. It is still developed by adding new articles and improving the TF-IDF Model performance.

## Stack
In this project I used HTML/CSS, Python with Flask and I test my TF-IDF Model in Jupyter Lab.

## Features
**Crime Matching**: Users input a description of an offense, and the application returns the most relevant articles from the penal code.

**TF-IDF Model**: Advanced text analysis using TF-IDF ensures precise matching of offenses. Before this stemming is applied. It is based on polish law and penal code, so stemming is on polish language.

**User-Friendly Interface**: A simple and intuitive interface allows for easy input and retrieval of results.

## How It Works
1. Input Description: Users enter a description of the offense in a text field.

![Zrzut ekranu 2024-11-06 230223](https://github.com/user-attachments/assets/9ff73ce1-a587-4bf1-bf65-5c1fa5d4e122)


2. Data Processing: The TF-IDF model analyzes the input text for word frequency in relation to defined offenses.


3. Output: The application returns the most relevant penal code article based on the input description and the penalty.

![Zrzut ekranu 2024-11-06 230240](https://github.com/user-attachments/assets/3199ec85-1b8a-471e-bfad-3331d1670973)


   
