import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Inbox } from 'lucide-react'
import MeetingRow from '../components/meetings/MeetingRow.jsx'
import Button from '../components/ui/Button.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import { meetings } from '../data/mockData.js'

const filters = ['all', 'done', 'processing', 'failed']

export default function AllMeetings() {
  const [filter, setFilter] = useState('all')

  const filtered = useMemo(
    () => (filter === 'all' ? meetings : meetings.filter((m) => m.status === filter)),
    [filter],
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">All meetings</h1>
          <p className="text-sm text-ink-soft mt-1">{meetings.length} recorded meetings</p>
        </div>
        <Link to="/upload">
          <Button>
            <Plus size={16} /> New meeting
          </Button>
        </Link>
      </div>

      <div className="flex gap-2">
        {filters.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3.5 py-1.5 rounded-full text-sm font-medium capitalize transition-colors ${
              filter === f ? 'bg-walnut-500 text-white' : 'bg-surface border border-line text-ink-soft'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {filtered.length ? (
        <div className="space-y-3">
          {filtered.map((m) => (
            <MeetingRow key={m.id} meeting={m} />
          ))}
        </div>
      ) : (
        <EmptyState icon={Inbox} title="No meetings in this filter" />
      )}
    </div>
  )
}
