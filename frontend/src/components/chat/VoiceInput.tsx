/**
 * Voice input component using Web Speech API.
 * Spec Reference: T059
 */

import React from 'react';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import styles from './chat.module.css';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  disabled?: boolean;
}

export const VoiceInput: React.FC<VoiceInputProps> = ({
  onTranscript,
  disabled = false,
}) => {
  const {
    isListening,
    interimTranscript,
    isSupported,
    startListening,
    stopListening,
    error,
  } = useSpeechRecognition({
    continuous: false,
    interimResults: true,
    onResult: (transcript) => {
      onTranscript(transcript);
    },
  });

  const handleClick = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  // Show fallback message for unsupported browsers
  if (!isSupported) {
    return (
      <button
        className={`${styles.voiceButton} ${styles.voiceButtonUnsupported}`}
        disabled
        title="Voice input is not supported in this browser. Try Chrome, Edge, or Safari."
      >
        <span className={styles.micIcon}>🎤</span>
        <span className={styles.unsupportedLabel}>Not supported</span>
      </button>
    );
  }

  return (
    <div className={styles.voiceInputContainer}>
      <button
        className={`${styles.voiceButton} ${
          isListening ? styles.voiceButtonListening : ''
        }`}
        onClick={handleClick}
        disabled={disabled}
        title={isListening ? 'Click to stop' : 'Click to speak'}
        aria-label={isListening ? 'Stop recording' : 'Start voice input'}
      >
        <span className={styles.micIcon}>
          {isListening ? '🔴' : '🎤'}
        </span>
        {isListening && (
          <span className={styles.pulseRing}></span>
        )}
      </button>

      {isListening && interimTranscript && (
        <div className={styles.interimTranscript}>
          {interimTranscript}...
        </div>
      )}

      {error && (
        <div className={styles.voiceError} role="alert">
          {error}
        </div>
      )}
    </div>
  );
};

export default VoiceInput;
