import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, DashboardTab } from './components/Sidebar';
import { LandingPage } from './pages/LandingPage';
import { DashboardOverview } from './pages/DashboardOverview';
import { StockAnalysisPage } from './pages/StockAnalysisPage';
import { StockForecastingPage } from './pages/StockForecastingPage';
import { MarketNewsPage } from './pages/MarketNewsPage';
import { PortfolioOptimizerPage } from './pages/PortfolioOptimizerPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { ChatbotPage } from './pages/ChatbotPage';
import { ArchitectureSettingsPage } from './pages/ArchitectureSettingsPage';
import {
  fetchStocks,
  fetchStockDetail,
  fetchForecast,
  fetchNews,
  fetchPortfolioOptimization,
  fetchRecommendation,
} from './services/api';
import {
  StockSummary,
  StockDetailResponse,
  ForecastResponse,
  NewsResponse,
  PortfolioResponse,
  RecommendationResponse,
} from './types';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<'landing' | 'dashboard'>('landing');
  const [activeTab, setActiveTab] = useState<DashboardTab>('overview');
  const [selectedStock, setSelectedStock] = useState<string>('NVDA');

  // Core Data States
  const [stocks, setStocks] = useState<StockSummary[]>([]);
  const [stockDetail, setStockDetail] = useState<StockDetailResponse | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [news, setNews] = useState<NewsResponse | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioResponse | null>(null);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);

  const [isRefreshing, setIsRefreshing] = useState(false);

  // Initial load
  useEffect(() => {
    loadAllData(selectedStock);
  }, []);

  // When selected stock changes
  useEffect(() => {
    loadStockSpecificData(selectedStock);
  }, [selectedStock]);

  const loadAllData = async (symbol: string) => {
    setIsRefreshing(true);
    try {
      const [stocksData, portData] = await Promise.all([
        fetchStocks(),
        fetchPortfolioOptimization(),
      ]);
      setStocks(stocksData);
      setPortfolio(portData);

      await loadStockSpecificData(symbol);
    } catch (err) {
      console.error('Failed to load initial data:', err);
    } finally {
      setIsRefreshing(false);
    }
  };

  const loadStockSpecificData = async (symbol: string) => {
    try {
      const [detailData, forecastData, newsData, recData] = await Promise.all([
        fetchStockDetail(symbol),
        fetchForecast(symbol),
        fetchNews(symbol),
        fetchRecommendation(symbol),
      ]);
      setStockDetail(detailData);
      setForecast(forecastData);
      setNews(newsData);
      setRecommendation(recData);
    } catch (err) {
      console.error(`Failed to load data for ${symbol}:`, err);
    }
  };

  const handleRefresh = () => {
    loadAllData(selectedStock);
  };

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-slate-950">
      {/* Top Navbar */}
      <Navbar
        currentView={currentView}
        setCurrentView={setCurrentView}
        selectedStock={selectedStock}
        setSelectedStock={setSelectedStock}
        stocks={stocks}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
      />

      {/* Main Content View Switcher */}
      {currentView === 'landing' ? (
        <LandingPage onExplore={() => setCurrentView('dashboard')} stocks={stocks} />
      ) : (
        <div className="flex-1 flex overflow-hidden">
          {/* Dashboard Left Sidebar */}
          <Sidebar
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            selectedStock={selectedStock}
          />

          {/* Active Tab Main View Area */}
          <main className="flex-1 p-6 lg:p-8 overflow-y-auto max-h-[calc(100vh-65px)]">
            {activeTab === 'overview' && (
              <DashboardOverview
                selectedStock={selectedStock}
                setSelectedStock={setSelectedStock}
                stocks={stocks}
                stockDetail={stockDetail}
                forecast={forecast}
                news={news}
                portfolio={portfolio}
                recommendation={recommendation}
                onNavigateTab={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'analysis' && (
              <StockAnalysisPage
                selectedStock={selectedStock}
                setSelectedStock={setSelectedStock}
                stocks={stocks}
                stockDetail={stockDetail}
              />
            )}

            {activeTab === 'forecasting' && (
              <StockForecastingPage
                selectedStock={selectedStock}
                setSelectedStock={setSelectedStock}
                stocks={stocks}
                forecast={forecast}
              />
            )}

            {activeTab === 'news' && (
              <MarketNewsPage
                selectedStock={selectedStock}
                setSelectedStock={setSelectedStock}
                stocks={stocks}
                news={news}
              />
            )}

            {activeTab === 'portfolio' && (
              <PortfolioOptimizerPage portfolio={portfolio} />
            )}

            {activeTab === 'recommendations' && (
              <RecommendationsPage
                selectedStock={selectedStock}
                setSelectedStock={setSelectedStock}
                stocks={stocks}
                recommendation={recommendation}
              />
            )}

            {activeTab === 'assistant' && <ChatbotPage />}

            {activeTab === 'settings' && <ArchitectureSettingsPage />}
          </main>
        </div>
      )}
    </div>
  );
};

export default App;
