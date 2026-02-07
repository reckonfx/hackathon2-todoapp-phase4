/**
 * Dashboard page for the Phase-2 Web-Based Todo Application.
 * Main page for authenticated users with Black & Gold premium theme.
 * Styled using modern-ui-skill methodology.
 */

import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import MainLayout from '../components/Layout/MainLayout';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import { Task } from '../types/Task';
import { User } from '../types/User';
import apiService from '../services/api';

const DashboardPage: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUserData();
    fetchTasks();

    // Listen for task changes from chat widget
    const handleTasksChanged = () => {
      console.log('Tasks changed event received, refreshing...');
      fetchTasks();
    };
    window.addEventListener('tasks-changed', handleTasksChanged);

    return () => {
      window.removeEventListener('tasks-changed', handleTasksChanged);
    };
  }, []);

  useEffect(() => {
    let result = [...tasks];

    if (filter === 'active') {
      result = result.filter(task => !task.completed);
    } else if (filter === 'completed') {
      result = result.filter(task => task.completed);
    }

    if (searchQuery.trim()) {
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (task.description?.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    setFilteredTasks(result);
  }, [tasks, filter, searchQuery]);

  const fetchUserData = async () => {
    try {
      const response = await apiService.getCurrentUser();
      if (response.success && response.user) {
        setUser(response.user);
      }
    } catch (err) {
      console.error('Failed to fetch user data:', err);
    }
  };

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAllTasks();
      if (response.success && response.tasks) {
        setTasks(response.tasks);
      }
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskSaved = (task: Task) => {
    setShowForm(false);
    fetchTasks();
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
  };

  const handleTaskDeleted = (taskId: string) => {
    setTasks(tasks.filter(t => t.id !== taskId));
  };

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const activeTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const stats = [
    {
      label: 'Total Tasks',
      value: totalTasks,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      ),
      gradient: 'from-[#d4af37] to-[#f4c430]'
    },
    {
      label: 'Active',
      value: activeTasks,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      gradient: 'from-amber-500 to-orange-500'
    },
    {
      label: 'Completed',
      value: completedTasks,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      gradient: 'from-emerald-500 to-green-500'
    },
    {
      label: 'Completion Rate',
      value: `${completionRate}%`,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
      gradient: 'from-purple-500 to-pink-500'
    }
  ];

  return (
    <MainLayout title="My Workspace">
      <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl text-gradient-gold">
              My Workspace
            </h1>
            {user && (
              <p className="mt-3 text-lg text-[#b8b8b8]">
                Welcome back, <span className="font-semibold text-[#d4af37]">{user.name || user.email.split('@')[0]}</span>! Manage your tasks with our premium interface.
              </p>
            )}
            {!user && (
              <p className="mt-3 text-lg text-[#b8b8b8]">
                Manage your tasks with our premium, distraction-free interface.
              </p>
            )}
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn-primary inline-flex items-center gap-1.5 px-3 py-2 text-xs w-fit self-start md:self-auto"
          >
            <span className={`text-sm font-bold transition-transform duration-300 ${showForm ? 'rotate-45' : ''}`}>+</span>
            <span className="font-semibold">{showForm ? 'Close' : 'Add Task'}</span>
          </button>
        </div>

        {/* Statistics Cards */}
        <div className="stats-grid-container grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-2">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="stat-card card relative overflow-hidden group"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="relative flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold uppercase tracking-wider text-[#b8b8b8] mb-2">
                    {stat.label}
                  </p>
                  <p className="text-3xl sm:text-4xl font-extrabold text-[#d4af37]">
                    {stat.value}
                  </p>
                </div>
                <div className={`w-12 h-12 sm:w-14 sm:h-14 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                  {stat.icon}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Task Form */}
        {showForm && (
          <div className="card glass !border-[#d4af37]/30 animate-in slide-in-from-top-4 duration-500">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-[#d4af37] to-[#f4c430] rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-[#0a0a0a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white">Create New Task</h3>
            </div>
            <TaskForm onTaskSaved={handleTaskSaved} onCancel={() => setShowForm(false)} />
          </div>
        )}

        {/* Search and Filter Controls */}
        <div className="card glass !border-[#d4af37]/20 mt-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="w-5 h-5 text-[#6b6b6b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search tasks by title or description..."
                  className="input-field pl-12 pr-4 py-4 w-full"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute inset-y-0 right-0 pr-4 flex items-center"
                  >
                    <svg className="w-5 h-5 text-[#6b6b6b] hover:text-[#d4af37] transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            {/* Filter Buttons */}
            <div className="filter-tabs-container flex gap-2 p-1.5 rounded-xl">
              {[
                { key: 'all', label: 'All Tasks', icon: '📋' },
                { key: 'active', label: 'Active', icon: '⚡' },
                { key: 'completed', label: 'Completed', icon: '✅' }
              ].map(({ key, label, icon }) => (
                <button
                  key={key}
                  onClick={() => setFilter(key as any)}
                  className={`filter-tab px-5 py-3 rounded-lg font-semibold text-sm transition-all duration-300 flex items-center gap-2 ${filter === key
                    ? 'bg-gradient-to-r from-[#d4af37] to-[#f4c430] text-[#0a0a0a] shadow-lg'
                    : 'text-[#b8b8b8] hover:text-white hover:bg-[#2a2a2a]'
                    }`}
                >
                  <span>{icon}</span>
                  <span className="hidden sm:inline">{label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Results Info */}
          <div className="mt-4 pt-4 border-t border-[#2a2a2a] flex items-center justify-between">
            <p className="text-sm text-[#b8b8b8]">
              {searchQuery ? (
                <>
                  Found <span className="font-bold text-[#d4af37]">{filteredTasks.length}</span> result{filteredTasks.length !== 1 ? 's' : ''} for "{searchQuery}"
                </>
              ) : (
                <>
                  Showing <span className="font-bold text-[#d4af37]">{filteredTasks.length}</span> {filter === 'all' ? 'task' : filter}{filteredTasks.length !== 1 ? 's' : ''}
                </>
              )}
            </p>
            {(searchQuery || filter !== 'all') && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setFilter('all');
                }}
                className="text-sm font-semibold text-[#d4af37] hover:text-[#f4c430] transition-colors duration-300"
              >
                Clear filters
              </button>
            )}
          </div>
        </div>

        {/* Task List */}
        <div className="space-y-4 mt-6">
          <div className="card glass !p-0 overflow-hidden !border-[#d4af37]/20">
            {loading ? (
              <div className="flex justify-center items-center py-20">
                <div className="relative">
                  <div className="w-16 h-16 border-4 border-[#2a2a2a] rounded-full" />
                  <div className="w-16 h-16 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin absolute top-0" />
                </div>
              </div>
            ) : (
              <TaskList
                tasks={filteredTasks}
                onTaskUpdate={handleTaskUpdate}
                onTaskDelete={handleTaskDeleted}
                key={`${filter}-${searchQuery}`}
              />
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
