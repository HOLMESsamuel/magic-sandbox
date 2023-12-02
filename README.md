# Magic sandbox

With this project, I aim to create a platform to load MTG decks from websites like Archidekt and enable playing Magic: The Gathering online with friends. The platform does not implement game rules but allows players to move cards around, mimicking the real-life experience. This project will be self-hosted and can be shared online using tools like ngrok.

## Technical Stack

-   Backend: FastAPI - A modern, fast web framework for building APIs with Python.
-   Frontend: Vite.js - A frontend build tool that significantly improves the frontend development experience.
-   Containerization: Docker - Used to containerize both frontend and backend services, ensuring easy deployment and consistent environments.
-   Orchestration: Docker Compose - Used for defining and running multi-container Docker applications.

## Prerequisites

-   Docker: Ensure Docker and Docker Compose are installed on your system. For installation instructions, visit Docker's official documentation.

## How to Launch

1. Clone the Repository: Clone this repository to your local machine.

2. Navigate to the Project Directory:


3. Start the Containers: Use Docker Compose to build and start the services.

'''
docker-compose up --build
'''

4. Serve online with ngrok
'''
ngrok http 5000
'''

## Accessing the Application

- Frontend: Once the services are up and running, access the frontend application at http://localhost:5000.
- Backend API: The FastAPI backend can be accessed at http://localhost:8000. The API documentation provided by FastAPI can be accessed at http://localhost:8000/docs.