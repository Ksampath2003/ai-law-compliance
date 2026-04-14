import type { RiskLevel, LawStatus } from "@/types";
import { RISK_CONFIG, STATUS_CONFIG } from "@/lib/utils";

export function RiskBadge({ level }: { level: RiskLevel }) {
  const c = RISK_CONFIG[level];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${c.bg} ${c.color}`}
      style={{ fontFamily: "var(--font-display)" }}>
      {c.label}
    </span>
  );
}

export function StatusBadge({ status }: { status: LawStatus }) {
  const c = STATUS_CONFIG[status];
  return (
    <span className={`inline-flex items-center text-xs font-medium ${c.color}`}>
      <span className={`status-dot ${c.dot}`} />
      {c.label}
    </span>
  );
}

export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`skeleton ${className}`} />;
}

export function EmptyState({ icon, title, description }: {
  icon: React.ReactNode; title: string; description: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: "var(--bg-elevated)", border: "1px solid var(--border)" }}>
        {icon}
      </div>
      <h3 className="text-base font-semibold mb-1" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
        {title}
      </h3>
      <p className="text-sm max-w-xs" style={{ color: "var(--text-secondary)" }}>{description}</p>
    </div>
  );
}

export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="rounded-xl p-4 text-sm"
      style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.2)", color: "#f87171" }}>
      ⚠️ {message}
    </div>
  );
}
