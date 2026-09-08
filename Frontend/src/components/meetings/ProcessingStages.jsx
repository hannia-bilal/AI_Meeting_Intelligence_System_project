import { Check, Loader2 } from 'lucide-react'

const stages = [
  'Uploading',
  'Transcribing',
  'Identifying speakers',
  'Running AI analysis',
  'Done',
]

export default function ProcessingStages({ currentIndex }) {
  return (
    <ol className="space-y-4">
      {stages.map((stage, i) => {
        const state = i < currentIndex ? 'done' : i === currentIndex ? 'active' : 'pending'
        return (
          <li key={stage} className="flex items-center gap-3">
            <span
              className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 text-xs font-medium ${
                state === 'done'
                  ? 'bg-olive-500 text-white'
                  : state === 'active'
                    ? 'bg-walnut-50 text-walnut-600'
                    : 'bg-paper text-ink-faint border border-line'
              }`}
            >
              {state === 'done' ? (
                <Check size={14} />
              ) : state === 'active' ? (
                <Loader2 size={14} className="animate-spin" />
              ) : (
                i + 1
              )}
            </span>
            <span
              className={`text-sm ${
                state === 'pending' ? 'text-ink-faint' : 'text-ink font-medium'
              }`}
            >
              {stage}
            </span>
          </li>
        )
      })}
    </ol>
  )
}
