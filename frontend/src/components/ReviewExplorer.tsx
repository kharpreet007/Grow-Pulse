"use client";

import { useState, useMemo } from 'react';
import { Review, ThemeSummary } from '@/lib/types';
import { Search, ThumbsUp, Star, ChevronDown, ChevronUp, Filter } from 'lucide-react';
import clsx from 'clsx';

interface ReviewExplorerProps {
  reviews: Review[];
  activeTheme?: ThemeSummary | null;
}

export default function ReviewExplorer({ reviews, activeTheme }: ReviewExplorerProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [ratingFilter, setRatingFilter] = useState<string>('all');
  const [versionFilter, setVersionFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'thumbs' | 'rating' | 'date'>('thumbs');

  const uniqueVersions = useMemo(() => {
    const versions = new Set(reviews.map(r => r.app_version).filter(Boolean));
    return Array.from(versions).sort((a, b) => b.localeCompare(a)); // Sort desc so newest is first
  }, [reviews]);

  const filteredReviews = useMemo(() => {
    let result = reviews;

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      result = result.filter(r => r.text.toLowerCase().includes(q));
    }

    if (ratingFilter !== 'all') {
      const rating = parseInt(ratingFilter, 10);
      result = result.filter(r => r.rating === rating);
    }

    if (versionFilter !== 'all') {
      result = result.filter(r => r.app_version === versionFilter);
    }

    // Sort
    result = [...result].sort((a, b) => {
      if (sortBy === 'thumbs') return b.thumbs_up - a.thumbs_up;
      if (sortBy === 'rating') return b.rating - a.rating;
      if (sortBy === 'date') {
        const dateA = a.date ? new Date(a.date).getTime() : 0;
        const dateB = b.date ? new Date(b.date).getTime() : 0;
        return dateB - dateA;
      }
      return 0;
    });

    return result;
  }, [reviews, searchQuery, ratingFilter, versionFilter, sortBy]);

  return (
    <div className="flex flex-col gap-6">
      <div 
        className="flex justify-between items-center cursor-pointer group"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        <h2 className="text-2xl font-sans font-semibold text-on-surface flex items-center gap-2 transition-colors group-hover:text-primary">
          Review Explorer
          {activeTheme && (
            <span className="text-primary text-lg">({activeTheme.theme_name})</span>
          )}
        </h2>
        <div className="p-2 rounded-full bg-surface-container hover:bg-surface-container-high transition-colors text-on-surface-variant group-hover:text-primary">
          {isCollapsed ? <ChevronDown className="w-5 h-5" /> : <ChevronUp className="w-5 h-5" />}
        </div>
      </div>

      {!isCollapsed && (
        <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-top-4 duration-300">
          
          {/* Filters Bar */}
          <div className="glass p-4 rounded-xl flex flex-wrap items-center gap-4 border border-white/5">
            <div className="flex items-center gap-2 text-on-surface-variant mr-2">
              <Filter className="w-4 h-4" />
              <span className="text-sm font-medium">Filters:</span>
            </div>

            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-on-surface-variant" />
              <input 
                type="text" 
                placeholder="Filter by review text..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-surface-container-high border border-white/10 rounded-lg py-2 pl-9 pr-4 text-sm text-on-surface placeholder:text-on-surface-variant focus:outline-none focus:ring-1 focus:ring-primary transition-all"
              />
            </div>

            <select 
              value={ratingFilter}
              onChange={(e) => setRatingFilter(e.target.value)}
              className="bg-surface-container-high border border-white/10 rounded-lg py-2 px-3 text-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary appearance-none cursor-pointer min-w-[120px]"
            >
              <option value="all">All Ratings</option>
              <option value="5">5 Stars</option>
              <option value="4">4 Stars</option>
              <option value="3">3 Stars</option>
              <option value="2">2 Stars</option>
              <option value="1">1 Star</option>
            </select>

            <select 
              value={versionFilter}
              onChange={(e) => setVersionFilter(e.target.value)}
              className="bg-surface-container-high border border-white/10 rounded-lg py-2 px-3 text-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary appearance-none cursor-pointer min-w-[140px]"
            >
              <option value="all">All Versions</option>
              {uniqueVersions.map(v => (
                <option key={v} value={v}>v{v}</option>
              ))}
            </select>

            <div className="w-px h-6 bg-white/10 mx-2 hidden md:block"></div>

            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="bg-surface-container-high border border-white/10 rounded-lg py-2 px-3 text-sm text-primary font-medium focus:outline-none focus:ring-1 focus:ring-primary appearance-none cursor-pointer"
            >
              <option value="thumbs">Sort by Upvotes</option>
              <option value="rating">Sort by Rating</option>
              <option value="date">Sort by Date</option>
            </select>
          </div>

          {activeTheme && (
            <div className="glass-card p-5 rounded-2xl border-l-4 border-l-primary">
              <h3 className="text-sm font-semibold text-primary mb-3 uppercase tracking-wider">Representative Quotes</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {activeTheme.quotes.map((quote, idx) => (
                  <div key={idx} className="bg-surface-container-low p-4 rounded-xl text-sm text-on-surface italic border border-white/5">
                    "{quote}"
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="glass rounded-2xl overflow-hidden flex flex-col">
            <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
              <table className="w-full text-left border-collapse relative">
                <thead className="sticky top-0 z-10 bg-surface-container-highest shadow-md">
                  <tr className="border-b border-white/10">
                    <th className="p-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider w-16">Rating</th>
                    <th className="p-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider">Review Text</th>
                    <th className="p-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider w-32">Version</th>
                    <th className="p-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider w-24">Upvotes</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {filteredReviews.slice(0, 100).map((review, idx) => (
                    <tr key={idx} className="hover:bg-white/[0.02] transition-colors group">
                      <td className="p-4">
                        <div className={clsx(
                          "flex items-center gap-1 text-sm font-medium w-fit px-2 py-1 rounded-md",
                          review.rating >= 4 ? "bg-primary/10 text-primary" : review.rating <= 2 ? "bg-error/10 text-error" : "bg-secondary/10 text-secondary"
                        )}>
                          {review.rating} <Star className="w-3 h-3 fill-current" />
                        </div>
                      </td>
                      <td className="p-4 text-sm text-on-surface max-w-xl">
                        {review.text}
                      </td>
                      <td className="p-4 text-sm text-on-surface-variant">
                        {review.app_version || 'Unknown'}
                        {review.date && <div className="text-xs opacity-50 mt-1">{new Date(review.date).toLocaleDateString()}</div>}
                      </td>
                      <td className="p-4 text-sm text-on-surface-variant">
                        <div className="flex items-center gap-1.5">
                          <ThumbsUp className="w-4 h-4 text-primary opacity-70" />
                          {review.thumbs_up}
                        </div>
                      </td>
                    </tr>
                  ))}
                  {filteredReviews.length === 0 && (
                    <tr>
                      <td colSpan={4} className="p-8 text-center text-on-surface-variant">
                        No reviews found matching your criteria.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {filteredReviews.length > 100 && (
              <div className="p-4 text-center text-xs text-on-surface-variant bg-surface-container-low border-t border-white/10">
                Showing top 100 results of {filteredReviews.length} total matches
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
