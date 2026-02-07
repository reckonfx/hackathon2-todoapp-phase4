# Authentication API Contract

## User Registration

### Endpoint
`POST /api/auth/register`

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

### Response (Success - 201 Created)
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-07T10:00:00Z"
  },
  "message": "User registered successfully"
}
```

### Response (Error - 400 Bad Request)
```json
{
  "success": false,
  "error": "Validation error message"
}
```

### Response (Error - 409 Conflict)
```json
{
  "success": false,
  "error": "User with this email already exists"
}
```

## User Login

### Endpoint
`POST /api/auth/login`

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "jwt-token-string",
  "message": "Login successful"
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Invalid email or password"
}
```

## User Logout

### Endpoint
`POST /api/auth/logout`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## Get Current User

### Endpoint
`GET /api/auth/me`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-07T10:00:00Z"
  }
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```