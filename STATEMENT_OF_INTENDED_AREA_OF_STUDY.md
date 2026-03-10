# Intended Area of Study

Full stack web development with a focus on building an **automated job board platform for language and localization professionals** using:

- Python
- Flask
- SQLAlchemy
- Web scraping
- API integration technologies

---

# Complete List of Resources

## Programming Language

- Python 3.x

## Backend Framework

- Flask

## Flask Extensions

- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-Login or JWT (authentication)
- Flask-WTF (forms and validation)
- Flask-CORS (for API communication)

## Database

- PostgreSQL (planned for production)
- SQLite (development environment)

## Web Scraping Tools

- BeautifulSoup4
- Requests
- Selenium (optional for dynamic websites)

## External Job APIs

Potential job sources may include:

- Indeed
- LinkedIn
- Localization-specific job platforms

## Development Tools

- Git
- GitHub (repository + Kanban project board)
- Visual Studio Code
- PowerShell terminal

## Learning Resources

- Flask Documentation
- SQLAlchemy Documentation
- BeautifulSoup Documentation
- Job API Documentation
- MDN Web Docs
- W3Schools

---

# Description of Intended Final Product

The final project will be a **full stack automated job board platform** designed for language and localization professionals.

The platform will aggregate job postings from multiple sources including:

- Scraped job websites
- External job APIs
- Direct recruiter job postings

The goal is to provide a centralized platform where language professionals can easily find job opportunities and recruiters can publish relevant positions.

---

# Key Features

## Job Aggregation

- Automated job scraping
- Job ingestion from external APIs
- Duplicate job detection and prevention

## User Features

- User registration and login
- User profiles
- Saved jobs functionality

## Recruiter Features

- Recruiter registration
- Job posting
- Editing and managing job listings

## Job Search

- Keyword search
- Location filtering
- Remote job filtering
- Job category filtering
- Date posted filtering

## User Interface

- Beginner-friendly interface
- Accessible for both job seekers and recruiters

---

# Backend Architecture (Flask)

The backend will follow a modular Flask architecture designed for scalability and maintainability.

## Architectural Approach

- Modular Flask application using Blueprints
- SQLAlchemy ORM models
- Flask-Migrate for database migrations
- REST API endpoints for job listings and recruiter actions
- Services layer for scraping and external API integrations

---

# Week 1 Study Plan

### Research and Planning

- Conduct research on job board platforms and their workflows
- Finalize project scope and feature set
- Choose the technology stack:
    - Python
    - Flask
    - SQLAlchemy
    - BeautifulSoup

### Architecture and Planning

- Create high-level project outline
- Define system architecture
- Create GitHub repository
- Set up GitHub Kanban project board

### Development Environment Setup

- Create Python virtual environment
- Install core backend dependencies
- Create Flask project structure
- Configure environment variables
- Set up SQLite database for development

---

# Week 2 Study Plan

### Backend Foundation

Build foundational backend components using Flask Blueprints.

Planned modules:

- Users
- Authentication
- Jobs
- Recruiters

### Development Tasks

- Create initial database models:
    - Job
    - User
    - Recruiter
    - Saved Jobs
- Configure database migrations using Flask-Migrate
- Implement a basic scraping prototype for one website
- Store scraped jobs in the database

---

# Week 3 Study Plan

### Data Ingestion Expansion

- Expand scraping module to support multiple job sources
- Integrate external job APIs
- Normalize API job data for storage

### Authentication

- Implement user registration
- Implement login
- Implement logout

### Frontend Preparation

- Build API endpoints to support a future frontend interface

---

# Week 4 Study Plan

### Recruiter Portal

- Post job listings
- Edit job listings
- Delete job listings

### User Features

- User profile functionality
- Saved jobs functionality

### Job Search Improvements

Add filtering options:

- Keyword
- Location
- Job type
- Remote jobs
- Job source
- Date posted

### System Testing

Test the full workflow:

- Job scraping
- API ingestion
- Recruiter job posting

---

# Week 5 Study Plan

### Optimization

- Improve scraping reliability
- Prevent duplicate job entries
- Implement logging and error handling

### Deployment Preparation

- Prepare deployment configuration
- Optional Docker setup
- Production environment configuration

### Documentation

- Project README
- User guide
- API documentation

## Architectural Approach

- Modular Flask application using Blueprints
- SQLAlchemy ORM models
- Flask-Migrate for database migrations
- REST API endpoints for job listings and recruiter actions
- Services layer for scraping and external API integrations

---

# Week 1 Study Plan

### Research and Planning

- Conduct research on job board platforms and their workflows
- Finalize project scope and feature set
- Choose the technology stack:
    - Python
    - Flask
    - SQLAlchemy
    - BeautifulSoup

### Architecture and Planning

- Create high-level project outline
- Define system architecture
- Create GitHub repository
- Set up GitHub Kanban project board

### Development Environment Setup

- Create Python virtual environment
- Install core backend dependencies
- Create Flask project structure
- Configure environment variables
- Set up SQLite database for development

---

# Week 2 Study Plan

### Backend Foundation

Build foundational backend components using Flask Blueprints.

Planned modules:

- Users
- Authentication
- Jobs
- Recruiters

### Development Tasks

- Create initial database models:
    - Job
    - User
    - Recruiter
    - Saved Jobs
- Configure database migrations using Flask-Migrate
- Implement a basic scraping prototype for one website
- Store scraped jobs in the database

---

# Week 3 Study Plan

### Data Ingestion Expansion

- Expand scraping module to support multiple job sources
- Integrate external job APIs
- Normalize API job data for storage

### Authentication

- Implement user registration
- Implement login
- Implement logout

### Frontend Preparation

- Build API endpoints to support a future frontend interface

---

# Week 4 Study Plan

### Recruiter Portal

- Post job listings
- Edit job listings
- Delete job listings

### User Features

- User profile functionality
- Saved jobs functionality

### Job Search Improvements

Add filtering options:

- Keyword
- Location
- Job type
- Remote jobs
- Job source
- Date posted

### System Testing

Test the full workflow:

- Job scraping
- API ingestion
- Recruiter job posting

---

# Week 5 Study Plan

### Optimization

- Improve scraping reliability
- Prevent duplicate job entries
- Implement logging and error handling

### Deployment Preparation

- Prepare deployment configuration
- Optional Docker setup
- Production environment configuration

### Documentation

- Project README
- User guide
- API documentation

### Final Presentation

- Prepare final project presentation
- Demonstrate system architecture and key features

---
