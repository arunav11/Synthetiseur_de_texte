# Synthetiseur_de_texte
First clone the project to your local machine:
```
git clone https://github.com/arunav11/Synthetiseur_de_texte.git
```
Now go inside the project directory or open the project in pycharm to run the commands on terminal

After that install all the dependencies:
```
 pip install -r requirements.txt (Python 2)
 pip3 install -r requirements.txt (Python 3)
```
Apply migrations to the database:
```
python manage.py migrate
```
Create a superuser to access the admin side of the project:
```
python manage.py createsuperuser
```

Now run the project:
```
python manage.py runserver
```

After that upload a test video (one has been provided in upload/testvideolecture.mp4)

Can check if upload is completed by going to  (http://127.0.0.1:8000/admin) and using credentials entered while creating the superuser you can login

Now goto Upload app and click on MediaFile object and there will be a MediaFile object that you have just uploaded

After the upload is completed goto views.py and in line 13 call to backend function has been commented remove the comment and save the file
This would hot reload the server 

As there is no dedicated button to run the backend therefore the call is made whenever the home page is rendered therefore to call the function click on (http://127.0.0.1:8000/) in terminal tab 

This would generate the summary.txt file inside the project directory
