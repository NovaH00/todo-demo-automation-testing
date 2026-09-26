"use client";

import React, { useState } from "react";
import { X } from "lucide-react";
import { Tag, Task, TaskUpdateInput, TodoList } from "@/types";

interface TaskEditModalProps {
  task: Task | null;
  lists: TodoList[];
  tags: Tag[];
  onClose: () => void;
  onSave: (taskId: number, updates: TaskUpdateInput) => Promise<void>;
}

interface TaskEditFormProps {
  task: Task;
  lists: TodoList[];
  tags: Tag[];
  onClose: () => void;
  onSave: (taskId: number, updates: TaskUpdateInput) => Promise<void>;
}

function TaskEditForm({
  task,
  lists,
  tags,
  onClose,
  onSave,
}: TaskEditFormProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [priority, setPriority] = useState<"low" | "medium" | "high">(task.priority);
  const [dueDate, setDueDate] = useState(task.due_date ? task.due_date.slice(0, 10) : "");
  const [listId, setListId] = useState<number | null>(task.list_id);
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>(task.tag_ids || []);
  const [recurrence, setRecurrence] = useState(task.recurrence || "none");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || saving) return;

    setSaving(true);
    try {
      await onSave(task.id, {
        title: title.trim(),
        description: description.trim() || null,
        priority,
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
        list_id: listId,
        recurrence,
        tag_ids: selectedTagIds,
      });
      onClose();
    } finally {
      setSaving(false);
    }
  };

  const toggleTag = (tagId: number) => {
    setSelectedTagIds((prev) =>
      prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId]
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-xs p-4">
      <div className="bg-white border border-[#E2E5EB] rounded-lg shadow-xl w-full max-w-lg overflow-hidden animate-in fade-in zoom-in-95 duration-100">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#E2E5EB]">
          <h2 className="text-sm font-semibold text-[#1A1D20]">Edit Task</h2>
          <button
            type="button"
            onClick={onClose}
            className="text-[#64748B] hover:text-[#1A1D20] p-1 rounded hover:bg-[#F1F3F7]"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-medium text-[#64748B] mb-1">
              Title
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full text-sm px-3 py-2 border border-[#E2E5EB] rounded-md focus:border-[#1D4ED8] focus:ring-1 focus:ring-[#1D4ED8] outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#64748B] mb-1">
              Notes
            </label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add optional notes or checklist items..."
              className="w-full text-sm px-3 py-2 border border-[#E2E5EB] rounded-md focus:border-[#1D4ED8] focus:ring-1 focus:ring-[#1D4ED8] outline-none resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as "low" | "medium" | "high")}
                className="w-full text-xs px-2.5 py-1.5 border border-[#E2E5EB] rounded-md bg-white text-[#1A1D20] outline-none"
              >
                <option value="low">Low priority</option>
                <option value="medium">Medium priority</option>
                <option value="high">High priority</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1">
                Due Date
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full text-xs px-2.5 py-1.5 border border-[#E2E5EB] rounded-md bg-white text-[#1A1D20] outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1">
                List
              </label>
              <select
                value={listId ?? ""}
                onChange={(e) =>
                  setListId(e.target.value ? Number(e.target.value) : null)
                }
                className="w-full text-xs px-2.5 py-1.5 border border-[#E2E5EB] rounded-md bg-white text-[#1A1D20] outline-none"
              >
                <option value="">No list</option>
                {lists.map((l) => (
                  <option key={l.id} value={l.id}>
                    {l.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1">
                Recurrence
              </label>
              <select
                value={recurrence}
                onChange={(e) => setRecurrence(e.target.value)}
                className="w-full text-xs px-2.5 py-1.5 border border-[#E2E5EB] rounded-md bg-white text-[#1A1D20] outline-none"
              >
                <option value="none">Does not repeat</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
          </div>

          {tags.length > 0 && (
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1">
                Tags
              </label>
              <div className="flex flex-wrap gap-1.5">
                {tags.map((tag) => {
                  const selected = selectedTagIds.includes(tag.id);
                  return (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => toggleTag(tag.id)}
                      className={`px-2 py-1 rounded text-xs border transition-colors ${
                        selected
                          ? "bg-[#1D4ED8] text-white border-[#1D4ED8]"
                          : "bg-white text-[#64748B] border-[#E2E5EB] hover:bg-[#F1F3F7]"
                      }`}
                    >
                      {tag.name}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#E2E5EB]">
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 text-xs text-[#64748B] hover:text-[#1A1D20] rounded hover:bg-[#F1F3F7]"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-3.5 py-1.5 bg-[#1D4ED8] hover:bg-[#1E40AF] text-white text-xs font-medium rounded transition-colors disabled:opacity-50"
            >
              {saving ? "Saving..." : "Save changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export function TaskEditModal({
  task,
  lists,
  tags,
  onClose,
  onSave,
}: TaskEditModalProps) {
  if (!task) return null;

  return (
    <TaskEditForm
      key={task.id}
      task={task}
      lists={lists}
      tags={tags}
      onClose={onClose}
      onSave={onSave}
    />
  );
}
