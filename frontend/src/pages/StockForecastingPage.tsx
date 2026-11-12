import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Cpu, TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { ForecastResponse, StockSummary } from '../types';

interface StockForecastingPageProps {
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  forecast: ForecastResponse | null;
}

export const StockForecastingPage: React.FC<StockForecastingPageProps> = ({
  selectedStock,
  setSelectedStock,
  stocks,
  forecast,
}) => {
  const currentStock = stocks.find((s) => s.symbol === selectedStock) || stocks[0];
  const isBullish = (forecast?.expected_return ?? 0) >= 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-white tracking-tight">LSTM Neural Price Forecasting</h2>
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400">
              Deep Learning
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Recurrent Neural Network multi-step price projection trained on historical OHLCV and technical sequences.
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

      {/* 3 Core Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Spot Price */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <p className="text-xs font-mono text-slate-400 uppercase">Current Market Price</p>
          <p className="text-3xl font-extrabold font-mono text-white mt-1">
            ${forecast?.current_price.toFixed(2) || currentStock?.current_price.toFixed(2)}
          </p>
          <p className="text-xs text-slate-500 mt-2 font-mono">Last Closing Quote</p>
        </div>

        {/* LSTM Projected Target */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <p className="text-xs font-mono text-cyan-400 uppercase">LSTM Target Price</p>
          <p className="text-3xl font-extrabold font-mono text-cyan-400 mt-1">
            ${forecast?.predicted_price.toFixed(2) || (currentStock?.current_price * 1.08).toFixed(2)}
          </p>
          <p className="text-xs text-slate-400 mt-2 font-mono">Target Horizon Estimate</p>
        </div>

        {/* Expected Return & Trend */}
        <div className={`p-5 rounded-2xl border ${isBullish ? 'bg-emerald-500/10 border-emerald-500/25' : 'bg-rose-500/10 border-rose-500/25'}`}>
          <p className={`text-xs font-mono uppercase ${isBullish ? 'text-emerald-300' : 'text-rose-300'}`}>
            Expected Return & Sentiment
          </p>
          <div className="flex items-baseline space-x-2 mt-1">
            <span className={`text-3xl font-extrabold font-mono ${isBullish ? 'text-emerald-400' : 'text-rose-400'}`}>
              {(forecast?.expected_return ?? 0) >= 0 ? '+' : ''}
              {forecast?.expected_return.toFixed(2)}%
            </span>
            <span className={`text-xs font-bold font-mono px-2 py-0.5 rounded ${isBullish ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
              {forecast?.trend.toUpperCase()}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-2 font-mono">
            {isBullish ? 'Projected Upside Momentum' : 'Downward Pressure Expected'}
          </p>
        </div>
      </div>

      {/* Main Comparison Chart: Actual vs Predicted */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <span>{selectedStock}: Actual Price vs. LSTM Model Prediction</span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Visualizing the last 100 evaluation steps comparing actual test prices against the model prediction curve.
            </p>
          </div>
          <div className="flex items-center space-x-3 text-xs font-mono">
            <span className="flex items-center space-x-1.5 text-slate-200">
              <span className="w-3 h-0.5 bg-slate-200 inline-block"></span>
              <span>Actual Price</span>
            </span>
            <span className="flex items-center space-x-1.5 text-cyan-400">
              <span className="w-3 h-0.5 bg-cyan-400 inline-block border-t border-dashed"></span>
              <span>LSTM Prediction</span>
            </span>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={forecast?.series || []} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <XAxis dataKey="index" stroke="#64748b" fontSize={11} tickLine={false} label={{ value: 'Evaluation Steps (Last 100 Periods)', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} />
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
              <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
              <Line type="monotone" dataKey="actual" stroke="#f8fafc" strokeWidth={2} dot={false} name="Actual Historical Price ($)" />
              <Line type="monotone" dataKey="predicted" stroke="#38bdf8" strokeWidth={2} strokeDasharray="4 4" dot={false} name="LSTM Predicted Trajectory ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model Architecture & Limitations Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model Specs */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Neural Architecture Details</span>
          </h3>
          <div className="mt-4 space-y-2 text-xs">
            <div className="flex justify-between py-1.5 border-b border-white/[0.04]">
              <span className="text-slate-400">Architecture</span>
              <span className="font-mono font-semibold text-white">Sequential LSTM (Keras 3)</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/[0.04]">
              <span className="text-slate-400">Sequence Window Length</span>
              <span className="font-mono font-semibold text-white">60 Trading Days</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/[0.04]">
              <span className="text-slate-400">Input Feature Dimensions</span>
              <span className="font-mono font-semibold text-white">9 Features (OHLCV + RSI + MACD + Vol)</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/[0.04]">
              <span className="text-slate-400">Feature Normalization</span>
              <span className="font-mono font-semibold text-white">MinMaxScaler (0, 1)</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Chronological Train/Test Split</span>
              <span className="font-mono font-semibold text-white">80% Train / 20% Out-of-Sample</span>
            </div>
          </div>
        </div>

        {/* Limitations & Legal Warning */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <h3 className="text-sm font-bold text-amber-400 flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4" />
            <span>Forecasting Limitations & Variance</span>
          </h3>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed">
            Machine learning models predict based purely on historical technical patterns. Unforeseen macroeconomic events,
            earnings surprises, geopolitical shocks, and liquidity crunches cannot be modeled by price sequences alone.
          </p>
          <div className="mt-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
            <strong>Important:</strong> FinAgent forecasts are estimates for quantitative analysis and backtesting. Never base
            unhedged capital allocations solely on a single algorithmic projection.
          </div>
        </div>
      </div>
    </div>
  );
};
