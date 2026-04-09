# Django Realtime Broadcast

A **production‑style realtime feed system** built with **Django, Django Channels, Redis, Celery, and Docker**.

This project demonstrates how to design a **modern realtime backend architecture** where users can create posts and see them **instantly broadcast to all connected clients** using WebSockets.
The system also includes **background workers, scheduled tasks, caching, and containerized infrastructure**.
This repository is intended as a **learning resource and backend architecture demonstration project**.

> ⚠️ **Note:** This project is currently configured for **local Docker-based testing**. Public deployment is not available at the moment, but the system is fully ready for deployment in a suitable environment.

---

## Repository

- **GitHub**: [https://github.com/anis191/django-realtime-broadcast](https://github.com/anis191/django-realtime-broadcast)
- **GitLab**: [https://gitlab.com/anisulalam-lab/django-realtime-broadcast-lab](https://gitlab.com/anisulalam-lab/django-realtime-broadcast-lab)

---

## Key Features

- **Realtime Post Broadcast**  
  New posts are instantly delivered to all connected clients using **Django Channels and WebSockets**.

- **Background Task Processing**  
  **Celery workers** handle asynchronous operations and scheduled tasks.

- **Scheduled Trending System**  
  A periodic task automatically selects trending posts and broadcasts them to the realtime feed.

- **Redis Infrastructure**  
  Redis is used for:
  - WebSocket channel layer
  - Celery broker
  - Celery result backend
  - Django caching

- **Redis‑based Feed Cache**  
  Recent posts are cached to improve feed performance.

- **Dockerized Architecture**  
  The entire system runs using **Docker Compose**, including:
  - Django ASGI server
  - Redis
  - Celery worker
  - Celery beat scheduler

- **Secure Redis Configuration**  
  Custom Redis configuration includes:
  - ACL authentication
  - Disabled destructive commands
  - Persistence configuration
  - Memory limits

- **Modern Python Tooling**  
  Dependency management uses **uv**, providing faster dependency resolution.

---

## Technology Stack

| Category             | Technology                      |
| -------------------- | ------------------------------- |
| **Backend**          | Django, Django Channels, Celery |
| **Database**         | Supabase Postgresql             |
| **Cache & Broker**   | Redis                           |
| **ASGI Server**      | Uvicorn                         |
| **Containerization** | Docker, Docker Compose          |
| **Dependency Mgmt**  | uv                              |

---

## System Architecture

```
Client Browser
│
▼
WebSocket Connection
│
▼
Django Channels (ASGI)
│
├── Redis Channel Layer
│
├── Redis Cache
│
└── Celery Broker
│
▼
Redis Server
│
├── Celery Worker
│
└── Celery Beat
```

---

## Realtime Event Flow

```
User submits post
│
▼
Django View saves Post
│
▼
Django Signal (post_save)
│
▼
Channels group_send
│
▼
Redis Channel Layer
│
▼
WebSocket Consumer
│
▼
All connected clients receive the post instantly
```

---

## Trending Rotation Flow

```
Celery Beat Scheduler
│
▼
rotate_trending_post task
│
▼
Random trending posts selected
│
▼
Channels broadcast
│
▼
Clients receive trending posts in realtime
```

---

## Project Structure

```
django-realtime-broadcast/
│
├── broadcast/               # Django project settings
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   └── urls.py
│
├── feed/                    # Main application
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── consumers.py
│   ├── routing.py
│   ├── signals.py
│   └── tasks.py
│
├── redis/
│   └── redis.conf           # Secure Redis configuration
│
├── templates/               # HTML templates
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml           # uv project definition
├── uv.lock
└── manage.py
```

---

## Deployment Status

This project is currently configured for **local Docker‑based testing**.

Because the system includes multiple infrastructure services:

- Django ASGI server
- Redis
- Celery workers
- Celery beat scheduler
- WebSocket broadcasting

a public deployment requires infrastructure capable of running multiple containers.

At the moment, a public deployment is **not available**, but the project is fully prepared for deployment and may be deployed in the future.

---

## Running the Project Locally

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/anis191/django-realtime-broadcast.git
   cd django-realtime-broadcast
   ```

2. **Configure environment variables**

   Create a `.env` file in the project root with the following content:

   ```env
   SECRET_KEY=your_secret_key_here
   REDIS_PASSWORD=your_secure_password_here
   REDIS_URL=redis://anis:your_secure_password_here@redis:6379/0
   ```

3. **Start all services**

   ```bash
   docker compose -f docker-compose.yml up -d --build
   ```

   Docker will start:
   - Django application server
   - Redis
   - Celery worker
   - Celery beat scheduler

4. **Access the application**

   Open your browser and navigate to:

   ```
   http://localhost:8000
   ```

---

## Docker Management Commands

| Action                                      | Command                                                                 |
|---------------------------------------------|-------------------------------------------------------------------------|
| Start all containers (detached)             | `docker compose -f docker-compose.yml up -d`                             |
| List running containers                     | `docker compose -f docker-compose.yml ps` <br/> or `docker ps`           |
| Open a shell inside the Django container    | `docker compose -f docker-compose.yml exec django_project bash`          |
| Access Redis CLI                            | `docker exec -it redis_server redis-cli -u redis://<username>:<password>@redis:6379/0` |
| Stop all containers (preserve state)        | `docker compose -f docker-compose.yml stop`                              |
| Start previously stopped containers         | `docker compose -f docker-compose.yml start`                             |
| Stop and remove containers, networks        | `docker compose -f docker-compose.yml down`                              |
| Restart Django container (after code changes)| `docker compose restart django_project`                                  |

> **Note**: Replace `<username>` and `<password>` with your actual Redis username and password defined in the `.env` file.

---

## Useful Django & Utility Commands

| Action                | Command                                                      |
|-----------------------|--------------------------------------------------------------|
| Run migrations        | `docker compose exec django_project uv run manage.py migrate` |
| Create superuser      | `docker compose exec django_project uv run manage.py createsuperuser` |
| View logs             | `docker compose logs -f`                                     |

---

## WebSocket Endpoint

```
ws://localhost:8000/ws/feed/
```

All realtime feed updates are delivered through this channel.

---

## Example Celery Task

```
rotate_trending_post
```

This task selects random posts and broadcasts them to the feed as trending posts.

---

## Git Remote Management

This project is pushed to both GitHub and GitLab using separate remotes:

```bash
# Push to GitHub
git push origin main

# Push to GitLab
git push gitlab main
```

The remotes are configured as:
- `origin` → GitHub
- `gitlab` → GitLab

---

## Learning Goals

This project demonstrates several important backend engineering concepts:

- Realtime systems with Django Channels
- WebSocket broadcasting
- Asynchronous background tasks
- Redis infrastructure usage
- Scheduled task processing
- Docker container orchestration
- Caching strategies

---

## Future Improvements

Possible extensions:

- Authentication system
- Likes and comments
- Infinite scrolling
- PostgreSQL support
- Media uploads
- Production deployment
- Monitoring and logging

---

## License

This project is provided for **learning and demonstration purposes**.

---

## Author

**Anisul Alam**

Backend project demonstrating **modern Django realtime architecture** using Channels, Redis, Celery, and Docker.
