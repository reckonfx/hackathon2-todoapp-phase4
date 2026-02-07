---
name: project-analysis-debugging
description: Can read a full project, analyze all files, identify errors, and provide fixes to make the project fully functional by detecting issues, suggesting corrections, and providing step-by-step guidance.
---
# Project-Analysis-Debugging-Skill

This skill enables Claude to comprehensively analyze entire projects, identify errors and inconsistencies, and provide actionable fixes to make projects fully functional.

## Purpose

The project-analysis-debugging skill provides Claude with the capability to:
- Read and understand complete project structures, files, and dependencies
- Detect errors, missing configurations, or code inconsistencies
- Suggest corrected code, configuration changes, or implementation instructions
- Provide step-by-step guidance to achieve project functionality
- Ensure compatibility with project requirements and development best practices

## Instructions for Project Analysis and Debugging

### 1. Project Structure Analysis
When analyzing a project:
- Identify the project type (Python, Node.js, Java, etc.) and technology stack
- Map out the directory structure and file organization
- Locate configuration files (package.json, requirements.txt, Dockerfile, etc.)
- Identify entry points and main execution files
- Determine dependencies and their relationships

### 2. Error Detection
When searching for errors:
- Look for missing imports, undefined variables, and syntax errors
- Check for configuration mismatches or missing environment variables
- Identify dependency conflicts or version incompatibilities
- Find inconsistent naming conventions or broken references
- Spot potential security vulnerabilities or performance issues

### 3. Fix Suggestions
When providing fixes:
- Prioritize critical errors that prevent execution
- Suggest the safest, most straightforward solution first
- Provide code replacements with proper context
- Include configuration updates with explanations
- Recommend dependency changes with justification

### 4. Step-by-Step Guidance
When providing implementation steps:
- Start with critical path fixes that enable basic functionality
- Proceed to enhancement fixes that improve performance or security
- Include verification steps to confirm fixes are working
- Provide rollback options if fixes cause new issues
- Document the reasoning behind each recommended change

## Examples

### Example 1: Missing Import Error in Python Project
**Input:**
```
Python project with a main.py file that has "NameError: name 'requests' is not defined" when trying to make HTTP requests.
```

**Expected Output:**
```
## Analysis
- Identified missing 'requests' library import in main.py
- Confirmed 'requests' is not listed in requirements.txt
- Project type: Python application

## Fix Steps
1. Add import statement to main.py:
   ```python
   import requests
   ```

2. Add requests to requirements.txt:
   ```
   requests==2.31.0
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Verification
- Run the application again to confirm the NameError is resolved
- Test the HTTP request functionality to ensure it works as expected
```

### Example 2: Backend/Frontend Integration Issues
**Input:**
```
Full-stack project with React frontend and FastAPI backend. Frontend shows CORS errors when making API calls to localhost:8000.
```

**Expected Output:**
```
## Analysis
- Identified CORS policy violation between React frontend (typically on localhost:3000) and FastAPI backend (localhost:8000)
- Backend lacks proper CORS middleware configuration
- Project type: Full-stack React/FastAPI application

## Fix Steps
1. Install python-multipart in backend requirements.txt (if not already present):
   ```
   python-multipart==0.0.6
   ```

2. Add CORS middleware to FastAPI app in main.py:
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app = FastAPI()

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],  # React dev server
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. For production, update allow_origins to include your domain:
   ```python
   # In production environment
   allow_origins=["https://yourdomain.com"]
   ```

## Verification
- Restart the FastAPI backend server
- Make a test API call from the frontend
- Confirm CORS errors are resolved and API calls succeed
```

### Example 3: Project Structure and Dependency Optimization
**Input:**
```
Python project with disorganized folder structure: all files in root directory, no virtual environment, missing requirements.txt, and no proper package structure.
```

**Expected Output:**
```
## Analysis
- Identified disorganized project structure with files scattered in root
- No virtual environment setup detected
- Missing requirements.txt for dependency management
- No proper package structure or separation of concerns
- Project type: Python application requiring reorganization

## Fix Steps
1. Create proper directory structure:
   ```
   project-name/
   ├── src/
   │   ├── __init__.py
   │   └── main.py
   ├── tests/
   │   └── __init__.py
   ├── requirements.txt
   ├── README.md
   └── .gitignore
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Create requirements.txt with current dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

4. Move source files to src/ directory and update imports accordingly

5. Update main.py entry point to work with new structure

## Verification
- Activate virtual environment and install dependencies: `pip install -r requirements.txt`
- Run the application from the new structure: `python -m src.main`
- Confirm all functionality works as expected with new organization
```

## Guidelines for Using This Skill

### When to Activate
- When asked to analyze an entire project for errors
- When debugging complex multi-file applications
- When reorganizing or refactoring existing projects
- When identifying missing dependencies or configurations
- When optimizing project structure for better maintainability

### Best Practices
- Always identify the project type and technology stack first
- Preserve existing functionality while making improvements
- Provide the safest, most conservative fix when multiple options exist
- Include verification steps for each recommended change
- Consider security implications of any changes suggested
- Maintain backward compatibility where possible

### Response Structure
1. **Analysis**: Identify the project type, structure, and specific issues
2. **Prioritization**: Rank issues by severity and impact
3. **Solutions**: Provide step-by-step fixes starting with the most critical
4. **Verification**: Include steps to confirm fixes are working
5. **Considerations**: Highlight any potential side effects or additional steps

### Quality Checks
- Does the analysis correctly identify the project type?
- Are the suggested fixes safe and appropriate?
- Do the solutions address the root cause of issues?
- Are verification steps included for each fix?
- Is backward compatibility maintained where needed?
- Are security implications considered?

Use this skill whenever comprehensive project analysis and debugging assistance is needed, ensuring safe, effective fixes that maintain project functionality while addressing identified issues.
