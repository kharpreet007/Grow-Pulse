"use client";

import { useState } from 'react';
import { ThemeSummary, Review } from '@/lib/types';
import ThemeCard from './ThemeCard';
import ReviewExplorer from './ReviewExplorer';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip } from 'recharts';
import { Users, TrendingUp, AlertCircle } from 'lucide-react';

interface DashboardClientProps {
  themes: ThemeSummary[];
  reviews: Review[];
}

export default function DashboardClient({ themes, reviews }: DashboardClientProps) {
  const [activeClusterId, setActiveClusterId] = useState<number | null>(null);

  const activeTheme = themes.find(t => t.cluster_id === activeClusterId) || null;

  // KPI calcs
  const totalReviews = reviews.length;
  const positiveReviews = reviews.filter(r => r.rating >= 4).length;
  const negativeReviews = reviews.filter(r => r.rating <= 2).length;
  const neutralReviews = totalReviews - positiveReviews - negativeReviews;

  const sentimentData = [
    { name: 'Positive', value: positiveReviews, color: '#4be277' }, // primary
    { name: 'Neutral', value: neutralReviews, color: '#4cd7f6' }, // secondary
    { name: 'Negative', value: negativeReviews, color: '#ffb4ab' }, // error
  ];

  return (
    <div className="flex flex-col gap-8 max-w-[1600px] mx-auto pb-12">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl font-sans font-bold text-on-surface mb-2 tracking-tight">Weekly Pulse</h1>
          <p className="text-on-surface-variant text-lg">Insights from {totalReviews.toLocaleString()} latest Google Play reviews.</p>
        </div>
      </header>

      {/* KPIs & Donut */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-3xl flex flex-col justify-center">
          <div className="flex items-center gap-3 text-on-surface-variant mb-4">
            <Users className="w-5 h-5" />
            <h3 className="font-medium uppercase tracking-wider text-sm">Total Volume</h3>
          </div>
          <div className="text-5xl font-sans font-bold text-on-surface">
            {totalReviews.toLocaleString()}
          </div>
        </div>

        <div className="glass-card p-6 rounded-3xl flex flex-col justify-center">
          <div className="flex items-center gap-3 text-on-surface-variant mb-4">
            <TrendingUp className="w-5 h-5 text-primary" />
            <h3 className="font-medium uppercase tracking-wider text-sm">Positive</h3>
          </div>
          <div className="text-5xl font-sans font-bold text-primary neon-glow" style={{ textShadow: '0 0 20px rgba(75, 226, 119, 0.4)'}}>
            {totalReviews > 0 ? Math.round((positiveReviews / totalReviews) * 100) : 0}%
          </div>
        </div>

        <div className="glass-card p-6 rounded-3xl flex flex-col justify-center">
          <div className="flex items-center gap-3 text-on-surface-variant mb-4">
            <AlertCircle className="w-5 h-5 text-error" />
            <h3 className="font-medium uppercase tracking-wider text-sm">Actionable</h3>
          </div>
          <div className="text-5xl font-sans font-bold text-error">
            {themes.reduce((acc, t) => acc + (t.action_ideas?.length || 0), 0)}
          </div>
          <div className="text-sm text-on-surface-variant mt-2">Product Ideas Found</div>
        </div>

        <div className="glass-card p-4 rounded-3xl h-48 flex items-center justify-center relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={70}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <RechartsTooltip 
                contentStyle={{ backgroundColor: '#171f33', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                itemStyle={{ color: '#dce1fb' }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span className="text-sm font-semibold text-on-surface-variant">Sentiment</span>
          </div>
        </div>
      </div>

      {/* Themes Grid */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-sans font-semibold text-on-surface">Emerging Themes</h2>
          {activeClusterId !== null && (
            <button 
              onClick={() => setActiveClusterId(null)}
              className="text-sm text-primary hover:underline"
            >
              Clear Filter
            </button>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {themes.map(theme => (
            <ThemeCard 
              key={theme.cluster_id} 
              theme={theme} 
              onClick={(id) => setActiveClusterId(id === activeClusterId ? null : id)}
              isActive={theme.cluster_id === activeClusterId}
            />
          ))}
        </div>
      </div>

      {/* Review Explorer */}
      <div className="mt-8" id="explorer">
        <ReviewExplorer reviews={reviews} activeTheme={activeTheme} />
      </div>
    </div>
  );
}
