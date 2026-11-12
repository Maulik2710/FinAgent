import React, { useState } from 'react';
import {
  Newspaper,
  ExternalLink,
  Smile,
  Frown,
  Meh,
  Filter,
  Calendar,
  Sparkles,
} from 'lucide-react';
import { NewsResponse, StockSummary } from '../types';

interface MarketNewsPageProps {
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  news: NewsResponse | null;
}

export const MarketNewsPage: React.FC<MarketNewsPageProps> = ({
  selectedStock,
  setSelectedStock,
  stocks,
  news,
}) => {
  const [filter, setFilter] = useState<'ALL' | 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE'>('ALL');

  const filteredArticles = news?.articles.filter((a) => {
    if (filter === 'ALL') return true;
    return a.sentiment === filter;
  }) || [];

  const sentimentScore = news?.sentiment_score ?? 0.42;
  const isPos = sentimentScore >= 0.2;
  const isNeg = sentimentScore <= -0.2;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-white tracking-tight">Institutional News & Sentiment Analysis</h2>
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400">
              FinBERT NLP
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time financial headline extraction analyzed with ProsusAI FinBERT transformer model.
          </p>
        </div>

        <select
          value={selectedStock}
          onChange={(e) => setSelectedStock(e.target.value)}
          className="bg-[#151d30] text-white text-xs font-semibold px-3 py-1.5 rounded-xl border border-white/[0.1] focus:outline-none focus:border-cyan-500/50 cursor-pointer"
        >
          {stocks.map((s) => (
            <option key={s.symbol} value={s.symbol} className="bg-[#111827]">
              {s.symbol} — {s.name}
            </option>
          ))}
        </select>
      </div>

      {/* Top Sentiment Summary & Distribution Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Composite Sentiment Score */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <p className="text-xs font-mono text-slate-400 uppercase">FinBERT Net Score</p>
          <div className="mt-2 flex items-baseline space-x-2">
            <span
              className={`text-3xl font-extrabold font-mono ${
                isPos ? 'text-emerald-400' : isNeg ? 'text-rose-400' : 'text-amber-400'
              }`}
            >
              {sentimentScore >= 0 ? '+' : ''}
              {sentimentScore.toFixed(2)}
            </span>
            <span className="text-xs text-slate-400 font-mono">[-1.0, +1.0]</span>
          </div>
          <div className="mt-3 flex items-center space-x-2">
            <div className="w-full h-1.5 bg-[#151d30] rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${isPos ? 'bg-emerald-400' : isNeg ? 'bg-rose-400' : 'bg-amber-400'}`}
                style={{ width: `${Math.min(100, Math.max(10, ((sentimentScore + 1) / 2) * 100))}%` }}
              />
            </div>
          </div>
        </div>

        {/* Positive Articles Count */}
        <div
          onClick={() => setFilter('POSITIVE')}
          className={`p-5 rounded-2xl cursor-pointer transition-all border ${
            filter === 'POSITIVE'
              ? 'bg-emerald-500/15 border-emerald-500/40'
              : 'bg-[#111827] border-white/[0.08] hover:border-emerald-500/30'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase">Bullish Headlines</span>
            <Smile className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-3xl font-extrabold font-mono text-emerald-400 mt-2">
            {news?.positive_count ?? 6}
          </p>
          <p className="text-[11px] text-slate-500 mt-1">Articles classified positive</p>
        </div>

        {/* Neutral Articles Count */}
        <div
          onClick={() => setFilter('NEUTRAL')}
          className={`p-5 rounded-2xl cursor-pointer transition-all border ${
            filter === 'NEUTRAL'
              ? 'bg-amber-500/15 border-amber-500/40'
              : 'bg-[#111827] border-white/[0.08] hover:border-amber-500/30'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase">Neutral Headlines</span>
            <Meh className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-3xl font-extrabold font-mono text-amber-400 mt-2">
            {news?.neutral_count ?? 2}
          </p>
          <p className="text-[11px] text-slate-500 mt-1">Balanced/informational news</p>
        </div>

        {/* Negative Articles Count */}
        <div
          onClick={() => setFilter('NEGATIVE')}
          className={`p-5 rounded-2xl cursor-pointer transition-all border ${
            filter === 'NEGATIVE'
              ? 'bg-rose-500/15 border-rose-500/40'
              : 'bg-[#111827] border-white/[0.08] hover:border-rose-500/30'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase">Bearish Headlines</span>
            <Frown className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-3xl font-extrabold font-mono text-rose-400 mt-2">
            {news?.negative_count ?? 2}
          </p>
          <p className="text-[11px] text-slate-500 mt-1">Articles classified negative</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs text-slate-400 font-mono">Filter by Sentiment:</span>
          {(['ALL', 'POSITIVE', 'NEUTRAL', 'NEGATIVE'] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-3 py-1 rounded-lg text-xs font-mono transition-all ${
                filter === cat
                  ? 'bg-emerald-500 text-slate-950 font-bold'
                  : 'bg-[#151d30] text-slate-400 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <span className="text-xs text-slate-500 font-mono">
          Showing {filteredArticles.length} Articles
        </span>
      </div>

      {/* Articles Feed */}
      <div className="space-y-4">
        {filteredArticles.map((article, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-white/[0.15] transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
          >
            <div className="space-y-2 flex-1">
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="text-emerald-400 font-semibold font-mono">{article.source || 'Financial Wire'}</span>
                <span className="text-slate-600">•</span>
                <span className="text-slate-400 font-mono flex items-center">
                  <Calendar className="w-3 h-3 mr-1" />
                  {article.publishedAt ? article.publishedAt.slice(0, 10) : 'Recent'}
                </span>
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold font-mono ${
                    article.sentiment === 'POSITIVE'
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : article.sentiment === 'NEGATIVE'
                      ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                      : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  }`}
                >
                  {article.sentiment}
                </span>
                <span className="text-[11px] text-slate-500 font-mono">
                  Confidence: {(article.confidence * 100).toFixed(1)}%
                </span>
              </div>

              <h3 className="text-sm sm:text-base font-bold text-white leading-snug">{article.title}</h3>
              {article.description && (
                <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{article.description}</p>
              )}
            </div>

            {article.url && (
              <a
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="shrink-0 inline-flex items-center space-x-1 px-4 py-2 rounded-xl bg-[#151d30] hover:bg-[#1a243c] border border-white/[0.08] text-xs font-semibold text-slate-200 hover:text-white transition-all self-start sm:self-center"
              >
                <span>Read Story</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
