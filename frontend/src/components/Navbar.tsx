import React from 'react';
import { RefreshCw, TrendingUp, Sparkles, LayoutDashboard, Globe, ChevronDown } from 'lucide-react';
import { StockSummary } from '../types';

interface NavbarProps {
  currentView: 'landing' | 'dashboard';
  setCurrentView: (view: 'landing' | 'dashboard') => void;
  selectedStock: string;
  setSelectedStock: (symbol: string) => void;
  stocks: StockSummary[];
  onRefresh: () => void;
  isRefreshing: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  setCurrentView,
  selectedStock,
  setSelectedStock,
  stocks,
  onRefresh,
  isRefreshing,
}) => {
  const activeStock = stocks.find((s) => s.symbol === selectedStock) || stocks[0];

  return (
    <header className="sticky top-0 z-50 bg-[#0a0e17]/90 backdrop-blur-md border-b border-white/[0.08] px-4 lg:px-8 py-3">
      <div className="flex items-center justify-between">
        {/* Brand / Logo */}
        <div className="flex items-center space-x-6">
          <div
            onClick={() => setCurrentView('landing')}
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 p-[1px] shadow-lg shadow-emerald-500/20 group-hover:shadow-emerald-500/30 transition-all">
              <div className="w-full h-full bg-[#0d1321] rounded-xl flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight text-white font-mono">FinAgent</span>
                <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center space-x-1">
                  <Sparkles className="w-2.5 h-2.5 mr-0.5" /> AI 2.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">Intelligent Investing • Data-Driven Decisions</p>
            </div>
          </div>

          {/* Quick Stock Selector when in Dashboard */}
          {currentView === 'dashboard' && (
            <div className="hidden md:flex items-center space-x-2 pl-4 border-l border-white/[0.08]">
              <span className="text-xs text-slate-400">Active Asset:</span>
              <div className="relative">
                <select
                  value={selectedStock}
                  onChange={(e) => setSelectedStock(e.target.value)}
                  className="appearance-none bg-[#151d30] hover:bg-[#1a243c] text-white text-xs font-semibold pl-3 pr-8 py-1.5 rounded-lg border border-white/[0.1] focus:outline-none focus:border-emerald-500/50 cursor-pointer transition-all"
                >
                  {stocks.map((stock) => (
                    <option key={stock.symbol} value={stock.symbol} className="bg-[#111827] text-white">
                      {stock.symbol} — {stock.name} (${stock.current_price.toFixed(2)})
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
              </div>

              {activeStock && (
                <div className="flex items-center space-x-2 ml-2 px-2.5 py-1 rounded-md bg-white/[0.03] border border-white/[0.05]">
                  <span className="text-xs font-mono font-bold text-white">${activeStock.current_price.toFixed(2)}</span>
                  <span
                    className={`text-[11px] font-semibold font-mono ${
                      activeStock.change >= 0 ? 'text-emerald-400' : 'text-rose-400'
                    }`}
                  >
                    {activeStock.change >= 0 ? '+' : ''}
                    {activeStock.change_percent.toFixed(2)}%
                  </span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Action Bar */}
        <div className="flex items-center space-x-3">
          {/* Live Market Status Indicator */}
          <div className="hidden sm:flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>US Markets Live</span>
          </div>

          {/* Refresh Action */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white bg-[#151d30] hover:bg-[#1c263f] border border-white/[0.08] rounded-lg transition-all"
            title="Refresh Financial Pipelines"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-emerald-400' : ''}`} />
            <span className="hidden sm:inline">Refresh</span>
          </button>

          {/* View Toggle (Landing Page vs App Dashboard) */}
          <div className="flex items-center bg-[#151d30] p-0.5 rounded-lg border border-white/[0.08]">
            <button
              onClick={() => setCurrentView('landing')}
              className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                currentView === 'landing'
                  ? 'bg-emerald-500 text-slate-950 font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Globe className="w-3.5 h-3.5" />
              <span>Landing</span>
            </button>
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                currentView === 'dashboard'
                  ? 'bg-emerald-500 text-slate-950 font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              <span>Dashboard</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
