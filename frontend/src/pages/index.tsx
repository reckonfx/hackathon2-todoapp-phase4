/**
 * Home page for the Phase-2 Web-Based Todo Application.
 * Landing page for unauthenticated users.
 */

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import MainLayout from '../components/Layout/MainLayout';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: (
        <svg className="w-8 h-8 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '32px', maxHeight: '32px' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      title: 'Lightning Fast',
      description: 'Instant sync across all devices with real-time updates and zero lag.'
    },
    {
      icon: (
        <svg className="w-8 h-8 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '32px', maxHeight: '32px' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
      title: 'Secure & Private',
      description: 'Bank-level encryption keeps your tasks safe and completely private.'
    },
    {
      icon: (
        <svg className="w-8 h-8 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '32px', maxHeight: '32px' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
      ),
      title: 'Beautiful Design',
      description: 'Crafted with care using modern design principles and smooth animations.'
    },
    {
      icon: (
        <svg className="w-8 h-8 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '32px', maxHeight: '32px' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      title: 'Smart Features',
      description: 'AI-powered suggestions and intelligent task organization for peak productivity.'
    }
  ];

  const stats = [
    { value: '10K+', label: 'Active Users' },
    { value: '500K+', label: 'Tasks Completed' },
    { value: '99.9%', label: 'Uptime' },
    { value: '24/7', label: 'Support' }
  ];

  return (
    <MainLayout title="Home - Todo App">
      <Head>
        <title>Home - Todo Premium | Your Ultimate Task Manager</title>
        <meta name="description" content="Streamline your productivity with Todo Premium - the modern, secure, and beautiful task management solution." />
      </Head>

      {/* Hero Section */}
      <div className="relative overflow-hidden -mt-10">
        {/* Animated Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-indigo-900/20 to-slate-900/40" />
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSg3NiwyMDEsMjQwLDAuMDUpIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-20" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
          <div className="text-center animate-in fade-in slide-in-from-bottom-8 duration-1000">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 text-blue-300 rounded-full text-sm font-semibold mb-8 animate-in fade-in zoom-in duration-700 delay-200 neon-glow">
              <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" style={{ maxWidth: '16px', maxHeight: '16px' }}>
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Trusted by thousands worldwide
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight mb-8">
              <span className="block mb-2 neon-text">Your Perfect</span>
              <span className="block bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-400 to-sky-400 neon-text">
                Task Manager
              </span>
            </h1>

            <p className="max-w-2xl mx-auto text-xl sm:text-2xl text-secondary mb-12 leading-relaxed neon-text">
              Streamline your productivity with our beautifully designed, lightning-fast task management platform.
              <span className="block mt-2 font-semibold text-white">Simple. Powerful. Yours.</span>
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
              <Link
                href="/register"
                className="neon-btn px-8 py-4 text-white text-lg font-bold rounded-2xl shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center gap-3"
              >
                Start Free Today
                <svg className="w-5 h-5 flex-shrink-0 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '20px', maxHeight: '20px' }}>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <Link
                href="/login"
                className="neon-btn px-8 py-4 text-white text-lg font-bold rounded-2xl shadow-xl transform hover:scale-105 transition-all duration-300"
              >
                Sign In
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div
                  key={index}
                  className="card glass text-center transform hover:scale-105 transition-all duration-300 animate-in fade-in zoom-in neon-glow"
                  style={{ animationDelay: `${index * 100 + 400}ms` }}
                >
                  <div className="text-3xl sm:text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 neon-text">
                    {stat.value}
                  </div>
                  <div className="text-sm sm:text-base text-secondary font-semibold mt-2">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <h2 className="text-4xl sm:text-5xl font-extrabold mb-4 neon-text">
              Everything You Need,
              <span className="block mt-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 neon-text">Nothing You Don't</span>
            </h2>
            <p className="text-xl text-secondary max-w-2xl mx-auto neon-text">
              Powerful features wrapped in a delightful user experience
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group card glass hover:ring-2 hover:ring-cyan-500/50 transition-all duration-500 transform hover:scale-105 animate-in fade-in slide-in-from-bottom-4 neon-glow"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex items-start gap-5">
                  <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-cyan-500/30 group-hover:shadow-xl group-hover:shadow-cyan-500/40 transition-all duration-300 group-hover:scale-110">
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold mb-3 text-white">{feature.title}</h3>
                    <p className="text-secondary leading-relaxed">{feature.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 opacity-95" />
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQtd2hpdGUiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAgTSAwIDIwIEwgNDAgMjAgTSAyMCAwIEwgMjAgNDAgTSAwIDMwIEwgNDAgMzAgTSAzMCAwIEwgMzAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZC13aGl0ZSkiLz48L3N2Zz4=')] opacity-20" />

        <div className="relative max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-6 animate-in fade-in slide-in-from-bottom-4 duration-700 neon-text">
            Ready to Transform Your Productivity?
          </h2>
          <p className="text-xl text-blue-200 mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-200">
            Join thousands of users who have already supercharged their workflow. Get started in seconds.
          </p>
          <Link
            href="/register"
            className="neon-btn inline-flex items-center gap-3 px-10 py-5 text-white text-lg font-bold rounded-2xl shadow-2xl transform hover:scale-105 transition-all duration-300 animate-in fade-in zoom-in duration-700 delay-400"
          >
            Create Free Account
            <svg className="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '24px', maxHeight: '24px' }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
          <p className="text-blue-200 text-sm mt-6 animate-in fade-in duration-700 delay-500">
            No credit card required • Free forever • 2 minute setup
          </p>
        </div>
      </div>
    </MainLayout>
  );
};

export default HomePage;