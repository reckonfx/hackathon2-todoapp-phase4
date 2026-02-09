/**
 * Floating chat bubble widget that appears on all pages.
 * Opens a chat popup window instead of navigating to a new page.
 * Spec Reference: T068
 */

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { ChatContainer } from './ChatContainer';
import apiService from '../../services/api';

interface ChatBubbleWidgetProps {
  userId?: string;
}

export const ChatBubbleWidget: React.FC<ChatBubbleWidgetProps> = ({ userId: propUserId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [userId, setUserId] = useState<string | null>(propUserId || null);
  const router = useRouter();

  // Wait for client-side mount to avoid SSR issues
  useEffect(() => {
    setMounted(true);
  }, []);

  // Get user ID when authenticated - re-fetch on route changes
  useEffect(() => {
    if (!propUserId && mounted) {
      // Only attempt to fetch if there's an auth token
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setUserId(null);
        return;
      }

      // Try to get user info from API service
      const fetchUser = async () => {
        try {
          const response = await apiService.getCurrentUser();
          console.log('ChatBubbleWidget: API response:', response);
          if (response.success && response.user) {
            console.log('ChatBubbleWidget: got user ID:', response.user.id);
            setUserId(response.user.id);
          } else {
            setUserId(null);
          }
        } catch (err) {
          console.error('ChatBubbleWidget: Failed to fetch user:', err);
          setUserId(null);
        }
      };
      fetchUser();
    }
  }, [propUserId, mounted, router.pathname]);

  // Don't render until mounted (avoid SSR hydration issues)
  if (!mounted) {
    return null;
  }

  // Don't show on auth pages or the chat page itself
  if (router.pathname === '/chat' || router.pathname === '/login' || router.pathname === '/register') {
    return null;
  }

  return (
    <>
      {/* Chat Popup Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '100px',
            right: '24px',
            width: 'min(380px, calc(100vw - 32px))',
            height: 'min(520px, calc(100vh - 120px))',
            zIndex: 99998,
            borderRadius: '16px',
            overflow: 'hidden',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)',
            border: '1px solid var(--accent-light)',
            backgroundColor: '#fff'
          }}
        >
          {/* Close button */}
          <button
            onClick={() => setIsOpen(false)}
            style={{
              position: 'absolute',
              top: '8px',
              right: '8px',
              zIndex: 10,
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              backgroundColor: 'rgba(255,255,255,0.9)',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '18px',
              color: '#666'
            }}
            aria-label="Close chat"
          >
            ×
          </button>
          {userId ? (
            <ChatContainer userId={userId} />
          ) : (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              padding: '20px',
              textAlign: 'center',
              color: '#666'
            }}>
              <p>Please log in to use the chat assistant.</p>
            </div>
          )}
        </div>
      )}

      {/* Floating Bubble Button */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          zIndex: 99999,
          width: '60px',
          height: '60px',
          backgroundColor: 'var(--accent-primary)',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 20px var(--accent-shadow)',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          transform: isOpen ? 'rotate(90deg)' : 'rotate(0deg)'
        }}
        aria-label={isOpen ? 'Close chat' : 'Open AI Chat'}
      >
        {isOpen ? (
          <svg
            width="24"
            height="24"
            fill="none"
            stroke="white"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          <svg
            width="28"
            height="28"
            fill="none"
            stroke="white"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        )}
      </div>
    </>
  );
};

export default ChatBubbleWidget;
