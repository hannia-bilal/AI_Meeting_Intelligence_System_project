import { Link } from 'react-router-dom'
import { Clock } from 'lucide-react'
import StatusBadge from '../ui/StatusBadge.jsx'
import Avatar from '../ui/Avatar.jsx'

const accentByStatus = {
  done: 'border-l-olive-500',
  processing: 'border-l-ochre-500',
  queued: 'border-l-tobacco-500',
  failed: 'border-l-oxblood-500',
}

export default function MeetingRow({ meeting }) {
  return (
    <Link
      to={`/meetings/${meeting.id}`}
      className={`flex items-center gap-4 bg-surface border border-line border-l-4 ${accentByStatus[meeting.status]} rounded-md px-4 py-4 hover:border-walnut-400 transition-colors`}
    >
      <div className="min-w-0 flex-1">
        <p className="font-medium text-sm truncate">{meeting.title}</p>
        <p className="text-xs text-ink-soft mt-1 line-clamp-2">{meeting.summaryShort}</p>
        <div className="flex items-center gap-4 mt-2 text-xs text-ink-faint">
          <span>{meeting.date}</span>
          <span className="flex items-center gap-1">
            <Clock size={12} /> {meeting.duration}
          </span>
        </div>
      </div>
      <div className="flex -space-x-2 shrink-0">
        {meeting.participants.slice(0, 3).map((p) => (
          <Avatar key={p} name={p} size={26} />
        ))}
      </div>
      <StatusBadge status={meeting.status} />
    </Link>
  )
}
