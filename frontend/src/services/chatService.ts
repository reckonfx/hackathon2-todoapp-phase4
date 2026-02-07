/**
 * Chat service for the Phase III Chat API.
 * Handles chat API requests to the backend.
 * Spec Reference: T062
 */

import axios, { AxiosInstance } from 'axios';
import { ChatRequest, ChatResponse, ChatApiResponse } from '../types/Chat';

class ChatService {
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
  }

  /**
   * Send a chat message to the API.
   *
   * @param userId - The authenticated user's ID
   * @param message - The message to send
   * @param conversationId - Optional conversation ID to continue
   * @returns ChatApiResponse with the assistant's response
   */
  async sendMessage(
    userId: string,
    message: string,
    conversationId?: string | null
  ): Promise<ChatApiResponse> {
    // Validate userId before making request
    if (!userId || userId === 'undefined' || userId === 'null') {
      console.error('Chat API error: Invalid userId:', userId);
      return {
        success: false,
        error: 'User not authenticated. Please log in again.',
      };
    }

    try {
      const request: ChatRequest = {
        message,
        ...(conversationId && { conversation_id: conversationId }),
      };

      const response = await this.api.post<ChatResponse>(
        `/api/${userId}/chat`,
        request
      );

      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      console.error('Chat API error:', error);

      // Handle different error types
      if (error.response?.status === 401) {
        return {
          success: false,
          error: 'Please log in to continue',
        };
      }

      if (error.response?.status === 404) {
        // If we had a conversation_id and got 404, it might be stale
        // Clear it so next attempt starts fresh
        if (conversationId) {
          console.warn('Conversation not found, clearing stale conversation_id');
          this.clearConversationId();
          return {
            success: false,
            error: 'Previous conversation expired. Please try again to start a new chat.',
          };
        }
        return {
          success: false,
          error: 'Chat service unavailable. Please try again.',
        };
      }

      return {
        success: false,
        error:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          'Failed to send message',
      };
    }
  }

  /**
   * Get the stored conversation ID from localStorage.
   */
  getStoredConversationId(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('chat_conversation_id');
  }

  /**
   * Store the conversation ID in localStorage for session continuity.
   */
  storeConversationId(conversationId: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('chat_conversation_id', conversationId);
  }

  /**
   * Clear the stored conversation ID to start a new conversation.
   */
  clearConversationId(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('chat_conversation_id');
  }
}

export default new ChatService();
