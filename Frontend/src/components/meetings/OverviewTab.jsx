import { useState } from 'react'
import { Users, Calendar, Clock, Smile, Meh, Frown } from 'lucide-react'
import Avatar from '../ui/Avatar.jsx'
import SpeakerMetrics from './SpeakerMetrics.jsx'

const sentimentConfig = {
  positive: { className: 'bg-olive-50 text-olive-600', icon: Smile },
  neutral: { className: 'bg-paper text-ink-soft border border-line', icon: Meh },
  negative: { className: 'bg-oxblood-50 text-oxblood-600', icon: Frown },
}

export default function OverviewTab({ meeting }) {
  const [mode, setMode] = useState('short')
  const sentiment = sentimentConfig[meeting.sentiment.category] || sentimentConfig.neutral
  const SentimentIcon = sentiment.icon

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <InfoPill icon={Calendar} label="Date" value={meeting.date} />
        <InfoPill icon={Clock} label="Duration" value={meeting.duration} />
        <InfoPill icon={Users} label="Participants" value={meeting.participants.length} />
        <div className="bg-surface border border-line rounded-lg p-4">
          <div className="flex items-center gap-1.5 text-ink-faint text-xs mb-1.5">
            <SentimentIcon size={13} /> Sentiment
          </div>
          <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium capitalize ${sentiment.className}`}>
            {meeting.sentiment.category}
            <span className="font-mono opacity-70">
              {meeting.sentiment.score > 0 ? '+' : ''}
              {meeting.sentiment.score.toFixed(2)}
            </span>
          </span>
        </div>
      </div>

      {meeting.sentiment.summary && (
        <p className="text-sm text-ink-soft italic border-l-2 border-line pl-3">
          {meeting.sentiment.summary}
        </p>
      )}

      <div className="bg-surface border border-line rounded-lg p-5">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-display font-semibold text-sm">Summary</h3>
          <div className="flex text-xs bg-paper border border-line rounded-full p-0.5">
            {['short', 'detailed'].map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`px-3 py-1 rounded-full capitalize transition-colors ${
                  mode === m ? 'bg-walnut-500 text-white' : 'text-ink-soft'
                }`}
              >
                {m}
              </button>
            ))}
          </div>
        </div>
        <p className="text-sm text-ink-soft leading-relaxed">
          {mode === 'short' ? meeting.summaryShort : meeting.summaryDetailed}
        </p>
      </div>

      <SpeakerMetrics speakers={meeting.speakers} />

      <div className="bg-surface border border-line rounded-lg p-5">
        <h3 className="font-display font-semibold text-sm mb-3">Participants</h3>
        <div className="flex flex-wrap gap-2">
          {meeting.participants.map((p) => (
            <span
              key={p}
              className="flex items-center gap-2 pl-1 pr-3 py-1 rounded-full bg-paper border border-line text-xs font-medium"
            >
              <Avatar name={p} size={22} />
              {p}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

function InfoPill({ icon: Icon, label, value }) {
  return (
    <div className="bg-surface border border-line rounded-lg p-4">
      <div className="flex items-center gap-1.5 text-ink-faint text-xs mb-1.5">
        <Icon size={13} /> {label}
      </div>
      <p className="text-sm font-semibold capitalize">{value}</p>
    </div>
  )
}
