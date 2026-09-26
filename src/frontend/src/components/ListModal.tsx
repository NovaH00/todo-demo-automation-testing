"use client";

import React, { useState } from "react";
import { X } from "lucide-react";
import { ListCreateInput } from "@/types";

interface ListModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateList: (data: ListCreateInput) => Promise<void>;
}

const COLOR_PRESETS = [
  "#2563EB", // Blue
  "#059669", // Emerald
  "#D97706", // Amber
  "#DC2626", // Red
  "#7C3AED", // Purple
  "#DB2777", // Pink
  "#4B5563", // Gray
];

export function ListModal({ isOpen, onClose, onCreateList }: ListModalProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [color, setColor] = useState(COLOR_PRESETS[0]);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || submitting) return;

    setSubmitting(true);
    try {
      await onCreateList({
        name: name.trim(),
        description: description.trim() || null,
        color,
      });
      setName("");
      setDescription("");
      setColor(COLOR_PRESETS[0]);
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-xs p-4">
      <div className="bg-white border border-[#E2E5EB] rounded-lg shadow-xl w-full max-w-sm overflow-hidden animate-in fade-in zoom-in-95 duration-100">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#E2E5EB]">
          <h2 className="text-sm font-semibold text-[#1A1D20]">New List</h2>
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
              List Name
            </label>
            <input
              type="text"
              required
              autoFocus
              placeholder="e.g. Engineering, Work, Home"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full text-sm px-3 py-2 border border-[#E2E5EB] rounded-md focus:border-[#1D4ED8] focus:ring-1 focus:ring-[#1D4ED8] outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#64748B] mb-1">
              Description (optional)
            </label>
            <input
              type="text"
              placeholder="Brief purpose of this list"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full text-sm px-3 py-2 border border-[#E2E5EB] rounded-md focus:border-[#1D4ED8] focus:ring-1 focus:ring-[#1D4ED8] outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#64748B] mb-1.5">
              Accent Color
            </label>
            <div className="flex items-center gap-2">
              {COLOR_PRESETS.map((c) => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setColor(c)}
                  className={`w-6 h-6 rounded-full transition-transform ${
                    color === c ? "ring-2 ring-offset-2 ring-[#1D4ED8] scale-110" : ""
                  }`}
                  style={{ backgroundColor: c }}
                />
              ))}
            </div>
          </div>

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
              disabled={submitting}
              className="px-3.5 py-1.5 bg-[#1D4ED8] hover:bg-[#1E40AF] text-white text-xs font-medium rounded transition-colors disabled:opacity-50"
            >
              {submitting ? "Creating..." : "Create list"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
