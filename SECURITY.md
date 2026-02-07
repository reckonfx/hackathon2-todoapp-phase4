# Security Guidelines

## Environment Variables

This application uses environment variables for configuration. **Important: Never commit sensitive information to version control.**

### Secure Configuration

Sensitive information like database credentials and API keys should be stored in environment variables, not in source code.

### .env File Protection

- The .env file is included in .gitignore to prevent committing sensitive data
- Use .env.example as a template for required environment variables
- Never hardcode credentials in source code

### Recommended Practice

Use environment variables for:
- Database connection strings
- API keys and secrets
- JWT tokens
- Third-party service credentials
