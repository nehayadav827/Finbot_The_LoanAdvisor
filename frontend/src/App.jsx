import React, { useRef, useEffect } from 'react'
import Header from './components/Header'
import StageBar from './components/StageBar'
import MessageBubble from './components/MessageBubble'
import TypingIndicator from './components/TypingIndicator'
import QuickReplies from './components/QuickReplies'
import ChatInput from './components/ChatInput'
import LoanPanel from './components/LoanPanel'
import WelcomeScreen from './components/WelcomeScreen'
import { useChat } from './hooks/useChat'

export default function App() {
  const { messages, stage, loanData, sanctionUrl, loading, send, reset } = useChat()
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const showWelcome = messages.length === 0 && !loading

  return (
    <div className="noise h-screen flex flex-col bg-navy-950 relative overflow-hidden">
      {/* Ambient background blobs */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-gold-500/5 blur-3xl" />
        <div className="absolute -bottom-40 -right-20 w-80 h-80 rounded-full bg-navy-700/30 blur-3xl" />
      </div>

      {/* Main layout */}
      <div className="relative z-10 flex flex-col h-full max-w-5xl w-full mx-auto">
        <Header onReset={reset} stage={stage} />
        <StageBar stage={stage} />

        {/* Content area */}
        <div className="flex flex-1 overflow-hidden">

          {/* Chat column */}
          <div className="flex flex-col flex-1 overflow-hidden">
            {/* Message list */}
            <div className="flex-1 overflow-y-auto px-4 pt-4">
              {showWelcome
                ? <WelcomeScreen onSend={send} />
                : (
                  <>
                    {messages.map(msg => (
                      <MessageBubble key={msg.id} message={msg} />
                    ))}
                    {loading && <TypingIndicator />}
                    <div ref={bottomRef} />
                  </>
                )
              }
            </div>

            {/* Input area */}
            {!showWelcome && (
              <QuickReplies stage={stage} onSelect={send} />
            )}
            <ChatInput onSend={send} disabled={loading} stage={stage} />
          </div>

          {/* Side panel (loan summary) */}
          {loanData?.amount && (
            <div className="hidden lg:flex flex-col w-64 border-l border-white/8 p-4 gap-4 overflow-y-auto">
              <LoanPanel loanData={loanData} sanctionUrl={sanctionUrl} stage={stage} />
              
              {/* Demo credentials hint */}
              <div className="gradient-border p-3">
                <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-widest mb-2">Demo KYC</p>
                <div className="space-y-1.5">
                  {[
                    { phone: '9876543210', pan: 'ABCDE1234F', note: 'Score 750 ✅' },
                    { phone: '9123456780', pan: 'FGHIJ5678K', note: 'Score 680 ✅' },
                    { phone: '9988776655', pan: 'LMNOP9012Q', note: 'Score 610 ❌' },
                    { phone: '8000000001', pan: 'RSTUV3456W', note: 'Score 720 ✅' },
                  ].map(c => (
                    <div key={c.phone} className="text-[10px] text-slate-500 font-mono">
                      <span className="text-slate-400">{c.phone}</span>
                      <span className="text-slate-600 mx-1">·</span>
                      <span>{c.pan}</span>
                      <br />
                      <span className="text-[9px] text-slate-600">{c.note}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
