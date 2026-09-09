import { useState } from 'react'
import { Search } from 'lucide-react'
import AudioPlayer from './AudioPlayer.jsx'
import EmptyState from '../ui/EmptyState.jsx'

export default function TranscriptTab({ meeting }) {
  const [query, setQuery] = useState('')
  const [activeTime, setActiveTime] = useState(null)

  if (!meeting.transcript.length) {
    return (
      <EmptyState
        icon={Search}
        title="Transcript not ready yet"
        description="This meeting is still processing. The transcript will appear here once it's done."
      />
    )
  }

  const filtered = meeting.transcript.filter((line) =>
    line.text.toLowerCase().includes(query.toLowerCase()),
  )

  return (
    <div className="space-y-4">
      <AudioPlayer jumpTo={activeTime} />

      <div className="relative">
        <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-faint" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search within transcript…"
          className="w-full pl-9 pr-3 py-2.5 text-sm rounded-md border border-line bg-surface focus:border-walnut-500 outline-none"
        />
      </div>

      <div className="bg-surface border border-line rounded-lg divide-y divide-line">
        {filtered.map((line) => (
          <button
            key={line.id}
            onClick={() => setActiveTime(line.time)}
            className="w-full flex gap-4 px-4 py-3 text-left hover:bg-paper transition-colors"
          >
            <span className="text-xs text-walnut-600 font-mono shrink-0 pt-0.5">
              {line.time}
            </span>
            <div>
              <p className="text-xs font-semibold text-ink-soft">{line.speaker}</p>
              <p className="text-sm mt-0.5">{line.text}</p>
            </div>
          </button>
        ))}
        {!filtered.length && (
          <p className="px-4 py-6 text-sm text-ink-faint text-center">No matching lines.</p>
        )}
      </div>
    </div>
  )
}
