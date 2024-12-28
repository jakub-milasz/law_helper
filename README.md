# Law helper
Law Helper is a web app created with Flask, Selenium and HTML/CSS.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [How it works](#how-it-works)
* [Model Description](#model-description)
* [Developing app](#developing-app)

## General info
Law helper is a web app which helps users to resolve doubts connected with law. They can write in a form an action they did and the app
shows the proper article for this. If the description given by user is not accurate, the app gives the subsidiary form with additional questions
in order to specify the description.

## Technologies
The app was created with Flask, HTML/CSS, Selenium. To process the user's input I used Gemini 1.5 Flash Model form Google API. Selenium
was used to create a database by scraping articles from ArsLege page.

## How it works
When user wants to load the page, the main page with form is shown. The user gets the instruction to enter an offence and submit the form.

![Zrzut ekranu 2024-12-28 130055](https://github.com/user-attachments/assets/696c4d57-706a-490e-ad59-c68ace0e2536)


After that, Gemini 1.5 Flash Model processes this input and compare with the articles from database. If model considers the description
not accurate, the user is redirected to another page with subsidiary form with additional questions.

![Zrzut ekranu 2024-12-28 125959](https://github.com/user-attachments/assets/418a7b3c-738f-4472-a546-601fe8a6b6da)


If user specifies the description, he is redirected to page with article which fits to it.

![Zrzut ekranu 2024-12-28 130039](https://github.com/user-attachments/assets/b5a5e2b5-1dcd-446c-b65c-43573765528a)


## Model Description
Gemini 1.5 Flash is a Large Language Model form Google API. The model has a context which is a database with articles from the criminal codex and the offence codex. Moreover, it has a history of conversation with user, so that it works properly with additional forms. It gets two kinds of prompt templates: the main prompt which is connected with form from main page and the additional prompt which is sent to model when user fills a subsidiary form.

## Developing app
The main and still goal is to upgrade model to be as accurate as possible. It is also crucial to include updates in law in our database.
The next stage of developing the app will be creating a new part of page connected with inheritance law. It could help users to find out more
about difficult inheritance cases in simple way.
