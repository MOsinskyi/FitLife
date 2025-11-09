# FitLife Backend Tests

This directory contains comprehensive tests for the FitLife Gym Training Network API.

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures for all tests
├── test_auth.py          # Authentication & authorization tests
├── test_security.py      # Password hashing & JWT token tests
├── test_users.py         # Manager/user management tests
├── test_coaches.py       # Coach management tests
├── test_customers.py     # Customer management tests
├── test_schedules.py     # Training schedule tests
└── test_bookings.py      # Booking system tests
```

## Running Tests

### Run all tests

```bash
make test
# or
cd backend && PYTHONPATH=src poetry run pytest tests/ -v
```

### Run specific test file

```bash
cd backend && PYTHONPATH=src poetry run pytest tests/test_auth.py -v
```

### Run specific test

```bash
cd backend && PYTHONPATH=src poetry run pytest tests/test_auth.py::test_login_success -v
```

### Run with coverage

```bash
cd backend && PYTHONPATH=src poetry run pytest tests/ --cov=fitlife --cov-report=html
```

## Test Coverage

### Authentication Tests (`test_auth.py`)

- Health check endpoint
- Root endpoint
- Login with valid/invalid credentials
- JWT token creation and validation
- Protected endpoint access with/without tokens
- Role-based access control

### Security Tests (`test_security.py`)

- Password hashing with bcrypt
- Password verification
- Hash uniqueness (salt generation)
- JWT token creation with default/custom expiry
- Token payload validation
- Invalid signature/algorithm handling

### User Management Tests (`test_users.py`)

- Create managers
- List managers
- Get manager by ID
- Handle duplicate emails
- Input validation

### Coach Tests (`test_coaches.py`)

- Coach registration
- List coaches
- Get coach by ID
- Duplicate email handling
- Authorization checks

### Customer Tests (`test_customers.py`)

- Customer registration
- List customers
- Get customer by ID
- Duplicate email handling
- Authorization checks

### Schedule Tests (`test_schedules.py`)

- Create schedules as coach
- Prevent customer from creating schedules
- List and retrieve schedules
- Invalid time range handling

### Booking Tests (`test_bookings.py`)

- Create bookings as customer
- Prevent coach from creating bookings
- List and retrieve bookings
- Get bookings by customer
- Handle nonexistent schedules

## Fixtures

The `conftest.py` file provides several useful fixtures:

- `client`: FastAPI TestClient instance
- `clean_db`: Clears all database tables before/after each test
- `sample_manager`: Creates a test manager user
- `sample_coach`: Creates a test coach user
- `sample_customer`: Creates a test customer user
- `manager_token`: JWT token for manager authentication
- `coach_token`: JWT token for coach authentication
- `customer_token`: JWT token for customer authentication

## Notes

- All tests use an in-memory database that is cleared between tests
- Tests are isolated and can run in any order
- Authentication tokens are generated fresh for each test
- Password is always "testpassword" for test users
