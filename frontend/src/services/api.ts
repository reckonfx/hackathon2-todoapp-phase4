/**
 * API service for the Phase-2 Web-Based Todo Application.
 * Handles all HTTP requests to the backend API.
 */

import axios, { AxiosInstance } from 'axios';
import { AuthResponse, LoginResponse, RegisterRequest, LoginRequest } from '../types/User';
import { TaskApiResponse, CreateTaskRequest, UpdateTaskRequest, Task } from '../types/Task';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests if available
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle token expiration and refresh if needed
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Clear auth token if unauthorized
          localStorage.removeItem('auth_token');
          // Only redirect if not already on login or register page to avoid redirect loops
          const currentPath = window.location.pathname;
          if (currentPath !== '/login' && currentPath !== '/register') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication methods
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await this.api.post('/api/auth/register', userData);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.error || 'Registration failed',
      } as AuthResponse;
    }
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await this.api.post('/api/auth/login', credentials);
      const { token } = response.data;

      if (token) {
        localStorage.setItem('auth_token', token);
      }

      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.error || 'Login failed',
      } as any;
    }
  }

  async logout(): Promise<AuthResponse> {
    try {
      const response = await this.api.post('/api/auth/logout');
      localStorage.removeItem('auth_token');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Logout failed',
      };
    }
  }

  async getCurrentUser(): Promise<AuthResponse> {
    try {
      const response = await this.api.get('/api/auth/me');
      // The backend now returns { success: true, user: ... }
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.error || 'Failed to get user',
      };
    }
  }

  // Task methods
  async getAllTasks(): Promise<TaskApiResponse> {
    try {
      const response = await this.api.get('/api/tasks');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get tasks',
      };
    }
  }

  async createTask(taskData: CreateTaskRequest): Promise<TaskApiResponse> {
    try {
      const response = await this.api.post('/api/tasks', taskData);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to create task',
      };
    }
  }

  async getTaskById(taskId: string): Promise<TaskApiResponse> {
    try {
      const response = await this.api.get(`/api/tasks/${taskId}`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get task',
      };
    }
  }

  async updateTask(taskId: string, taskData: UpdateTaskRequest): Promise<TaskApiResponse> {
    try {
      const response = await this.api.put(`/api/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to update task',
      };
    }
  }

  async deleteTask(taskId: string): Promise<TaskApiResponse> {
    try {
      const response = await this.api.delete(`/api/tasks/${taskId}`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to delete task',
      };
    }
  }

  async toggleTaskCompletion(taskId: string): Promise<TaskApiResponse> {
    try {
      const response = await this.api.patch(`/api/tasks/${taskId}/toggle`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to toggle task completion',
      };
    }
  }
}

export default new ApiService();