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
            <div className="w-16 h-16 border-4 border-[#2a2a2a] rounded-full" />
            <div className="w-16 h-16 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin absolute top-0" />
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
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-gradient-gold">
              AI Task Assistant
            </h1>
            <p className="mt-2 text-[#b8b8b8]">
              Manage your tasks using natural language or voice commands
            </p>
          </div>
          <div className="flex gap-3">
            <a
              href="/dashboard"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] text-[#b8b8b8] hover:text-white hover:border-[#d4af37]/50 transition-all duration-300"
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
          <div className="card glass !p-4 !border-[#d4af37]/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#d4af37] to-[#f4c430] flex items-center justify-center text-xl">
                💬
              </div>
              <div>
                <h3 className="font-semibold text-white">Natural Language</h3>
                <p className="text-sm text-[#b8b8b8]">Type your requests naturally</p>
              </div>
            </div>
          </div>
          <div className="card glass !p-4 !border-[#d4af37]/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl">
                🎤
              </div>
              <div>
                <h3 className="font-semibold text-white">Voice Commands</h3>
                <p className="text-sm text-[#b8b8b8]">Speak to manage tasks</p>
              </div>
            </div>
          </div>
          <div className="card glass !p-4 !border-[#d4af37]/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500 to-green-500 flex items-center justify-center text-xl">
                ✅
              </div>
              <div>
                <h3 className="font-semibold text-white">Smart Actions</h3>
                <p className="text-sm text-[#b8b8b8]">AI understands your intent</p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Container */}
        <div className="card glass !p-0 overflow-hidden !border-[#d4af37]/30" style={{ height: 'calc(100vh - 380px)', minHeight: '400px' }}>
          <ChatContainer userId={user.id} />
        </div>

        {/* Quick Tips */}
        <div className="card glass !border-[#2a2a2a] !p-4">
          <h4 className="text-sm font-semibold text-[#d4af37] mb-2">💡 Quick Tips</h4>
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
                className="px-3 py-1 text-xs rounded-full bg-[#1a1a1a] text-[#b8b8b8] border border-[#2a2a2a]"
              >
                "{tip}"
              </span>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ChatPage;
