# Contributing to Eduak Backend

Thank you for your interest in contributing to Eduak Backend! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professional communication

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setting Up Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/eduak-backend.git
cd eduak-backend
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy .env.example to .env and configure:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Development Workflow

### Branch Naming Convention

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes
- `refactor/what-is-refactored` - Code refactoring
- `docs/documentation-update` - Documentation updates

### Commit Message Convention

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(accounts): add password reset functionality

fix(courses): resolve N+1 query issue in course list

docs(readme): update installation instructions
```

### Pull Request Process

1. Create a new branch from `develop`:
```bash
git checkout -b feature/your-feature-name develop
```

2. Make your changes and commit:
```bash
git add .
git commit -m "feat(scope): description"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request:
   - Target the `develop` branch
   - Provide clear description of changes
   - Reference related issues
   - Add screenshots if UI changes

5. Wait for review and address feedback

## Code Style Guidelines

### Python Style

Follow PEP 8 with these specifics:

- Line length: 100 characters max
- Use 4 spaces for indentation
- Use meaningful variable names
- Add docstrings to functions and classes

Example:
```python
def user_create(name: str, email: str, role: str, password: str, phone: str = None) -> User:
    """
    Create a new user with the given parameters.
    
    Args:
        name: User's full name
        email: User's email address
        role: User role (teacher or student)
        password: User's password
        phone: Optional phone number
        
    Returns:
        User: Created user instance
        
    Raises:
        ValidationError: If user creation fails
    """
    # Implementation
```

### Django Best Practices

1. **Models**:
   - Use meaningful model names
   - Add `db_index=True` for frequently queried fields
   - Use `select_related()` and `prefetch_related()`
   - Add `__str__()` method

2. **Views**:
   - Use class-based views
   - Keep views thin, logic in services
   - Add proper permissions
   - Use serializers for validation

3. **Services**:
   - Business logic goes in services
   - One service function = one responsibility
   - Return meaningful data
   - Raise appropriate exceptions

4. **Serializers**:
   - Separate input and output serializers
   - Add custom validation methods
   - Use `read_only` and `write_only` appropriately

### File Organization

```
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── services.py          # Business logic
├── selectors.py         # Database queries
├── permissions.py       # Custom permissions
├── validators.py        # Custom validators
├── urls.py
├── views.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

## Testing

### Writing Tests

1. Create tests for all new features
2. Test edge cases and error conditions
3. Use meaningful test names
4. Keep tests isolated and independent

Example:
```python
from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test that user is created successfully"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'test@example.com')
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Database Migrations

### Creating Migrations

```bash
# Create migrations
python manage.py makemigrations

# Create empty migration for data migration
python manage.py makemigrations --empty app_name

# Name your migration
python manage.py makemigrations --name add_user_indexes
```

### Migration Best Practices

1. Review generated migrations before committing
2. Test migrations on a copy of production data
3. Make migrations reversible when possible
4. Add data migrations separately from schema changes
5. Document complex migrations

## API Documentation

### Documenting Endpoints

Use drf-spectacular decorators:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    tags=['Accounts'],
    summary='Create new user',
    description='Register a new user account',
    request=UserInputSerializer,
    responses={
        201: UserOutputSerializer,
        400: 'Bad Request'
    }
)
class UserCreateAPI(APIView):
    # Implementation
```

## Security Guidelines

1. **Never commit sensitive data**:
   - API keys
   - Passwords
   - Secret keys
   - Database credentials

2. **Input Validation**:
   - Validate all user inputs
   - Use serializers for validation
   - Sanitize data before database operations

3. **Authentication & Authorization**:
   - Always check permissions
   - Use JWT tokens properly
   - Implement rate limiting

4. **Error Handling**:
   - Don't expose internal errors to users
   - Log errors properly
   - Return appropriate HTTP status codes

## Performance Guidelines

1. **Database Queries**:
   - Use `select_related()` for ForeignKey
   - Use `prefetch_related()` for ManyToMany
   - Add indexes to frequently queried fields
   - Avoid N+1 queries

2. **Caching**:
   - Cache expensive operations
   - Use appropriate cache timeouts
   - Invalidate cache when data changes

3. **API Responses**:
   - Implement pagination
   - Return only necessary fields
   - Use compression for large responses

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Join our community discussions
- Contact maintainers for urgent matters

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

Thank you for contributing to Eduak Backend! 🚀
