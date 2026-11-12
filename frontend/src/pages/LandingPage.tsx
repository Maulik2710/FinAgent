import React from 'react';
import {
  TrendingUp,
  Cpu,
  Newspaper,
  PieChart,
  BrainCircuit,
  MessageSquareCode,
  ArrowRight,
  Shield,
  Layers,
  Sparkles,
  BarChart2,
  CheckCircle2,
} from 'lucide-react';
import { StockSummary } from '../types';

interface LandingPageProps {
  onExplore: () => void;
  stocks: StockSummary[];
}

export const LandingPage: React.FC<LandingPageProps> = ({ onExplore, stocks }) => {
  const topStock = stocks.find((s) => s.symbol === 'NVDA') || stocks[0] || {
    symbol: 'NVDA',
    name: 'NVIDIA Corp.',
    current_price: 182.4,
    change: 3.5,
    change_percent: 1.96,
  };

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-16 lg:pt-28 lg:pb-24 px-4 sm:px-6 lg:px-8 border-b border-white/[0.06]">
        {/* Subtle Ambient Background Gradients */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-emerald-500/10 blur-[130px] rounded-full pointer-events-none" />
        <div className="absolute top-1/3 left-1/4 w-[400px] h-[300px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-6xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-xs font-medium mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Next-Generation Quantitative Analytics & AI Portfolio Engine</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
            Make Smarter Investment Decisions with{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              Artificial Intelligence
            </span>
          </h1>

          <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Analyze markets, evaluate institutional sentiment with FinBERT, forecast price movements with LSTM neural
            networks, optimize portfolios with SciPy MPT, and interrogate financial documents with a grounded RAG assistant.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={onExplore}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/25 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5"
            >
              <span>Explore Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <a
              href="#features"
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-[#151d30] hover:bg-[#1a243c] border border-white/[0.1] text-slate-200 hover:text-white font-medium text-sm transition-all"
            >
              Discover Features
            </a>
          </div>

          {/* Interactive Live Product Preview Card */}
          <div className="mt-14 max-w-5xl mx-auto rounded-2xl bg-[#0f172a]/90 border border-white/[0.12] p-4 sm:p-6 shadow-2xl text-left">
            <div className="flex items-center justify-between pb-4 border-b border-white/[0.08]">
              <div className="flex items-center space-x-3">
                <div className="flex space-x-1.5">
                  <span className="w-3 h-3 rounded-full bg-rose-500/80"></span>
                  <span className="w-3 h-3 rounded-full bg-amber-500/80"></span>
                  <span className="w-3 h-3 rounded-full bg-emerald-500/80"></span>
                </div>
                <span className="text-xs text-slate-400 font-mono">FinAgent Terminal Preview</span>
              </div>
              <span className="text-xs font-mono text-emerald-400 font-medium">Model Status: ACTIVE</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-5">
              {/* Card 1: Asset Info */}
              <div className="p-4 rounded-xl bg-[#151d30] border border-white/[0.06]">
                <p className="text-xs text-slate-400 uppercase font-mono">Featured Asset</p>
                <div className="mt-1 flex items-baseline space-x-2">
                  <span className="text-2xl font-bold font-mono text-white">{topStock.symbol}</span>
                  <span className="text-xs text-slate-400">{topStock.name}</span>
                </div>
                <div className="mt-2 flex items-baseline space-x-2">
                  <span className="text-xl font-bold font-mono text-white">${topStock.current_price.toFixed(2)}</span>
                  <span className="text-xs font-bold text-emerald-400 font-mono">
                    +{topStock.change_percent.toFixed(2)}%
                  </span>
                </div>
              </div>

              {/* Card 2: Neural Forecast */}
              <div className="p-4 rounded-xl bg-[#151d30] border border-white/[0.06]">
                <p className="text-xs text-slate-400 uppercase font-mono">LSTM Forecast (T+30)</p>
                <p className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                  ${(topStock.current_price * 1.085).toFixed(2)}
                </p>
                <p className="text-xs text-emerald-400 mt-2 font-semibold">📈 +8.5% Expected Bullish Return</p>
              </div>

              {/* Card 3: Portfolio Weight */}
              <div className="p-4 rounded-xl bg-[#151d30] border border-white/[0.06]">
                <p className="text-xs text-slate-400 uppercase font-mono">Sharpe Optimal Weight</p>
                <p className="text-2xl font-bold font-mono text-cyan-400 mt-1">53.88%</p>
                <p className="text-xs text-slate-400 mt-2 font-mono">Sharpe Ratio: 1.30 • Vol: 38.7%</p>
              </div>

              {/* Card 4: AI Decision */}
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <p className="text-xs text-emerald-300 uppercase font-mono">Composite AI Signal</p>
                <p className="text-2xl font-bold font-mono text-emerald-400 mt-1">STRONG BUY</p>
                <p className="text-xs text-slate-300 mt-2">Confidence: 84.5% • Multi-Factor</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-extrabold text-white tracking-tight">Institutional-Grade Intelligence Modules</h2>
          <p className="mt-3 text-slate-400 text-sm max-w-xl mx-auto">
            Combining predictive deep learning, natural language processing, mathematical portfolio theory, and generative AI.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-105 transition-transform">
              <Cpu className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">LSTM Stock Forecasting</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Trained Sequential Recurrent Neural Networks process 60-day historical time series sequences, extracting
              momentum and predicting next-period target values.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-105 transition-transform">
              <Newspaper className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">FinBERT News Sentiment</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Specialized financial NLP transformer classifies real-time institutional headlines into Positive, Neutral,
              and Negative sentiments with calibrated confidence scores.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
              <PieChart className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Portfolio Optimization (MPT)</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Modern Portfolio Theory implemented via SciPy SLSQP optimization. Maximizes the Sharpe ratio across the
              equity universe and benchmarks against equal-weight allocations.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4 group-hover:scale-105 transition-transform">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Transparent AI Recommendations</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Multi-signal decision engine combines forecast momentum (40%), news sentiment (30%), and portfolio weight
              (30%) into clear, explainable Strong Buy/Buy/Hold/Sell actions.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-4 group-hover:scale-105 transition-transform">
              <MessageSquareCode className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Financial RAG Assistant</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Context-grounded assistant interrogates curated financial texts and SEC documents. Guarantees no hallucination
              by enforcing strict context citation.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="p-6 rounded-2xl bg-[#111827] border border-white/[0.08] hover:border-emerald-500/30 transition-all group">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4 group-hover:scale-105 transition-transform">
              <BarChart2 className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Full Technical Indicators</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">
              Pre-computed technical indicators including 20-period SMA, 20-period EMA, 14-period RSI, MACD with signal line,
              and 20-day rolling annualized volatility.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works Pipeline Section */}
      <section className="py-20 bg-[#0d1321] border-y border-white/[0.06] px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-extrabold text-white tracking-tight">The FinAgent Analytical Pipeline</h2>
            <p className="mt-3 text-slate-400 text-sm max-w-xl mx-auto">
              How raw market feeds and news articles transform into high-confidence investment decisions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-[#151d30] border border-white/[0.08]">
              <span className="text-xs font-mono font-bold text-emerald-400">STEP 01</span>
              <h4 className="text-sm font-bold text-white mt-2">Data Ingestion & Cleaning</h4>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                Automated yfinance and NewsAPI data collection with validation, missing value imputation, and schema normalization.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-[#151d30] border border-white/[0.08]">
              <span className="text-xs font-mono font-bold text-cyan-400">STEP 02</span>
              <h4 className="text-sm font-bold text-white mt-2">Feature Engineering</h4>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                Calculation of RSI, MACD oscillators, Exponential Moving Averages, and historical covariance matrices.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-[#151d30] border border-white/[0.08]">
              <span className="text-xs font-mono font-bold text-purple-400">STEP 03</span>
              <h4 className="text-sm font-bold text-white mt-2">Dual-Model Inference</h4>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                LSTM neural network generates price trajectory while FinBERT processes sentiment across fresh news.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-[#151d30] border border-white/[0.08]">
              <span className="text-xs font-mono font-bold text-amber-400">STEP 04</span>
              <h4 className="text-sm font-bold text-white mt-2">MPT & Decision Engine</h4>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                SciPy SLSQP maximizes Sharpe ratio, and the recommendation engine combines all weights with explainable reasoning.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack Badges */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto text-center">
        <p className="text-xs font-mono uppercase tracking-wider text-slate-400 font-semibold mb-6">
          Architected on Industry Standard Open-Source Technologies
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          {[
            'Python 3.12',
            'FastAPI',
            'TensorFlow / Keras',
            'HuggingFace Transformers',
            'FinBERT',
            'SciPy SLSQP',
            'Pandas / NumPy',
            'React 19',
            'TypeScript',
            'Tailwind CSS',
            'Recharts',
            'Google Gemini AI',
          ].map((tech) => (
            <span
              key={tech}
              className="px-3.5 py-1.5 rounded-lg bg-[#151d30] border border-white/[0.08] text-xs font-medium text-slate-300 font-mono"
            >
              {tech}
            </span>
          ))}
        </div>
      </section>

      {/* Disclaimer Section */}
      <footer className="py-10 border-t border-white/[0.08] bg-[#070a10] px-4 text-center">
        <div className="max-w-3xl mx-auto">
          <p className="text-xs text-slate-500 leading-relaxed">
            <strong className="text-slate-400">Disclaimer:</strong> FinAgent is designed strictly for financial analysis,
            academic exploration, and educational research purposes. Machine learning stock price forecasts and automated
            recommendations are mathematical estimates subject to market volatility and do not constitute guaranteed investment,
            tax, or legal advice.
          </p>
          <p className="text-[11px] text-slate-600 mt-4 font-mono">
            © {new Date().getFullYear()} FinAgent AI • Production SaaS Architecture
          </p>
        </div>
      </footer>
    </div>
  );
};
