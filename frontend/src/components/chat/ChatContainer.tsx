/**
 * Main chat container component.
 * Orchestrates chat UI, state management, and API communication.
 * Spec Reference: T055
 */

import React, { useCallback } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatMessageList } from './ChatMessageList';
import { ChatInput } from './ChatInput';
import styles from './chat.module.css';

interface ChatContainerProps {
  userId: string;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ userId }) => {
  const {
    messages,
    conversationId,
    isLoading,
    error,
    sendMessage,
    clearConversation,
  } = useChat({
    userId,
    onError: (err) => {
      console.error('Chat error:', err);
    },
  });

  const handleSend = useCallback(
    (text: string) => {
      sendMessage(text);
    },
    [sendMessage]
  );

  const handleNewConversation = useCallback(() => {
    if (window.confirm('Start a new conversation? Current history will be cleared.')) {
      clearConversation();
    }
  }, [clearConversation]);

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <div className={styles.headerContent}>
          <h2 className={styles.headerTitle}>
            <span className={styles.headerIcon}>🤖</span>
            Todo AI Assistant
          </h2>
          <p className={styles.headerSubtitle}>
            Manage your tasks with natural language
          </p>
        </div>
        <div className={styles.headerActions}>
          {conversationId && (
            <button
              className={styles.newConversationButton}
              onClick={handleNewConversation}
              title="Start new conversation"
            >
              ➕ New Chat
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className={styles.errorBanner} role="alert">
          <span className={styles.errorIcon}>⚠️</span>
          {error}
        </div>
      )}

      <ChatMessageList messages={messages} isLoading={isLoading} />

      <div className={styles.inputArea}>
        <ChatInput onSend={handleSend} isLoading={isLoading} maxLength={10000} />
      </div>
    </div>
  );
};

export default ChatContainer;
