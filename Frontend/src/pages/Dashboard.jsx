import { Link } from 'react-router-dom'
import { Video, ListChecks, CheckCircle2, CalendarClock, Plus, Inbox } from 'lucide-react'
import StatCard from '../components/ui/StatCard.jsx'
import MeetingRow from '../components/meetings/MeetingRow.jsx'
import Button from '../components/ui/Button.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import { meetings, dashboardStats, getUpcomingDeadlines } from '../data/mockData.js'

export default function Dashboard() {
  const recent = meetings.slice(0, 4)
  const deadlines = getUpcomingDeadlines(4)

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Dashboard</h1>
          <p className="text-sm text-ink-soft mt-1">Here's what's happening across your meetings.</p>
        </div>
        <Link to="/upload">
          <Button>
            <Plus size={16} /> New meeting
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total meetings" value={dashboardStats.totalMeetings} icon={Video} tone="walnut" />
        <StatCard label="Action items" value={dashboardStats.totalActionItems} icon={ListChecks} tone="tobacco" />
        <StatCard label="Pending decisions" value={dashboardStats.pendingDecisions} icon={CheckCircle2} tone="olive" />
        <StatCard label="Upcoming deadlines" value={dashboardStats.upcomingDeadlines} icon={CalendarClock} tone="oxblood" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-display font-semibold text-base">Recent meetings</h2>
            <Link to="/meetings" className="text-sm text-walnut-600 hover:underline">
              View all
            </Link>
          </div>

          {recent.length ? (
            <div className="space-y-3">
              {recent.map((m) => (
                <MeetingRow key={m.id} meeting={m} />
              ))}
            </div>
          ) : (
            <EmptyState
              icon={Inbox}
              title="No meetings yet"
              description="Upload your first recording to get a structured summary, action items and decisions."
              action={
                <Link to="/upload">
                  <Button>Upload a meeting</Button>
                </Link>
              }
            />
          )}
        </div>

        <div>
          <h2 className="font-display font-semibold text-base mb-3">Upcoming deadlines</h2>
          <div className="bg-surface border border-line rounded-lg divide-y divide-line">
            {deadlines.length ? (
              deadlines.map((d) => (
                <Link
                  key={d.id}
                  to={`/meetings/${d.meetingId}`}
                  className="flex items-start justify-between gap-3 px-4 py-3 hover:bg-paper transition-colors"
                >
                  <div className="min-w-0">
                    <p className="text-sm font-medium truncate">{d.context}</p>
                    <p className="text-xs text-ink-faint mt-0.5 truncate">{d.meetingTitle}</p>
                  </div>
                  <span className="font-mono text-xs bg-oxblood-50 text-oxblood-600 px-2 py-1 rounded-md shrink-0">
                    {d.date.slice(5)}
                  </span>
                </Link>
              ))
            ) : (
              <p className="text-sm text-ink-faint px-4 py-6 text-center">Nothing coming up.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
