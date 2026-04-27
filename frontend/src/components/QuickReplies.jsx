import React from 'react'

const SUGGESTIONS_BY_STAGE = {
  greeting: [
    'I need a personal loan',
    'Home renovation loan',
    'Education loan for college',
    'Medical emergency loan',
  ],
  sales: [
    '₹2 lakh for 24 months',
    '₹5 lakh for 36 months',
    'My salary is ₹50,000/month',
    'Change the amount',
  ],
  verification: [
    'My phone is 9876543210',
    'My PAN is ABCDE1234F',
  ],
}

export default function QuickReplies({ stage, onSelect }) {
  const suggestions = SUGGESTIONS_BY_STAGE[stage] || []
  if (!suggestions.length) return null

  return (
    <div className="flex flex-wrap gap-2 px-4 pb-2">
      {suggestions.map((s) => (
        <button
          key={s}
          onClick={() => onSelect(s)}
          className="text-xs px-3 py-1.5 rounded-full border border-gold-500/25
            text-gold-400/80 bg-gold-500/5 hover:bg-gold-500/15 hover:border-gold-500/50
            transition-all duration-150 hover:scale-105 active:scale-95"
        >
          {s}
        </button>
      ))}
    </div>
  )
}
