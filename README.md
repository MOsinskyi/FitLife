# FitLife - Gym Training Network

A modern full-stack application for managing gym operations, including memberships, coaches, customers, training schedules, and booking systems.

**Backend**: FastAPI REST API
**Frontend**: Vue 3 + Vite web application

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

### Backend

- **Framework**: FastAPI ^0.119.0
- **Authentication**: JWT (python-jose) with OAuth2
- **Password Hashing**: bcrypt (via passlib)
- **Validation**: Pydantic
- **Configuration**: pydantic-settings
- **Server**: Uvicorn
- **Testing**: pytest
- **Dependency Management**: Poetry

### Frontend

- **Framework**: Vue 3 (^3.5.22)
- **Build Tool**: Vite (^7.1.11)
- **Dev Tools**: Vue DevTools plugin

### Code Quality Tools

- **Formatter**: Black (line length: 100)
- **Import Sorter**: isort (profile: black)
- **Linter**: Ruff (fast linter)
- **Type Checker**: MyPy
- **Security Scanner**: Bandit
- **Pre-commit Hooks**: Automated code quality checks

## Prerequisites

- Python 3.12+
- Poetry (for backend dependency management)
- Node.js 20.19+ or 22.12+ (for frontend)

## Installation

### Quick Setup (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd fitlife
```

2. Setup backend:

```bash
make setup
```

This will install backend dependencies and create a `.env` file from the template.

3. Edit `backend/.env` and set your `SECRET_KEY`:

```bash
# Generate a secure key:
openssl rand -hex 32
```

4. Setup frontend:

```bash
cd frontend
npm install
```

### Manual Setup

#### Backend Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd fitlife
```

2. Navigate to the backend directory and install dependencies:

```bash
cd backend
poetry install --no-root
```

3. Configure environment variables:

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

#### Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Backend

#### Using Makefile (Recommended)

**Development mode with auto-reload:**

```bash
make dev
```

**Production mode:**

```bash
make run
```

**See all available commands:**

```bash
make help
```

#### Manual Execution

**Development Server with auto-reload:**

```bash
cd backend
PYTHONPATH=src poetry run uvicorn fitlife.main:app --reload --host 0.0.0.0 --port 8000
```

**Production Server:**

```bash
cd backend
PYTHONPATH=src poetry run uvicorn fitlife.main:app --host 0.0.0.0 --port 8000
```

**IMPORTANT**: Always use `PYTHONPATH=src` when running Python commands directly to ensure proper module resolution.

The API will be available at:

- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

### Frontend

**Development server:**

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:5173 (default Vite port).

**Production build:**

```bash
cd frontend
npm run build      # Build for production
npm run preview    # Preview production build
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
│   ├── src/fitlife/             # Main application package
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings via pydantic-settings
│   │   ├── database.py          # In-memory database (dict-based stores)
│   │   ├── security.py          # Password hashing & JWT creation
│   │   ├── deps.py              # FastAPI dependencies (auth, role checks)
│   │   ├── routers.py           # Central router registration
│   │   │
│   │   ├── auth/                # Authentication endpoints
│   │   ├── user/                # User management (managers)
│   │   ├── customer/            # Customer management
│   │   ├── coach/               # Coach management
│   │   ├── schedule/            # Training schedule management
│   │   ├── booking/             # Booking system
│   │   └── membership/          # Membership management
│   │
│   ├── tests/                   # Test suite (pytest)
│   ├── pyproject.toml           # Poetry dependencies & tool configs
│   ├── poetry.lock              # Locked dependencies
│   └── .env.templates           # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── main.js              # Vue app entry point
│   │   ├── App.vue              # Root Vue component
│   │   ├── assets/              # Static assets (CSS, images)
│   │   └── components/          # Vue components
│   │
│   ├── vite.config.js           # Vite configuration
│   └── package.json             # NPM dependencies
│
├── Makefile                     # Common development commands
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── CLAUDE.md                    # Development guide
└── README.md                    # This file
```

