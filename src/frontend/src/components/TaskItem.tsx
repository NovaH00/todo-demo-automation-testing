"use client";

import React from "react";
import {
  AlertCircle,
  Calendar,
  Check,
  Edit3,
  Flag,
  Trash2,
} from "lucide-react";
import { Tag, Task, TodoList } from "@/types";

interface TaskItemProps {
  task: Task;
  lists: TodoList[];
  tags: Tag[];
  onToggleComplete: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

export function TaskItem({
  task,
  lists,
  tags,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const list = lists.find((l) => l.id === task.list_id);
  const taskTags = tags.filter((t) => task.tag_ids.includes(t.id));

  // Determine due date status
  let dueStatus: { label: string; isOverdue: boolean; isToday: boolean } | null = null;
  if (task.due_date) {
    const due = new Date(task.due_date);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const dueDateOnly = new Date(due.getFullYear(), due.getMonth(), due.getDate());

    const isToday = dueDateOnly.getTime() === today.getTime();
    const isOverdue = !task.is_completed && dueDateOnly.getTime() < today.getTime();

    const formatted = due.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });

    dueStatus = {
      label: isToday ? "Today" : formatted,
      isOverdue,
      isToday,
    };
  }

  const priorityColors = {
    high: "text-red-700 bg-red-50 border-red-200",
    medium: "text-amber-800 bg-amber-50 border-amber-200",
    low: "text-slate-600 bg-slate-50 border-slate-200",
  };

  return (
    <div
      className={`group flex items-start justify-between px-4 py-3 bg-white border-b border-[#E2E5EB] transition-colors hover:bg-[#FAFBFD] ${
        task.is_completed ? "opacity-60 bg-gray-50/50" : ""
      }`}
    >
      <div className="flex items-start gap-3 flex-1 min-w-0 pr-4">
        {/* Tactile Checkbox */}
        <button
          type="button"
          onClick={() => onToggleComplete(task)}
          className={`mt-0.5 w-4 h-4 rounded border flex items-center justify-center shrink-0 transition-colors ${
            task.is_completed
              ? "bg-[#15803D] border-[#15803D] text-white"
              : "border-[#CBD5E1] bg-white hover:border-[#1D4ED8]"
          }`}
          aria-label={task.is_completed ? "Mark incomplete" : "Mark complete"}
        >
          {task.is_completed && <Check className="w-3 h-3 stroke-[3]" />}
        </button>

        <div className="flex-1 min-w-0 space-y-1">
          {/* Title */}
          <div
            onClick={() => onEdit(task)}
            className={`text-sm cursor-pointer select-text ${
              task.is_completed
                ? "line-through text-[#94A3B8]"
                : "text-[#1A1D20] font-normal hover:text-[#1D4ED8]"
            }`}
          >
            {task.title}
          </div>

          {/* Description */}
          {task.description && (
            <p className="text-xs text-[#64748B] line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}

          {/* Metadata chips */}
          <div className="flex flex-wrap items-center gap-1.5 pt-1 text-[11px]">
            {/* List indicator */}
            {list && (
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded border border-[#E2E5EB] text-[#64748B] bg-white">
                <span
                  className="w-1.5 h-1.5 rounded-full"
                  style={{ backgroundColor: list.color || "#64748B" }}
                />
                <span>{list.name}</span>
              </span>
            )}

            {/* Due date badge */}
            {dueStatus && (
              <span
                className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded border ${
                  dueStatus.isOverdue
                    ? "text-red-700 bg-red-50 border-red-200 font-medium"
                    : dueStatus.isToday
                    ? "text-amber-800 bg-amber-50 border-amber-200 font-medium"
                    : "text-[#64748B] bg-white border-[#E2E5EB]"
                }`}
              >
                {dueStatus.isOverdue ? (
                  <AlertCircle className="w-3 h-3 text-red-600" />
                ) : (
                  <Calendar className="w-3 h-3 opacity-70" />
                )}
                <span>{dueStatus.label}</span>
              </span>
            )}

            {/* Priority */}
            {task.priority !== "low" && (
              <span
                className={`inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded border ${
                  priorityColors[task.priority]
                }`}
              >
                <Flag className="w-2.5 h-2.5" />
                <span className="capitalize">{task.priority}</span>
              </span>
            )}

            {/* Tags */}
            {taskTags.map((tag) => (
              <span
                key={tag.id}
                className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded border border-[#E2E5EB] bg-white text-[#64748B]"
              >
                <span
                  className="w-1.5 h-1.5 rounded-full"
                  style={{ backgroundColor: tag.color || "#94A3B8" }}
                />
                <span>{tag.name}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Row Actions */}
      <div className="flex items-center gap-1 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          type="button"
          onClick={() => onEdit(task)}
          className="p-1 text-[#64748B] hover:text-[#1A1D20] hover:bg-[#F1F3F7] rounded"
          title="Edit task"
        >
          <Edit3 className="w-3.5 h-3.5" />
        </button>
        <button
          type="button"
          onClick={() => onDelete(task.id)}
          className="p-1 text-[#64748B] hover:text-red-600 hover:bg-red-50 rounded"
          title="Delete task"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
