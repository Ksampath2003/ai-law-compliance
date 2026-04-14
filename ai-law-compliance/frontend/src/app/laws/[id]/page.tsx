"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, ExternalLink, CheckSquare, Calendar, Building2, Tag } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import { RiskBadge, StatusBadge, Skeleton, ErrorMessage } from "@/components/ui";
import { api } from "@/lib/api";
import { US_STATES } from "@/lib/utils";
import type { LawDetail } from "@/types";

export default function LawDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [law, setLaw] = useState<LawDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api.getLaw(id)
      .then(setLaw)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <div className="min-h-screen relative z-10">
      <Navbar />
      <main className="max-w-3xl mx-auto px-6 py-10">
        <Link href="/" className="inline-flex items-center gap-2 text-sm mb-8 transition-colors"
          style={{ color: "var(--text-secondary)" }}
          onMouseEnter={e => (e.currentTarget.style.color = "var(--text-primary)")}
          onMouseLeave={e => (e.currentTarget.style.color = "var(--text-secondary)")}>
          <ArrowLeft size={14} /> Back to Laws
        </Link>

        {error && <ErrorMessage message={error} />}

        {loading ? (
          <div>
            <Skeleton className="h-8 w-3/4 mb-4" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-2/3 mb-8" />
            <Skeleton className="h-32 w-full mb-4" />
            <Skeleton className="h-48 w-full" />
          </div>
        ) : law ? (
          <div className="fade-in">
            {/* Header */}
            <div className="mb-8">
              <div className="flex flex-wrap items-center gap-2 mb-4">
                <span className="font-mono text-sm px-2.5 py-1 rounded"
                  style={{ background: "rgba(59,110,240,0.1)", color: "var(--brand-light)", border: "1px solid rgba(59,110,240,0.2)" }}>
                  {law.state} — {US_STATES[law.state] || law.state}
                </span>
                <StatusBadge status={law.status} />
                <RiskBadge level={law.risk_level} />
              </div>
              <h1 className="text-2xl font-800 leading-snug mb-4"
                style={{ fontFamily: "var(--font-display)", fontWeight: 800, color: "var(--text-primary)" }}>
                {law.title}
              </h1>

              <div className="flex flex-wrap gap-4 text-xs" style={{ color: "var(--text-secondary)" }}>
                {law.effective_date && (
                  <div className="flex items-center gap-1.5">
                    <Calendar size={11} /> Effective {law.effective_date}
                  </div>
                )}
                {law.ai_category && (
                  <div className="flex items-center gap-1.5">
                    <Tag size={11} /> {law.ai_category}
                  </div>
                )}
                {law.industries_affected?.length > 0 && (
                  <div className="flex items-center gap-1.5">
                    <Building2 size={11} /> {law.industries_affected.join(", ")}
                  </div>
                )}
              </div>
            </div>

            {/* Plain English Summary */}
            {law.plain_english_summary && (
              <div className="card p-5 mb-5">
                <div className="text-xs font-semibold mb-2 uppercase tracking-wider"
                  style={{ color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
                  Plain English Summary
                </div>
                <p className="text-sm leading-relaxed" style={{ color: "var(--text-primary)" }}>
                  {law.plain_english_summary}
                </p>
              </div>
            )}

            {/* Technical Summary */}
            <div className="card p-5 mb-5">
              <div className="text-xs font-semibold mb-2 uppercase tracking-wider"
                style={{ color: "var(--text-secondary)", fontFamily: "var(--font-display)" }}>
                Technical Summary
              </div>
              <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                {law.summary}
              </p>
            </div>

            {/* Compliance Steps */}
            {law.compliance_steps?.length > 0 && (
              <div className="card p-5 mb-5">
                <div className="text-xs font-semibold mb-3 uppercase tracking-wider"
                  style={{ color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
                  Compliance Checklist
                </div>
                <ol className="space-y-3">
                  {law.compliance_steps.map((step, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-5 h-5 rounded flex items-center justify-center text-xs font-bold mt-0.5"
                        style={{ background: "rgba(59,110,240,0.15)", color: "var(--brand-light)", fontFamily: "var(--font-display)" }}>
                        {i + 1}
                      </div>
                      <span className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {/* Full Text */}
            {law.full_text && (
              <details className="card mb-5">
                <summary className="p-5 text-sm font-semibold cursor-pointer"
                  style={{ fontFamily: "var(--font-display)", color: "var(--text-secondary)" }}>
                  Full Legislative Text
                </summary>
                <div className="px-5 pb-5">
                  <p className="text-sm leading-relaxed whitespace-pre-wrap"
                    style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: "12px" }}>
                    {law.full_text}
                  </p>
                </div>
              </details>
            )}

            {/* Source */}
            {law.source_url && (
              <a href={law.source_url} target="_blank" rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm btn-primary">
                View Official Source <ExternalLink size={13} />
              </a>
            )}
          </div>
        ) : null}
      </main>
    </div>
  );
}