## Database

**Current Implementation**: The application uses an in-memory dictionary-based database for simplicity and rapid development. Data is not persisted between restarts.

**Future Enhancement**: The repository pattern is already implemented, making it straightforward to migrate to a persistent database (PostgreSQL, MySQL, etc.) by replacing the repository implementations.

## Development

### Common Development Commands

The project includes a Makefile with helpful commands:

```bash
make help                # Show all available commands
make setup               # Complete setup (install + create .env)
make dev                 # Run development server with auto-reload
make run                 # Run production server
make test                # Run all tests
make lint                # Run linting checks
make format              # Format code with black and isort
make clean               # Remove cache files
make shell               # Open Poetry shell
make docs                # Show API documentation URLs
make info                # Show project information
make add-dep             # Add a dependency (usage: make add-dep DEP=package-name)
make update-deps         # Update all dependencies
make pre-commit-install  # Install pre-commit hooks
make pre-commit-run      # Run pre-commit on staged files
make pre-commit-all      # Run pre-commit on all files
```

### Testing

**Run all tests:**

```bash
make test
# or manually:
cd backend && PYTHONPATH=src poetry run pytest tests/ -v
```

**Run specific test file:**

```bash
cd backend && PYTHONPATH=src poetry run pytest tests/test_auth.py -v
```

**Run specific test:**

```bash
cd backend && PYTHONPATH=src poetry run pytest tests/test_auth.py::test_login_success -v
```

**Test fixtures** available in `backend/tests/conftest.py`:

- `client`: FastAPI TestClient
- `clean_db`: Clears database
- `sample_manager`, `sample_coach`, `sample_customer`: Test users
- `manager_token`, `coach_token`, `customer_token`: Auth tokens
- Test password for all users: "testpassword"

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

**Install hooks (recommended):**

```bash
make pre-commit-install
```

**Run on staged files:**

```bash
make pre-commit-run
```

**Run on all files:**

```bash
make pre-commit-all
```

Pre-commit hooks automatically run on `git commit` and include:

- Black (code formatter)
- isort (import sorter)
- Ruff (linter)
- MyPy (type checker)
- Bandit (security scanner)

### Code Organization

#### Backend Module Structure

Each backend module follows a consistent pattern:

- `schemas.py`: Pydantic models for request/response validation
- `views.py`: FastAPI route handlers (APIRouter)
- `services.py`: Business logic layer (if present)
- `repositories.py`: Data access layer (if present)

All modules are registered in `routers.py` under the `/api/v1` prefix.

#### Adding a New Backend Feature

1. Define request/response schemas in `<module>/schemas.py`
2. Implement business logic in `<module>/services.py` (if complex)
3. Create data access methods in `<module>/repositories.py` (if needed)
4. Add route handler in `<module>/views.py`
5. Register router in `routers.py` (if new module)
6. Write tests in `backend/tests/test_<module>.py`

### Architecture Patterns

#### Dependency Injection

FastAPI's `Depends()` is used throughout:

- `get_db()`: Provides database access
- `get_current_user()`: Validates authentication
- Role-specific dependencies for authorization

#### Repository Pattern

Data access is abstracted through repository classes:

- Example: `UserRepository(db)`, `BookingRepository(db)`
- Methods: `create()`, `get_by_*()`, etc.
- Enables future database migration without changing business logic

#### Service Layer

Complex business logic is isolated in service classes:

- Example: `AuthService` handles authentication logic
- Example: `BookingService` manages booking validation and creation
- Keeps views thin and focused on HTTP concerns

### Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- Token validation in `deps.py:get_current_user`
- Role-based access control via dependencies:
  - `get_current_manager`: Manager role only
  - `get_current_coach`: Coach role only
  - `get_current_customer`: Customer role only
- CORS is currently open for development (`allow_origins=["*"]`) - configure appropriately for production
- Never commit `.env` files with real secrets
- Pre-commit hooks include Bandit security scanner

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
