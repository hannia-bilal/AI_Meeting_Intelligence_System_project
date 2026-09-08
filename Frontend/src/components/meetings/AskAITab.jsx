import { useState } from 'react'
import { Send, Bot, User } from 'lucide-react'

export default function AskAITab({ meeting }) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      text: `Ask me anything about "${meeting.title}" — I'll answer using this meeting's content only.`,
    },
  ])
  const [input, setInput] = useState('')

  const handleSend = (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMsg = { id: crypto.randomUUID(), role: 'user', text: input.trim() }

    
    const assistantMsg = {
      id: crypto.randomUUID(),
      role: 'assistant',
      text: meeting.decisions[0]
        ? `Based on this meeting: ${meeting.decisions[0].text}`
        : "This meeting doesn't have a recorded answer for that yet.",
      timestamp: meeting.transcript[meeting.transcript.length - 1]?.time,
    }

    setMessages((prev) => [...prev, userMsg, assistantMsg])
    setInput('')
  }

  return (
    <div className="flex flex-col h-[520px] bg-surface border border-line rounded-lg overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div key={m.id} className={`flex gap-3 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                m.role === 'user' ? 'bg-walnut-500 text-white' : 'bg-caramel-50 text-caramel-600'
              }`}
            >
              {m.role === 'user' ? <User size={15} /> : <Bot size={15} />}
            </div>
            <div
              className={`max-w-[75%] rounded-lg px-3.5 py-2.5 text-sm ${
                m.role === 'user' ? 'bg-walnut-500 text-white' : 'bg-paper text-ink'
              }`}
            >
              {m.text}
              {m.timestamp && (
                <span className="block mt-1.5 text-xs text-caramel-600 font-mono">
                  ↳ jump to {m.timestamp}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="border-t border-line p-3 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="What did we decide about the marketing budget?"
          className="flex-1 px-3 py-2.5 text-sm rounded-md border border-line bg-paper focus:bg-surface focus:border-walnut-500 outline-none"
        />
        <button
          type="submit"
          className="w-10 h-10 rounded-md bg-walnut-500 text-white flex items-center justify-center shrink-0 hover:bg-walnut-600 transition-colors"
          aria-label="Send"
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  )
}
