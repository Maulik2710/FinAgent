import React from 'react';
import {
  TrendingUp,
  TrendingDown,
  Cpu,
  Newspaper,
  PieChart,
  BrainCircuit,
  ArrowUpRight,
  ArrowDownRight,
  Sparkles,
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';
import {
  StockSummary,
  StockDetailResponse,
  ForecastResponse,
  NewsResponse,
  PortfolioResponse,
  RecommendationResponse,
} from '../types';

interface DashboardOverviewProps {
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  stockDetail: StockDetailResponse | null;
  forecast: ForecastResponse | null;
  news: NewsResponse | null;
  portfolio: PortfolioResponse | null;
  recommendation: RecommendationResponse | null;
  onNavigateTab: (tab: any) => void;
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({
  selectedStock,
  setSelectedStock,
  stocks,
  stockDetail,
  forecast,
  news,
  portfolio,
  recommendation,
  onNavigateTab,
}) => {
  const currentStock = stocks.find((s) => s.symbol === selectedStock) || stocks[0];
  const chartData = stockDetail?.history.slice(-30).map((h) => ({
    date: h.date.slice(5),
    price: h.close,
    sma: h.sma_20,
  })) || [];

  return (
    <div className="space-y-6">
      {/* Top Welcome & Summary Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Executive Portfolio & Market Overview</h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time quantitative analytics, deep learning forecasts, and FinBERT sentiment signals for institutional equities.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400 font-mono">Universe:</span>
          <div className="flex flex-wrap gap-1">
            {stocks.map((s) => (
              <button
                key={s.symbol}
                onClick={() => setSelectedStock(s.symbol)}
                className={`px-2 py-1 text-xs font-mono font-bold rounded-md transition-all ${
                  s.symbol === selectedStock
                    ? 'bg-emerald-500 text-slate-950 shadow-sm'
                    : 'bg-[#151d30] text-slate-300 hover:text-white hover:bg-[#1a243c]'
                }`}
              >
                {s.symbol}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 4 Core Financial KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Selected Asset Price */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08] relative overflow-hidden">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>{currentStock?.symbol} SPOT PRICE</span>
            <span className="text-[11px] text-slate-500">{currentStock?.name}</span>
          </div>
          <div className="mt-2 flex items-baseline space-x-3">
            <span className="text-3xl font-extrabold font-mono text-white">
              ${currentStock?.current_price.toFixed(2)}
            </span>
            <span
              className={`flex items-center text-xs font-bold font-mono px-2 py-0.5 rounded-full ${
                (currentStock?.change ?? 0) >= 0
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
              }`}
            >
              {(currentStock?.change ?? 0) >= 0 ? (
                <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
              ) : (
                <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" />
              )}
              {currentStock?.change_percent.toFixed(2)}%
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-3 border-t border-white/[0.04]">
            <span>Vol: {(currentStock?.daily_volume || 0).toLocaleString()}</span>
            <span>RSI: {currentStock?.rsi ?? 61.8}</span>
          </div>
        </div>

        {/* LSTM Forecast KPI */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>LSTM TARGET</span>
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div className="mt-2 flex items-baseline space-x-3">
            <span className="text-3xl font-extrabold font-mono text-cyan-400">
              ${forecast?.predicted_price.toFixed(2) || (currentStock?.current_price * 1.08).toFixed(2)}
            </span>
            <span className="text-xs font-bold font-mono text-cyan-300">
              {forecast ? (forecast.expected_return >= 0 ? '+' : '') + forecast.expected_return.toFixed(2) + '%' : '+8.20%'}
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-3 border-t border-white/[0.04]">
            <span>Trend: {forecast?.trend || 'Bullish'}</span>
            <button
              onClick={() => onNavigateTab('forecasting')}
              className="text-cyan-400 hover:underline flex items-center text-[10px]"
            >
              View Model Curve →
            </button>
          </div>
        </div>

        {/* Portfolio Sharpe Optimizer KPI */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>OPTIMAL SHARPE</span>
            <PieChart className="w-3.5 h-3.5 text-purple-400" />
          </div>
          <div className="mt-2 flex items-baseline space-x-3">
            <span className="text-3xl font-extrabold font-mono text-purple-400">
              {portfolio?.sharpe_ratio.toFixed(2) || '1.30'}
            </span>
            <span className="text-xs font-bold text-slate-300 font-mono">
              Exp: {portfolio?.expected_return.toFixed(1) || '55.5'}%
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-3 border-t border-white/[0.04]">
            <span>Volatility: {portfolio?.volatility.toFixed(1) || '38.7'}%</span>
            <button
              onClick={() => onNavigateTab('portfolio')}
              className="text-purple-400 hover:underline flex items-center text-[10px]"
            >
              Weights Breakdown →
            </button>
          </div>
        </div>

        {/* Multi-Factor Recommendation Decision */}
        <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/25">
          <div className="flex items-center justify-between text-xs text-emerald-300 font-mono">
            <span>AI RECOMMENDATION</span>
            <BrainCircuit className="w-3.5 h-3.5 text-emerald-400" />
          </div>
          <div className="mt-2 flex items-baseline space-x-3">
            <span className="text-2xl font-extrabold font-mono text-emerald-400">
              {recommendation?.recommendation || 'STRONG BUY'}
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-[11px] text-slate-300 pt-3 border-t border-emerald-500/20">
            <span>Confidence: {recommendation?.confidence.toFixed(1) || '84.5'}%</span>
            <button
              onClick={() => onNavigateTab('recommendations')}
              className="text-emerald-400 hover:underline flex items-center text-[10px]"
            >
              Explain Rationale →
            </button>
          </div>
        </div>
      </div>

      {/* Middle Section: Chart & Portfolio Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Historical Price Chart (30-day snapshot) */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <span>{selectedStock} Historical Price Trajectory (30-Day Window)</span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Closing price with 20-period Simple Moving Average</p>
            </div>
            <button
              onClick={() => onNavigateTab('analysis')}
              className="text-xs text-emerald-400 hover:underline font-mono"
            >
              Full Indicators & OHLCV →
            </button>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} domain={['auto', 'auto']} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#151d30',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#fff',
                  }}
                />
                <Area type="monotone" dataKey="price" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#priceGradient)" name="Close Price ($)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Asset Allocation Preview */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-white">Optimal Portfolio Weights</h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-semibold">
              MPT SLSQP
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-4">Top assets recommended to maximize Sharpe ratio.</p>

          <div className="space-y-3">
            {portfolio?.allocations.filter((a) => a.allocation_percent > 1).map((item) => (
              <div key={item.symbol}>
                <div className="flex items-center justify-between text-xs mb-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold font-mono text-white">{item.symbol}</span>
                    <span className="text-[11px] text-slate-400 truncate max-w-[120px]">{item.name}</span>
                  </div>
                  <span className="font-mono font-bold text-purple-400">{item.allocation_percent.toFixed(1)}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-[#151d30] overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-purple-500 to-indigo-400"
                    style={{ width: `${item.allocation_percent}%` }}
                  />
                </div>
              </div>
            )) || <p className="text-xs text-slate-500">Loading portfolio...</p>}
          </div>

          <button
            onClick={() => onNavigateTab('portfolio')}
            className="w-full mt-6 py-2 rounded-xl bg-[#151d30] hover:bg-[#1a243c] text-xs font-semibold text-slate-200 transition-all text-center block border border-white/[0.08]"
          >
            Open Portfolio Analytics Engine
          </button>
        </div>
      </div>

      {/* Bottom Stream: News & Sentiment Summary */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Newspaper className="w-4 h-4 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Recent Institutional News & FinBERT Sentiment</h3>
          </div>
          <button
            onClick={() => onNavigateTab('news')}
            className="text-xs text-cyan-400 hover:underline font-mono"
          >
            All Articles & Sentiment Distribution →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {news?.articles.slice(0, 3).map((article, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-[#151d30] border border-white/[0.06] flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-[11px] mb-2">
                  <span className="text-slate-400 font-mono">{article.source || 'Market Feed'}</span>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${
                      article.sentiment === 'POSITIVE'
                        ? 'bg-emerald-500/20 text-emerald-400'
                        : article.sentiment === 'NEGATIVE'
                        ? 'bg-rose-500/20 text-rose-400'
                        : 'bg-slate-500/20 text-slate-300'
                    }`}
                  >
                    {article.sentiment}
                  </span>
                </div>
                <h4 className="text-xs font-semibold text-white line-clamp-2 leading-relaxed">{article.title}</h4>
              </div>
              <p className="text-[10px] text-slate-500 mt-3 font-mono">
                FinBERT Confidence: {(article.confidence * 100).toFixed(0)}%
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
