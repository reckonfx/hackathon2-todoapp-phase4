/**
 * Chat message list component with auto-scroll.
 * Spec Reference: T057
 */

import React, { useEffect, useRef } from 'react';
import { ChatMessage } from '../../types/Chat';
import { ChatBubble } from './ChatBubble';
import styles from './chat.module.css';

interface ChatMessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export const ChatMessageList: React.FC<ChatMessageListProps> = ({
  messages,
  isLoading,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  return (
    <div className={styles.messageList} ref={containerRef} aria-live="polite">
      {messages.length === 0 && !isLoading && (
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>💬</div>
          <h3>Start a conversation</h3>
          <p>
            Type a message or use voice to manage your tasks.
            <br />
            Try: &quot;Add buy groceries to my list&quot;
          </p>
        </div>
      )}

      {messages.map((message) => (
        <ChatBubble key={message.id} message={message} />
      ))}

      {isLoading && (
        <div className={styles.loadingIndicator}>
          <div className={styles.typingDots}>
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span className={styles.loadingText}>AI is thinking...</span>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};

export default ChatMessageList;
