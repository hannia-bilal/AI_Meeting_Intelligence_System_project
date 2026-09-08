import { CheckCircle2, AlertCircle, ListChecks, Lightbulb, CalendarClock, ArrowUpRightSquare } from 'lucide-react'
import EmptyState from '../ui/EmptyState.jsx'

const priorityStyle = {
  high: 'bg-oxblood-50 text-oxblood-600',
  medium: 'bg-ochre-50 text-ochre-600',
  low: 'bg-tobacco-50 text-tobacco-600',
}

const urgencyStyle = {
  high: 'bg-oxblood-50 text-oxblood-600',
  medium: 'bg-ochre-50 text-ochre-600',
  low: 'bg-paper text-ink-soft',
}

export default function InsightsTab({ meeting }) {
  const hasAnything =
    meeting.decisions.length ||
    meeting.actionItems.length ||
    meeting.keyPoints.length ||
    meeting.deadlines.length

  if (!hasAnything) {
    return (
      <EmptyState
        icon={Lightbulb}
        title="Insights not ready yet"
        description="Key points, decisions and action items will show up here once AI analysis finishes."
      />
    )
  }

  return (
    <div className="space-y-6">
      {/* AI / Insights — Violet */}
      <Section icon={Lightbulb} title="Key discussion points" tone="caramel">
        <ul className="space-y-2.5">
          {meeting.keyPoints.map((point) => (
            <li key={point.id} className="text-sm text-ink-soft flex gap-2.5">
              <span className="font-mono text-xs text-caramel-600 shrink-0 pt-0.5">{point.time}</span>
              {point.text}
            </li>
          ))}
        </ul>
      </Section>

      {/* Decisions / completed — Emerald */}
      <Section icon={CheckCircle2} title="Decisions made" tone="olive">
        <ul className="space-y-3">
          {meeting.decisions.map((d) => (
            <li key={d.id} className="bg-olive-50 rounded-md px-3.5 py-3">
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm text-olive-600 font-medium">{d.text}</p>
                <span className="font-mono text-xs text-olive-600 opacity-70 shrink-0">{d.time}</span>
              </div>
              {d.rationale && (
                <p className="text-xs text-ink-soft mt-1.5">{d.rationale}</p>
              )}
            </li>
          ))}
        </ul>
      </Section>

      {/* Action items / active — Blue */}
      <Section icon={ListChecks} title="Action items" tone="tobacco">
        <div className="overflow-hidden rounded-md border border-line">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-paper text-left text-xs text-ink-faint uppercase tracking-wide">
                <th className="px-4 py-2.5 font-medium">Task</th>
                <th className="px-4 py-2.5 font-medium">Owner</th>
                <th className="px-4 py-2.5 font-medium">Deadline</th>
                <th className="px-4 py-2.5 font-medium">Priority</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {meeting.actionItems.map((item) => (
                <tr key={item.id}>
                  <td className="px-4 py-2.5">{item.task}</td>
                  <td className="px-4 py-2.5 text-ink-soft">{item.owner}</td>
                  <td className="px-4 py-2.5 text-ink-soft font-mono text-xs">{item.deadline}</td>
                  <td className="px-4 py-2.5">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${priorityStyle[item.priority]}`}>
                      {item.priority}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      {/* Deadlines / urgency — Rose */}
      <Section icon={CalendarClock} title="Deadlines detected" tone="oxblood">
        {meeting.deadlines.length ? (
          <ul className="divide-y divide-line">
            {meeting.deadlines.map((d) => (
              <li key={d.id} className="flex items-center justify-between gap-4 py-2.5 first:pt-0 last:pb-0">
                <div>
                  <p className="text-sm">{d.context}</p>
                  <p className="text-xs text-ink-faint mt-0.5">said as "{d.phrase}"</p>
                </div>
                <span className="font-mono text-xs bg-oxblood-50 text-oxblood-600 px-2.5 py-1 rounded-md shrink-0">
                  {d.date}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-ink-faint">No dates or deadlines were mentioned.</p>
        )}
      </Section>

      {/* Unresolved / warning — Amber */}
      <Section icon={AlertCircle} title="Unresolved issues" tone="ochre">
        {meeting.unresolved.length ? (
          <ul className="space-y-2">
            {meeting.unresolved.map((item) => (
              <li key={item.id} className="flex items-center justify-between gap-3 bg-ochre-50 rounded-md px-3.5 py-2.5">
                <span className="text-sm text-ochre-600">{item.text}</span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize shrink-0 ${urgencyStyle[item.urgency]}`}>
                  {item.urgency}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-ink-faint">Nothing outstanding from this meeting.</p>
        )}
      </Section>

      {/* AI-recommended follow-ups — Violet, pairs with Key discussion points */}
      <Section icon={ArrowUpRightSquare} title="Follow-up items" tone="caramel">
        {meeting.followUps.length ? (
          <ul className="divide-y divide-line">
            {meeting.followUps.map((f) => (
              <li key={f.id} className="flex items-center justify-between gap-4 py-2.5 first:pt-0 last:pb-0">
                <p className="text-sm">{f.text}</p>
                <div className="text-right shrink-0">
                  <p className="text-xs font-medium">{f.owner}</p>
                  <p className="text-xs text-ink-faint">{f.timeframe}</p>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-ink-faint">No follow-ups recommended.</p>
        )}
      </Section>
    </div>
  )
}

function Section({ icon: Icon, title, tone, children }) {
  const tones = {
    walnut: 'text-walnut-500',
    caramel: 'text-caramel-500',
    tobacco: 'text-tobacco-500',
    olive: 'text-olive-500',
    ochre: 'text-ochre-500',
    oxblood: 'text-oxblood-500',
  }
  return (
    <div className="bg-surface border border-line rounded-lg p-5">
      <h3 className="font-display font-semibold text-sm flex items-center gap-2 mb-3">
        <Icon size={16} className={tones[tone]} />
        {title}
      </h3>
      {children}
    </div>
  )
}
