/**
 * Chat page for the Phase III AI Chatbot.
 * Main page for AI-powered task management via natural language.
 * Spec Reference: T068
 */

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import MainLayout from '../components/Layout/MainLayout';
import { ChatContainer } from '../components/chat';
import { User } from '../types/User';
import apiService from '../services/api';

const ChatPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await apiService.getCurrentUser();
      if (response.success && response.user) {
        setUser(response.user);
      } else {
        // Redirect to login if not authenticated
        router.push('/login');
      }
    } catch (err) {
      console.error('Failed to fetch user data:', err);
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <MainLayout title="AI Assistant">
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-primary rounded-full" />
            <div className="w-16 h-16 border-4 border-t-transparent rounded-full animate-spin absolute top-0" style={{ borderColor: 'var(--accent-primary)', borderTopColor: 'transparent' }} />
          </div>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return null; // Will redirect
  }

  return (
    <MainLayout title="AI Assistant">
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight" style={{ background: 'linear-gradient(to right, var(--accent-gradient-from), var(--accent-gradient-to))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              AI Task Assistant
            </h1>
            <p className="mt-2 text-secondary">
              Manage your tasks using natural language or voice commands
            </p>
          </div>
          <div className="flex gap-3">
            <a
              href="/dashboard"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border text-secondary hover:border-opacity-50 transition-all duration-300 focus-ring"
              style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border-color)' }}
              onMouseEnter={e => (e.currentTarget.style.borderColor = 'var(--accent-primary)')}
              onMouseLeave={e => (e.currentTarget.style.borderColor = 'var(--border-color)')}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span className="hidden sm:inline font-medium">View Tasks</span>
            </a>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="card glass !p-4" style={{ borderColor: 'var(--accent-light)' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center text-xl" style={{ background: 'linear-gradient(to bottom right, var(--accent-gradient-from), var(--accent-gradient-to))' }}>
                <span role="img" aria-label="Chat bubble">💬</span>
              </div>
              <div>
                <h3 className="font-semibold" style={{ color: 'var(--text-primary)' }}>Natural Language</h3>
                <p className="text-sm text-secondary">Type your requests naturally</p>
              </div>
            </div>
          </div>
          <div className="card glass !p-4" style={{ borderColor: 'var(--accent-light)' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl">
                <span role="img" aria-label="Microphone">🎤</span>
              </div>
              <div>
                <h3 className="font-semibold" style={{ color: 'var(--text-primary)' }}>Voice Commands</h3>
                <p className="text-sm text-secondary">Speak to manage tasks</p>
              </div>
            </div>
          </div>
          <div className="card glass !p-4" style={{ borderColor: 'var(--accent-light)' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500 to-green-500 flex items-center justify-center text-xl">
                <span role="img" aria-label="Checkmark">✅</span>
              </div>
              <div>
                <h3 className="font-semibold" style={{ color: 'var(--text-primary)' }}>Smart Actions</h3>
                <p className="text-sm text-secondary">AI understands your intent</p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Container */}
        <div className="card glass !p-0 overflow-hidden" style={{ height: 'calc(100vh - 380px)', minHeight: '400px', borderColor: 'var(--accent-shadow)' }}>
          <ChatContainer userId={user.id} />
        </div>

        {/* Quick Tips */}
        <div className="card glass !p-4" style={{ borderColor: 'var(--border-color)' }}>
          <h2 className="text-sm font-semibold mb-2" style={{ color: 'var(--accent-primary)' }}>
            <span role="img" aria-label="Light bulb">💡</span> Quick Tips
          </h2>
          <div className="flex flex-wrap gap-2">
            {[
              'Add buy groceries',
              'Show my tasks',
              'Mark grocery shopping done',
              'Delete the meeting task',
              'What tasks do I have?'
            ].map((tip, i) => (
              <span
                key={i}
                className="px-3 py-1 text-xs rounded-full text-secondary border"
                style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border-color)' }}
              >
                &quot;{tip}&quot;
              </span>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ChatPage;
