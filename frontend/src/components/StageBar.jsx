import React from 'react'

const STAGES = [
  { key: 'greeting', label: 'Welcome', icon: '👋' },
  { key: 'sales',    label: 'Loan Details', icon: '💬' },
  { key: 'verification', label: 'KYC', icon: '🔍' },
  { key: 'underwriting', label: 'Assessment', icon: '⚙️' },
  { key: 'approved', label: 'Approved', icon: '✅' },
  { key: 'rejected', label: 'Declined', icon: '❌' },
]

const STAGE_ORDER = ['greeting', 'sales', 'verification', 'underwriting', 'approved']

export default function StageBar({ stage }) {
  const isRejected = stage === 'rejected'
  const currentIdx = STAGE_ORDER.indexOf(stage)

  return (
    <div className="flex items-center gap-1 px-4 py-2 overflow-x-auto no-scrollbar">
      {STAGES.filter(s => s.key !== 'rejected').map((s, i) => {
        const idx = STAGE_ORDER.indexOf(s.key)
        const isActive = s.key === stage
        const isDone = !isRejected && currentIdx > idx
        const isPending = !isActive && !isDone

        return (
          <React.Fragment key={s.key}>
            <div className={`
              flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-300
              ${isActive && !isRejected
                ? 'bg-gold-500/20 text-gold-400 border border-gold-500/40 stage-glow'
                : isDone
                ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                : 'bg-navy-800/60 text-slate-500 border border-white/5'}
            `}>
              <span>{isDone ? '✓' : s.icon}</span>
              <span className="hidden sm:inline">{s.label}</span>
            </div>
            {i < STAGES.filter(s => s.key !== 'rejected').length - 1 && (
              <div className={`h-px w-3 flex-shrink-0 transition-colors duration-300 ${isDone ? 'bg-emerald-500/40' : 'bg-white/10'}`} />
            )}
          </React.Fragment>
        )
      })}
      {isRejected && (
        <div className="ml-auto flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-red-500/15 text-red-400 border border-red-500/30">
          <span>❌</span>
          <span>Declined</span>
        </div>
      )}
    </div>
  )
}
