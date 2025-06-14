# Django Social Media App

# requirements

- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker)

---

## how to Run the Project

1. **Caone the repository:**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name



1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name


2. Make sure the media/ folder exists (this folder holds uploaded images, posts, and other media):

bash
Copy
Edit
mkdir -p media


3. docker-compose up --build
The Django app will run inside a Docker container named django_web.

Elasticsearch will run in a container named elasticsearch.

4 Open your browser and visit:
http://localhost:8000




Stopping the App
To stop the running containers, press Ctrl + C in the terminal.

To restart the app later, just run:


docker-compose up
