"use client";
import { useState } from "react";
import { Search, Sparkles } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import LawCard from "@/components/LawCard";
import { EmptyState, ErrorMessage } from "@/components/ui";
import { api } from "@/lib/api";
import { US_STATES } from "@/lib/utils";
import type { SearchResult, RiskLevel, LawStatus } from "@/types";

const EXAMPLE_QUERIES = [
  "automated hiring decisions and bias audits",
  "generative AI training data transparency",
  "facial recognition in employment",
  "algorithmic decision systems in healthcare",
  "AI video interview requirements",
];

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stateFilter, setStateFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState<LawStatus | "">("");
  const [riskFilter, setRiskFilter] = useState<RiskLevel | "">("");

  const handleSearch = async (q?: string) => {
    const searchQuery = q || query;
    if (!searchQuery.trim()) return;
    setLoading(true);
    setError(null);
    setSearched(true);
    try {
      const data = await api.search({
        query: searchQuery,
        state: stateFilter || undefined,
        status: statusFilter || undefined,
        risk_level: riskFilter || undefined,
        top_k: 15,
      });
      setResults(data.results);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative z-10">
      <Navbar />
      <main className="max-w-3xl mx-auto px-6 py-10">
        <div className="mb-10">
          <h1 className="text-3xl font-800 tracking-tight mb-2"
            style={{ fontFamily: "var(--font-display)", fontWeight: 800, color: "var(--text-primary)" }}>
            Semantic Search
          </h1>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
            Describe your AI use case and find relevant legislation instantly.
          </p>
        </div>

        {/* Search box */}
        <div className="card p-5 mb-6">
          <div className="relative mb-4">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2"
              style={{ color: "var(--text-muted)" }} />
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleSearch()}
              placeholder="e.g. we use AI to screen job applicants in New York…"
              className="input-field pl-9"
            />
          </div>

          {/* Filters row */}
          <div className="flex flex-wrap gap-2 mb-4">
            <select value={stateFilter} onChange={e => setStateFilter(e.target.value)}
              className="input-field text-xs" style={{ width: "auto" }}>
              <option value="">All States</option>
              {Object.entries(US_STATES).map(([code, name]) => (
                <option key={code} value={code}>{code} — {name}</option>
              ))}
            </select>
            <select value={statusFilter} onChange={e => setStatusFilter(e.target.value as LawStatus | "")}
              className="input-field text-xs" style={{ width: "auto" }}>
              <option value="">Any Status</option>
              <option value="active">Active</option>
              <option value="pending">Pending</option>
            </select>
            <select value={riskFilter} onChange={e => setRiskFilter(e.target.value as RiskLevel | "")}
              className="input-field text-xs" style={{ width: "auto" }}>
              <option value="">Any Risk</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <button onClick={() => handleSearch()} disabled={loading || !query.trim()} className="btn-primary w-full">
            {loading ? "Searching…" : "Search Laws"}
          </button>
        </div>

        {/* Example queries */}
        {!searched && (
          <div>
            <div className="flex items-center gap-2 text-xs mb-3"
              style={{ color: "var(--text-muted)", fontFamily: "var(--font-display)" }}>
              <Sparkles size={11} /> Try these examples
            </div>
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_QUERIES.map(q => (
                <button key={q} onClick={() => { setQuery(q); handleSearch(q); }}
                  className="text-xs px-3 py-1.5 rounded-lg transition-all"
                  style={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", color: "var(--text-secondary)" }}>
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {error && <ErrorMessage message={error} />}

        {/* Results */}
        {searched && !loading && results.length === 0 && !error && (
          <EmptyState
            icon={<Search size={20} style={{ color: "var(--text-muted)" }} />}
            title="No matches found"
            description="Try broadening your query or removing filters."
          />
        )}

        {results.length > 0 && (
          <div>
            <div className="text-xs mb-4" style={{ color: "var(--text-muted)" }}>
              {results.length} result{results.length !== 1 ? "s" : ""} — ranked by relevance
            </div>
            <div className="grid gap-3">
              {results.map(({ law, score }) => (
                <div key={law.id} className="relative">
                  <LawCard law={law} />
                  <div className="absolute top-3 right-10 text-xs font-mono"
                    style={{ color: "var(--text-muted)" }}>
                    {(score * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
