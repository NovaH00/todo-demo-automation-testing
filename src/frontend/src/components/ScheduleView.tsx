"use client";

import React, { useState } from "react";
import { AlertCircle, Calendar, Clock, RefreshCw } from "lucide-react";
import { ScheduleOverview, Tag, Task, TodoList } from "@/types";
import { TaskItem } from "./TaskItem";

interface ScheduleViewProps {
  overview: ScheduleOverview | null;
  upcomingTasks: Task[];
  lists: TodoList[];
  tags: Tag[];
  onToggleComplete: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onReschedule: (taskIds: number[], newDueDate: string) => Promise<void>;
}

export function ScheduleView({
  overview,
  upcomingTasks,
  lists,
  tags,
  onToggleComplete,
  onEdit,
  onDelete,
  onReschedule,
}: ScheduleViewProps) {
  const [rescheduling, setRescheduling] = useState(false);

  const handleRescheduleOverdueToToday = async () => {
    if (!overview || overview.tasks_overdue.length === 0) return;
    setRescheduling(true);
    try {
      const todayIso = new Date().toISOString();
      const ids = overview.tasks_overdue.map((t) => t.id);
      await onReschedule(ids, todayIso);
    } finally {
      setRescheduling(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-white border border-[#E2E5EB] rounded-lg p-4">
          <div className="flex items-center justify-between text-xs text-[#64748B]">
            <span>Overdue Tasks</span>
            <AlertCircle className="w-4 h-4 text-red-500" />
          </div>
          <div className="text-2xl font-semibold text-[#1A1D20] mt-1 tabular-nums">
            {overview?.overdue_count ?? 0}
          </div>
          <div className="text-[11px] text-[#64748B] mt-1">
            Tasks past due requiring attention
          </div>
        </div>

        <div className="bg-white border border-[#E2E5EB] rounded-lg p-4">
          <div className="flex items-center justify-between text-xs text-[#64748B]">
            <span>Due Today</span>
            <Clock className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-semibold text-[#1A1D20] mt-1 tabular-nums">
            {overview?.today_count ?? 0}
          </div>
          <div className="text-[11px] text-[#64748B] mt-1">
            Scheduled for completion today
          </div>
        </div>

        <div className="bg-white border border-[#E2E5EB] rounded-lg p-4">
          <div className="flex items-center justify-between text-xs text-[#64748B]">
            <span>Upcoming (7 Days)</span>
            <Calendar className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-semibold text-[#1A1D20] mt-1 tabular-nums">
            {overview?.upcoming_count ?? 0}
          </div>
          <div className="text-[11px] text-[#64748B] mt-1">
            Planned for the next week
          </div>
        </div>
      </div>

      {/* Section 1: Overdue */}
      {overview && overview.tasks_overdue.length > 0 && (
        <div className="bg-white border border-[#E2E5EB] rounded-lg overflow-hidden">
          <div className="px-4 py-3 border-b border-[#E2E5EB] bg-red-50/40 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-600" />
              <h3 className="text-sm font-semibold text-red-900">
                Overdue Tasks ({overview.tasks_overdue.length})
              </h3>
            </div>
            <button
              type="button"
              disabled={rescheduling}
              onClick={handleRescheduleOverdueToToday}
              className="text-xs px-2.5 py-1 bg-white border border-red-200 text-red-700 hover:bg-red-50 rounded transition-colors flex items-center gap-1 font-medium disabled:opacity-50"
            >
              <RefreshCw className={`w-3 h-3 ${rescheduling ? "animate-spin" : ""}`} />
              <span>Reschedule all to today</span>
            </button>
          </div>
          <div>
            {overview.tasks_overdue.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                lists={lists}
                tags={tags}
                onToggleComplete={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </div>
        </div>
      )}

      {/* Section 2: Today */}
      <div className="bg-white border border-[#E2E5EB] rounded-lg overflow-hidden">
        <div className="px-4 py-3 border-b border-[#E2E5EB] bg-amber-50/30 flex items-center gap-2">
          <Clock className="w-4 h-4 text-amber-700" />
          <h3 className="text-sm font-semibold text-[#1A1D20]">
            Due Today ({overview?.tasks_today.length ?? 0})
          </h3>
        </div>
        <div>
          {overview?.tasks_today && overview.tasks_today.length > 0 ? (
            overview.tasks_today.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                lists={lists}
                tags={tags}
                onToggleComplete={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))
          ) : (
            <div className="px-4 py-6 text-center text-xs text-[#94A3B8]">
              No tasks scheduled for today.
            </div>
          )}
        </div>
      </div>

      {/* Section 3: Upcoming */}
      <div className="bg-white border border-[#E2E5EB] rounded-lg overflow-hidden">
        <div className="px-4 py-3 border-b border-[#E2E5EB] bg-[#FAFBFD] flex items-center gap-2">
          <Calendar className="w-4 h-4 text-blue-600" />
          <h3 className="text-sm font-semibold text-[#1A1D20]">
            Upcoming Tasks ({upcomingTasks.length})
          </h3>
        </div>
        <div>
          {upcomingTasks.length > 0 ? (
            upcomingTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                lists={lists}
                tags={tags}
                onToggleComplete={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))
          ) : (
            <div className="px-4 py-6 text-center text-xs text-[#94A3B8]">
              No upcoming tasks found in the next 7 days.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
