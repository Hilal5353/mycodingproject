# Survey Project

This is a Django-based survey project where users can create surveys, answer questions, and view results. The project supports question types such as text input, checkboxes, and radio buttons.

## Requirements

Before running the project, ensure you have Python 3.x, Docker, and Docker Compose installed.

## Installation & Running the Project

Clone the repository:  
`git clone https://github.com/your-username/survey-project.git`  
`cd survey-project`  

To run the project locally, install the dependencies:  
`pip install -r requirements.txt`  
Then, apply migrations and run the server:  
`python manage.py migrate`  
`python manage.py runserver`  
Access the project at `http://127.0.0.1:8000`.

For Docker, build and start the containers:  
`docker-compose up --build`  
After the build completes, the project will be accessible at `http://localhost:8000`.

To access the Django admin panel, visit `http://127.0.0.1:8000/admin` and log in. From there, you can create surveys, manage survey questions, and view answers.


