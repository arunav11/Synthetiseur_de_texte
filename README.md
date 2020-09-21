# Synthetiseur_de_texte
# Introduction
Synthétiseur de texte is a transcript-generating summarizer that aims to help students to create a comprehensive and concise summary of recorded lectures and save their time.
User can either upload a lecture video or audio file OR can enter a youtube video link to get the summary and probable questions.

# Key features and technologies
## Django and python 
Django and python have been used to write the web app.
## NLTK
NLTK libraries have been used to generate questions and summary.

# Running the project on local machine:
First clone the project to your local machine:
```
git clone https://github.com/arunav11/Synthetiseur_de_texte.git
```
Install the dependencies:
```
 pip install -r requirements.txt (Python 2)
 pip3 install -r requirements.txt (Python 3)
```
Apply migrations to the database:
```
python manage.py makemigrations
python manage.py migrate
```
Now run the project:
```
python manage.py runserver
```

The project should be up and running on (http://127.0.0.1:8000)

Sample files have been provided for testing.
 
