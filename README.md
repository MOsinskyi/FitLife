# FitLife - Gym Training Network API

A modern REST API for managing gym operations, including memberships, coaches, customers, training schedules, and booking systems.

## Features

- **User Management**: Support for multiple user roles (managers, coaches, customers)
- **Authentication**: Secure JWT-based authentication with role-based access control
- **Coach Management**: Create and manage coach profiles
- **Customer Management**: Handle customer registrations and profiles
- **Training Schedules**: Create and manage training sessions with capacity limits
- **Booking System**: Book training sessions with automatic availability tracking
- **Membership Management**: Handle gym membership plans
- **Interactive API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **Framework**: FastAPI
- **Authentication**: JWT (python-jose) with OAuth2
- **Password Hashing**: bcrypt (via passlib)
- **Validation**: Pydantic
- **Configuration**: pydantic-settings
- **Server**: Uvicorn
- **Dependency Management**: Poetry

## Prerequisites

- Python 3.12+
- Poetry (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fitlife
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Configure environment variables:
```bash
cp .env.templates .env
```

Edit `.env` and set the following variables:
```env
PROJECT_NAME=Gym Training Network API
VERSION=1.0.0
API_V1_STR=/api/v1

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Generate a secure `SECRET_KEY` for production use:
```bash
openssl rand -hex 32
```

## Running the Application

### Development Server

```bash
cd backend
poetry run uvicorn fitlife.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

### Alternative: Direct Python Execution

```bash
cd backend
poetry run python -m fitlife.main
```

## API Overview

### Authentication

All protected endpoints require a JWT token obtained via login.

**Login:**
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Using the token:**
```bash
curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/v1/customers
```

### API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Authenticate and get access token

#### Managers (Users)
- `GET /api/v1/managers` - List all managers
- `POST /api/v1/managers` - Create a new manager
- `GET /api/v1/managers/{id}` - Get manager details

#### Coaches
- `GET /api/v1/coaches` - List all coaches
- `POST /api/v1/coaches` - Create a new coach
- `GET /api/v1/coaches/{id}` - Get coach details

#### Customers
- `GET /api/v1/customers` - List all customers
- `POST /api/v1/customers` - Create a new customer
- `GET /api/v1/customers/{id}` - Get customer details

#### Schedules
- `GET /api/v1/schedules` - List all training schedules
- `POST /api/v1/schedules` - Create a new schedule (coach only)
- `GET /api/v1/schedules/{id}` - Get schedule details

#### Bookings
- `GET /api/v1/bookings` - List bookings
- `POST /api/v1/bookings` - Create a booking (customer only)
- `GET /api/v1/bookings/{id}` - Get booking details

## User Roles

The API supports three user roles with different permissions:

- **Manager**: Administrative access to manage all aspects of the gym
- **Coach**: Can create and manage training schedules
- **Customer**: Can view schedules and book training sessions

## Project Structure

```
fitlife/
├── backend/
│   ├── src/fitlife/
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # In-memory database
│   │   ├── security.py          # Authentication utilities
│   │   ├── deps.py              # FastAPI dependencies
│   │   ├── routers.py           # Router registration
│   │   ├── auth/                # Authentication module
│   │   ├── user/                # User/manager management
│   │   ├── customer/            # Customer management
│   │   ├── coach/               # Coach management
│   │   ├── schedule/            # Schedule management
│   │   ├── booking/             # Booking system
│   │   └── membership/          # Membership management
│   ├── pyproject.toml           # Poetry dependencies
│   ├── poetry.lock              # Locked dependencies
│   └── .env.templates           # Environment template
├── CLAUDE.md                    # Development guide
└── README.md                    # This file
```

## Database

**Current Implementation**: The application uses an in-memory dictionary-based database for simplicity and rapid development. Data is not persisted between restarts.

**Future Enhancement**: The repository pattern is already implemented, making it straightforward to migrate to a persistent database (PostgreSQL, MySQL, etc.) by replacing the repository implementations.

## Development

### Code Organization

Each module follows a consistent pattern:
- `schemas.py`: Pydantic models for validation
- `views.py`: FastAPI route handlers
- `services.py`: Business logic (where applicable)
- `repositories.py`: Data access layer (where applicable)

### Adding a New Feature

1. Define request/response models in `schemas.py`
2. Implement business logic in `services.py`
3. Create data access methods in `repositories.py`
4. Add route handlers in `views.py`
5. Register the router in `routers.py`

### Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- CORS is currently open for development (`allow_origins=["*"]`) - configure appropriately for production
- Never commit `.env` files with real secrets

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

1. Start the server
2. Navigate to http://localhost:8000/api/v1/docs
3. Use the "Authorize" button to log in
4. Test endpoints directly from the browser

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Maksym Osinskyi - maximosinskiy@gmail.com

## Contributing

This project is in active development. Contributions, issues, and feature requests are welcome.
