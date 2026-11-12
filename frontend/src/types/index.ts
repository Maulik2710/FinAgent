export interface StockSummary {
  symbol: string;
  name: string;
  current_price: number;
  previous_close: number;
  change: number;
  change_percent: number;
  daily_volume: number;
  rsi?: number;
  macd?: number;
}

export interface HistoricalDataPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  daily_return?: number;
  sma_20?: number;
  ema_20?: number;
  rsi_14?: number;
  macd?: number;
  macd_signal?: number;
  rolling_volatility?: number;
}

export interface StockDetailResponse {
  symbol: string;
  name: string;
  current_price: number;
  change: number;
  change_percent: number;
  history: HistoricalDataPoint[];
}

export interface ForecastDataPoint {
  index: number;
  actual?: number;
  predicted?: number;
}

export interface ForecastResponse {
  symbol: string;
  current_price: number;
  predicted_price: number;
  expected_return: number;
  trend: 'Bullish' | 'Bearish';
  series: ForecastDataPoint[];
}

export interface NewsArticle {
  title: string;
  description?: string;
  source?: string;
  publishedAt?: string;
  url?: string;
  sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  confidence: number;
}

export interface NewsResponse {
  symbol: string;
  overall_sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  sentiment_score: number;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  articles: NewsArticle[];
}

export interface StockAllocation {
  symbol: string;
  name: string;
  weight: number;
  allocation_percent: number;
}

export interface PortfolioBenchmark {
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
}

export interface PortfolioResponse {
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
  allocations: StockAllocation[];
  benchmark: PortfolioBenchmark;
}

export interface RecommendationResponse {
  symbol: string;
  name: string;
  current_price: number;
  predicted_price: number;
  expected_return: number;
  sentiment_score: number;
  portfolio_weight: number;
  recommendation: 'Strong Buy' | 'Buy' | 'Hold' | 'Sell' | 'Strong Sell';
  confidence: number;
  score: number;
  reasons: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: string;
}
