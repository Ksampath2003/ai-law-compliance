"use client";
import { useEffect, useState, useCallback } from "react";
import { BookOpen, Filter, X } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import LawCard from "@/components/LawCard";
import { Skeleton, EmptyState, ErrorMessage } from "@/components/ui";
import { api } from "@/lib/api";
import { US_STATES } from "@/lib/utils";
import type { LawListItem, RiskLevel, LawStatus } from "@/types";

const STAT_CARDS = [
  { label: "Laws Tracked", value: null as number | null, key: "total" },
  { label: "Active Laws",  value: null as number | null, key: "active" },
  { label: "High Risk",    value: null as number | null, key: "high" },
  { label: "States",       value: null as number | null, key: "states" },
];

export default function HomePage() {
  const [laws, setLaws] = useState<LawListItem[]>([]);
  const [filtered, setFiltered] = useState<LawListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stateFilter, setStateFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState<LawStatus | "">("");
  const [riskFilter, setRiskFilter] = useState<RiskLevel | "">("");

  useEffect(() => {
    api.getLaws()
      .then(data => { setLaws(data); setFiltered(data); })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    let result = laws;
    if (stateFilter) result = result.filter(l => l.state === stateFilter);
    if (statusFilter) result = result.filter(l => l.status === statusFilter);
    if (riskFilter) result = result.filter(l => l.risk_level === riskFilter);
    setFiltered(result);
  }, [laws, stateFilter, statusFilter, riskFilter]);

  const stats = {
    total: laws.length,
    active: laws.filter(l => l.status === "active").length,
    high: laws.filter(l => l.risk_level === "high").length,
    states: new Set(laws.map(l => l.state)).size,
  };

  const hasFilters = stateFilter || statusFilter || riskFilter;
  const clearFilters = () => { setStateFilter(""); setStatusFilter(""); setRiskFilter(""); };

  return (
    <div className="min-h-screen relative z-10">
      <Navbar />
      <main className="max-w-6xl mx-auto px-6 py-10">

        {/* Hero */}
        <div className="mb-10">
          <div className="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full mb-4"
            style={{ background: "rgba(59,110,240,0.1)", border: "1px solid rgba(59,110,240,0.25)", color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
            <span className="status-dot bg-blue-400" />
            AI-specific laws only
          </div>
          <h1 className="text-4xl font-800 tracking-tight mb-3"
            style={{ fontFamily: "var(--font-display)", fontWeight: 800, color: "var(--text-primary)" }}>
            U.S. AI Law Tracker
          </h1>
          <p className="text-base max-w-xl" style={{ color: "var(--text-secondary)" }}>
            Track every AI-specific law across all 50 states — filtered, explained in plain English, and mapped to your compliance obligations.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {[
            { label: "Laws Tracked", value: stats.total },
            { label: "Active", value: stats.active },
            { label: "High Risk", value: stats.high },
            { label: "States", value: stats.states },
          ].map(({ label, value }) => (
            <div key={label} className="card p-4 text-center">
              {loading
                ? <Skeleton className="h-8 w-12 mx-auto mb-1" />
                : <div className="text-3xl font-800 mb-0.5"
                    style={{ fontFamily: "var(--font-display)", fontWeight: 800, color: "var(--brand-light)" }}>
                    {value}
                  </div>
              }
              <div className="text-xs" style={{ color: "var(--text-secondary)" }}>{label}</div>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <div className="flex items-center gap-2 text-xs font-medium" style={{ color: "var(--text-secondary)", fontFamily: "var(--font-display)" }}>
            <Filter size={12} /> Filters
          </div>

          <select value={stateFilter} onChange={e => setStateFilter(e.target.value)}
            className="input-field" style={{ width: "auto", paddingRight: "32px" }}>
            <option value="">All States</option>
            {Object.entries(US_STATES).map(([code, name]) => (
              <option key={code} value={code}>{code} — {name}</option>
            ))}
          </select>

          <select value={statusFilter} onChange={e => setStatusFilter(e.target.value as LawStatus | "")}
            className="input-field" style={{ width: "auto" }}>
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="pending">Pending</option>
          </select>

          <select value={riskFilter} onChange={e => setRiskFilter(e.target.value as RiskLevel | "")}
            className="input-field" style={{ width: "auto" }}>
            <option value="">All Risk Levels</option>
            <option value="high">High Risk</option>
            <option value="medium">Medium Risk</option>
            <option value="low">Low Risk</option>
          </select>

          {hasFilters && (
            <button onClick={clearFilters}
              className="flex items-center gap-1.5 text-xs px-3 py-2 rounded-lg transition-colors"
              style={{ color: "var(--text-secondary)", border: "1px solid var(--border)" }}>
              <X size={11} /> Clear
            </button>
          )}

          <span className="ml-auto text-xs" style={{ color: "var(--text-muted)" }}>
            {filtered.length} result{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        {/* Content */}
        {error && <ErrorMessage message={error} />}

        {loading ? (
          <div className="grid gap-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="card p-5">
                <Skeleton className="h-4 w-3/4 mb-3" />
                <Skeleton className="h-3 w-full mb-1" />
                <Skeleton className="h-3 w-2/3 mb-4" />
                <div className="flex gap-3">
                  <Skeleton className="h-3 w-12" />
                  <Skeleton className="h-3 w-20" />
                  <Skeleton className="h-5 w-16 ml-auto rounded-full" />
                </div>
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={<BookOpen size={22} style={{ color: "var(--text-muted)" }} />}
            title="No laws found"
            description={hasFilters ? "Try adjusting your filters." : "No AI laws are tracked yet. Run the seed script to populate data."}
          />
        ) : (
          <div className="grid gap-3">
            {filtered.map(law => <LawCard key={law.id} law={law} />)}
          </div>
        )}
      </main>
    </div>
  );
}
