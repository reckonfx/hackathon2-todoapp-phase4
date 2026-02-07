/**
 * Main layout component for the Phase-2 Web-Based Todo Application.
 * Provides consistent structure and navigation for the app.
 */

import React, { ReactNode, useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import apiService from '../../services/api';
import { User } from '../../types/User';
import { useTheme } from '../../context/ThemeContext';
import { ChatBubbleWidget } from '../chat';

interface MainLayoutProps {
  children: ReactNode;
  title?: string;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, title = 'Todo App' }) => {
  const [user, setUser] = useState<User | null>(null);
  const { theme, toggleTheme } = useTheme();
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const response = await apiService.getCurrentUser();
        if (response.success && response.user) {
          setUser(response.user);
        } else if (response.error && (router.pathname !== '/login' && router.pathname !== '/register')) {
          localStorage.removeItem('auth_token');
          router.push('/login');
        }
      }
    };
    fetchUser();
  }, []);

  const handleLogout = async () => {
    try {
      await apiService.logout();
      setUser(null);
      window.location.href = '/login';
    } catch (err) {
      console.error('Logout error:', err);
      // Fallback
      localStorage.removeItem('auth_token');
      setUser(null);
      window.location.href = '/login';
    }
  };

  return (
    <>
      <Head>
        <title>{`${title} | Todo Premium`}</title>
        <meta name="description" content="A modern, high-performance todo application." />
      </Head>

      <div className="min-h-screen bg-primary">
        <header className="sticky top-0 z-50 glass border-b border-primary shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-24">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
                  <svg className="w-6 h-6 flex-shrink-0 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '24px', maxHeight: '24px' }}>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600">
                  Todo
                </h1>
              </div>

              <nav className="hidden md:flex items-center space-x-8">
                <Link href="/" className="text-secondary hover:text-indigo-600 font-medium transition-colors duration-200">Home</Link>
                <Link href="/dashboard" className="text-secondary hover:text-indigo-600 font-medium transition-colors duration-200">Tasks</Link>
                <Link href="/chat" className="text-secondary hover:text-indigo-600 font-medium transition-colors duration-200 flex items-center gap-1.5">
                  <span>🤖</span>
                  <span>AI Chat</span>
                </Link>
              </nav>

              <div className="flex items-center gap-4">
                <button
                  onClick={toggleTheme}
                  className="p-2.5 rounded-xl hover:bg-tertiary transition-all duration-200"
                  aria-label="Toggle theme"
                >
                  {theme === 'light' ? (
                    <svg className="w-6 h-6 flex-shrink-0 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '24px', maxHeight: '24px' }}>
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '24px', maxHeight: '24px' }}>
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M16.243 17.657l.707.707M6.343 6.343l.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z" />
                    </svg>
                  )}
                </button>

                <div className="h-8 w-[1px] bg-slate-200 dark:bg-slate-700 mx-2" />

                {user ? (
                  <div className="flex items-center gap-4">
                    <div className="hidden sm:flex flex-col items-end bg-slate-50 dark:bg-slate-800/50 px-3 py-1.5 rounded-lg">
                      <span className="text-sm font-semibold">{user.name || 'User'}</span>
                      <span className="text-xs text-secondary">{user.email}</span>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="px-5 py-2.5 bg-slate-100 dark:bg-slate-800 text-sm font-semibold rounded-xl hover:bg-slate-200 dark:hover:bg-slate-700 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5"
                    >
                      Sign Out
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-3">
                    <Link href="/login" className="px-5 py-2.5 text-sm font-semibold hover:text-indigo-600 transition-colors duration-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">Sign In</Link>
                    <Link href="/register" className="btn-primary py-2.5 px-6 text-sm shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all duration-300">Join Free</Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          {children}
        </main>

        <footer className="border-t border-primary mt-20 py-12">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-secondary text-sm">
              &copy; {new Date().getFullYear()} Todo Premium. Designed for modern productivity.
            </p>
          </div>
        </footer>
      </div>

      {/* Floating Chat Bubble Widget */}
      <ChatBubbleWidget />

      <style jsx global>{`
        .bg-primary { background-color: var(--bg-primary); }
        .text-secondary { color: var(--text-secondary); }
        .bg-tertiary { background-color: var(--bg-tertiary); }
        .border-primary { border-color: var(--border-color); }
      `}</style>
    </>
  );
};

export default MainLayout;