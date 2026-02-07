/**
 * Chat state hook for the Phase III Chat API.
 * Manages conversation state and API interactions.
 * Spec Reference: T063
 */

import { useState, useCallback, useEffect } from 'react';
import { ChatMessage, ToolCall } from '../types/Chat';
import chatService from '../services/chatService';

interface UseChatOptions {
  userId: string;
  onError?: (error: string) => void;
}

interface UseChatReturn {
  messages: ChatMessage[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
  clearConversation: () => void;
}

export function useChat({ userId, onError }: UseChatOptions): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load stored conversation ID on mount
  useEffect(() => {
    const storedId = chatService.getStoredConversationId();
    if (storedId) {
      setConversationId(storedId);
    }
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      setIsLoading(true);
      setError(null);

      // Add user message immediately for responsive UX
      const userMessage: ChatMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: text.trim(),
        createdAt: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      try {
        const response = await chatService.sendMessage(
          userId,
          text.trim(),
          conversationId
        );

        if (!response.success || !response.data) {
          const errorMsg = response.error || 'Failed to send message';
          setError(errorMsg);
          onError?.(errorMsg);
          // Remove the optimistic user message on error
          setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));

          // If conversation expired, reset the conversation state so user can retry
          if (errorMsg.includes('expired') || errorMsg.includes('conversation')) {
            setConversationId(null);
          }
          return;
        }

        const { data } = response;

        // Update conversation ID if this is a new conversation
        if (!conversationId) {
          setConversationId(data.conversation_id);
          chatService.storeConversationId(data.conversation_id);
        }

        // Update user message with actual ID from server
        setMessages((prev) =>
          prev.map((m) =>
            m.id === userMessage.id
              ? { ...m, id: `user-${data.message_id}` }
              : m
          )
        );

        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: data.message_id,
          role: 'assistant',
          content: data.response,
          toolCalls: data.tool_calls.length > 0 ? data.tool_calls : undefined,
          createdAt: new Date(data.created_at),
        };
        setMessages((prev) => [...prev, assistantMessage]);

        // If any task-modifying tools were called, dispatch event to refresh task list
        const taskModifyingTools = ['add_task', 'complete_task', 'delete_task', 'update_task'];
        const hasTaskChanges = data.tool_calls.some(
          (tc: any) => taskModifyingTools.includes(tc.tool)
        );
        if (hasTaskChanges && typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('tasks-changed'));
        }
      } catch (err: any) {
        const errorMsg = err.message || 'An unexpected error occurred';
        setError(errorMsg);
        onError?.(errorMsg);
        // Remove the optimistic user message on error
        setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
      } finally {
        setIsLoading(false);
      }
    },
    [userId, conversationId, onError]
  );

  const clearConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    chatService.clearConversationId();
  }, []);

  return {
    messages,
    conversationId,
    isLoading,
    error,
    sendMessage,
    clearConversation,
  };
}
