# Movie Soulmate 🎥

**Movie Soulmate** is a web application designed to recommend movies based on user preferences. This project was developed as part of the **Astana Hub GARAGE Startup Incubator** under the **Movie Soulmate** initiative.

## Features 🚀

- **Personalized Movie Recommendations**: Utilizes the Jaccard similarity index algorithm to recommend movies based on user preferences.
- **High Performance**: Optimized with asynchronous operations and caching for enhanced responsiveness.
- **Scalable Architecture**: Built using modern tools and frameworks for scalability and maintainability.

## Tech Stack 🛠️

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance), Python-based web framework.
  
### Database
- **Relational Database**: [PostgreSQL](https://www.postgresql.org/) - Managed asynchronously using:
  - **asyncpg**: Async database driver for PostgreSQL.
  - **SQLAlchemy**: ORM for database management.
  - **Alembic**: For database migrations.

### Caching
- **Redis**: Implemented for quick data retrieval and caching.


## Deployment 🌐

The **Minimal Viable Product (MVP)** has been deployed on [Render.com](https://render.com/), a cloud hosting platform.  
Access the live project here: [Movie Soulmate](https://fastapi-g23k.onrender.com/pages/)

## How It Works 🤔

1. **User Input**: Users select their preferred movie genres or titles.
2. **Algorithm**: The application applies the Jaccard similarity index to compare user preferences with existing data.
3. **Recommendation**: Movies matching the user's taste are recommended.

## Getting Started 💻

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/movie-soulmate.git](https://github.com/snazh/MoiveMatch2.0-FastAPI.git)
   cd movie-soulmate
2. Run website
   ```bash
   docker-compose up
