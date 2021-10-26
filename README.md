<!-- PROJECT INFO -->
<h1 align="center">HeLP Network API</h1>

<p align="center">
  <a href="https://github.com/marlitas/rails_engine/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/mental-health-org/mental_health_be?style=for-the-badge" alt="contributors_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/issues">
    <img src="https://img.shields.io/github/issues/mental-health-org/mental_health_be?style=for-the-badge" alt="issues_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/network/members">
    <img src="https://img.shields.io/github/forks/mental-health-org/mental_health_be?style=for-the-badge" alt="forks_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/stargazers">
    <img src="https://img.shields.io/github/stars/mental-health-org/mental_health_be?style=for-the-badge" alt="stars_badge">
  </a>
</p>

<h4 align="center">Ask. Help. Connect. Grow.</h4>

<p align="center">
The HeLP Network API is a RESTful API for the HeLP Network frontend application. To experience the UI our frontend team built please visit their [website](http://mental-health-fe.herokuapp.com/). Otherwise you may hit our endpoints through an http request helper such as Postman.
</p><br>

<!-- CONTENTS -->
<p align="center">
  <a href="#about-the-project">About The Project</a> •
  <a href="#tools-used">Tools Used</a> •
  <a href="#set-up">Set Up</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#database-schema">Database Schema</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>


## About The Project

The HeLP Network is a platform that allows helping and law professionals such as mental health counselors, special education teachers, dieticians, and paralegals to connect and share resources.

### Learning Goals

* Building a RESTful API with a Django/Python backend
* Collaborating with a frontend team
* Python TDD practices


## Technologies

| Development | Testing       | Dependencies          |
|-------------|---------------|-----------------------|
| Python 3.9.7| unittest      | djangorestframework   |
| Django      |               |                       |
| CircleCI    |               |                       |
| Git/Github  |               |                       |
| Heroku      |               |                       |

<p>
  <b>Framework:</b><br>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
</p>

<p>
  <b>Languages:</b><br>
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-4169E1.svg?style=for-the-badge&logo=SQL&logoColor=white" />
</p>

<p>
  <b>Tools:</b><br>
  <img src="https://img.shields.io/badge/Atom-66595C.svg?&style=for-the-badge&logo=atom&logoColor=white" />  
  <img src="https://img.shields.io/badge/git-F05032.svg?&style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717.svg?&style=for-the-badge&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Heroku-430098.svg?&style=for-the-badge&logo=heroku&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?&style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" />
</p>

<p>
  <b>Processes:</b><br>
  <img src="https://img.shields.io/badge/OOP-b81818.svg?&style=for-the-badge&logo=OOP&logoColor=white" />
  <img src="https://img.shields.io/badge/TDD-b87818.svg?&style=for-the-badge&logo=TDD&logoColor=white" />
  <img src="https://img.shields.io/badge/MVC-b8b018.svg?&style=for-the-badge&logo=MVC&logoColor=white" />
  <img src="https://img.shields.io/badge/REST-33b818.svg?&style=for-the-badge&logo=REST&logoColor=white" />  
</p>


## Local Setup

1. Create and invoke your virtual environment in your local project directory
  ```sh
  python3 -m venv <env>

  source <env>/bin/activate
  ```

2. Fork and clone this repo into your local project directory

4. Install dependencies
   ```sh
   python3 -m pip install -r requirements.txt
   ```

5. Setup the database
  ```sh
  psql

  CREATE DATABASE <db_name>;
  ```

6. Add PostgreSQL database info to settings.py file
  ```py
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db_name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '',
    }
  }
  ```

7. python manage.py migrate


## Getting Started

The `base path` of each endpoint is:

```
https://developer-mental-health-org.herokuapp.com/api/v1
```

- For `GET` requests, you can simply send the endpoint requests through your internet browser.  
- For any other requests (i.e. `POST`, `PATCH`, `DELETE`), you will need to use an API client to provide the request body and access the endpoints.

## Endpoints

The following table presents each API endpoint and its documentation.  

HTTP Verb | Endpoint          | Description                                    | Docs
----------|-------------------|------------------------------------------------|------
GET       | /questions        | Get all questions                              |
POST      | /questions/       | Ask a new question                             |  
GET       | /search/questions | Find questions with keyword or phrase in title |  
GET       | /filter/questions | Filter questions by tag name                   |  
GET       | /questions/:id    | Get a single question                          |  
PATCH     | /questions/:id/   | Update a question                              |  
DELETE    | /questions/:id/   | Delete a question                              |  
POST      | /responses/       | Post a response to a question                  |  
PATCH     | /responses/:id/   | Update a response                              |  
DELETE    | /responses/:id/   | Delete a response                              |  
GET       | /tags             | Get all tags                                   |  
GET       | /tags/:id         | Get a single tag                               |  
POST      | /users/           | Create a new user                              |  
GET       | /users/:id        | Get a single user                              |  
DELETE    | /users/:id/       | Delete a user                                  |  


## Database Schema
![schema](/storage/images/schema.png)


## Contributing

![](https://avatars.githubusercontent.com/u/81713591?s=25) **Antonio King**
- [GitHub](https://github.com/antoniojking)
- [LinkedIn](https://www.linkedin.com/in/antoniojking/)

![](https://avatars.githubusercontent.com/u/78898641?s=25) **Jason Knoll**
- [GitHub](https://github.com/JasonPKnoll)
- [LinkedIn](https://www.linkedin.com/in/jason-p-knoll/)

![](https://avatars.githubusercontent.com/u/77070949?s=25) **Matt Roden**
- [GitHub](https://github.com/Matt-Roden)
- [LinkedIn](https://www.linkedin.com/in/matt-roden-35bb3413b/)

![](https://avatars.githubusercontent.com/u/60903966?s=25) **Stephanie Magdic**
- [GitHub](https://github.com/stephaniemagdic)
- [LinkedIn](https://www.linkedin.com/in/stephaniemagdic/)


## Acknowledgements

* [Turing School of Software and Design](https://turing.edu/)
  - Project created for completion towards Backend Engineering Program
