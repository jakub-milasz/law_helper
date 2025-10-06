# Law helper
Law Helper is a web app created with Flask, Selenium and HTML/CSS.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Set up](#set-up)
* [How it works](#how-it-works)
* [Model Description](#model-description)
* [Developing app](#developing-app)

## General info
Law helper is a web app which helps users to resolve doubts connected with law. It can help them with **criminal** or **inheritance** cases. In the criminal section they can write in a form an action they did and the app shows the proper article and penalty foreseen in the **Polish Penal Code**. In the inheritance section they can write some problems connected with inheritance and the app shows the solution. If the description given by user is not accurate, the app gives the subsidiary form with additional questions
in order to specify the description. Polish language is used in the app because the Penal Code is written in Polish.

## Technologies
The app was created with Flask, HTML/CSS, Selenium. To process the user's input I used Gemini 2.5 Flash Model form Google API. Selenium
was used to create a database by scraping articles from ArsLege page.

## Set up
To run project on your computer, you have to clone the repository, then open project in code editor and enter in terminal ```pip install -r requirements.txt```. Then, you have to enter ```python app.py``` and click on link with local server. You have to also create .env file with your API key and assign it to GOOGLE_AI_API_KEY constant. It is obligatory to connect with Gemini API in order to use a model.


## How it works
When user loads the page, the main page with menu is shown. Here the user can choose the section they are interested in.

<img width="1915" height="1003" alt="Zrzut ekranu 2025-09-24 205242" src="https://github.com/user-attachments/assets/af388317-60fb-423f-a5d7-717f6a607813" />

In the criminal section user gets the instruction to select a category of the offence, enter the description and submit the form.

<img width="1919" height="1000" alt="Zrzut ekranu 2025-09-24 205307" src="https://github.com/user-attachments/assets/452a7576-4557-4396-88d6-22e08c1e9af7" />

<img width="1919" height="1003" alt="Zrzut ekranu 2025-09-24 205327" src="https://github.com/user-attachments/assets/4f155c0e-5dcb-4127-8dd1-f6ecbc9e7344" />

In the inheritance section user gets the instruction to describe a problem.

<img width="959" height="500" alt="image" src="https://github.com/user-attachments/assets/43c4f195-3cc9-4aea-893f-059c8b4ae537" />

### Example in the criminal section
After that, Gemini 2.5 Flash Model processes this input and compare with the articles from database. If model considers the description
not accurate, the user is redirected to another page with subsidiary form with additional questions.

<img width="1919" height="997" alt="Zrzut ekranu 2025-09-24 205415" src="https://github.com/user-attachments/assets/1db3d600-38d9-4eb1-b0b5-5a4f8aec027a" />

If user specifies the description, he is redirected to page with a relevant article.

<img width="1919" height="1002" alt="Zrzut ekranu 2025-09-24 205623" src="https://github.com/user-attachments/assets/347e3444-7160-4619-9281-f5ab51f935d6" />


## Model Description
Gemini 2.5 Flash is a Large Language Model from Google API. The model has a context which is a database with articles from the criminal, offence and civil (inheritance chapter) code. Moreover, it has a history of conversation with user, so that it works properly with additional forms. It gets two kinds of prompt templates: the main prompt which is connected with form from main page and the additional prompt which is sent to model when user fills a subsidiary form.

## Developing app
The main and still goal is to upgrade model to be as accurate as possible. It is also crucial to include updates in law in our database.
The next important task would be to optimise model performance.
