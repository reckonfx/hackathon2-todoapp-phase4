/**
 * Chat types for the Phase III Chat API.
 * Corresponds to contracts/chat-api.yaml schemas.
 */

export interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCall[];
  createdAt: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  response: string;
  tool_calls: ToolCall[];
  created_at: string;
}

export interface ChatApiResponse {
  success: boolean;
  data?: ChatResponse;
  error?: string;
}

export interface ConversationState {
  conversationId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}
