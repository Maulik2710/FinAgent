import React from 'react';
import {
  BarChart3,
  TrendingUp,
  Cpu,
  Newspaper,
  PieChart,
  BrainCircuit,
  MessageSquareCode,
  Sliders,
  ShieldCheck,
} from 'lucide-react';

export type DashboardTab =
  | 'overview'
  | 'analysis'
  | 'forecasting'
  | 'news'
  | 'portfolio'
  | 'recommendations'
  | 'assistant'
  | 'settings';

interface SidebarProps {
  activeTab: DashboardTab;
  setActiveTab: (tab: DashboardTab) => void;
  selectedStock: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, selectedStock }) => {
  const navItems = [
    {
      id: 'overview' as DashboardTab,
      label: 'Overview',
      icon: BarChart3,
      badge: 'Live',
    },
    {
      id: 'analysis' as DashboardTab,
      label: 'Stock Analysis',
      icon: TrendingUp,
      badge: selectedStock,
    },
    {
      id: 'forecasting' as DashboardTab,
      label: 'LSTM Forecasting',
      icon: Cpu,
      badge: 'AI',
    },
    {
      id: 'news' as DashboardTab,
      label: 'News & Sentiment',
      icon: Newspaper,
      badge: 'FinBERT',
    },
    {
      id: 'portfolio' as DashboardTab,
      label: 'Portfolio Optimizer',
      icon: PieChart,
      badge: 'MPT',
    },
    {
      id: 'recommendations' as DashboardTab,
      label: 'AI Recommendations',
      icon: BrainCircuit,
      badge: 'Signal',
    },
    {
      id: 'assistant' as DashboardTab,
      label: 'Financial Assistant',
      icon: MessageSquareCode,
      badge: 'RAG',
    },
    {
      id: 'settings' as DashboardTab,
      label: 'Model Architecture',
      icon: Sliders,
    },
  ];

  return (
    <aside className="w-64 bg-[#0a0e17] border-r border-white/[0.08] flex flex-col justify-between py-5 px-3 min-h-[calc(100vh-60px)]">
      <div>
        {/* Navigation Category Label */}
        <div className="px-3 mb-2">
          <p className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold">
            Core Modules
          </p>
        </div>

        {/* Navigation Buttons */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-[#151d30]/60 border border-transparent'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                      isActive
                        ? 'bg-emerald-500/20 text-emerald-300 font-semibold'
                        : 'bg-white/[0.05] text-slate-400'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* System Status Footnote */}
      <div className="mt-8 px-3">
        <div className="p-3 rounded-xl bg-[#111827] border border-white/[0.06]">
          <div className="flex items-center space-x-2 text-emerald-400 text-xs font-semibold">
            <ShieldCheck className="w-4 h-4" />
            <span>FinAgent v2.0 Engine</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
            Connected to 10 Equities • LSTM Forecast • FinBERT News • SciPy MPT
          </p>
        </div>
      </div>
    </aside>
  );
};
