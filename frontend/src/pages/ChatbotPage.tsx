import React, { useState } from 'react';
import {
  MessageSquareCode,
  Send,
  Sparkles,
  User,
  Bot,
  FileText,
  Trash2,
  HelpCircle,
  Lightbulb,
} from 'lucide-react';
import { ChatMessage } from '../types';
import { sendChatMessage } from '../services/api';

export const ChatbotPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content:
        'Hello! I am FinAgent, your AI Financial Assistant. I answer questions using grounded knowledge documents from our asset allocation, stocks, mutual funds, and portfolio research database.\n\nAsk me anything or select one of the suggestions below!',
      sources: ['saving_and_investing.txt'],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const starters = [
    'What does diversification mean?',
    'What is the Sharpe ratio?',
    'Explain the difference between equity and debt.',
    'How does asset allocation manage portfolio risk?',
  ];

  const handleSend = async (questionText?: string) => {
    const q = questionText || input;
    if (!q.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(q);
      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.answer,
        sources: res.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I apologize, but I could not retrieve an answer at this time. Please try again.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: 'Conversation cleared. How can I assist you with your financial research today?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  return (
    <div className="h-[calc(100vh-140px)] flex flex-col justify-between max-w-4xl mx-auto bg-[#111827] rounded-3xl border border-white/[0.08] overflow-hidden">
      {/* Chat Header */}
      <div className="p-4 px-6 bg-[#0d1321] border-b border-white/[0.08] flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <span>Financial RAG Assistant</span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Grounded
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Indexed against 4 institutional financial documents</p>
          </div>
        </div>

        <button
          onClick={handleClear}
          className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-rose-400 p-2 rounded-lg hover:bg-white/[0.04] transition-all"
          title="Clear Conversation"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Clear</span>
        </button>
      </div>

      {/* Message List */}
      <div className="flex-1 p-6 overflow-y-auto space-y-5">
        {messages.map((msg) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={msg.id}
              className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
            >
              <div
                className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                  isUser ? 'bg-emerald-500 text-slate-950 font-bold' : 'bg-[#151d30] border border-white/[0.08] text-emerald-400'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-line ${
                    isUser
                      ? 'bg-emerald-500 text-slate-950 font-medium rounded-tr-none'
                      : 'bg-[#151d30] text-slate-100 border border-white/[0.08] rounded-tl-none'
                  }`}
                >
                  {msg.content}
                </div>

                {/* Sources / Citations */}
                {!isUser && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-2 flex flex-wrap items-center gap-1.5 text-[10px]">
                    <span className="text-slate-500 font-mono">Sources:</span>
                    {msg.sources.map((src, i) => (
                      <span
                        key={i}
                        className="inline-flex items-center space-x-1 px-2 py-0.5 rounded bg-white/[0.05] border border-white/[0.06] text-cyan-400 font-mono"
                      >
                        <FileText className="w-2.5 h-2.5" />
                        <span>{src}</span>
                      </span>
                    ))}
                  </div>
                )}

                <span className="text-[10px] text-slate-500 font-mono mt-1 block">
                  {msg.timestamp}
                </span>
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-start space-x-3">
            <div className="w-7 h-7 rounded-lg bg-[#151d30] border border-white/[0.08] flex items-center justify-center text-emerald-400">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-3.5 rounded-2xl bg-[#151d30] border border-white/[0.08] rounded-tl-none flex items-center space-x-2 text-xs text-slate-400">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></div>
              <span>Searching knowledge base and synthesizing grounded answer...</span>
            </div>
          </div>
        )}
      </div>

      {/* Quick Suggestion Starters */}
      <div className="px-6 py-2 bg-[#0d1321] border-t border-white/[0.04]">
        <div className="flex items-center space-x-2 overflow-x-auto pb-1 text-xs">
          <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0" />
          <span className="text-slate-500 text-[11px] shrink-0 font-mono">Suggested:</span>
          {starters.map((starter, i) => (
            <button
              key={i}
              onClick={() => handleSend(starter)}
              className="px-2.5 py-1 rounded-lg bg-[#151d30] hover:bg-[#1c263f] border border-white/[0.06] text-slate-300 hover:text-white text-xs whitespace-nowrap transition-all"
            >
              {starter}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-4 px-6 bg-[#0d1321] border-t border-white/[0.08] flex items-center space-x-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about investing, diversification, or portfolio theory..."
          className="flex-1 bg-[#151d30] text-white text-xs sm:text-sm px-4 py-2.5 rounded-xl border border-white/[0.1] focus:outline-none focus:border-emerald-500/50 placeholder:text-slate-500"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-slate-950 font-bold transition-all"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
