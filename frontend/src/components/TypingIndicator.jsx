import React from 'react'

export default function TypingIndicator() {
  return (
    <div className="msg-enter flex justify-start mb-3">
      <div className="w-8 h-8 rounded-full bg-gold-500/20 border border-gold-500/30 flex items-center justify-center text-sm flex-shrink-0 mt-1 mr-2">
        🤖
      </div>
      <div className="bg-navy-800/80 border border-white/8 px-4 py-3.5 rounded-2xl rounded-bl-sm flex items-center gap-1.5">
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  )
}
