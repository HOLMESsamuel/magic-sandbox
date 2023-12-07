# Magic sandbox

With this project, I aim to create a platform to load MTG decks from websites like Archidekt and enable playing Magic: The Gathering online with friends. The platform does not implement game rules but allows players to move cards around, mimicking the real-life experience. This project will be self-hosted and can be shared online using tools like ngrok.

## Technical Stack

-   Backend: FastAPI - A modern, fast web framework for building APIs with Python.
-   Frontend: Vite.js - A frontend build tool that significantly improves the frontend development experience.
-   Frontend: Vue.js - A frontend framework that is integrated with vite
-   Containerization: Docker - Used to containerize both frontend and backend services, ensuring easy deployment and consistent environments.
-   Orchestration: Docker Compose - Used for defining and running multi-container Docker applications.
-   Webscraping: Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML.

## Prerequisites

-   Docker: Ensure Docker and Docker Compose are installed on your system. For installation instructions, visit Docker's official documentation.

## How to Launch with docker

1. Clone the Repository: Clone this repository to your local machine.

2. Navigate to the Project Directory:


3. Start the Containers: Use Docker Compose to build and start the services.

```
docker-compose up --build
```

4. Serve online with ngrok

```
ngrok http 5000

```

## How to start backend locally

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

## How to start frontend locally

1. Go to front folder
2. run npm install
3. run npm run dev

## Accessing the Application

- Frontend: Once the services are up and running, access the frontend application at http://localhost:5000.
- Backend API: The FastAPI backend can be accessed at http://localhost:8000. The API documentation provided by FastAPI can be accessed at http://localhost:8000/docs.