# Law helper
Law Helper is a web application designed to assist users in identifying the most relevant criminal offenses
from the penal code based on the description provided by the user. The application employs a Gemini 1.5 Flash Model which matches the most suitable
legal articles to the description. The next step in the development of this app will be adding subsidiary forms with additional questions for users to provide more specific descriptions.
In that way, the fitting a proper crime by model could be more accurate.

## Stack
In this project I used HTML/CSS, Python with Flask.

## Features
**Crime Matching**: Users input a description of an offense, and the application returns the most relevant articles from the penal code.

**Gemini 1.5 Flash Model**: Model used from Google Gemini API processes the user's input and gives a response.

**User-Friendly Interface**: A simple and intuitive interface allows for easy input and retrieval of results.

## How It Works
1. Input Description: Users enter a description of the offense in a text field.

![Zrzut ekranu 2024-12-25 174339](https://github.com/user-attachments/assets/3ee9b559-c5cb-40a1-8e67-1bd4c49a596c)


2. Data Processing: The Gemini 1.5 Flash Model analyses the input and generate a response with proper articles.


3. Output: The application returns the most relevant penal code article based on the input description and the penalty.

![Zrzut ekranu 2024-12-25 174429](https://github.com/user-attachments/assets/acc65570-f0a8-42d1-af53-dd51604bcc16)
