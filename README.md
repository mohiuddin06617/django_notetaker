# Django Note Taker

This repository contains a simple Django note taking application that is configured to run within Docker containers. It includes a Django web application and a PostgreSQL database running in separate Docker containers.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your development machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to set up and run the project:

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/mohiuddin06617/django_notetaker.git
   cd django_notetaker
2. Create a **.env** file by copying the provided **.env.example** file:
    ```bash
    cp .env.example .env
3. Use Docker Compose to build and run the containers
    ```bash
    docker-compose up -d --build
   
4. Open a terminal and access bash of the Django application container by typing:
    ```bash
    docker exec -it django_note_taking_app bash
5. Once inside the container's bash shell, please run Django migrations with
    ```bash
   python manage.py migrate
