import React from 'react'
import { RefreshCw, Wifi } from 'lucide-react'

export default function Header({ onReset, stage }) {
  return (
    <div className="flex items-center justify-between px-5 py-4 border-b border-white/8">
      <div className="flex items-center gap-3">
        {/* Logo mark */}
        <div className="relative w-9 h-9">
          <div className="absolute inset-0 rounded-xl bg-gold-500/20 blur-sm" />
          <div className="relative w-9 h-9 rounded-xl bg-navy-800 border border-gold-500/30 flex items-center justify-center text-lg">
            🤖
          </div>
        </div>
        <div>
          <h1 className="font-display text-white font-semibold text-base leading-tight">
            Fin<span className="shimmer-text">Bot</span>
          </h1>
          <div className="flex items-center gap-1.5 mt-0.5">
            <Wifi size={9} className="text-emerald-400" />
            <span className="text-[10px] text-emerald-400 font-medium">AI Loan Advisor · NBFC</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-navy-800/80 border border-white/8">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[10px] text-slate-400">Groq LLM</span>
        </div>
        <button
          onClick={onReset}
          title="Start over"
          className="p-2 rounded-xl bg-navy-800/60 border border-white/8 text-slate-400
            hover:text-gold-400 hover:border-gold-500/30 transition-all duration-150
            hover:scale-105 active:scale-95"
        >
          <RefreshCw size={14} />
        </button>
      </div>
    </div>
  )
}
