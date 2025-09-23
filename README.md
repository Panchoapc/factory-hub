# Factory-Hub: A Sales Order Management Platform

A web-based platform designed to streamline the sales order process for a manufacturing factory. This project automates the creation, management, and dispatch of sales orders, moving the process from manual, paper-based forms to a digital, efficient workflow.

## Technologies Used

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Containerization**: Docker, Dev Containers
- **Version Control**: Git

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- **Docker Desktop**: Ensure Docker is installed and running on your system.
- **Visual Studio Code**: The recommended IDE for this project, with the [**Dev Containers**](https://code.visualstudio.com/docs/devcontainers/containers) extension installed.

### Setup

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/factory-hub.git
    cd factory-hub
    ```

2.  **Open in Dev Container**:
    Open the project folder in VS Code. VS Code will detect the `.devcontainer` folder and prompt you to "Reopen in Container". Click this button to start the environment. This will build and run all the necessary services (backend, frontend, and database).

3.  **Install Dependencies**:
    The container will automatically install all dependencies. You can verify this by checking the `requirements.txt` file in the `backend` directory.

4.  **Database Migration**:
    Once the Dev Container is running, open the integrated terminal and run the database migrations.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server**:
    The Django development server should start automatically. You can access it in your browser at `http://localhost:8000`.

## Project Roadmap

This project is under active development. The following features are planned for future releases:

- **Order Tracking**: A dashboard to track the status of orders (e.g., in progress, shipped, completed).
- **Client Dashboard**: A dedicated view for salespeople to manage their clients and past orders.
- **User Authentication**: Implement user accounts and secure access to the platform.
- **Production Module**: A new app to manage production schedules and inventory.

## License

License: "This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details."
