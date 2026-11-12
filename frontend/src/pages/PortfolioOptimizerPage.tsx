import React from 'react';
import {
  PieChart,
  TrendingUp,
  ShieldAlert,
  Sliders,
  Scale,
  Award,
  HelpCircle,
} from 'lucide-react';
import { PortfolioResponse } from '../types';

interface PortfolioOptimizerPageProps {
  portfolio: PortfolioResponse | null;
}

export const PortfolioOptimizerPage: React.FC<PortfolioOptimizerPageProps> = ({ portfolio }) => {
  const allocations = portfolio?.allocations || [];
  const benchmark = portfolio?.benchmark || {
    expected_return: 38.12,
    volatility: 34.25,
    sharpe_ratio: 0.98,
  };

  const optReturn = portfolio?.expected_return ?? 55.47;
  const optVol = portfolio?.volatility ?? 38.72;
  const optSharpe = portfolio?.sharpe_ratio ?? 1.30;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-white tracking-tight">Modern Portfolio Theory (MPT) Optimizer</h2>
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400">
              SciPy SLSQP
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Quadratic mathematical optimization maximizing the Sharpe Ratio over the 10-stock universe.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <span>Objective:</span>
          <span className="px-2 py-1 rounded bg-[#151d30] text-emerald-400 font-bold border border-white/[0.08]">
            Max Sharpe Ratio (Rf = 2.0%)
          </span>
        </div>
      </div>

      {/* Side-by-Side Comparison: Equal-Weight vs Optimized MPT Portfolio */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Optimized Portfolio Card */}
        <div className="p-6 rounded-2xl bg-[#111827] border-2 border-purple-500/40 relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-purple-500 text-slate-950 text-[10px] font-mono font-bold px-3 py-1 rounded-bl-xl uppercase tracking-wider flex items-center space-x-1">
            <Award className="w-3 h-3 mr-1" />
            <span>Optimal SLSQP Allocation</span>
          </div>

          <p className="text-xs font-mono text-purple-400 uppercase">FinAgent Optimized Strategy</p>
          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Exp Return</p>
              <p className="text-2xl font-bold font-mono text-emerald-400 mt-1">{optReturn.toFixed(1)}%</p>
              <p className="text-[10px] text-emerald-400 mt-0.5">+{(optReturn - benchmark.expected_return).toFixed(1)}% vs Bench</p>
            </div>
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Volatility</p>
              <p className="text-2xl font-bold font-mono text-slate-200 mt-1">{optVol.toFixed(1)}%</p>
              <p className="text-[10px] text-slate-400 mt-0.5">Annualized StdDev</p>
            </div>
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Sharpe Ratio</p>
              <p className="text-2xl font-bold font-mono text-purple-400 mt-1">{optSharpe.toFixed(2)}</p>
              <p className="text-[10px] text-purple-300 mt-0.5">+{(optSharpe - benchmark.sharpe_ratio).toFixed(2)} Outperform</p>
            </div>
          </div>
        </div>

        {/* Benchmark Equal-Weight Card */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <p className="text-xs font-mono text-slate-400 uppercase">Benchmark Baseline (1/N Equal Weight)</p>
          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Exp Return</p>
              <p className="text-2xl font-bold font-mono text-slate-300 mt-1">{benchmark.expected_return.toFixed(1)}%</p>
              <p className="text-[10px] text-slate-500 mt-0.5">Equal 10% Each</p>
            </div>
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Volatility</p>
              <p className="text-2xl font-bold font-mono text-slate-300 mt-1">{benchmark.volatility.toFixed(1)}%</p>
              <p className="text-[10px] text-slate-500 mt-0.5">Unhedged Baseline</p>
            </div>
            <div className="p-3 rounded-xl bg-[#151d30]">
              <p className="text-[10px] text-slate-400 font-mono uppercase">Sharpe Ratio</p>
              <p className="text-2xl font-bold font-mono text-slate-300 mt-1">{benchmark.sharpe_ratio.toFixed(2)}</p>
              <p className="text-[10px] text-slate-500 mt-0.5">Standard Baseline</p>
            </div>
          </div>
        </div>
      </div>

      {/* Asset Allocation Breakdown Table */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <h3 className="text-base font-bold text-white mb-2">Optimal Equity Allocations</h3>
        <p className="text-xs text-slate-400 mb-6">
          Distribution derived by the Sequential Least Squares Programming solver subject to budget constraint (Σw = 1.0).
        </p>

        <div className="space-y-4">
          {allocations.map((item) => (
            <div key={item.symbol} className="p-3.5 rounded-xl bg-[#151d30] border border-white/[0.04]">
              <div className="flex items-center justify-between text-xs mb-2">
                <div className="flex items-center space-x-3">
                  <span className="font-mono font-bold text-white text-sm">{item.symbol}</span>
                  <span className="text-slate-400">{item.name}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-slate-500 font-mono">Weight: {item.weight.toFixed(4)}</span>
                  <span className="font-mono font-bold text-purple-400 text-sm">
                    {item.allocation_percent.toFixed(2)}%
                  </span>
                </div>
              </div>
              <div className="w-full h-2 rounded-full bg-[#0a0e17] overflow-hidden">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-purple-500 to-indigo-400"
                  style={{ width: `${Math.max(item.allocation_percent, 0.5)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Educational Guide on Sharpe Ratio & MPT Limitations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <h4 className="text-sm font-bold text-white flex items-center space-x-2">
            <Scale className="w-4 h-4 text-purple-400" />
            <span>Understanding the Sharpe Ratio</span>
          </h4>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed">
            The Sharpe ratio measures the excess return per unit of volatility:
            <code className="block mt-2 p-2 rounded bg-[#0a0e17] font-mono text-purple-300 text-center">
              Sharpe Ratio = (Expected Return - Risk-Free Rate) / Portfolio Volatility
            </code>
            A higher Sharpe ratio indicates superior risk-adjusted performance, allowing an investor to achieve greater gains
            without taking on excessive covariance risk.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <h4 className="text-sm font-bold text-amber-400 flex items-center space-x-2">
            <ShieldAlert className="w-4 h-4" />
            <span>Limitations of Historical Optimization</span>
          </h4>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed">
            Markowitz optimization assumes that past returns and covariance matrices will remain stationary in the future.
            During market regime shifts or black swan events, asset correlations often converge toward 1.0, reducing
            the real-world diversification benefit.
          </p>
        </div>
      </div>
    </div>
  );
};
