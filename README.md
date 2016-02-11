\* What it does ?<br/>
User sigin/login<br/>
User can CRUD over a contact and phone


It has no style<br/>
Full tested

--
Run local

\*
You should have this things instaled:<br/>
make<br/>
git<br/>
pip<br/>
python 3<br/>
virtualenv<br/>


```sh
# type this commands on terminal. I will omit $
# download and prepare the environment
git clone https://github.com/alexaleluia12/agenda-app.git
cd agenda-app
virtualenv env --python=your_python_3
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate

# run the server
# go in http://127.0.0.1:8000/agenda/
make run

# run tests
make test

# leave viartualenv
deactive

# cancel server: Ctrl + c
```

--
Selenium

It use Selenium to test the app on browser.

To run the view test You need Firefox and [Selenium Server](http://docs.seleniumhq.org/download/)

```sh
# run the selenium server
java -jar selenium-server-standalone-2***.jar

# run the django sever
make run

# run the tests
cd agenda
PYTHONPATH=.. python test-view.py

```
