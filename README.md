# TrainMath - Math Training Platform

A comprehensive Django-based platform for practicing various types of mathematical problems including arithmetic, algebra, calculus, and more.

## Features

### Problem Types
- **Mental Arithmetic**: Basic operations (+, -, *, /) with different difficulty levels
- **Algebraic Identities**: Expanding and factoring algebraic expressions
- **Exponential & Logarithmic**: Working with exponential expressions and logarithms
- **Linear & Quadratic Equations**: Solving various types of equations
- **Derivatives & Integrals**: Calculus problems with symbolic computation

### User Features
- **Guest Mode**: Practice without registration
- **User Registration**: Save progress and statistics
- **Statistics Tracking**: Accuracy, average time, progress per type/difficulty
- **Result Sharing**: Share results via unique URLs
- **Admin Dashboard**: Comprehensive analytics and user management

### Technical Features
- **SymPy Integration**: Symbolic mathematics computation
- **Responsive Design**: Bootstrap-based modern UI
- **Docker Support**: Easy deployment with Docker Compose
- **PostgreSQL**: Production-ready database
- **Nginx**: Reverse proxy and static file serving
- **Comprehensive Testing**: Unit tests for all components

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trainmath-monorepo
   ```

2. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

3. **Deploy with Docker**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Access the application**
   - Main application: http://localhost
   - Admin panel: http://localhost/admin/
   - Admin dashboard: http://localhost/admin/dashboard/

## Development Setup

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py populate_problem_types
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Running Tests

```bash
python manage.py test
```

## Project Structure

```
trainmath-monorepo/
├── core/                    # Core application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── admin.py            # Admin configuration
│   └── templates/          # Core templates
├── exercises/              # Problem generators
│   ├── arithmetic.py       # Arithmetic problems
│   ├── algebraic.py        # Algebraic identities
│   ├── exponential.py      # Exponential/logarithmic
│   ├── equations.py        # Linear/quadratic equations
│   ├── calculus.py         # Derivatives/integrals
│   └── base.py             # Base problem class
├── users/                  # User management
│   ├── models.py           # Custom user model
│   ├── views.py            # Authentication views
│   └── forms.py            # User forms
├── trainmath/              # Project settings
│   ├── settings.py         # Development settings
│   └── production_settings.py  # Production settings
├── templates/              # Base templates
├── static/                 # Static files
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── nginx.conf              # Nginx configuration
├── deploy.sh               # Deployment script
└── backup.sh               # Backup script
```

## Configuration

### Environment Variables

Key environment variables for production:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=0
DJANGO_PRODUCTION=1
DJANGO_ALLOWED_HOSTS=yourdomain.com

# Database
POSTGRES_DB=trainmath
POSTGRES_USER=trainmath
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Adding New Problem Types

1. Create a new problem class in `exercises/` directory
2. Inherit from `BaseProblem` class
3. Implement `generate()` and `check()` methods
4. Add to `PROBLEM_REGISTRY` in `core/views.py`
5. Run `python manage.py populate_problem_types`

Example:
```python
class MyProblem(BaseProblem):
    slug = 'my_problem'
    name = 'My Problem Type'
    
    def generate(self, difficulty):
        # Generate problem logic
        return {
            'question': 'Question text',
            'canonical_answer': 'Correct answer',
            'params': {'key': 'value'}
        }
    
    def check(self, user_input, canonical_answer, params):
        # Validation logic
        return is_correct, feedback
```

## Deployment

### Production Deployment

1. **Set up server**
   - Install Docker and Docker Compose
   - Configure firewall (ports 80, 443)
   - Set up SSL certificates (recommended)

2. **Deploy application**
   ```bash
   git clone <repository-url>
   cd trainmath-monorepo
   cp env.example .env
   # Edit .env with production values
   ./deploy.sh
   ```

3. **Set up monitoring**
   - Configure log rotation
   - Set up health checks
   - Monitor resource usage

### Backup and Maintenance

**Backup database:**
```bash
./backup.sh
```

**Update application:**
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f web
```

## API Documentation

### Problem Generation
- **Endpoint**: `/start/<problem_type>/`
- **Method**: GET
- **Parameters**: `difficulty` (1-3)
- **Response**: Redirects to question page

### Answer Submission
- **Endpoint**: `/submit/<problem_id>/`
- **Method**: POST
- **Parameters**: `answer` (string)
- **Response**: Redirects to result page

### Statistics
- **Endpoint**: `/exercises/stats/`
- **Method**: GET
- **Authentication**: Required
- **Response**: User statistics by problem type and difficulty

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test cases for usage examples
