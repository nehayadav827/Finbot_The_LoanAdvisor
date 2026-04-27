import React, { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react'

export default function ChatInput({ onSend, disabled, stage }) {
  const [text, setText] = useState('')
  const ref = useRef(null)

  useEffect(() => {
    if (!disabled) ref.current?.focus()
  }, [disabled])

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setText('')
  }

  const isDone = stage === 'approved' || stage === 'rejected'

  return (
    <div className="px-4 pb-4 pt-2">
      <div className={`
        flex items-end gap-2 px-4 py-3 rounded-2xl border transition-all duration-200
        ${isDone
          ? 'bg-navy-900/50 border-white/5 opacity-60'
          : 'bg-navy-800/60 border-white/10 focus-within:border-gold-500/40 focus-within:bg-navy-800/80'}
      `}>
        <textarea
          ref={ref}
          rows={1}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKey}
          disabled={disabled || isDone}
          placeholder={
            isDone
              ? 'Application complete — start a new chat to apply again'
              : 'Type your message...'
          }
          className="flex-1 bg-transparent text-sm text-slate-200 placeholder-slate-500
            resize-none outline-none leading-relaxed max-h-28 min-h-[20px]
            disabled:cursor-not-allowed"
          style={{ height: 'auto' }}
          onInput={e => {
            e.target.style.height = 'auto'
            e.target.style.height = Math.min(e.target.scrollHeight, 112) + 'px'
          }}
        />
        <button
          onClick={submit}
          disabled={disabled || isDone || !text.trim()}
          className={`
            p-2 rounded-xl transition-all duration-150 flex-shrink-0
            ${!disabled && !isDone && text.trim()
              ? 'bg-gold-500/20 text-gold-400 hover:bg-gold-500/30 hover:scale-105 active:scale-95 border border-gold-500/40'
              : 'bg-white/5 text-slate-600 cursor-not-allowed'}
          `}
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  )
}
