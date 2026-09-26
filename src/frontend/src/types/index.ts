export type TaskPriority = "low" | "medium" | "high";

export type TaskStatusFilter = "all" | "pending" | "completed";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  priority: TaskPriority;
  due_date: string | null;
  list_id: number | null;
  recurrence: string;
  tag_ids: number[];
  created_at: string;
  updated_at: string;
}

export interface TaskCreateInput {
  title: string;
  description?: string | null;
  is_completed?: boolean;
  priority?: TaskPriority;
  due_date?: string | null;
  list_id?: number | null;
  recurrence?: string;
  tag_ids?: number[];
}

export interface TaskUpdateInput {
  title?: string;
  description?: string | null;
  is_completed?: boolean;
  priority?: TaskPriority;
  due_date?: string | null;
  list_id?: number | null;
  recurrence?: string;
  tag_ids?: number[];
}

export interface TodoList {
  id: number;
  name: string;
  description: string | null;
  color: string | null;
  task_count: number;
  created_at: string;
  updated_at: string;
}

export interface ListCreateInput {
  name: string;
  description?: string | null;
  color?: string | null;
}

export interface Tag {
  id: number;
  name: string;
  color: string | null;
  created_at: string;
}

export interface TagCreateInput {
  name: string;
  color?: string | null;
}

export interface ScheduleOverview {
  overdue_count: number;
  today_count: number;
  upcoming_count: number;
  tasks_today: Task[];
  tasks_overdue: Task[];
}

export type ViewType =
  | { kind: "all" }
  | { kind: "today" }
  | { kind: "overdue" }
  | { kind: "upcoming" }
  | { kind: "list"; listId: number }
  | { kind: "tag"; tagId: number };
