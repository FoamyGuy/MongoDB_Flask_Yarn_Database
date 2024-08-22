# Yarn Database

Made with Flask + MongoDB

### User Setup

Data is protected behind user authentication. 
Passwords are hashed and stored and checked in accordance with best practices.

To create a user:
```
python register.py --username my_name
```

It will prompt you to enter a password. 
Type in a password and press enter. The password is not shown as you type it.

Open in a browser `http://localhost:5000/login`
Enter the username and password specified before.


### Running Development Server

Requires:
- MongoDB installed and running on default port 27017 (Update app.py and register.py for different port)
- Environment variable `FLASK_SECRET_KEY` set to a secure random value

```
export FLASK_SECRET_KEY='YOUR_SUPER_DUPER_SECURE_PASSWORD_HERE'
python app.py
```


### Running Production Server

Requires:
- Nginx installed and running
- MongoDB Installed and Running on Default Port 27017 (Update app.py and register.py for different port)
- Python venv with requirements installed
  - `pip install -r requirements.txt`

Copy conf files:
- `/etc/systemd/system/yarn_db.service`
- `/etc/nginx/sites-available/yarn_db`

Fill in the `FLASK_SECRET_KEY` value in yarn_db.service

Create enabled symbolic link
```
cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/yarn_db ./
```


