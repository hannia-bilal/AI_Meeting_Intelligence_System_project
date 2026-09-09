import { useSearchParams } from 'react-router-dom'
import { SearchX } from 'lucide-react'
import MeetingRow from '../components/meetings/MeetingRow.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import { searchMeetings } from '../data/mockData.js'

export default function SearchResults() {
  const [params] = useSearchParams()
  const query = params.get('q') || ''
  const results = searchMeetings(query)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Search results</h1>
        <p className="text-sm text-ink-soft mt-1">
          {results.length} result{results.length === 1 ? '' : 's'} for "{query}"
        </p>
      </div>

      {results.length ? (
        <div className="space-y-3">
          {results.map((m) => (
            <MeetingRow key={m.id} meeting={m} />
          ))}
        </div>
      ) : (
        <EmptyState
          icon={SearchX}
          title="No matches found"
          description="Try a different keyword, participant name, or decision."
        />
      )}
    </div>
  )
}
