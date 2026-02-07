/**
 * Task type definitions for the Phase-2 Web-Based Todo Application.
 */

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskApiResponse {
  success: boolean;
  task?: Task;
  tasks?: Task[];
  count?: number;
  message?: string;
  error?: string;
}