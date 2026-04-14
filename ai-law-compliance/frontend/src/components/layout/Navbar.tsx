"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Scale, Search, Shield, BookOpen } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/",           label: "Laws",       icon: BookOpen },
  { href: "/search",     label: "Search",     icon: Search },
  { href: "/compliance", label: "Compliance", icon: Shield },
];

export default function Navbar() {
  const path = usePathname();
  return (
    <header className="glass sticky top-0 z-50 border-b" style={{ borderColor: "var(--border)" }}>
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: "var(--brand)" }}>
            <Scale size={16} color="#fff" />
          </div>
          <span className="font-display font-700 text-base tracking-tight"
            style={{ color: "var(--text-primary)", fontFamily: "var(--font-display)", fontWeight: 700 }}>
            AI<span style={{ color: "var(--brand)" }}>Law</span>
          </span>
        </Link>

        <nav className="flex items-center gap-1">
          {NAV.map(({ href, label, icon: Icon }) => {
            const active = path === href;
            return (
              <Link key={href} href={href}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all",
                  active
                    ? "text-white"
                    : "hover:text-white"
                )}
                style={{
                  fontFamily: "var(--font-display)",
                  background: active ? "rgba(59,110,240,0.2)" : "transparent",
                  color: active ? "var(--brand-light)" : "var(--text-secondary)",
                  border: active ? "1px solid rgba(59,110,240,0.3)" : "1px solid transparent",
                }}
              >
                <Icon size={14} />
                {label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
