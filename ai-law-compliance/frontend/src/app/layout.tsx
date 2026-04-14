import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Law Compliance | Track U.S. AI Legislation",
  description: "Track, understand, and comply with AI-specific laws across all U.S. states.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
