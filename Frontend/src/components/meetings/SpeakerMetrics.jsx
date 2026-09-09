import Avatar from '../ui/Avatar.jsx'

function formatDuration(totalSeconds) {
  const m = Math.floor(totalSeconds / 60)
  const s = totalSeconds % 60
  return `${m}m ${String(s).padStart(2, '0')}s`
}

// Speaker mapping + contribution metrics, as produced by the diarization
// step (SPEAKER_XX -> real name) and the AI analysis module (speaking time,
// contribution %, turn count).
export default function SpeakerMetrics({ speakers }) {
  if (!speakers.length) return null

  return (
    <div className="bg-surface border border-line rounded-lg p-5">
      <h3 className="font-display font-semibold text-sm mb-4">Speaking time & contribution</h3>
      <div className="space-y-4">
        {speakers.map((sp) => (
          <div key={sp.id}>
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-2">
                <Avatar name={sp.name} size={22} />
                <span className="text-sm font-medium">{sp.name}</span>
                <span className="font-mono text-xs bg-walnut-50 text-walnut-600 px-1.5 py-0.5 rounded">
                  {sp.label}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs text-ink-faint shrink-0">
                <span className="font-mono">{formatDuration(sp.speakingSeconds)}</span>
                <span>{sp.turns} turns</span>
                <span className="font-medium text-ink">{sp.contributionPct}%</span>
              </div>
            </div>
            <div className="h-1.5 rounded-full bg-paper overflow-hidden">
              <div
                className="h-full bg-walnut-500 rounded-full"
                style={{ width: `${sp.contributionPct}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
