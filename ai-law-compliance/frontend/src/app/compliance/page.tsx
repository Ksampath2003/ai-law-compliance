"use client";
import { useState } from "react";
import { Shield, CheckCircle2, XCircle, AlertTriangle, ChevronDown, ChevronUp } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import { RiskBadge, StatusBadge, ErrorMessage } from "@/components/ui";
import { api } from "@/lib/api";
import { US_STATES, AI_USAGE_TYPES, INDUSTRIES, RISK_CONFIG } from "@/lib/utils";
import type { ComplianceResponse, LawApplicability } from "@/types";

function LawResult({ item }: { item: LawApplicability }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="card mb-3 overflow-hidden">
      <button className="w-full p-4 flex items-start gap-3 text-left"
        onClick={() => setOpen(o => !o)}>
        {item.applicable
          ? <AlertTriangle size={16} className="flex-shrink-0 mt-0.5" style={{ color: "#f59e0b" }} />
          : <CheckCircle2 size={16} className="flex-shrink-0 mt-0.5" style={{ color: "#10b981" }} />
        }
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="text-sm font-semibold" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
              {item.law_title}
            </span>
            <RiskBadge level={item.risk_level} />
            <StatusBadge status={item.status} />
          </div>
          <p className="text-xs" style={{ color: "var(--text-secondary)" }}>{item.reason}</p>
        </div>
        {open
          ? <ChevronUp size={14} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
          : <ChevronDown size={14} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
        }
      </button>

      {open && item.compliance_steps?.length > 0 && (
        <div className="px-4 pb-4 border-t" style={{ borderColor: "var(--border)" }}>
          <div className="text-xs font-semibold mb-2 mt-3 uppercase tracking-wider"
            style={{ color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
            Required Actions
          </div>
          <ol className="space-y-2">
            {item.compliance_steps.map((step, i) => (
              <li key={i} className="flex items-start gap-2.5">
                <span className="flex-shrink-0 w-4 h-4 rounded text-xs flex items-center justify-center font-bold mt-0.5"
                  style={{ background: "rgba(59,110,240,0.15)", color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
                  {i + 1}
                </span>
                <span className="text-xs leading-relaxed" style={{ color: "var(--text-secondary)" }}>{step}</span>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default function CompliancePage() {
  const [industry, setIndustry] = useState("");
  const [state, setState] = useState("");
  const [aiUsage, setAiUsage] = useState<string[]>([]);
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComplianceResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const toggleUsage = (val: string) =>
    setAiUsage(prev => prev.includes(val) ? prev.filter(v => v !== val) : [...prev, val]);

  const handleAnalyze = async () => {
    if (!industry || !state || aiUsage.length === 0) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.analyzeCompliance({
        industry, state, ai_usage_types: aiUsage,
        company_description: description || undefined,
      });
      setResult(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const applicable = result?.applicable_laws ?? [];
  const notApplicable: any[] = []; // compliance API returns only applicable ones

  return (
    <div className="min-h-screen relative z-10">
      <Navbar />
      <main className="max-w-3xl mx-auto px-6 py-10">
        <div className="mb-10">
          <h1 className="text-3xl font-800 tracking-tight mb-2"
            style={{ fontFamily: "var(--font-display)", fontWeight: 800, color: "var(--text-primary)" }}>
            Compliance Analyzer
          </h1>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
            Describe your company and AI usage. Get a tailored compliance report in seconds.
          </p>
        </div>

        {/* Form */}
        <div className="card p-6 mb-6">
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-xs font-semibold mb-1.5"
                style={{ fontFamily: "var(--font-display)", color: "var(--text-secondary)" }}>
                Industry *
              </label>
              <select value={industry} onChange={e => setIndustry(e.target.value)} className="input-field">
                <option value="">Select industry…</option>
                {INDUSTRIES.map(i => (
                  <option key={i} value={i}>{i.replace("_", " ").replace(/\b\w/g, c => c.toUpperCase())}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold mb-1.5"
                style={{ fontFamily: "var(--font-display)", color: "var(--text-secondary)" }}>
                Operating State *
              </label>
              <select value={state} onChange={e => setState(e.target.value)} className="input-field">
                <option value="">Select state…</option>
                {Object.entries(US_STATES).map(([code, name]) => (
                  <option key={code} value={code}>{code} — {name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-xs font-semibold mb-2"
              style={{ fontFamily: "var(--font-display)", color: "var(--text-secondary)" }}>
              AI Usage Types * <span style={{ color: "var(--text-muted)", fontWeight: 400 }}>(select all that apply)</span>
            </label>
            <div className="flex flex-wrap gap-2">
              {AI_USAGE_TYPES.map(({ value, label }) => {
                const active = aiUsage.includes(value);
                return (
                  <button key={value} onClick={() => toggleUsage(value)}
                    className="text-xs px-3 py-1.5 rounded-lg transition-all"
                    style={{
                      background: active ? "rgba(59,110,240,0.2)" : "var(--bg-elevated)",
                      border: `1px solid ${active ? "rgba(59,110,240,0.5)" : "var(--border)"}`,
                      color: active ? "var(--brand-light)" : "var(--text-secondary)",
                    }}>
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="mb-5">
            <label className="block text-xs font-semibold mb-1.5"
              style={{ fontFamily: "var(--font-display)", color: "var(--text-secondary)" }}>
              Company Description <span style={{ color: "var(--text-muted)", fontWeight: 400 }}>(optional, improves accuracy)</span>
            </label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} rows={2}
              placeholder="e.g. B2B SaaS company with 200 employees using AI to screen resumes and route customer support tickets…"
              className="input-field resize-none" />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading || !industry || !state || aiUsage.length === 0}
            className="btn-primary w-full flex items-center justify-center gap-2">
            <Shield size={14} />
            {loading ? "Analyzing…" : "Analyze Compliance"}
          </button>
        </div>

        {error && <ErrorMessage message={error} />}

        {/* Results */}
        {result && (
          <div className="fade-in">
            {/* Summary card */}
            <div className="card p-5 mb-6">
              <div className="flex items-center justify-between mb-3">
                <div className="text-xs font-semibold uppercase tracking-wider"
                  style={{ fontFamily: "var(--font-display)", color: "var(--brand-light)" }}>
                  Executive Summary
                </div>
                <div className="flex items-center gap-3 text-xs" style={{ color: "var(--text-muted)" }}>
                  <span>{result.total_laws_checked} laws checked</span>
                  <span>·</span>
                  <span style={{ color: "#f87171" }}>{result.high_risk_count} high risk</span>
                </div>
              </div>
              <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                {result.summary}
              </p>

              {/* Stats row */}
              <div className="grid grid-cols-3 gap-3 mt-4 pt-4 border-t" style={{ borderColor: "var(--border)" }}>
                {[
                  { label: "Applicable",    value: applicable.length, color: "#f59e0b" },
                  { label: "High Risk",     value: result.high_risk_count, color: "#f87171" },
                  { label: "Total Checked", value: result.total_laws_checked, color: "var(--brand-light)" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="text-center">
                    <div className="text-2xl font-800" style={{ fontFamily: "var(--font-display)", fontWeight: 800, color }}>
                      {value}
                    </div>
                    <div className="text-xs" style={{ color: "var(--text-muted)" }}>{label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Applicable laws */}
            {applicable.length > 0 && (
              <div className="mb-6">
                <h2 className="text-sm font-semibold mb-3"
                  style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
                  ⚠️ Applicable Laws — Action Required
                </h2>
                {applicable.map(item => <LawResult key={item.law_id} item={item} />)}
              </div>
            )}

            {applicable.length === 0 && (
              <div className="card p-6 text-center">
                <CheckCircle2 size={32} className="mx-auto mb-3" style={{ color: "#10b981" }} />
                <p className="text-sm font-semibold mb-1"
                  style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
                  No applicable laws found
                </p>
                <p className="text-xs" style={{ color: "var(--text-secondary)" }}>
                  Based on the laws we track for {result.state}, your profile does not trigger specific AI compliance obligations.
                  Continue monitoring as legislation evolves.
                </p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
