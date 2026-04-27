import React from 'react'

const FEATURES = [
  { icon: '⚡', text: 'Instant eligibility check' },
  { icon: '🔒', text: 'Secure KYC verification' },
  { icon: '📋', text: 'Auto sanction letter' },
  { icon: '🤖', text: 'Groq-powered AI decisions' },
]

export default function WelcomeScreen({ onSend }) {
  return (
    <div className="flex flex-col items-center justify-center h-full px-6 text-center select-none">
      {/* Hero icon */}
      <div className="relative mb-6">
        <div className="absolute inset-0 rounded-3xl bg-gold-500/15 blur-2xl scale-150" />
        <div className="relative w-20 h-20 rounded-3xl bg-navy-800 border border-gold-500/30
          flex items-center justify-center text-4xl shadow-2xl">
          🏦
        </div>
      </div>

      <h2 className="font-display text-2xl text-white font-semibold mb-2">
        Welcome to <span className="shimmer-text">FinBot</span>
      </h2>
      <p className="text-slate-400 text-sm max-w-xs leading-relaxed mb-8">
        Your intelligent loan assistant. Get a personal loan from ₹10,000 to ₹20 lakh — fully automated, in minutes.
      </p>

      {/* Feature pills */}
      <div className="grid grid-cols-2 gap-2 mb-8 w-full max-w-xs">
        {FEATURES.map(f => (
          <div key={f.text}
            className="flex items-center gap-2 px-3 py-2.5 rounded-xl
              bg-navy-800/60 border border-white/8 text-left">
            <span className="text-base">{f.icon}</span>
            <span className="text-xs text-slate-300 leading-tight">{f.text}</span>
          </div>
        ))}
      </div>

      {/* CTA */}
      <button
        onClick={() => onSend('I need a personal loan')}
        className="px-6 py-3 rounded-2xl bg-gold-500/20 border border-gold-500/40
          text-gold-400 font-semibold text-sm hover:bg-gold-500/30
          transition-all duration-200 hover:scale-105 active:scale-95 stage-glow"
      >
        Apply for a Loan →
      </button>

      <p className="text-[10px] text-slate-600 mt-6">
        Demo accounts: 9876543210 · 9123456780 · 8000000001
      </p>
    </div>
  )
}
