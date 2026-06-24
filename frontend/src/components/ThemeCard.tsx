import { useState } from "react";
import { ThemeSummary } from "@/lib/types";
import { Star, MessageSquareQuote, Target, ChevronDown, ChevronUp, Lightbulb } from "lucide-react";
import clsx from "clsx";

interface ThemeCardProps {
  theme: ThemeSummary;
  onClick: (clusterId: number) => void;
  isActive?: boolean;
}

export default function ThemeCard({ theme, onClick, isActive }: ThemeCardProps) {
  const isPositive = theme.avg_rating >= 4.0;
  const isNegative = theme.avg_rating <= 2.5;

  return (
    <div
      className={clsx(
        "text-left p-5 rounded-2xl transition-all duration-300 group flex flex-col gap-4 relative overflow-hidden",
        "hover:neon-glow",
        isActive ? "glass-card ring-1 ring-primary neon-glow" : "glass hover:-translate-y-1"
      )}
    >
      {/* Background flare on hover */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 blur-[50px] opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

      {/* Clickable Header Area */}
      <div 
        className="flex flex-col gap-4 cursor-pointer z-10"
        onClick={() => onClick(theme.cluster_id)}
      >
        <div className="flex justify-between items-start">
          <h3 className="font-sans font-semibold text-lg text-on-surface pr-4">
            {theme.theme_name}
          </h3>
          <div 
            className={clsx(
              "flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-sm font-medium shrink-0",
              isPositive ? "bg-primary/10 text-primary" : isNegative ? "bg-error/10 text-error" : "bg-secondary/10 text-secondary"
            )}
          >
            <Star className="w-4 h-4 fill-current" />
            {(theme.avg_rating || 0).toFixed(1)}
          </div>
        </div>

        <p className={clsx(
          "text-sm text-on-surface-variant flex-1",
          !isActive && "line-clamp-2"
        )}>
          {theme.description}
        </p>

        <div className="flex items-center justify-between text-xs text-on-surface-variant mt-2 border-t border-white/5 pt-4">
          <div className="flex items-center gap-1.5">
            <MessageSquareQuote className="w-4 h-4 text-secondary" />
            <span>{theme.size} reviews</span>
          </div>
          
          <div className="flex items-center gap-1 text-primary hover:underline">
            {isActive ? "Hide Details" : "View Details"}
            {isActive ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </div>
        </div>
      </div>

      {/* Expanded Content Area */}
      {isActive && (
        <div className="animate-in fade-in slide-in-from-top-2 duration-300 z-10 flex flex-col gap-6 mt-4 border-t border-white/10 pt-4">
          
          {/* Quotes Section */}
          {theme.quotes && theme.quotes.length > 0 && (
            <div className="flex flex-col gap-3">
              <h4 className="text-sm font-semibold text-primary uppercase tracking-wider flex items-center gap-2">
                <MessageSquareQuote className="w-4 h-4" />
                Representative Reviews
              </h4>
              <div className="flex flex-col gap-2">
                {theme.quotes.slice(0, 3).map((quote, idx) => (
                  <div key={idx} className="bg-surface-container-low p-3 rounded-xl border border-white/5 text-sm text-on-surface italic">
                    "{quote}"
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Action Ideas Section */}
          {theme.action_ideas && theme.action_ideas.length > 0 && (
            <div className="flex flex-col gap-3">
              <h4 className="text-sm font-semibold text-primary uppercase tracking-wider flex items-center gap-2">
                <Lightbulb className="w-4 h-4" />
                Action Steps
              </h4>
              <div className="flex flex-col gap-2">
                {theme.action_ideas.map((action, idx) => (
                  <div key={idx} className="bg-surface-container-low p-3 rounded-xl border border-white/5 flex flex-col gap-1.5">
                    <span className="text-xs font-medium text-secondary uppercase tracking-wide flex items-center gap-1">
                      <Target className="w-3 h-3" />
                      {action.team}
                    </span>
                    <p className="text-sm text-on-surface">{action.idea}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
