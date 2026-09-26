"use client";

import React, { useEffect, useState } from "react";
import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Clock,
  Inbox,
  Search,
  Tag as TagIcon,
} from "lucide-react";
import { ListModal } from "@/components/ListModal";
import { ScheduleView } from "@/components/ScheduleView";
import { Sidebar } from "@/components/Sidebar";
import { TagModal } from "@/components/TagModal";
import { TaskEditModal } from "@/components/TaskEditModal";
import { TaskInput } from "@/components/TaskInput";
import { TaskItem } from "@/components/TaskItem";
import { api } from "@/lib/api";
import {
  ListCreateInput,
  ScheduleOverview,
  Tag,
  TagCreateInput,
  Task,
  TaskCreateInput,
  TaskPriority,
  TaskStatusFilter,
  TaskUpdateInput,
  TodoList,
  ViewType,
} from "@/types";

export default function HomePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [lists, setLists] = useState<TodoList[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [scheduleOverview, setScheduleOverview] = useState<ScheduleOverview | null>(null);
  const [upcomingTasks, setUpcomingTasks] = useState<Task[]>([]);

  const [currentView, setCurrentView] = useState<ViewType>({ kind: "all" });
  const [statusFilter, setStatusFilter] = useState<TaskStatusFilter>("all");
  const [priorityFilter, setPriorityFilter] = useState<TaskPriority | "">("");
  const [searchQuery, setSearchQuery] = useState("");

  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isListModalOpen, setIsListModalOpen] = useState(false);
  const [isTagModalOpen, setIsTagModalOpen] = useState(false);

  const [backendOnline, setBackendOnline] = useState(true);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const refreshData = () => {
    setRefreshKey((k) => k + 1);
  };

  useEffect(() => {
    let active = true;

    async function fetchData() {
      try {
        // Health check
        try {
          await api.checkHealth();
          if (active) setBackendOnline(true);
        } catch {
          if (active) setBackendOnline(false);
        }

        // Lists and tags
        const [fetchedLists, fetchedTags] = await Promise.all([
          api.getLists().catch(() => []),
          api.getTags().catch(() => []),
        ]);
        if (active) {
          setLists(fetchedLists);
          setTags(fetchedTags);
        }

        // Schedule overview
        try {
          const overview = await api.getScheduleOverview();
          if (active) setScheduleOverview(overview);
          const upcoming = await api.getUpcomingTasks(7);
          if (active) setUpcomingTasks(upcoming);
        } catch {
          // Schedule endpoints fallback
        }

        // Tasks query
        let fetchedTasks: Task[] = [];
        if (currentView.kind === "today") {
          fetchedTasks = await api.getTodayTasks().catch(() => []);
        } else if (currentView.kind === "overdue") {
          fetchedTasks = await api.getOverdueTasks().catch(() => []);
        } else if (currentView.kind === "list") {
          fetchedTasks = await api.getTasks({
            list_id: currentView.listId,
            status: statusFilter,
            priority: priorityFilter || undefined,
            search: searchQuery || undefined,
          }).catch(() => []);
        } else if (currentView.kind === "tag") {
          fetchedTasks = await api.getTasks({
            tag_id: currentView.tagId,
            status: statusFilter,
            priority: priorityFilter || undefined,
            search: searchQuery || undefined,
          }).catch(() => []);
        } else if (currentView.kind === "all") {
          fetchedTasks = await api.getTasks({
            status: statusFilter,
            priority: priorityFilter || undefined,
            search: searchQuery || undefined,
          }).catch(() => []);
        }

        if (active) {
          setTasks(fetchedTasks);
          setErrorMessage(null);
        }
      } catch (err: unknown) {
        if (active) {
          setErrorMessage(err instanceof Error ? err.message : "Failed to load tasks");
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      active = false;
    };
  }, [currentView, statusFilter, priorityFilter, searchQuery, refreshKey]);

  // Task Mutations
  const handleToggleComplete = async (task: Task) => {
    try {
      const nextCompleted = !task.is_completed;
      // Optimistic update
      setTasks((prev) =>
        prev.map((t) => (t.id === task.id ? { ...t, is_completed: nextCompleted } : t))
      );
      await api.updateTask(task.id, { is_completed: nextCompleted });
      refreshData();
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : "Failed to update task");
      refreshData();
    }
  };

  const handleAddTask = async (data: TaskCreateInput) => {
    try {
      await api.createTask(data);
      refreshData();
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : "Failed to add task");
    }
  };

  const handleUpdateTask = async (taskId: number, updates: TaskUpdateInput) => {
    try {
      await api.updateTask(taskId, updates);
      refreshData();
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      await api.deleteTask(taskId);
      refreshData();
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : "Failed to delete task");
      refreshData();
    }
  };

  const handleCreateList = async (data: ListCreateInput) => {
    const created = await api.createList(data);
    setLists((prev) => [...prev, created]);
    setCurrentView({ kind: "list", listId: created.id });
  };

  const handleCreateTag = async (data: TagCreateInput) => {
    const created = await api.createTag(data);
    setTags((prev) => [...prev, created]);
  };

  const handleReschedule = async (taskIds: number[], newDueDate: string) => {
    await api.reschedule(taskIds, newDueDate);
    refreshData();
  };

  // View Title & Subtitle computation
  let viewTitle = "All Tasks";
  let viewIcon = <Inbox className="w-5 h-5 text-[#1D4ED8]" />;

  if (currentView.kind === "today") {
    viewTitle = "Due Today";
    viewIcon = <Clock className="w-5 h-5 text-amber-600" />;
  } else if (currentView.kind === "overdue") {
    viewTitle = "Overdue Tasks";
    viewIcon = <CheckCircle2 className="w-5 h-5 text-red-600" />;
  } else if (currentView.kind === "upcoming") {
    viewTitle = "Upcoming Schedule";
    viewIcon = <Calendar className="w-5 h-5 text-blue-600" />;
  } else if (currentView.kind === "list") {
    const activeList = lists.find((l) => l.id === currentView.listId);
    viewTitle = activeList ? activeList.name : "List";
    viewIcon = (
      <span
        className="w-3.5 h-3.5 rounded-full"
        style={{ backgroundColor: activeList?.color || "#2563EB" }}
      />
    );
  } else if (currentView.kind === "tag") {
    const activeTag = tags.find((t) => t.id === currentView.tagId);
    viewTitle = activeTag ? `#${activeTag.name}` : "Tag";
    viewIcon = <TagIcon className="w-4 h-4 text-[#1D4ED8]" />;
  }

  const activeTaskCount = tasks.filter((t) => !t.is_completed).length;
  const completedTaskCount = tasks.filter((t) => t.is_completed).length;

  return (
    <div className="flex h-screen bg-[#F7F8FA] overflow-hidden text-[#1A1D20]">
      {/* Left Sidebar */}
      <Sidebar
        currentView={currentView}
        onSelectView={setCurrentView}
        lists={lists}
        tags={tags}
        scheduleOverview={scheduleOverview}
        totalTaskCount={tasks.length}
        onOpenNewList={() => setIsListModalOpen(true)}
        onOpenNewTag={() => setIsTagModalOpen(true)}
        backendOnline={backendOnline}
      />

      {/* Main Workspace Stage */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Workspace Top Toolbar */}
        <header className="px-8 py-5 bg-white border-b border-[#E2E5EB] flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-[#F1F3F7] rounded-md flex items-center justify-center">
              {viewIcon}
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight text-[#1A1D20]">
                {viewTitle}
              </h1>
              <div className="text-xs text-[#64748B] mt-0.5">
                {activeTaskCount} active · {completedTaskCount} completed
              </div>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="flex items-center gap-3">
            {/* Search Input */}
            <div className="relative">
              <Search className="w-4 h-4 absolute left-2.5 top-2.5 text-[#94A3B8]" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tasks..."
                className="text-xs pl-8 pr-3 py-1.5 border border-[#E2E5EB] rounded-md bg-[#FAFBFD] text-[#1A1D20] placeholder-[#94A3B8] focus:bg-white focus:border-[#1D4ED8] focus:ring-1 focus:ring-[#1D4ED8] outline-none w-48 transition-all"
              />
            </div>

            {/* Status Segmented Control */}
            <div className="flex items-center p-0.5 bg-[#F1F3F7] rounded-md text-xs">
              <button
                type="button"
                onClick={() => setStatusFilter("all")}
                className={`px-2.5 py-1 rounded transition-colors ${
                  statusFilter === "all"
                    ? "bg-white font-medium text-[#1A1D20] shadow-2xs"
                    : "text-[#64748B] hover:text-[#1A1D20]"
                }`}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => setStatusFilter("pending")}
                className={`px-2.5 py-1 rounded transition-colors ${
                  statusFilter === "pending"
                    ? "bg-white font-medium text-[#1A1D20] shadow-2xs"
                    : "text-[#64748B] hover:text-[#1A1D20]"
                }`}
              >
                Active
              </button>
              <button
                type="button"
                onClick={() => setStatusFilter("completed")}
                className={`px-2.5 py-1 rounded transition-colors ${
                  statusFilter === "completed"
                    ? "bg-white font-medium text-[#1A1D20] shadow-2xs"
                    : "text-[#64748B] hover:text-[#1A1D20]"
                }`}
              >
                Done
              </button>
            </div>

            {/* Priority Filter */}
            <div className="flex items-center gap-1">
              <select
                value={priorityFilter}
                onChange={(e) =>
                  setPriorityFilter(e.target.value as TaskPriority | "")
                }
                className="text-xs px-2 py-1.5 border border-[#E2E5EB] rounded-md bg-[#FAFBFD] text-[#64748B] outline-none hover:bg-white"
              >
                <option value="">All Priorities</option>
                <option value="high">High priority</option>
                <option value="medium">Medium priority</option>
                <option value="low">Low priority</option>
              </select>
            </div>
          </div>
        </header>

        {/* Workspace Content Canvas */}
        <div className="flex-1 overflow-y-auto px-8 py-6 max-w-4xl w-full mx-auto space-y-6">
          {/* Offline warning if FastAPI is not running */}
          {!backendOnline && (
            <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-md text-amber-800 text-xs flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span>
                  The backend API is not responding. Please verify the server is running.
                </span>
              </div>
              <button
                type="button"
                onClick={refreshData}
                className="px-2.5 py-1 bg-white border border-amber-300 rounded font-medium text-amber-900 hover:bg-amber-100"
              >
                Retry
              </button>
            </div>
          )}

          {/* Error Banner */}
          {errorMessage && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-md">
              {errorMessage}
            </div>
          )}

          {/* Schedule View Mode or Regular Stream */}
          {currentView.kind === "upcoming" ? (
            <ScheduleView
              overview={scheduleOverview}
              upcomingTasks={upcomingTasks}
              lists={lists}
              tags={tags}
              onToggleComplete={handleToggleComplete}
              onEdit={setEditingTask}
              onDelete={handleDeleteTask}
              onReschedule={handleReschedule}
            />
          ) : (
            <>
              {/* Quick Task Intake Line */}
              <TaskInput
                onAddTask={handleAddTask}
                lists={lists}
                tags={tags}
                defaultListId={
                  currentView.kind === "list" ? currentView.listId : null
                }
                defaultDueDate={
                  currentView.kind === "today"
                    ? new Date().toISOString().slice(0, 10)
                    : null
                }
              />

              {/* Task Ledger Table */}
              <div className="bg-white border border-[#E2E5EB] rounded-lg shadow-2xs overflow-hidden">
                {loading ? (
                  <div className="p-8 text-center text-xs text-[#94A3B8]">
                    Loading task ledger...
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="p-12 text-center space-y-2">
                    <p className="text-sm font-medium text-[#1A1D20]">
                      No tasks found in this view
                    </p>
                    <p className="text-xs text-[#64748B]">
                      Type above to log a new task into the ledger.
                    </p>
                  </div>
                ) : (
                  <div>
                    {tasks.map((task) => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        lists={lists}
                        tags={tags}
                        onToggleComplete={handleToggleComplete}
                        onEdit={setEditingTask}
                        onDelete={handleDeleteTask}
                      />
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </main>

      {/* Modals */}
      <TaskEditModal
        task={editingTask}
        lists={lists}
        tags={tags}
        onClose={() => setEditingTask(null)}
        onSave={handleUpdateTask}
      />

      <ListModal
        isOpen={isListModalOpen}
        onClose={() => setIsListModalOpen(false)}
        onCreateList={handleCreateList}
      />

      <TagModal
        isOpen={isTagModalOpen}
        onClose={() => setIsTagModalOpen(false)}
        onCreateTag={handleCreateTag}
      />
    </div>
  );
}
