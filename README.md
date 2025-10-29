# Modern Python Project Setup Guide

A comprehensive guide for creating production-ready Python projects using modern tooling and best practices.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure Overview](#project-structure-overview)
- [Step-by-Step Project Creation](#step-by-step-project-creation)
- [Dependency Decisions Explained](#dependency-decisions-explained)
- [Development Dependencies Explained](#development-dependencies-explained)
- [Tool Configurations Explained](#tool-configurations-explained)
- [Project Templates by Use Case](#project-templates-by-use-case)
- [Common Commands](#common-commands)
- [Best Practices](#best-practices)

## Prerequisites

Before starting, make sure you have:

- **Python 3.12+** - [Download from python.org](https://www.python.org/downloads/)
- **uv** - Modern Python package manager ([Installation guide](https://github.com/astral-sh/uv#installation))

```bash
# Verify installations
python --version    # Should be 3.12+
uv --version        # Should be installed
```

### Why uv over pip/poetry?
- **10-100x faster** than pip for dependency resolution and installation
- **Drop-in replacement** for pip with better UX
- **Built-in virtual environment management**
- **Lock files** for reproducible builds
- **Modern dependency groups** support

## Project Structure Overview

Our standard project structure follows modern Python best practices:

```
my-project/
├── src/                    # Source code (src layout)
│   └── my_project/        # Main package
│       ├── __init__.py
│       ├── main.py        # Entry point
│       └── config.py      # Configuration
├── tests/                 # Test files
├── docs/                  # Documentation  
├── pyproject.toml         # Project configuration
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── .python-version       # Python version pinning
```

### Why src/ layout?
- **Prevents import issues** during development
- **Forces proper package installation** 
- **Industry standard** for Python packages
- **Better testing isolation**

## Step-by-Step Project Creation

### 1. Create Project Directory Structure

```bash
# Create and navigate to your projects directory
mkdir -p ~/projects
cd ~/projects

# Create a new project
PROJECT_NAME="my-awesome-project"
mkdir $PROJECT_NAME
cd $PROJECT_NAME

# Create directory structure
mkdir -p src/${PROJECT_NAME//-/_}  # Convert hyphens to underscores for Python
mkdir -p tests docs .github/workflows
```

### 2. Initialize with uv

```bash
# Initialize the project with uv
uv init --name $PROJECT_NAME

# Set Python version (optional but recommended)
echo "3.13" > .python-version
```

### 3. Create pyproject.toml

Create the foundation configuration file:

```toml
[project]
name = "my-awesome-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
requires-python = ">=3.12"
dependencies = [
    # Core dependencies will be added based on project type
]

[build-system]
requires = ["hatchling"]  # or "uv_build>=0.8.3" for ultra-fast builds
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    # Development dependencies will be added
]
```

### 4. Add Dependencies Based on Project Type

Choose your dependencies based on your project's purpose:

#### For General Python Projects
```bash
# Core observability and validation
uv add "logfire>=4.14.2" "loguru>=0.7.3" "pydantic>=2.12.3"
```

#### For Web APIs
```bash
# API framework + observability
uv add "fastapi>=0.104.0" "uvicorn[standard]>=0.24.0" 
uv add "logfire[fastapi]>=4.14.2" "pydantic>=2.12.3"
```

#### For Data Processing/Migration
```bash
# Data manipulation + validation + observability  
uv add "pandas>=2.1.0" "sqlalchemy>=2.0.0" "pydantic>=2.12.3"
uv add "logfire>=4.14.2" "loguru>=0.7.3"
```

#### For CLI Applications
```bash
# CLI framework + rich output + observability
uv add "click>=8.1.0" "rich>=13.0.0" 
uv add "loguru>=0.7.3" "pydantic>=2.12.3"
```

### 5. Add Development Dependencies

```bash
# Code quality and testing tools
uv add --group dev "black>=24.0.0" "ruff>=0.1.0" "mypy>=1.8.0"
uv add --group dev "pytest>=8.0.0" "pytest-cov>=4.0.0"
```

### 6. Configure Tools in pyproject.toml

Add tool configurations to your `pyproject.toml`:

```toml
# Tool configurations
[tool.black]
line-length = 88
target-version = ['py312']

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "C90", "I", "N", "UP", "B", "A", "C4"]

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

### 7. Create Initial Source Files

```bash
# Create package __init__.py
cat > src/${PROJECT_NAME//-/_}/__init__.py << 'EOF'
"""Package for my-awesome-project."""

__version__ = "0.1.0"
EOF

# Create main.py (template varies by project type - see templates below)
```

### 8. Install Dependencies

```bash
# Install all dependencies including dev dependencies
uv sync --group dev

# Verify installation
uv run python -c "import sys; print(sys.executable)"
```

## Dependency Decisions Explained

### Core Dependencies

#### logfire[flask] >= 4.14.2
**Purpose:** Modern observability and automatic instrumentation
**Why chosen:**
- **Automatic Pydantic instrumentation** - logs all validation automatically
- **Production-ready observability** with minimal configuration  
- **Better than traditional logging** - structured, searchable, traceable
- **Flask extra** provides web framework integration

**When to use:** All projects that need observability (which is most projects)
**Alternatives:** OpenTelemetry (more complex), structlog (manual setup)

```python
# What you get automatically:
import logfire
logfire.configure()

user = User(name="Alice", email="alice@example.com") 
# ^ Validation automatically logged with full context
```

#### loguru >= 0.7.3  
**Purpose:** Developer-friendly logging with great defaults
**Why chosen:**
- **Zero configuration** - works beautifully out of the box
- **Automatic log rotation** and cleanup
- **Colored console output** for development
- **Thread-safe** by default
- **Complements Logfire** - Logfire for production observability, Loguru for development

**When to use:** All projects (pairs perfectly with Logfire)
**Alternatives:** Standard logging (more verbose), structlog (more complex)

```python
# Beautiful, simple logging:
from loguru import logger
logger.info("User created", user_id=123, email="user@example.com")
```

#### pydantic >= 2.12.3
**Purpose:** Data validation, settings management, and API schemas  
**Why chosen:**
- **Runtime type checking** - catches data errors early
- **Automatic API documentation** when used with FastAPI
- **Perfect integration with Logfire** - validation automatically logged
- **Performance** - Pydantic v2 is built on Rust (much faster than v1)
- **Industry standard** for modern Python applications

**When to use:** Almost all projects that handle external data
**Alternatives:** dataclasses (no validation), attrs (less features)

```python
# Type-safe data handling:
class User(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')

user = User(name="Alice", email="alice@example.com")  # Validated!
```

### Project-Type Specific Dependencies

#### FastAPI + Uvicorn (Web APIs)
```bash
uv add "fastapi>=0.104.0" "uvicorn[standard]>=0.24.0"
```
**Why FastAPI:**
- **Automatic API documentation** (OpenAPI/Swagger)
- **Built-in Pydantic integration** 
- **Async support** by default
- **High performance** - one of the fastest Python web frameworks
- **Type hints everywhere** - excellent developer experience

**Why Uvicorn:**
- **ASGI server** for async applications
- **Production-ready** performance
- **Hot reload** for development

#### Pandas + SQLAlchemy (Data Processing)
```bash
uv add "pandas>=2.1.0" "sqlalchemy>=2.0.0"
```
**Why Pandas:**
- **Industry standard** for data manipulation
- **Excellent performance** for data operations
- **Rich ecosystem** of data science tools

**Why SQLAlchemy:**
- **Database abstraction** - works with any SQL database
- **ORM and Core** - flexible usage patterns
- **Async support** in SQLAlchemy 2.0
- **Type hints** support

## Development Dependencies Explained

### Code Quality Tools

#### black >= 24.0.0
**Purpose:** Code formatting (opinionated, consistent)
**Why chosen:**
- **Zero configuration** - one way to format code
- **Eliminates bikeshedding** - no more formatting debates
- **Fast** - formats entire codebases in seconds
- **Industry adoption** - used by major Python projects

```bash
uv run black src/  # Format all code consistently
```

#### ruff >= 0.1.0  
**Purpose:** Lightning-fast linting (replaces flake8, pylint, isort)
**Why chosen:**
- **10-100x faster** than traditional linters
- **Replaces multiple tools** - linting, import sorting, more
- **Rust-based** - exceptional performance
- **Growing rapidly** - modern choice for new projects

```bash
uv run ruff check src/     # Lightning-fast linting
uv run ruff format src/    # Can replace Black (optional)
```

#### mypy >= 1.8.0
**Purpose:** Static type checking
**Why chosen:**
- **Catches bugs** before runtime
- **Better IDE support** - autocomplete, refactoring
- **Gradual typing** - can adopt incrementally  
- **Industry standard** for Python type checking

```bash
uv run mypy src/  # Check types
```

### Testing Tools

#### pytest >= 8.0.0 + pytest-cov >= 4.0.0
**Purpose:** Testing framework with coverage reporting
**Why chosen:**
- **Simple syntax** - easy to write and read tests
- **Powerful fixtures** - excellent test organization
- **Plugin ecosystem** - extends functionality easily
- **Coverage integration** - see what code is tested

```bash
uv run pytest                    # Run tests
uv run pytest --cov=src         # Run with coverage
```

## Tool Configurations Explained

### Black Configuration
```toml
[tool.black]
line-length = 88          # Slightly longer than PEP 8's 79 for readability
target-version = ['py312'] # Format code for Python 3.12+
```

### Ruff Configuration  
```toml
[tool.ruff]
line-length = 88          # Match Black's line length
target-version = "py312"  # Target Python 3.12+

[tool.ruff.lint]
select = ["E", "F", "W", "C90", "I", "N", "UP", "B", "A", "C4"]
# E: pycodestyle errors
# F: pyflakes  
# W: pycodestyle warnings
# C90: mccabe complexity
# I: isort (import sorting)
# N: pep8-naming
# UP: pyupgrade (modern Python syntax)
# B: flake8-bugbear (bug detection)
# A: flake8-builtins (builtin shadowing)
# C4: flake8-comprehensions (better comprehensions)
```

### MyPy Configuration
```toml
[tool.mypy]
python_version = "3.12"   # Target Python version
strict = true             # Enable all strict checks
```
**Strict mode enables:**
- `--warn-unused-configs` - warn about unused config
- `--disallow-any-generics` - require type parameters
- `--disallow-subclassing-any` - prevent Any subclassing
- `--disallow-untyped-calls` - require typed function calls
- `--disallow-untyped-defs` - require function type annotations
- And more...

## Project Templates by Use Case

### 1. Web API Service

```bash
# Create project
mkdir my-api-service && cd my-api-service
uv init --name my-api-service

# Add dependencies  
uv add "fastapi>=0.104.0" "uvicorn[standard]>=0.24.0"
uv add "logfire[fastapi]>=4.14.2" "pydantic>=2.12.3" 
uv add --group dev "black>=24.0.0" "ruff>=0.1.0" "mypy>=1.8.0" "pytest>=8.0.0"
```

**Main.py template:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
import logfire

# Configure observability
logfire.configure()
app = FastAPI()
logfire.instrument_fastapi(app)

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: User):
    # Validation automatically logged by Logfire
    return {"message": f"Created user {user.name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Data Processing Project

```bash
# Create project
mkdir data-pipeline && cd data-pipeline  
uv init --name data-pipeline

# Add dependencies
uv add "pandas>=2.1.0" "sqlalchemy>=2.0.0" "pydantic>=2.12.3"
uv add "logfire>=4.14.2" "loguru>=0.7.3"
uv add --group dev "black>=24.0.0" "ruff>=0.1.0" "mypy>=1.8.0" "pytest>=8.0.0"
```

**Main.py template:**
```python
import pandas as pd
from pydantic import BaseModel, Field
from loguru import logger
import logfire

logfire.configure()

class DataRecord(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)  
    value: float

def process_data(input_file: str) -> pd.DataFrame:
    logger.info("Loading data", file=input_file)
    
    df = pd.read_csv(input_file)
    
    # Validate each record with automatic logging
    valid_records = []
    for _, row in df.iterrows():
        try:
            record = DataRecord(**row.to_dict())
            valid_records.append(record.model_dump())
        except Exception as e:
            logger.error("Invalid record", row=row.to_dict(), error=str(e))
    
    result_df = pd.DataFrame(valid_records)
    logger.success("Processing completed", records=len(result_df))
    return result_df
```

### 3. CLI Application  

```bash
# Create project
mkdir my-cli-tool && cd my-cli-tool
uv init --name my-cli-tool

# Add dependencies
uv add "click>=8.1.0" "rich>=13.0.0" "pydantic>=2.12.3"
uv add "loguru>=0.7.3" 
uv add --group dev "black>=24.0.0" "ruff>=0.1.0" "mypy>=1.8.0" "pytest>=8.0.0"
```

**Main.py template:**
```python
import click
from rich.console import Console
from loguru import logger

console = Console()

@click.group()
@click.option('--verbose', is_flag=True, help='Verbose output')
def cli(verbose: bool):
    """My awesome CLI tool."""
    if verbose:
        logger.add(console.print, level="DEBUG")

@cli.command()
@click.argument('name')
def hello(name: str):
    """Say hello to someone."""
    logger.info("Greeting user", name=name)
    console.print(f"[bold green]Hello {name}![/bold green]")

if __name__ == "__main__":
    cli()
```

## Common Commands

### Project Setup Commands
```bash
# Create new project
mkdir my-project && cd my-project
uv init --name my-project

# Install dependencies
uv add "dependency-name>=version"        # Add runtime dependency
uv add --group dev "dev-dependency"      # Add development dependency  
uv sync --group dev                      # Install all dependencies

# Update dependencies
uv lock                                  # Update lock file
uv sync                                  # Sync with lock file
```

### Development Commands
```bash
# Code quality (run these frequently)
uv run ruff check src/                   # Fast linting
uv run black src/                        # Code formatting  
uv run mypy src/                         # Type checking
uv run pytest                           # Run tests

# Run application
uv run python -m my_project              # Run as module
uv run my-project                        # Run via script (if configured)

# Dependency management
uv tree                                  # Show dependency tree
uv pip list                              # List installed packages
```

### Production Commands
```bash
# Build for distribution
uv build                                 # Create wheel and sdist

# Install in production
uv pip install dist/my-project-0.1.0.tar.gz

# Lock dependencies for reproducible builds  
uv lock --upgrade                        # Update lock file
```

## Best Practices

### 1. Dependency Management
- **Pin major versions** in pyproject.toml (`>=1.0.0,<2.0.0`)
- **Use lock files** for reproducible builds (`uv.lock`)
- **Separate dev dependencies** using dependency groups
- **Regular updates** - run `uv lock --upgrade` periodically

### 2. Code Quality
- **Run quality checks** before every commit:
  ```bash
  uv run ruff check src/ && uv run black src/ && uv run mypy src/ && uv run pytest
  ```
- **Use pre-commit hooks** to automate quality checks
- **Type hints everywhere** - leverage mypy's strict mode
- **Test coverage** - aim for >80% coverage

### 3. Project Structure
- **Use src/ layout** for all projects
- **One package per project** - avoid multi-package repositories
- **Clear entry points** - define scripts in pyproject.toml
- **Documentation** - keep README.md updated

### 4. Observability
- **Configure logging early** - set up Logfire/Loguru in main()
- **Structured logging** - use key-value pairs, not string formatting
- **Error handling** - log errors with context before re-raising
- **Performance tracking** - use Logfire spans for important operations

### 5. Testing
- **Test early and often** - write tests as you develop
- **Use fixtures** for common test setup
- **Mock external dependencies** - don't test third-party services
- **Test edge cases** - especially data validation scenarios

---

## Summary

This setup gives you:
- **🚀 Ultra-fast tooling** (uv, Ruff) for great developer experience
- **🔍 Built-in observability** (Logfire + Loguru) for production readiness
- **✅ Type safety** (Pydantic + MyPy) for catching bugs early  
- **🧹 Code quality** (Black + Ruff) for maintainable code
- **📦 Modern packaging** with proper dependency management

The result is a **production-ready Python project template** that scales from simple scripts to complex applications, with excellent developer experience and enterprise-grade observability built in from day one.
