import { useState, useCallback } from 'react'
import { sendMessage, resetSession } from '../utils/api'

export function useChat() {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [stage, setStage] = useState('greeting')
  const [loanData, setLoanData] = useState(null)
  const [sanctionUrl, setSanctionUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const pushMessage = useCallback((role, content, meta = {}) => {
    setMessages(prev => [...prev, { id: Date.now() + Math.random(), role, content, meta, ts: new Date() }])
  }, [])

  const send = useCallback(async (text) => {
    if (!text.trim() || loading) return
    setError(null)
    pushMessage('user', text)
    setLoading(true)

    try {
      const data = await sendMessage(sessionId, text)
      if (!sessionId) setSessionId(data.session_id)
      setStage(data.stage)
      if (data.loan_data) setLoanData(data.loan_data)
      if (data.sanction_url) setSanctionUrl(data.sanction_url)
      pushMessage('bot', data.reply, { stage: data.stage })
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Connection error. Is the backend running?'
      setError(msg)
      pushMessage('bot', `⚠️ ${msg}`, { isError: true })
    } finally {
      setLoading(false)
    }
  }, [sessionId, loading, pushMessage])

  const reset = useCallback(async () => {
    await resetSession(sessionId)
    setMessages([])
    setSessionId(null)
    setStage('greeting')
    setLoanData(null)
    setSanctionUrl(null)
    setError(null)
  }, [sessionId])

  return { messages, stage, loanData, sanctionUrl, loading, error, send, reset }
}
