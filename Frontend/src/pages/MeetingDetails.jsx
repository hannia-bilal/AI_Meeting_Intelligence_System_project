import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import Tabs from '../components/ui/Tabs.jsx'
import StatusBadge from '../components/ui/StatusBadge.jsx'
import OverviewTab from '../components/meetings/OverviewTab.jsx'
import TranscriptTab from '../components/meetings/TranscriptTab.jsx'
import InsightsTab from '../components/meetings/InsightsTab.jsx'
import AskAITab from '../components/meetings/AskAITab.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import { getMeetingById } from '../data/mockData.js'
import { FileQuestion } from 'lucide-react'

const tabs = [
  { key: 'overview', label: 'Overview' },
  { key: 'transcript', label: 'Transcript' },
  { key: 'insights', label: 'AI Insights' },
  { key: 'ask', label: 'Ask AI' },
]

export default function MeetingDetails() {
  const { id } = useParams()
  const meeting = getMeetingById(id)
  const [active, setActive] = useState('overview')

  if (!meeting) {
    return (
      <EmptyState
        icon={FileQuestion}
        title="Meeting not found"
        description="It may have been deleted, or the link is incorrect."
        action={
          <Link to="/meetings" className="text-sm text-walnut-600 hover:underline">
            Back to all meetings
          </Link>
        }
      />
    )
  }

  return (
    <div className="space-y-6">
      <Link to="/meetings" className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink">
        <ArrowLeft size={15} /> All meetings
      </Link>

      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">{meeting.title}</h1>
          <p className="text-sm text-ink-soft mt-1">
            {meeting.date} · {meeting.duration}
          </p>
        </div>
        <StatusBadge status={meeting.status} />
      </div>

      <Tabs tabs={tabs} active={active} onChange={setActive} />

      <div>
        {active === 'overview' && <OverviewTab meeting={meeting} />}
        {active === 'transcript' && <TranscriptTab meeting={meeting} />}
        {active === 'insights' && <InsightsTab meeting={meeting} />}
        {active === 'ask' && <AskAITab meeting={meeting} />}
      </div>
    </div>
  )
}
