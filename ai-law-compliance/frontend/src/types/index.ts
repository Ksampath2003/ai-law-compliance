export type LawStatus = "active" | "pending" | "failed" | "repealed";
export type RiskLevel = "high" | "medium" | "low";

export interface LawListItem {
  id: string;
  title: string;
  state: string;
  status: LawStatus;
  risk_level: RiskLevel;
  ai_category: string | null;
  effective_date: string | null;
  plain_english_summary: string | null;
}

export interface LawDetail extends LawListItem {
  summary: string;
  full_text: string | null;
  industries_affected: string[];
  compliance_steps: string[];
  source_url: string | null;
  last_updated: string;
  is_ai_relevant: boolean;
  vector_indexed: boolean;
}

export interface ComplianceRequest {
  industry: string;
  state: string;
  ai_usage_types: string[];
  company_description?: string;
}

export interface LawApplicability {
  law_id: string;
  law_title: string;
  applicable: boolean;
  reason: string;
  risk_level: RiskLevel;
  compliance_steps: string[];
  status: LawStatus;
}

export interface ComplianceResponse {
  state: string;
  industry: string;
  ai_usage_types: string[];
  applicable_laws: LawApplicability[];
  total_laws_checked: number;
  high_risk_count: number;
  summary: string;
}

export interface SearchRequest {
  query: string;
  state?: string;
  status?: LawStatus;
  risk_level?: RiskLevel;
  top_k?: number;
}

export interface SearchResult {
  law: LawListItem;
  score: number;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
}
