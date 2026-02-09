/**
 * TaskForm component for the Phase-2 Web-Based Todo Application.
 * Handles creating and updating tasks.
 */

import React, { useState } from 'react';
import apiService from '../services/api';
import { CreateTaskRequest, UpdateTaskRequest, Task } from '../types/Task';

interface TaskFormProps {
  task?: Task; // If provided, this is an edit form
  onTaskSaved?: (task: Task) => void;
  onCancel?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onTaskSaved, onCancel }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (task) {
        // Update existing task
        const updateData: UpdateTaskRequest = {};
        if (title !== task.title) updateData.title = title;
        if (description !== task.description) updateData.description = description;

        if (Object.keys(updateData).length > 0) {
          const response = await apiService.updateTask(task.id, updateData);

          if (response.success && response.task) {
            if (onTaskSaved) {
              onTaskSaved(response.task);
            }
          } else {
            setError(response.error || 'Failed to update task');
          }
        } else {
          // No changes made, just return the original task
          if (onTaskSaved) {
            onTaskSaved(task);
          }
        }
      } else {
        // Create new task
        const response = await apiService.createTask({ title, description });

        if (response.success && response.task) {
          if (onTaskSaved) {
            onTaskSaved(response.task);
          }
          // Reset form for new task
          setTitle('');
          setDescription('');
        } else {
          setError(response.error || 'Failed to create task');
        }
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Task operation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-4 bg-danger/10 border border-danger/20 rounded-xl text-danger text-sm font-medium animate-in fade-in zoom-in duration-300">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      <div className="space-y-2">
        <label htmlFor="title" className="text-sm font-bold uppercase tracking-wider text-secondary flex justify-between">
          Title <span className="text-tertiary">Required</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
          required
          maxLength={200}
          className="input-field py-4 focus-ring"
          placeholder="What needs to be done?"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="description" className="text-sm font-bold uppercase tracking-wider text-secondary">
          Description
        </label>
        <textarea
          id="description"
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          maxLength={1000}
          className="input-field min-h-[120px] resize-none focus-ring"
          placeholder="Add some details (optional)..."
        />
      </div>

      <div className="pt-4 flex items-center justify-end gap-3">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="px-6 py-3 text-sm font-bold text-secondary hover:text-primary transition-colors disabled:opacity-50 focus-ring"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary min-w-[140px] flex items-center justify-center gap-2 focus-ring"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ maxWidth: '20px', maxHeight: '20px' }}>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              {task ? 'Save Changes' : 'Create Task'}
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;