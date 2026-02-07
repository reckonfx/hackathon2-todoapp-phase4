/**
 * TaskList component for the Phase-2 Web-Based Todo Application.
 * Displays a table of tasks with headers and completion status.
 * Styled using modern-ui-skill with Black & Gold theme.
 */

import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import { Task } from '../types/Task';

interface TaskListProps {
  tasks?: Task[];
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks: externalTasks, onTaskUpdate, onTaskDelete }) => {
  const [internalTasks, setInternalTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(!externalTasks);
  const [error, setError] = useState('');

  const tasks = externalTasks || internalTasks;

  useEffect(() => {
    if (!externalTasks) {
      fetchTasks();
    }
  }, [externalTasks]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAllTasks();

      if (response.success && response.tasks) {
        setInternalTasks(response.tasks);
      } else {
        setError(response.error || 'Failed to fetch tasks');
      }
    } catch (err) {
      setError('An unexpected error occurred while fetching tasks');
      console.error('Fetch tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      const response = await apiService.toggleTaskCompletion(taskId);

      if (response.success && response.task) {
        setInternalTasks(tasks.map(task =>
          task.id === taskId ? response.task! : task
        ));

        if (onTaskUpdate) {
          onTaskUpdate(response.task);
        }
      } else {
        setError(response.error || 'Failed to update task');
      }
    } catch (err) {
      setError('An unexpected error occurred while updating task');
      console.error('Toggle task error:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      const response = await apiService.deleteTask(taskId);

      if (response.success) {
        setInternalTasks(tasks.filter(task => task.id !== taskId));

        if (onTaskDelete) {
          onTaskDelete(taskId);
        }
      } else {
        setError(response.error || 'Failed to delete task');
      }
    } catch (err) {
      setError('An unexpected error occurred while deleting task');
      console.error('Delete task error:', err);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-16">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-[#2a2a2a] rounded-full" />
          <div className="w-16 h-16 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin absolute top-0" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="m-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
        <p className="text-red-400 text-sm font-medium">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="px-8 py-20 text-center">
        <div className="w-20 h-20 bg-[#1f1f1f] rounded-2xl flex items-center justify-center mx-auto mb-6 border border-[#d4af37]/30">
          <svg className="w-10 h-10 text-[#d4af37]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="text-2xl font-bold text-white mb-2">No tasks yet</h3>
        <p className="text-[#b8b8b8]">Get started by creating your first task above.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="task-table w-full">
        {/* Table Header */}
        <thead className="task-table-header">
          <tr>
            <th className="w-16 text-center">
              <span className="sr-only">Complete</span>
              Done
            </th>
            <th className="min-w-[200px]">Title</th>
            <th className="min-w-[250px]">Details</th>
            <th className="w-32">Created At</th>
            <th className="w-32">Completed At</th>
            <th className="w-28 text-center">Status</th>
            <th className="w-20 text-center">Actions</th>
          </tr>
        </thead>

        {/* Table Body */}
        <tbody>
          {tasks.map((task, index) => (
            <tr
              key={task.id}
              className="task-table-row group"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {/* Checkbox */}
              <td className="text-center">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggleComplete(task.id)}
                  className="gold-checkbox"
                  aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
                />
              </td>

              {/* Title */}
              <td>
                <span className={`font-semibold text-base ${task.completed ? 'text-[#6b6b6b] line-through' : 'text-white'}`}>
                  {task.title}
                </span>
              </td>

              {/* Details/Description */}
              <td>
                <p className={`text-sm ${task.completed ? 'text-[#6b6b6b]' : 'text-[#b8b8b8]'} line-clamp-2`}>
                  {task.description || <span className="italic text-[#4a4a4a]">No description</span>}
                </p>
              </td>

              {/* Created At */}
              <td>
                <div className="flex items-center gap-2 text-sm text-[#b8b8b8]">
                  <svg className="w-4 h-4 text-[#d4af37]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>{formatDate(task.created_at)}</span>
                </div>
              </td>

              {/* Completed At */}
              <td>
                {task.completed && task.completed_at ? (
                  <div className="flex items-center gap-2 text-sm text-emerald-400">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{formatDate(task.completed_at)}</span>
                  </div>
                ) : (
                  <span className="text-sm text-[#4a4a4a] italic">—</span>
                )}
              </td>

              {/* Status Badge */}
              <td className="text-center">
                <span className={task.completed ? 'badge-completed' : 'badge-active'}>
                  {task.completed ? 'Completed' : 'Active'}
                </span>
              </td>

              {/* Actions */}
              <td className="text-center">
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="p-2 text-[#6b6b6b] hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all duration-300 opacity-0 group-hover:opacity-100"
                  aria-label={`Delete "${task.title}"`}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TaskList;
