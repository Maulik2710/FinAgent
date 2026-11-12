import React from 'react';
import { Sliders, Cpu, Server, Code, CheckCircle2, ShieldCheck, Terminal } from 'lucide-react';

export const ArchitectureSettingsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-white/[0.08]">
        <h2 className="text-2xl font-bold text-white tracking-tight">FinAgent Architecture & System Specifications</h2>
        <p className="text-xs text-slate-400 mt-1">
          Technical parameters, neural network configurations, and REST API topology.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ML & DL Models */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center space-x-2 text-cyan-400 text-sm font-bold mb-4">
            <Cpu className="w-4 h-4" />
            <span>Machine Learning & NLP Configuration</span>
          </div>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">LSTM Framework</span>
              <span className="font-mono text-white">TensorFlow 2.17 / Keras 3</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Lookback Sequence Window</span>
              <span className="font-mono text-white">60 Timesteps</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Loss Function & Optimizer</span>
              <span className="font-mono text-white">MSE / Adam</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">FinBERT Sentiment Model</span>
              <span className="font-mono text-white">ProsusAI/finbert (PyTorch)</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">RAG Embedding & LLM</span>
              <span className="font-mono text-white">TF-IDF Vector Space & Gemini 2.5</span>
            </div>
          </div>
        </div>

        {/* Portfolio & Math Engine */}
        <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
          <div className="flex items-center space-x-2 text-purple-400 text-sm font-bold mb-4">
            <Sliders className="w-4 h-4" />
            <span>Modern Portfolio Theory Solver</span>
          </div>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Optimization Algorithm</span>
              <span className="font-mono text-white">SciPy SLSQP (Sequential Least Squares)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Objective Function</span>
              <span className="font-mono text-white">Maximize Sharpe Ratio (Negative Minimize)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Risk-Free Benchmark Rate (Rf)</span>
              <span className="font-mono text-white">2.0% Annualized</span>
            </div>
            <div className="flex justify-between py-2 border-b border-white/[0.04]">
              <span className="text-slate-400">Budget Constraint</span>
              <span className="font-mono text-white">Σ weights = 1.0 (No leverage)</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Long-Only Bounds</span>
              <span className="font-mono text-white">weight ∈ [0.0, 1.0]</span>
            </div>
          </div>
        </div>
      </div>

      {/* REST API Endpoints Specification Table */}
      <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08]">
        <div className="flex items-center space-x-2 text-emerald-400 text-sm font-bold mb-4">
          <Server className="w-4 h-4" />
          <span>FastAPI Production Endpoints Topology</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-white/[0.08] text-slate-400 font-mono">
                <th className="py-2.5 px-3">METHOD</th>
                <th className="py-2.5 px-3">ENDPOINT</th>
                <th className="py-2.5 px-3">DESCRIPTION</th>
                <th className="py-2.5 px-3">OUTPUT SCHEMA</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04] text-slate-200 font-mono">
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/stocks</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">List all 10 equities with latest close & change</td>
                <td className="py-2.5 px-3 text-slate-300">StockSummary[]</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/stocks/&#123;symbol&#125;</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">Full OHLCV history & technical indicators</td>
                <td className="py-2.5 px-3 text-slate-300">StockDetailResponse</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/forecast/&#123;symbol&#125;</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">LSTM actual vs predicted sequence series</td>
                <td className="py-2.5 px-3 text-slate-300">ForecastResponse</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/news/&#123;symbol&#125;</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">NewsAPI articles with FinBERT sentiment & confidence</td>
                <td className="py-2.5 px-3 text-slate-300">NewsResponse</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/portfolio/optimization</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">SLSQP weights, expected return, vol & benchmark</td>
                <td className="py-2.5 px-3 text-slate-300">PortfolioResponse</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-emerald-400 font-bold">GET</td>
                <td className="py-2.5 px-3 text-white">/api/recommendations/&#123;symbol&#125;</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">Multi-factor recommendation with confidence & reasons</td>
                <td className="py-2.5 px-3 text-slate-300">RecommendationResponse</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 text-cyan-400 font-bold">POST</td>
                <td className="py-2.5 px-3 text-white">/api/chat</td>
                <td className="py-2.5 px-3 text-slate-400 font-sans">Grounded RAG assistant with source documents</td>
                <td className="py-2.5 px-3 text-slate-300">ChatResponse</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
