import React from 'react'

function Row({ label, value, highlight }) {
  if (!value && value !== 0) return null
  return (
    <div className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
      <span className="text-xs text-slate-400">{label}</span>
      <span className={`text-xs font-medium font-mono ${highlight ? 'text-gold-400' : 'text-slate-200'}`}>
        {value}
      </span>
    </div>
  )
}

function fmt(n) {
  if (!n) return null
  return '₹' + Number(n).toLocaleString('en-IN')
}

function fmtRate(r) {
  if (!r) return null
  return (r * 100).toFixed(1) + '% p.a.'
}

export default function LoanPanel({ loanData, sanctionUrl, stage }) {
  if (!loanData) return null

  const hasData = loanData.amount || loanData.purpose || loanData.customer_name

  if (!hasData) return null

  const decisionColor = loanData.decision === 'approved'
    ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
    : loanData.decision === 'rejected'
    ? 'text-red-400 bg-red-500/10 border-red-500/30'
    : null

  return (
    <div className="gradient-border p-4 flex flex-col gap-3 animate-fade-up">
      <div className="flex items-center gap-2">
        <div className="w-1.5 h-4 rounded-full bg-gold-400" />
        <h3 className="text-xs font-semibold text-gold-400 uppercase tracking-widest">Application</h3>
      </div>

      <div>
        {loanData.customer_name && (
          <p className="text-sm font-semibold text-white mb-2">{loanData.customer_name}</p>
        )}
        <Row label="Loan Amount"   value={fmt(loanData.amount)} highlight />
        <Row label="Tenure"        value={loanData.tenure ? `${loanData.tenure} months` : null} />
        <Row label="Purpose"       value={loanData.purpose} />
        <Row label="Monthly EMI"   value={fmt(loanData.emi)} highlight />
        <Row label="Interest Rate" value={fmtRate(loanData.interest_rate)} />
        <Row label="Credit Score"  value={loanData.credit_score} />
      </div>

      {loanData.decision && (
        <div className={`mt-1 px-3 py-2 rounded-lg border text-xs font-semibold text-center uppercase tracking-wider ${decisionColor}`}>
          {loanData.decision === 'approved' ? '✅ Loan Approved' : '❌ Application Declined'}
        </div>
      )}

      {sanctionUrl && loanData.decision === 'approved' && (
        <a
          href={sanctionUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl
            bg-gold-500/20 hover:bg-gold-500/30 border border-gold-500/40
            text-gold-400 text-xs font-semibold transition-all duration-200
            hover:scale-[1.02] active:scale-[0.98]"
        >
          <span>📄</span>
          Download Sanction Letter
        </a>
      )}
    </div>
  )
}
