<!-- PROJECT INFO -->
<h1 align="center">
  <br>
  Mental Health Org Backend API
  <br>
</h1>

<h4 align="center">RESTful API for Mental Health Org frontend application consumption.</h4>

<p align="center">
  <a href="https://github.com/marlitas/rails_engine/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/mental-health-org/mental_health_be?style=for-the-badge" alt="contributors_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/network/members">
    <img src="https://img.shields.io/github/forks/mental-health-org/mental_health_be?style=for-the-badge" alt="forks_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/stargazers">
    <img src="https://img.shields.io/github/stars/mental-health-org/mental_health_be?style=for-the-badge" alt="stars_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/issues">
    <img src="https://img.shields.io/github/issues/mental-health-org/mental_health_be?style=for-the-badge" alt="issues_badge">


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

Mental Health Org is a platform that allows professionals such as mental health counselors, school counselors, dieticians, and human services to connect and share resources.

### Learning Goals

* Building a RESTful API with a Django/Python backend
* Collaborating with a Front End team
* Python TDD practices


## Tools Used

| Development | Testing       | Dependencies          |
|   :----:    |    :----:     |    :----:             |
| Python 3.9.7| unittest      | djangorestframework   |
| Django      |               |                       |
| CircleCI    |               |                       |
| Git/Github  |               |                       |
| Heroku      |               |                       |




## Set Up


## Run Locally

1. Fork this repo
    
2. Clone your new repo
   ```sh
   git clone https://github.com/mental-health-org/mental_health_be.git
   ```
    
3. Create and Invoke your virtual environment
  ```sh
  python3 -m virtualenv venv

  source <virtual env>/bin/activate
  ```
    
4. Install dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```
    
5. Setup the database
  ```sh
  psql

  CREATE DATABASE <project name>;
  ```

6. Add PostgreSQL database info to settings.py file

7. python manage.py migrate


## How To Use

To experience the UI our frontend team built please [visit](http://mental-health-fe.herokuapp.com/). Otherwise you may hit our endpoints through an http request helper such as Postman.

### Endpoint Documentation

Domain: 'https://developer-mental-health-org.herokuapp.com/'


## Database Schema
![schema](/storage/images/schema.png)

## Contributing

👤  **Antonio King**
- [GitHub](https://github.com/antoniojking)
- [LinkedIn](https://www.linkedin.com/in/antoniojking/)

👤  **Jason Knoll**
- [GitHub](https://github.com/JasonPKnoll)
- [LinkedIn](https://www.linkedin.com/in/jason-p-knoll/)

👤  **Matt Roden**
- [GitHub](https://github.com/Matt-Roden)
- [LinkedIn](https://www.linkedin.com/in/matt-roden-35bb3413b/)

👤  **Stephanie Magdic**
- [GitHub](https://github.com/stephaniemagdic)
- [LinkedIn](https://www.linkedin.com/in/stephaniemagdic/)


## Acknowledgements

* [Turing School of Software and Design](https://turing.edu/)
  - Project created for completion towards Backend Engineering Program
