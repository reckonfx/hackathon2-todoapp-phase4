# Tasks API Contract

## Get All Tasks

### Endpoint
`GET /api/tasks`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-07T10:00:00Z",
      "updated_at": "2026-01-07T10:00:00Z"
    }
  ],
  "count": 1
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```

## Create Task

### Endpoint
`POST /api/tasks`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Request Body
```json
{
  "title": "New task title",
  "description": "Detailed description of the task"
}
```

### Response (Success - 201 Created)
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "New task title",
    "description": "Detailed description of the task",
    "completed": false,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

### Response (Error - 400 Bad Request)
```json
{
  "success": false,
  "error": "Validation error message"
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```

## Get Task by ID

### Endpoint
`GET /api/tasks/{task_id}`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T10:00:00Z"
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

### Response (Error - 404 Not Found)
```json
{
  "success": false,
  "error": "Task not found"
}
```

## Update Task

### Endpoint
`PUT /api/tasks/{task_id}`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Request Body
```json
{
  "title": "Updated task title",
  "description": "Updated description of the task",
  "completed": true
}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated description of the task",
    "completed": true,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T11:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### Response (Error - 400 Bad Request)
```json
{
  "success": false,
  "error": "Validation error message"
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### Response (Error - 404 Not Found)
```json
{
  "success": false,
  "error": "Task not found"
}
```

## Delete Task

### Endpoint
`DELETE /api/tasks/{task_id}`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### Response (Error - 404 Not Found)
```json
{
  "success": false,
  "error": "Task not found"
}
```

## Toggle Task Completion

### Endpoint
`PATCH /api/tasks/{task_id}/toggle`

### Request Headers
```
Authorization: Bearer {jwt-token}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T11:00:00Z"
  },
  "message": "Task completion status updated"
}
```

### Response (Error - 401 Unauthorized)
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### Response (Error - 404 Not Found)
```json
{
  "success": false,
  "error": "Task not found"
}
```