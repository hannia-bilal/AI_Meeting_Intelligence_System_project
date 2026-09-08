import { useState } from 'react'
import { Play, Pause } from 'lucide-react'

// Placeholder transport UI. Wire the `src` prop to the real file URL
// and replace the fake progress with a real <audio>/<video> element
// once the backend serves processed media.
export default function AudioPlayer({ jumpTo }) {
  const [playing, setPlaying] = useState(false)

  return (
    <div className="flex items-center gap-4 bg-surface border border-line rounded-lg px-4 py-3">
      <button
        onClick={() => setPlaying((p) => !p)}
        className="w-9 h-9 rounded-full bg-walnut-500 text-white flex items-center justify-center shrink-0"
        aria-label={playing ? 'Pause' : 'Play'}
      >
        {playing ? <Pause size={16} /> : <Play size={16} className="ml-0.5" />}
      </button>
      <div className="flex-1">
        <div className="h-1.5 rounded-full bg-line overflow-hidden">
          <div className="h-full bg-walnut-500 w-1/3" />
        </div>
      </div>
      <span className="text-xs text-ink-faint font-mono shrink-0">
        {jumpTo || '00:00'}
      </span>
    </div>
  )
}
