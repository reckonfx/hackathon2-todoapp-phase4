/**
 * Chat bubble component for displaying messages.
 * Spec Reference: T056
 */

import React, { useState } from 'react';
import { ChatMessage, ToolCall } from '../../types/Chat';
import styles from './chat.module.css';

interface ChatBubbleProps {
  message: ChatMessage;
}

const ToolCallBadge: React.FC<{ toolCall: ToolCall }> = ({ toolCall }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getToolIcon = (tool: string) => {
    switch (tool) {
      case 'add_task':
        return '➕';
      case 'list_tasks':
        return '📋';
      case 'complete_task':
        return '✅';
      case 'delete_task':
        return '🗑️';
      case 'update_task':
        return '✏️';
      default:
        return '🔧';
    }
  };

  const getToolLabel = (tool: string) => {
    return tool.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  };

  return (
    <div className={styles.toolCallBadge}>
      <button
        className={styles.toolCallHeader}
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
      >
        <span className={styles.toolIcon}>{getToolIcon(toolCall.tool)}</span>
        <span className={styles.toolName}>{getToolLabel(toolCall.tool)}</span>
        <span className={styles.expandIcon}>{isExpanded ? '▼' : '▶'}</span>
      </button>
      {isExpanded && (
        <div className={styles.toolCallDetails}>
          <div className={styles.toolCallSection}>
            <strong>Parameters:</strong>
            <pre>{JSON.stringify(toolCall.parameters, null, 2)}</pre>
          </div>
          <div className={styles.toolCallSection}>
            <strong>Result:</strong>
            <pre>{JSON.stringify(toolCall.result, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const formatTime = (date: Date) => {
    return new Date(date).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={`${styles.bubbleContainer} ${
        isUser ? styles.userBubbleContainer : styles.assistantBubbleContainer
      }`}
    >
      <div
        className={`${styles.bubble} ${
          isUser ? styles.userBubble : styles.assistantBubble
        }`}
      >
        <div className={styles.messageContent}>{message.content}</div>
        {message.toolCalls && message.toolCalls.length > 0 && (
          <div className={styles.toolCalls}>
            {message.toolCalls.map((tc, index) => (
              <ToolCallBadge key={`${tc.tool}-${index}`} toolCall={tc} />
            ))}
          </div>
        )}
        <div className={styles.timestamp}>{formatTime(message.createdAt)}</div>
      </div>
    </div>
  );
};

export default ChatBubble;
