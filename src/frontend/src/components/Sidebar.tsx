"use client";

import React from "react";
import {
  Calendar,
  CheckCircle2,
  Clock,
  Inbox,
  Plus,
} from "lucide-react";
import { ScheduleOverview, Tag, TodoList, ViewType } from "@/types";

interface SidebarProps {
  currentView: ViewType;
  onSelectView: (view: ViewType) => void;
  lists: TodoList[];
  tags: Tag[];
  scheduleOverview: ScheduleOverview | null;
  totalTaskCount: number;
  onOpenNewList: () => void;
  onOpenNewTag: () => void;
  backendOnline: boolean;
}

export function Sidebar({
  currentView,
  onSelectView,
  lists,
  tags,
  scheduleOverview,
  totalTaskCount,
  onOpenNewList,
  onOpenNewTag,
  backendOnline,
}: SidebarProps) {
  const isViewActive = (kind: string, id?: number) => {
    if (currentView.kind !== kind) return false;
    if (kind === "list" && "listId" in currentView) return currentView.listId === id;
    if (kind === "tag" && "tagId" in currentView) return currentView.tagId === id;
    return true;
  };

  return (
    <aside className="w-64 bg-white border-r border-[#E2E5EB] flex flex-col h-screen select-none shrink-0">
      {/* Brand Header */}
      <div className="px-5 py-4 border-b border-[#E2E5EB] flex items-center justify-between">
        <div>
          <div className="text-base font-semibold tracking-tight text-[#1A1D20]">
            Task Ledger
          </div>
          <div className="text-xs text-[#64748B]">FastAPI + Next.js</div>
        </div>
        <div
          title={backendOnline ? "Backend connected" : "Backend disconnected (start FastAPI at :8000)"}
          className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-medium border"
          style={{
            borderColor: backendOnline ? "#BBF7D0" : "#FECACA",
            backgroundColor: backendOnline ? "#F0FDF4" : "#FEF2F2",
            color: backendOnline ? "#166534" : "#991B1B",
          }}
        >
          <span
            className="w-1.5 h-1.5 rounded-full"
            style={{ backgroundColor: backendOnline ? "#22C55E" : "#EF4444" }}
          />
          {backendOnline ? "API Live" : "API Offline"}
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {/* Core Views */}
        <div>
          <div className="px-2 mb-1.5 text-xs font-medium text-[#64748B]">
            Views
          </div>
          <ul className="space-y-0.5">
            <li>
              <button
                type="button"
                onClick={() => onSelectView({ kind: "all" })}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 text-sm rounded-md transition-colors ${
                  isViewActive("all")
                    ? "bg-[#1D4ED8] text-white font-medium"
                    : "text-[#1A1D20] hover:bg-[#F1F3F7]"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Inbox className="w-4 h-4 opacity-80" />
                  <span>All Tasks</span>
                </div>
                <span
                  className={`text-xs tabular-nums px-1.5 py-0.5 rounded ${
                    isViewActive("all") ? "bg-blue-800 text-white" : "text-[#64748B]"
                  }`}
                >
                  {totalTaskCount}
                </span>
              </button>
            </li>

            <li>
              <button
                type="button"
                onClick={() => onSelectView({ kind: "today" })}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 text-sm rounded-md transition-colors ${
                  isViewActive("today")
                    ? "bg-[#1D4ED8] text-white font-medium"
                    : "text-[#1A1D20] hover:bg-[#F1F3F7]"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Clock className="w-4 h-4 opacity-80 text-amber-600" />
                  <span>Today</span>
                </div>
                {scheduleOverview && (
                  <span
                    className={`text-xs tabular-nums px-1.5 py-0.5 rounded ${
                      isViewActive("today") ? "bg-blue-800 text-white" : "text-amber-700 bg-amber-50"
                    }`}
                  >
                    {scheduleOverview.today_count}
                  </span>
                )}
              </button>
            </li>

            <li>
              <button
                type="button"
                onClick={() => onSelectView({ kind: "overdue" })}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 text-sm rounded-md transition-colors ${
                  isViewActive("overdue")
                    ? "bg-[#1D4ED8] text-white font-medium"
                    : "text-[#1A1D20] hover:bg-[#F1F3F7]"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className="w-4 h-4 opacity-80 text-red-600" />
                  <span>Overdue</span>
                </div>
                {scheduleOverview && scheduleOverview.overdue_count > 0 && (
                  <span
                    className={`text-xs tabular-nums px-1.5 py-0.5 rounded font-medium ${
                      isViewActive("overdue") ? "bg-blue-800 text-white" : "text-red-700 bg-red-50"
                    }`}
                  >
                    {scheduleOverview.overdue_count}
                  </span>
                )}
              </button>
            </li>

            <li>
              <button
                type="button"
                onClick={() => onSelectView({ kind: "upcoming" })}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 text-sm rounded-md transition-colors ${
                  isViewActive("upcoming")
                    ? "bg-[#1D4ED8] text-white font-medium"
                    : "text-[#1A1D20] hover:bg-[#F1F3F7]"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Calendar className="w-4 h-4 opacity-80 text-blue-600" />
                  <span>Upcoming Schedule</span>
                </div>
                {scheduleOverview && (
                  <span
                    className={`text-xs tabular-nums px-1.5 py-0.5 rounded ${
                      isViewActive("upcoming") ? "bg-blue-800 text-white" : "text-[#64748B]"
                    }`}
                  >
                    {scheduleOverview.upcoming_count}
                  </span>
                )}
              </button>
            </li>
          </ul>
        </div>

        {/* Lists Section */}
        <div>
          <div className="flex items-center justify-between px-2 mb-1.5">
            <span className="text-xs font-medium text-[#64748B]">Lists</span>
            <button
              type="button"
              onClick={onOpenNewList}
              className="text-[#64748B] hover:text-[#1A1D20] p-0.5 rounded hover:bg-[#F1F3F7]"
              title="Create new list"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>

          {lists.length === 0 ? (
            <div className="px-2 py-2 text-xs text-[#94A3B8] italic">
              No lists created yet.
            </div>
          ) : (
            <ul className="space-y-0.5">
              {lists.map((list) => {
                const active = isViewActive("list", list.id);
                return (
                  <li key={list.id}>
                    <button
                      type="button"
                      onClick={() => onSelectView({ kind: "list", listId: list.id })}
                      className={`w-full flex items-center justify-between px-2.5 py-1.5 text-sm rounded-md transition-colors ${
                        active
                          ? "bg-[#1D4ED8] text-white font-medium"
                          : "text-[#1A1D20] hover:bg-[#F1F3F7]"
                      }`}
                    >
                      <div className="flex items-center gap-2 truncate">
                        <span
                          className="w-2.5 h-2.5 rounded-full shrink-0"
                          style={{ backgroundColor: list.color || "#64748B" }}
                        />
                        <span className="truncate">{list.name}</span>
                      </div>
                      <span
                        className={`text-xs tabular-nums px-1.5 py-0.5 rounded ${
                          active ? "bg-blue-800 text-white" : "text-[#64748B]"
                        }`}
                      >
                        {list.task_count}
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        {/* Tags Section */}
        <div>
          <div className="flex items-center justify-between px-2 mb-1.5">
            <span className="text-xs font-medium text-[#64748B]">Tags</span>
            <button
              type="button"
              onClick={onOpenNewTag}
              className="text-[#64748B] hover:text-[#1A1D20] p-0.5 rounded hover:bg-[#F1F3F7]"
              title="Create new tag"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>

          {tags.length === 0 ? (
            <div className="px-2 py-2 text-xs text-[#94A3B8] italic">
              No tags created yet.
            </div>
          ) : (
            <div className="flex flex-wrap gap-1 px-1">
              {tags.map((tag) => {
                const active = isViewActive("tag", tag.id);
                return (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => onSelectView({ kind: "tag", tagId: tag.id })}
                    className={`inline-flex items-center gap-1.5 px-2 py-1 text-xs rounded border transition-colors ${
                      active
                        ? "bg-[#1D4ED8] text-white border-[#1D4ED8] font-medium"
                        : "bg-white text-[#1A1D20] border-[#E2E5EB] hover:bg-[#F1F3F7]"
                    }`}
                  >
                    <span
                      className="w-1.5 h-1.5 rounded-full"
                      style={{ backgroundColor: tag.color || "#64748B" }}
                    />
                    <span>{tag.name}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </nav>

      {/* Footer info */}
      <div className="p-3 border-t border-[#E2E5EB] text-[11px] text-[#64748B]">
        Draftsman workspace mode
      </div>
    </aside>
  );
}
