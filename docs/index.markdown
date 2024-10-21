---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---
# Magic sandbox

[How to play ?](./how-to-play.html)

## Technical Stack

-   Backend: FastAPI - A modern, fast web framework for building APIs with Python.
-   Frontend: Vite.js - A frontend build tool that significantly improves the frontend development experience.
-   Frontend: Vue.js - A frontend framework that is integrated with vite
-   Containerization: Docker - Used to containerize both frontend and backend services, ensuring easy deployment and consistent environments.
-   Orchestration: Docker Compose - Used for defining and running multi-container Docker applications.
-   Selenium: Python library to automate web browsing, allow to load web content.
-   Webscraping: Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML.
-   Jekyll: Generate and serve documentation with markdown file.
  

## Run locally

### Prerequisites

-   Docker: Ensure Docker and Docker Compose are installed on your system. For installation instructions, visit Docker's official documentation.

### How to Launch with docker

1. Clone the Repository: Clone this repository to your local machine.

2. Navigate to the front Project Directory:

3. run commands :

```
npm install
npm run build:test
```

4. Start the Containers: Use Docker Compose to build and start the services.

```
docker-compose up --build
```

5. You can expose the app publically with ngrok 

```
ngrok http 5000
```

### How to start backend

1. Go to back folder
2. Create a venv if not created already (python -m venv .venv for linux, python -m venv venv for windows)
3. Activate the venv (source .venv/bin/activate for linux, .\venv\Scripts\activate for windows)
4. You need to have google chrome executable installed
5. Install dependencies on the venv :
```
pip install --no-cache-dir -r requirements.txt
```
6. run fastAPI with uvicorn : 
```
uvicorn main:app --reload
```

### How to start frontend locally

1. Go to front folder
2. run npm install
3. run npm run dev

#### Accessing the Application

- Frontend: Once the services are up and running, access the frontend application at http://localhost:5000. The frontend acts as a reverse proxy and pass requests containing /api to the backend but for test purposes you can still access the backend directly.
- Backend API: The FastAPI backend can be accessed at http://localhost:8000. The API documentation provided by FastAPI can be accessed at http://localhost:8000/docs.

## Documentation

The documentation is a github page, it is generated and serve with Jekyll, on each push to master the documentation is built with a github action workflow that is automatically added by github. It is also automatically served on [https://holmessamuel.github.io/magic-sandbox/=](https://holmessamuel.github.io/magic-sandbox/)
 
