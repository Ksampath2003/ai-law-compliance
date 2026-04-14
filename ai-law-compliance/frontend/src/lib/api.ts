import type {
  LawListItem, LawDetail, ComplianceRequest, ComplianceResponse,
  SearchRequest, SearchResponse
} from "@/types";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Laws
  getLaws: (params?: { state?: string; status?: string; risk_level?: string }) => {
    const qs = new URLSearchParams();
    if (params?.state) qs.set("state", params.state);
    if (params?.status) qs.set("status", params.status);
    if (params?.risk_level) qs.set("risk_level", params.risk_level);
    return request<LawListItem[]>(`/api/laws?${qs}`);
  },
  getLaw: (id: string) => request<LawDetail>(`/api/laws/${id}`),
  getLawsByState: (state: string) => request<LawListItem[]>(`/api/laws/state/${state}`),

  // Compliance
  analyzeCompliance: (body: ComplianceRequest) =>
    request<ComplianceResponse>("/api/compliance/analyze", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  // Search
  search: (body: SearchRequest) =>
    request<SearchResponse>("/api/search", {
      method: "POST",
      body: JSON.stringify(body),
    }),
};
