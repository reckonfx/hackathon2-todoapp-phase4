/**
 * Chat input component with text and voice input.
 * Spec Reference: T058, T061
 */

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { VoiceInput } from './VoiceInput';
import styles from './chat.module.css';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  maxLength?: number;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  isLoading,
  maxLength = 10000,
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = useCallback(
    (e?: React.FormEvent) => {
      e?.preventDefault();
      const trimmed = message.trim();
      if (trimmed && !isLoading) {
        onSend(trimmed);
        setMessage('');
        // Reset textarea height
        if (textareaRef.current) {
          textareaRef.current.style.height = 'auto';
        }
      }
    },
    [message, isLoading, onSend]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setMessage(value);
    }
  };

  const handleVoiceTranscript = useCallback((transcript: string) => {
    setMessage((prev) => {
      const newValue = prev ? `${prev} ${transcript}` : transcript;
      return newValue.slice(0, maxLength);
    });
    // Focus the textarea after voice input
    textareaRef.current?.focus();
  }, [maxLength]);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [message]);

  const remainingChars = maxLength - message.length;
  const isNearLimit = remainingChars < 200;

  return (
    <form className={styles.inputForm} onSubmit={handleSubmit}>
      <div className={styles.inputContainer}>
        <textarea
          ref={textareaRef}
          className={styles.textInput}
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Type a message or use voice..."
          disabled={isLoading}
          rows={1}
          aria-label="Message input"
        />

        <div className={styles.inputActions}>
          <VoiceInput onTranscript={handleVoiceTranscript} disabled={isLoading} />

          <button
            type="submit"
            className={styles.sendButton}
            disabled={!message.trim() || isLoading}
            aria-label="Send message"
          >
            {isLoading ? (
              <span className={styles.sendingSpinner}>⏳</span>
            ) : (
              <span className={styles.sendIcon}>➤</span>
            )}
          </button>
        </div>
      </div>

      <div className={styles.inputMeta}>
        <span
          className={`${styles.charCount} ${
            isNearLimit ? styles.charCountWarning : ''
          }`}
        >
          {message.length} / {maxLength}
        </span>
        <span className={styles.inputHint}>
          Press Enter to send, Shift+Enter for new line
        </span>
      </div>
    </form>
  );
};

export default ChatInput;
