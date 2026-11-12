import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  ReferenceLine,
} from 'recharts';
import { TrendingUp, Layers, Activity, Calendar } from 'lucide-react';
import { StockDetailResponse, StockSummary } from '../types';

interface StockAnalysisPageProps {
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  stockDetail: StockDetailResponse | null;
}

export const StockAnalysisPage: React.FC<StockAnalysisPageProps> = ({
  selectedStock,
  setSelectedStock,
  stocks,
  stockDetail,
}) => {
  const [timeRange, setTimeRange] = useState<'30' | '90' | '180' | '365'>('90');
  const [showSMA, setShowSMA] = useState(true);
  const [showEMA, setShowEMA] = useState(true);

  const activeStock = stocks.find((s) => s.symbol === selectedStock) || stocks[0];
  const historySlice = stockDetail?.history.slice(-parseInt(timeRange, 10)) || [];
  const latest = historySlice[historySlice.length - 1];

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-white tracking-tight">{activeStock?.name}</h2>
            <span className="text-sm font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
              {activeStock?.symbol}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Complete technical indicators, moving averages, momentum oscillators, and volume analysis.
          </p>
        </div>

        {/* Timeframe Selector & Stock Picker */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center bg-[#151d30] p-1 rounded-xl border border-white/[0.08]">
            {(['30', '90', '180', '365'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setTimeRange(r)}
                className={`px-3 py-1 rounded-lg text-xs font-mono font-medium transition-all ${
                  timeRange === r
                    ? 'bg-emerald-500 text-slate-950 font-bold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {r}D
              </button>
            ))}
          </div>

          <select
            value={selectedStock}
            onChange={(e) => setSelectedStock(e.target.value)}
            className="bg-[#151d30] text-white text-xs font-semibold px-3 py-1.5 rounded-xl border border-white/[0.1] focus:outline-none focus:border-emerald-500/50 cursor-pointer"
          >
            {stocks.map((s) => (
              <option key={s.symbol} value={s.symbol} className="bg-[#111827]">
                {s.symbol}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* OHLCV Snapshot Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">Spot Price</p>
          <p className="text-lg font-bold font-mono text-white mt-1">${stockDetail?.current_price.toFixed(2)}</p>
          <p className={`text-[11px] font-mono font-semibold ${(stockDetail?.change ?? 0) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {(stockDetail?.change ?? 0) >= 0 ? '+' : ''}{stockDetail?.change_percent.toFixed(2)}%
          </p>
        </div>
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">Open</p>
          <p className="text-lg font-bold font-mono text-slate-200 mt-1">${latest?.open.toFixed(2) || '0.00'}</p>
          <p className="text-[11px] text-slate-500 font-mono">Day Start</p>
        </div>
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">High</p>
          <p className="text-lg font-bold font-mono text-emerald-400 mt-1">${latest?.high.toFixed(2) || '0.00'}</p>
          <p className="text-[11px] text-slate-500 font-mono">Session Max</p>
        </div>
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">Low</p>
          <p className="text-lg font-bold font-mono text-rose-400 mt-1">${latest?.low.toFixed(2) || '0.00'}</p>
          <p className="text-[11px] text-slate-500 font-mono">Session Min</p>
        </div>
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">RSI (14)</p>
          <p className="text-lg font-bold font-mono text-amber-400 mt-1">{latest?.rsi_14?.toFixed(1) || '58.2'}</p>
          <p className="text-[11px] text-slate-500 font-mono">Momentum</p>
        </div>
        <div className="p-3.5 rounded-xl bg-[#111827] border border-white/[0.06]">
          <p className="text-[10px] font-mono text-slate-400 uppercase">Volatility</p>
          <p className="text-lg font-bold font-mono text-cyan-400 mt-1">{((latest?.rolling_volatility || 0.02) * 100).toFixed(1)}%</p>
          <p className="text-[11px] text-slate-500 font-mono">20D Rolling</p>
        </div>
      </div>

      {/* Main Historical Price Chart with Moving Averages */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-base font-bold text-white">Price Action & Moving Average Envelopes</h3>
            <p className="text-xs text-slate-400 mt-0.5">Historical closing prices against 20-day SMA and EMA</p>
          </div>
          <div className="flex items-center space-x-4 text-xs font-mono">
            <label className="flex items-center space-x-1.5 cursor-pointer text-emerald-400">
              <input type="checkbox" checked={showSMA} onChange={(e) => setShowSMA(e.target.checked)} className="rounded" />
              <span>SMA 20</span>
            </label>
            <label className="flex items-center space-x-1.5 cursor-pointer text-cyan-400">
              <input type="checkbox" checked={showEMA} onChange={(e) => setShowEMA(e.target.checked)} className="rounded" />
              <span>EMA 20</span>
            </label>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={historySlice} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
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
              <Line type="monotone" dataKey="close" stroke="#f8fafc" strokeWidth={2} dot={false} name="Close ($)" />
              {showSMA && <Line type="monotone" dataKey="sma_20" stroke="#10b981" strokeWidth={1.5} dot={false} name="SMA 20" />}
              {showEMA && <Line type="monotone" dataKey="ema_20" stroke="#38bdf8" strokeWidth={1.5} dot={false} name="EMA 20" />}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Secondary Indicators: RSI (14) & MACD Oscillators */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* RSI Chart */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Relative Strength Index (RSI 14)</h3>
              <p className="text-[11px] text-slate-400 mt-0.5">Overbought: &gt;70 • Oversold: &lt;30</p>
            </div>
            <span className="text-xs font-mono font-bold text-amber-400">{latest?.rsi_14?.toFixed(2) || '58.20'}</span>
          </div>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={historySlice} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} />
                <YAxis domain={[0, 100]} stroke="#64748b" fontSize={10} ticks={[30, 50, 70]} tickLine={false} />
                <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" />
                <ReferenceLine y={30} stroke="#10b981" strokeDasharray="3 3" />
                <Tooltip contentStyle={{ backgroundColor: '#151d30', borderColor: 'rgba(255,255,255,0.1)', fontSize: '11px' }} />
                <Line type="monotone" dataKey="rsi_14" stroke="#f59e0b" strokeWidth={1.8} dot={false} name="RSI (14)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* MACD Chart */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">MACD Trend & Signal Oscillator</h3>
              <p className="text-[11px] text-slate-400 mt-0.5">MACD (12, 26, 9) Momentum Crossover</p>
            </div>
            <span className="text-xs font-mono font-bold text-purple-400">Signal: {latest?.macd_signal?.toFixed(2) || '1.85'}</span>
          </div>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={historySlice} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                <ReferenceLine y={0} stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#151d30', borderColor: 'rgba(255,255,255,0.1)', fontSize: '11px' }} />
                <Line type="monotone" dataKey="macd" stroke="#a855f7" strokeWidth={1.8} dot={false} name="MACD" />
                <Line type="monotone" dataKey="macd_signal" stroke="#38bdf8" strokeWidth={1.5} dot={false} strokeDasharray="3 3" name="Signal" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
