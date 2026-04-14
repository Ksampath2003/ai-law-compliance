import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { RiskLevel, LawStatus } from "@/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const RISK_CONFIG: Record<RiskLevel, { label: string; color: string; bg: string }> = {
  high:   { label: "High Risk",   color: "text-red-400",    bg: "bg-red-500/10 border-red-500/30" },
  medium: { label: "Medium Risk", color: "text-amber-400",  bg: "bg-amber-500/10 border-amber-500/30" },
  low:    { label: "Low Risk",    color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30" },
};

export const STATUS_CONFIG: Record<LawStatus, { label: string; color: string; dot: string }> = {
  active:   { label: "Active",   color: "text-emerald-400", dot: "bg-emerald-400" },
  pending:  { label: "Pending",  color: "text-amber-400",   dot: "bg-amber-400" },
  failed:   { label: "Failed",   color: "text-slate-400",   dot: "bg-slate-400" },
  repealed: { label: "Repealed", color: "text-red-400",     dot: "bg-red-400" },
};

export const US_STATES: Record<string, string> = {
  AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California",
  CO: "Colorado", CT: "Connecticut", DE: "Delaware", FL: "Florida", GA: "Georgia",
  HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa",
  KS: "Kansas", KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
  MA: "Massachusetts", MI: "Michigan", MN: "Minnesota", MS: "Mississippi", MO: "Missouri",
  MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire", NJ: "New Jersey",
  NM: "New Mexico", NY: "New York", NC: "North Carolina", ND: "North Dakota", OH: "Ohio",
  OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
  SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
  VA: "Virginia", WA: "Washington", WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming",
};

export const AI_USAGE_TYPES = [
  { value: "LLM", label: "Large Language Models (ChatGPT, Claude, etc.)" },
  { value: "computer_vision", label: "Computer Vision / Image Recognition" },
  { value: "automated_decision", label: "Automated Decision Systems" },
  { value: "NLP", label: "Natural Language Processing" },
  { value: "facial_recognition", label: "Facial Recognition" },
  { value: "predictive_analytics", label: "Predictive Analytics / ML Models" },
  { value: "hiring_ai", label: "AI in Hiring / HR" },
  { value: "recommendation", label: "Recommendation Systems" },
];

export const INDUSTRIES = [
  "technology", "healthcare", "finance", "retail", "manufacturing",
  "education", "legal", "real_estate", "insurance", "government",
  "media", "transportation", "energy", "staffing",
];
