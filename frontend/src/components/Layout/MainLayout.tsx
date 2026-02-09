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
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
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

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [router.pathname]);

  const handleLogout = async () => {
    try {
      await apiService.logout();
      setUser(null);
      window.location.href = '/login';
    } catch (err) {
      console.error('Logout error:', err);
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
            <div className="flex justify-between items-center h-16 sm:h-20">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center shadow-lg" style={{ background: 'linear-gradient(to bottom right, var(--accent-gradient-from), var(--accent-gradient-to))', boxShadow: '0 10px 15px -3px var(--accent-shadow)' }}>
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h1 className="text-xl sm:text-2xl font-bold" style={{ background: 'linear-gradient(to right, var(--accent-gradient-from), var(--accent-gradient-to))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                  Todo
                </h1>
              </div>

              {/* Desktop nav */}
              <nav className="hidden md:flex items-center space-x-8">
                <Link href="/" className="text-secondary font-medium transition-colors duration-200" style={{ '--hover-color': 'var(--accent-primary)' } as React.CSSProperties} onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent-primary)')} onMouseLeave={e => (e.currentTarget.style.color = '')}>Home</Link>
                <Link href="/dashboard" className="text-secondary font-medium transition-colors duration-200" onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent-primary)')} onMouseLeave={e => (e.currentTarget.style.color = '')}>Tasks</Link>
                <Link href="/chat" className="text-secondary font-medium transition-colors duration-200 flex items-center gap-1.5" onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent-primary)')} onMouseLeave={e => (e.currentTarget.style.color = '')}>
                  <span role="img" aria-label="AI Assistant">🤖</span>
                  <span>AI Chat</span>
                </Link>
              </nav>

              <div className="flex items-center gap-3 sm:gap-4">
                {/* Mobile hamburger */}
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="md:hidden p-2 rounded-xl hover:bg-tertiary transition-all duration-200 focus-ring"
                  aria-label="Navigation menu"
                  aria-expanded={mobileMenuOpen}
                >
                  <svg className="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {mobileMenuOpen ? (
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                    ) : (
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                    )}
                  </svg>
                </button>

                <button
                  onClick={toggleTheme}
                  className="p-2.5 rounded-xl hover:bg-tertiary transition-all duration-200 focus-ring"
                  aria-label="Toggle theme"
                >
                  {theme === 'light' ? (
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M16.243 17.657l.707.707M6.343 6.343l.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z" />
                    </svg>
                  )}
                </button>

                <div className="hidden sm:block h-8 w-[1px] bg-slate-200 dark:bg-slate-700 mx-1" />

                {user ? (
                  <div className="flex items-center gap-3 sm:gap-4">
                    <div className="hidden sm:flex flex-col items-end bg-slate-50 dark:bg-slate-800/50 px-3 py-1.5 rounded-lg">
                      <span className="text-sm font-semibold max-w-[150px] truncate" title={user.name || 'User'}>{user.name || 'User'}</span>
                      <span className="text-xs text-secondary max-w-[150px] truncate" title={user.email}>{user.email}</span>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="px-4 sm:px-5 py-2 sm:py-2.5 bg-slate-100 dark:bg-slate-800 text-sm font-semibold rounded-xl hover:bg-slate-200 dark:hover:bg-slate-700 hover:shadow-md transition-all duration-200 focus-ring"
                    >
                      Sign Out
                    </button>
                  </div>
                ) : (
                  <div className="hidden sm:flex gap-3">
                    <Link href="/login" className="px-5 py-2.5 text-sm font-semibold transition-colors duration-200 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 focus-ring" onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent-primary)')} onMouseLeave={e => (e.currentTarget.style.color = '')}>Sign In</Link>
                    <Link href="/register" className="btn-primary py-2.5 px-6 text-sm transition-all duration-200 rounded-xl focus-ring" style={{ boxShadow: '0 10px 15px -3px var(--accent-shadow)' }}>Join Free</Link>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Mobile nav panel */}
          {mobileMenuOpen && (
            <nav className="md:hidden border-t border-primary px-4 py-4 space-y-2" aria-label="Mobile navigation">
              <Link href="/" className="block px-4 py-3 rounded-xl text-secondary font-medium hover:bg-tertiary transition-all duration-200">Home</Link>
              <Link href="/dashboard" className="block px-4 py-3 rounded-xl text-secondary font-medium hover:bg-tertiary transition-all duration-200">Tasks</Link>
              <Link href="/chat" className="block px-4 py-3 rounded-xl text-secondary font-medium hover:bg-tertiary transition-all duration-200">
                <span role="img" aria-label="AI Assistant">🤖</span> AI Chat
              </Link>
              {!user && (
                <div className="pt-2 space-y-2 border-t border-primary">
                  <Link href="/login" className="block px-4 py-3 rounded-xl text-secondary font-medium hover:bg-tertiary transition-all duration-200">Sign In</Link>
                  <Link href="/register" className="block px-4 py-3 rounded-xl text-center btn-primary font-medium">Join Free</Link>
                </div>
              )}
            </nav>
          )}
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
          {children}
        </main>

        <footer className="border-t border-primary mt-20 py-8 sm:py-12">
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
        .text-tertiary { color: var(--text-tertiary); }
        .bg-tertiary { background-color: var(--bg-tertiary); }
        .border-primary { border-color: var(--border-color); }
      `}</style>
    </>
  );
};

export default MainLayout;
