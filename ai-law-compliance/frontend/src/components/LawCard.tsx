"use client";
import Link from "next/link";
import { ArrowRight, MapPin, Calendar, Tag } from "lucide-react";
import { RiskBadge, StatusBadge } from "@/components/ui";
import type { LawListItem } from "@/types";

export default function LawCard({ law }: { law: LawListItem }) {
  return (
    <Link href={`/laws/${law.id}`} className="block card card-hover p-5 fade-in">
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="text-sm font-semibold leading-snug flex-1"
          style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
          {law.title}
        </h3>
        <ArrowRight size={14} style={{ color: "var(--text-muted)", flexShrink: 0, marginTop: 2 }} />
      </div>

      {law.plain_english_summary && (
        <p className="text-xs leading-relaxed mb-4 line-clamp-2"
          style={{ color: "var(--text-secondary)" }}>
          {law.plain_english_summary}
        </p>
      )}

      <div className="flex flex-wrap items-center gap-3 mt-auto">
        <div className="flex items-center gap-1.5 text-xs" style={{ color: "var(--text-secondary)" }}>
          <MapPin size={11} />
          <span className="font-mono font-medium" style={{ color: "var(--brand-light)" }}>{law.state}</span>
        </div>

        {law.ai_category && (
          <div className="flex items-center gap-1.5 text-xs" style={{ color: "var(--text-secondary)" }}>
            <Tag size={11} />
            {law.ai_category}
          </div>
        )}

        {law.effective_date && (
          <div className="flex items-center gap-1.5 text-xs" style={{ color: "var(--text-secondary)" }}>
            <Calendar size={11} />
            {law.effective_date}
          </div>
        )}

        <div className="ml-auto flex items-center gap-2">
          <StatusBadge status={law.status} />
          <RiskBadge level={law.risk_level} />
        </div>
      </div>
    </Link>
  );
}
