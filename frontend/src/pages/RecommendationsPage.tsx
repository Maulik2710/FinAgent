import React from 'react';
import {
  BrainCircuit,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Layers,
  Sparkles,
  TrendingUp,
  Cpu,
  Newspaper,
  PieChart,
} from 'lucide-react';
import { RecommendationResponse, StockSummary } from '../types';

interface RecommendationsPageProps {
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  recommendation: RecommendationResponse | null;
}

export const RecommendationsPage: React.FC<RecommendationsPageProps> = ({
  selectedStock,
  setSelectedStock,
  stocks,
  recommendation,
}) => {
  const currentStock = stocks.find((s) => s.symbol === selectedStock) || stocks[0];
  const recAction = recommendation?.recommendation || 'Strong Buy';

  const isBuy = recAction.includes('Buy');
  const isHold = recAction.includes('Hold');
  const isSell = recAction.includes('Sell');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-white tracking-tight">AI Investment Recommendation</h2>
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
              Multi-Factor Engine
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Synthesizes LSTM neural forecast, FinBERT sentiment, and MPT allocation into an explainable decision.
          </p>
        </div>

        <select
          value={selectedStock}
          onChange={(e) => setSelectedStock(e.target.value)}
          className="bg-[#151d30] text-white text-xs font-semibold px-3 py-1.5 rounded-xl border border-white/[0.1] focus:outline-none focus:border-emerald-500/50 cursor-pointer"
        >
          {stocks.map((s) => (
            <option key={s.symbol} value={s.symbol} className="bg-[#111827]">
              {s.symbol} — {s.name}
            </option>
          ))}
        </select>
      </div>

      {/* Main Recommendation Hero Banner */}
      <div
        className={`p-8 rounded-3xl border ${
          isBuy
            ? 'bg-gradient-to-br from-emerald-500/15 via-[#111827] to-[#0a0e17] border-emerald-500/40 shadow-lg shadow-emerald-500/10'
            : isHold
            ? 'bg-gradient-to-br from-amber-500/15 via-[#111827] to-[#0a0e17] border-amber-500/40'
            : 'bg-gradient-to-br from-rose-500/15 via-[#111827] to-[#0a0e17] border-rose-500/40'
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center space-x-2 text-xs font-mono text-slate-400 uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
              <span>Algorithmic Verdict for {recommendation?.symbol || selectedStock}</span>
            </div>
            <h1
              className={`text-4xl sm:text-5xl font-black font-mono tracking-tight mt-2 ${
                isBuy ? 'text-emerald-400' : isHold ? 'text-amber-400' : 'text-rose-400'
              }`}
            >
              {recAction.toUpperCase()}
            </h1>
            <p className="text-xs text-slate-300 mt-2 max-w-lg leading-relaxed">
              Based on mathematical synthesis of neural momentum, institutional sentiment analysis, and risk-adjusted MPT weights.
            </p>
          </div>

          <div className="flex items-center space-x-6">
            <div className="text-center p-4 rounded-2xl bg-[#151d30]/80 border border-white/[0.08] min-w-[130px]">
              <p className="text-[10px] font-mono uppercase text-slate-400">Confidence</p>
              <p className="text-3xl font-extrabold font-mono text-white mt-1">
                {recommendation?.confidence.toFixed(1) || '84.5'}%
              </p>
              <p className="text-[10px] text-emerald-400 mt-1 font-semibold">High Conviction</p>
            </div>

            <div className="text-center p-4 rounded-2xl bg-[#151d30]/80 border border-white/[0.08] min-w-[130px]">
              <p className="text-[10px] font-mono uppercase text-slate-400">Composite Score</p>
              <p className="text-3xl font-extrabold font-mono text-emerald-400 mt-1">
                {(recommendation?.score ?? 0.72) >= 0 ? '+' : ''}
                {recommendation?.score.toFixed(2) || '0.72'}
              </p>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">[-1.0, +1.0]</p>
            </div>
          </div>
        </div>
      </div>

      {/* 3 Underlying Multi-Factor Inputs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Signal 1: Forecast */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1.5 text-cyan-400">
              <Cpu className="w-3.5 h-3.5" />
              <span>LSTM FORECAST (40%)</span>
            </span>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-xl font-bold font-mono text-white">
              ${recommendation?.predicted_price.toFixed(2) || '0.00'}
            </span>
            <span className="text-xs font-bold font-mono text-cyan-400">
              {(recommendation?.expected_return ?? 0) >= 0 ? '+' : ''}
              {recommendation?.expected_return.toFixed(2)}%
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Target price vs spot price (${recommendation?.current_price.toFixed(2)})
          </p>
        </div>

        {/* Signal 2: News Sentiment */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1.5 text-emerald-400">
              <Newspaper className="w-3.5 h-3.5" />
              <span>FINBERT SENTIMENT (30%)</span>
            </span>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-xl font-bold font-mono text-emerald-400">
              {(recommendation?.sentiment_score ?? 0.42) >= 0 ? '+' : ''}
              {recommendation?.sentiment_score.toFixed(2) || '0.42'}
            </span>
            <span className="text-xs font-bold font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
              {(recommendation?.sentiment_score ?? 0) >= 0.2 ? 'POSITIVE' : 'NEUTRAL'}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Aggregate institutional headline sentiment
          </p>
        </div>

        {/* Signal 3: Portfolio Weight */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1.5 text-purple-400">
              <PieChart className="w-3.5 h-3.5" />
              <span>PORTFOLIO WEIGHT (30%)</span>
            </span>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-xl font-bold font-mono text-purple-400">
              {recommendation?.portfolio_weight.toFixed(1) || '15.6'}%
            </span>
            <span className="text-xs font-bold font-mono text-purple-300">
              {(recommendation?.portfolio_weight ?? 0) >= 15 ? 'HIGH ALLOC' : 'MODERATE'}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Recommended capital share from MPT optimizer
          </p>
        </div>
      </div>

      {/* Transparent Supporting Reasons */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <h3 className="text-base font-bold text-white mb-1 flex items-center space-x-2">
          <BrainCircuit className="w-4 h-4 text-emerald-400" />
          <span>Explainable Supporting Rationales</span>
        </h3>
        <p className="text-xs text-slate-400 mb-5">
          Transparent, deterministic logic produced by the multi-factor recommendation engine.
        </p>

        <div className="space-y-3">
          {recommendation?.reasons.map((reason, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl bg-[#151d30] border border-white/[0.06] flex items-start space-x-3"
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">{reason}</p>
            </div>
          )) || <p className="text-xs text-slate-500">Loading rationale signals...</p>}
        </div>
      </div>
    </div>
  );
};
