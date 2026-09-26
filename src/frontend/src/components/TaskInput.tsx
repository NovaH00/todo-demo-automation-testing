"use client";

import React, { useState } from "react";
import { Calendar, Flag, Hash, Plus, Tag as TagIcon, X } from "lucide-react";
import { Tag, TaskCreateInput, TaskPriority, TodoList } from "@/types";

interface TaskInputProps {
  onAddTask: (data: TaskCreateInput) => Promise<void>;
  lists: TodoList[];
  tags: Tag[];
  defaultListId?: number | null;
  defaultDueDate?: string | null;
}

export function TaskInput({
  onAddTask,
  lists,
  tags,
  defaultListId = null,
  defaultDueDate = null,
}: TaskInputProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<TaskPriority>("medium");
  const [dueDate, setDueDate] = useState<string>(defaultDueDate || "");
  const [listId, setListId] = useState<number | null>(defaultListId);
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);
  const [expanded, setExpanded] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || submitting) return;

    setSubmitting(true);
    try {
      await onAddTask({
        title: title.trim(),
        description: description.trim() || null,
        priority,
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
        list_id: listId,
        tag_ids: selectedTagIds,
      });

      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate(defaultDueDate || "");
      setSelectedTagIds([]);
      setExpanded(false);
    } finally {
      setSubmitting(false);
    }
  };

  const toggleTag = (tagId: number) => {
    setSelectedTagIds((prev) =>
      prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId]
    );
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white border border-[#E2E5EB] rounded-lg shadow-sm transition-all focus-within:border-[#1D4ED8] focus-within:ring-1 focus-within:ring-[#1D4ED8]"
    >
      <div className="flex items-center px-4 py-3">
        <Plus className="w-5 h-5 text-[#94A3B8] shrink-0 mr-3" />
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onFocus={() => setExpanded(true)}
          placeholder="Add a new task... (press Enter to save)"
          className="w-full text-sm text-[#1A1D20] placeholder-[#94A3B8] bg-transparent outline-none"
        />
        {title.trim() && (
          <button
            type="submit"
            disabled={submitting}
            className="ml-2 px-3 py-1 bg-[#1D4ED8] hover:bg-[#1E40AF] text-white text-xs font-medium rounded transition-colors disabled:opacity-50"
          >
            {submitting ? "Adding..." : "Add task"}
          </button>
        )}
      </div>

      {expanded && (
        <div className="px-4 pb-3 pt-1 border-t border-[#E2E5EB] space-y-3 bg-[#FAFBFD] rounded-b-lg">
          {/* Optional notes */}
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add notes or details..."
            className="w-full text-xs text-[#1A1D20] placeholder-[#94A3B8] bg-transparent outline-none py-1"
          />

          <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
            {/* Priority selector */}
            <div className="flex items-center gap-1 bg-white border border-[#E2E5EB] rounded px-2 py-1">
              <Flag className="w-3.5 h-3.5 text-[#64748B]" />
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as TaskPriority)}
                className="bg-transparent text-xs text-[#1A1D20] outline-none"
              >
                <option value="low">Low priority</option>
                <option value="medium">Medium priority</option>
                <option value="high">High priority</option>
              </select>
            </div>

            {/* Due date picker */}
            <div className="flex items-center gap-1 bg-white border border-[#E2E5EB] rounded px-2 py-1">
              <Calendar className="w-3.5 h-3.5 text-[#64748B]" />
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="bg-transparent text-xs text-[#1A1D20] outline-none"
              />
              {dueDate && (
                <button
                  type="button"
                  onClick={() => setDueDate("")}
                  className="text-[#94A3B8] hover:text-[#1A1D20]"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>

            {/* List picker */}
            {lists.length > 0 && (
              <div className="flex items-center gap-1 bg-white border border-[#E2E5EB] rounded px-2 py-1">
                <Hash className="w-3.5 h-3.5 text-[#64748B]" />
                <select
                  value={listId ?? ""}
                  onChange={(e) =>
                    setListId(e.target.value ? Number(e.target.value) : null)
                  }
                  className="bg-transparent text-xs text-[#1A1D20] outline-none"
                >
                  <option value="">No list</option>
                  {lists.map((l) => (
                    <option key={l.id} value={l.id}>
                      {l.name}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Tag selector chips */}
            {tags.length > 0 && (
              <div className="flex items-center gap-1 flex-wrap">
                <TagIcon className="w-3.5 h-3.5 text-[#64748B] ml-1" />
                {tags.map((tag) => {
                  const selected = selectedTagIds.includes(tag.id);
                  return (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => toggleTag(tag.id)}
                      className={`px-2 py-0.5 rounded text-[11px] border transition-colors ${
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
            )}
          </div>
        </div>
      )}
    </form>
  );
}
