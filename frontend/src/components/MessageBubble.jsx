import React from 'react'

function formatContent(text) {
  // Bold **text**
  let parts = text.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="font-semibold text-gold-400">{part.slice(2, -2)}</strong>
    }
    // Handle inline links [text](url)
    const linkParts = part.split(/(\[[^\]]+\]\([^)]+\))/g)
    return linkParts.map((lp, j) => {
      const match = lp.match(/^\[([^\]]+)\]\(([^)]+)\)$/)
      if (match) {
        return (
          <a key={j} href={match[2]} target="_blank" rel="noopener noreferrer"
            className="text-gold-400 underline underline-offset-2 hover:text-gold-300">
            {match[1]}
          </a>
        )
      }
      return lp
    })
  })
}

function parseMessage(text) {
  return text.split('\n').map((line, i) => {
    if (!line.trim()) return <br key={i} />
    return <p key={i} className="mb-1 last:mb-0 leading-relaxed">{formatContent(line)}</p>
  })
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const isError = message.meta?.isError

  return (
    <div className={`msg-enter flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gold-500/20 border border-gold-500/30 flex items-center justify-center text-sm flex-shrink-0 mt-1 mr-2">
          🤖
        </div>
      )}

      <div className={`
        max-w-[78%] px-4 py-3 rounded-2xl text-sm leading-relaxed
        ${isUser
          ? 'bg-navy-700/80 border border-navy-600/60 text-slate-100 rounded-br-sm ml-10'
          : isError
          ? 'bg-red-500/10 border border-red-500/30 text-red-300 rounded-bl-sm'
          : 'bg-navy-800/80 border border-white/8 text-slate-200 rounded-bl-sm'}
      `}>
        {parseMessage(message.content)}
        <span className="block text-right text-[10px] text-slate-500 mt-1.5">
          {message.ts?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-navy-700/60 border border-white/10 flex items-center justify-center text-sm flex-shrink-0 mt-1 ml-2">
          👤
        </div>
      )}
    </div>
  )
}
