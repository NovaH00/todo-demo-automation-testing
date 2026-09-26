import {
  ListCreateInput,
  ScheduleOverview,
  Tag,
  TagCreateInput,
  Task,
  TaskCreateInput,
  TaskUpdateInput,
  TodoList,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    let errorDetail = `Request failed with status ${res.status}`;
    try {
      const errorJson = await res.json();
      if (errorJson.detail) {
        errorDetail = typeof errorJson.detail === "string"
          ? errorJson.detail
          : JSON.stringify(errorJson.detail);
      }
    } catch {
      // Use fallback error message
    }
    throw new Error(errorDetail);
  }

  if (res.status === 204) {
    return null as unknown as T;
  }

  return res.json();
}

export const api = {
  // Health
  checkHealth: () => request<{ status: string; app: string; version: string }>("/health"),

  // Tasks
  getTasks: (params?: {
    status?: string;
    priority?: string;
    search?: string;
    list_id?: number;
    tag_id?: number;
  }) => {
    const query = new URLSearchParams();
    if (params?.status && params.status !== "all") query.set("status", params.status);
    if (params?.priority) query.set("priority", params.priority);
    if (params?.search) query.set("search", params.search);
    if (params?.list_id !== undefined) query.set("list_id", String(params.list_id));
    if (params?.tag_id !== undefined) query.set("tag_id", String(params.tag_id));
    const qs = query.toString();
    return request<Task[]>(`/tasks/${qs ? `?${qs}` : ""}`);
  },

  getTask: (id: number) => request<Task>(`/tasks/${id}`),

  createTask: (data: TaskCreateInput) =>
    request<Task>("/tasks/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateTask: (id: number, data: TaskUpdateInput) =>
    request<Task>(`/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  deleteTask: (id: number) =>
    request<null>(`/tasks/${id}`, {
      method: "DELETE",
    }),

  // Lists
  getLists: () => request<TodoList[]>("/lists/"),

  getList: (id: number) => request<TodoList>(`/lists/${id}`),

  createList: (data: ListCreateInput) =>
    request<TodoList>("/lists/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateList: (id: number, data: Partial<ListCreateInput>) =>
    request<TodoList>(`/lists/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  deleteList: (id: number) =>
    request<null>(`/lists/${id}`, {
      method: "DELETE",
    }),

  // Tags
  getTags: () => request<Tag[]>("/tags/"),

  createTag: (data: TagCreateInput) =>
    request<Tag>("/tags/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  deleteTag: (id: number) =>
    request<null>(`/tags/${id}`, {
      method: "DELETE",
    }),

  // Schedule
  getScheduleOverview: () => request<ScheduleOverview>("/schedule/overview"),

  getTodayTasks: () => request<Task[]>("/schedule/today"),

  getOverdueTasks: () => request<Task[]>("/schedule/overdue"),

  getUpcomingTasks: (days: number = 7) => request<Task[]>(`/schedule/upcoming?days=${days}`),

  reschedule: (taskIds: number[], newDueDate: string | null) =>
    request<Task[]>("/schedule/reschedule", {
      method: "POST",
      body: JSON.stringify({ task_ids: taskIds, new_due_date: newDueDate }),
    }),
};
