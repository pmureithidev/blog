# Blog Project

## Clone the Repository
Download the project to you PC and naviagte to the source directory.
```
git clone https://github.com/pmureithidev/blog.git
cd project-repo
```
## Set Up a Virtual Environment
```
python -m venv venv         # Create virtual environment
source venv/bin/activate    # Activate the virtual environment Linux
```
## Install Dependencies
```
pip install -r requirements.txt
```
## Configure Environment Variables
Create a .env file in the project folder

Edit .env with your settings
## Apply Database Migrations
```
python manage.py makemigrations
```
```
python manage.py migrate
```
## Create Superuser 
This is for admin access since the project doesn't have authentification to let other users create accounts and write posts.  
This feature will be added in due course.
```
python manage.py createsuperuser
```
## Run the Development Server
```
python manage.py runserver
```
## Access the Project
- Open your browser to: http://localhost:8000
* Admin panel: http://localhost:8000/admin
