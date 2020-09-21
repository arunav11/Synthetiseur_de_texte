<div align="center">
<h1>Synthetiseur_de_texte</h1>
<blockquote>
<p><i>Synthétiseur de texte is a transcript-generating summarizer that aims to help students to create a comprehensive and concise summary of recorded lectures and save their time.</b></i></p>
</blockquote>
</div>

# Motivation
<i> During the global paendamic students attended online classes instead of physical classes.But due to network issues all were not able to follow what was being taught in the class. So to overcome this we came up with Synthetiseur_de_texte.Technology can never take place of the teacher but stil we tried to bridge the gap as much as possible.</i>

# Key features 
* **Recorded lectures** can be provided which are then converted into summary for quick **revision**.

* **Questions** are also generated from the summary to help better understand the lecture.

* If the recorded lecture is not available **youtube link** to the video can be provided.

# Screenshots
![ss1](/website-1.JPG)

<div align="center"><i><b>Upload file</b></i></div>




![ss2](/webiste-2.JPG)
<div align="center"><b><i>Copy UUID </i></b></div>




![ss3](/website3.JPG)

<div align="center"><b><i>Summary and questions generated</b></i></div>


# Technologies used
## Django and Python 
Django and python have been used to write the web app.
## NLTK Library
NLTK libraries have been used to **generate questions and summary**.

# Running the project on local machine:
First clone the project to your local machine:
```
git clone https://github.com/arunav11/Synthetiseur_de_texte.git
```
Install the dependencies:
```
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

## Testing 
Sample **file** have been provided for testing.
 
 https://synthetiseur-de-texte-files.s3.amazonaws.com/files/sample.mp4
 
 Sample **youtube link** have been provided for testing.
 
 https://www.youtube.com/watch?v=beAvFHP4wDI&ab_channel=OneMinuteEconomics


