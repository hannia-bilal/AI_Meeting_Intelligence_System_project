// Mock data layer, shaped to match the real backend contract described in
// the AI Meeting Intelligence module (MeetingIntelligenceService /
// to_database_records). Replace these exports with calls through
// src/api/client.js once the FastAPI backend is live.

export const meetings = [
  {
    id: 'm1',
    title: 'Q3 Product Launch Planning',
    date: '2026-09-02',
    duration: '48:12',
    status: 'done',
    sentiment: {
      score: 0.62,
      category: 'positive',
      summary: 'Confident and collaborative — the team converged quickly on a launch date with only minor budget friction.',
    },
    participants: ['Ali Raza', 'Sara Khan', 'Bilal Ahmed'],
    actionItemsCount: 4,
    decisionsCount: 2,
    unresolvedCount: 1,
    summaryShort:
      'Team aligned on a September 1 launch date and split remaining backend and marketing work.',
    summaryDetailed:
      'The team reviewed launch readiness across engineering, design and marketing. Ali confirmed backend completion by Friday, Sara will finalize the homepage copy, and the group agreed to move the launch date to September 1 pending QA sign-off. Marketing budget concerns were raised but deferred to a follow-up sync.',
    keyPoints: [
      { id: 'k1', text: 'Backend is the critical path for launch readiness.', time: '01:15' },
      { id: 'k2', text: 'Marketing budget still needs finance approval.', time: '18:42' },
      { id: 'k3', text: 'QA sign-off required before the public announcement.', time: '26:03' },
    ],
    decisions: [
      {
        id: 'd1',
        text: 'Product launch date is September 1.',
        rationale: 'Backend and homepage work both land by end of week, leaving a few days buffer for QA.',
        time: '32:45',
      },
      {
        id: 'd2',
        text: 'Homepage redesign will ship ahead of launch, not after.',
        rationale: 'Team agreed a mismatched homepage at launch would hurt the announcement more than a short delay.',
        time: '35:10',
      },
    ],
    actionItems: [
      { id: 'a1', task: 'Finish backend', owner: 'Ali Raza', deadline: '2026-09-05', priority: 'high' },
      { id: 'a2', task: 'Complete homepage', owner: 'Sara Khan', deadline: '2026-09-06', priority: 'high' },
      { id: 'a3', task: 'Prepare QA checklist', owner: 'Bilal Ahmed', deadline: '2026-09-04', priority: 'medium' },
      { id: 'a4', task: 'Draft launch announcement', owner: 'Sara Khan', deadline: '2026-09-08', priority: 'low' },
    ],
    deadlines: [
      { id: 'dl1', phrase: 'by Friday', date: '2026-09-05', context: 'Backend completion' },
      { id: 'dl2', phrase: 'by Friday', date: '2026-09-06', context: 'Homepage completion' },
      { id: 'dl3', phrase: 'September 1', date: '2026-09-01', context: 'Public launch date' },
    ],
    unresolved: [
      { id: 'u1', text: 'Marketing budget approval is still pending finance.', urgency: 'high' },
    ],
    followUps: [
      { id: 'f1', text: 'Circle back with finance on marketing spend.', owner: 'Sara Khan', timeframe: 'Within 2 days' },
    ],
    speakers: [
      { id: 'sp1', label: 'SPEAKER_00', name: 'Ali Raza', speakingSeconds: 620, contributionPct: 43, turns: 14 },
      { id: 'sp2', label: 'SPEAKER_01', name: 'Sara Khan', speakingSeconds: 512, contributionPct: 35, turns: 12 },
      { id: 'sp3', label: 'SPEAKER_02', name: 'Bilal Ahmed', speakingSeconds: 320, contributionPct: 22, turns: 7 },
    ],
    transcript: [
      { id: 't1', speaker: 'Ali Raza', time: '00:12', text: 'We should launch the website next week.' },
      { id: 't2', speaker: 'Sara Khan', time: '00:24', text: "I'll complete the homepage by Friday." },
      { id: 't3', speaker: 'Ali Raza', time: '01:03', text: 'Good. Bilal, where are we on the backend?' },
      { id: 't4', speaker: 'Bilal Ahmed', time: '01:15', text: 'Backend will be done by Friday as well.' },
      { id: 't5', speaker: 'Ali Raza', time: '32:45', text: 'Marketing budget is finalized for the launch push.' },
    ],
  },
  {
    id: 'm2',
    title: 'Weekly Engineering Sync',
    date: '2026-09-01',
    duration: '22:40',
    status: 'done',
    sentiment: {
      score: 0.1,
      category: 'neutral',
      summary: 'A routine planning conversation — measured tone, no disagreement, one scope trade-off.',
    },
    participants: ['Bilal Ahmed', 'Hina Tariq'],
    actionItemsCount: 2,
    decisionsCount: 1,
    unresolvedCount: 0,
    summaryShort: 'Sprint scope trimmed; API rate limiting moved to next sprint.',
    summaryDetailed:
      'The team reviewed current sprint velocity and agreed to defer API rate limiting work to next sprint in favor of finishing the reporting dashboard on time.',
    keyPoints: [
      { id: 'k4', text: 'Sprint velocity is slightly below target.', time: '02:10' },
      { id: 'k5', text: 'Rate limiting is not launch-blocking.', time: '09:47' },
    ],
    decisions: [
      {
        id: 'd3',
        text: 'Rate limiting work moves to next sprint.',
        rationale: 'Reporting dashboard is customer-visible and takes priority this sprint.',
        time: '10:02',
      },
    ],
    actionItems: [
      { id: 'a5', task: 'Finish reporting dashboard', owner: 'Hina Tariq', deadline: '2026-09-08', priority: 'high' },
      { id: 'a6', task: 'Write migration notes', owner: 'Bilal Ahmed', deadline: '2026-09-09', priority: 'medium' },
    ],
    deadlines: [
      { id: 'dl4', phrase: 'end of this week', date: '2026-09-08', context: 'Reporting dashboard' },
      { id: 'dl5', phrase: 'next Monday', date: '2026-09-09', context: 'Migration notes' },
    ],
    unresolved: [],
    followUps: [
      { id: 'f2', text: 'Revisit rate limiting scope at next sprint planning.', owner: 'Bilal Ahmed', timeframe: 'Next sprint planning' },
    ],
    speakers: [
      { id: 'sp4', label: 'SPEAKER_00', name: 'Bilal Ahmed', speakingSeconds: 410, contributionPct: 55, turns: 10 },
      { id: 'sp5', label: 'SPEAKER_01', name: 'Hina Tariq', speakingSeconds: 335, contributionPct: 45, turns: 9 },
    ],
    transcript: [
      { id: 't6', speaker: 'Bilal Ahmed', time: '00:05', text: 'Let’s trim scope this sprint.' },
      { id: 't7', speaker: 'Hina Tariq', time: '00:40', text: 'Agreed, rate limiting can wait.' },
    ],
  },
  {
    id: 'm3',
    title: 'Client Onboarding Call — Northwind',
    date: '2026-08-30',
    duration: '35:07',
    status: 'processing',
    sentiment: { score: 0, category: 'neutral', summary: '' },
    participants: ['Sara Khan', 'Client: Northwind Traders'],
    actionItemsCount: 0,
    decisionsCount: 0,
    unresolvedCount: 0,
    summaryShort: 'Processing…',
    summaryDetailed: 'This meeting is still being processed.',
    keyPoints: [],
    decisions: [],
    actionItems: [],
    deadlines: [],
    unresolved: [],
    followUps: [],
    speakers: [],
    transcript: [],
  },
  {
    id: 'm4',
    title: 'Design Review — Onboarding Flow',
    date: '2026-08-27',
    duration: '18:52',
    status: 'failed',
    sentiment: { score: 0, category: 'neutral', summary: '' },
    participants: ['Hina Tariq'],
    actionItemsCount: 0,
    decisionsCount: 0,
    unresolvedCount: 0,
    summaryShort: 'Processing failed — unsupported audio codec.',
    summaryDetailed: 'Processing failed — unsupported audio codec.',
    keyPoints: [],
    decisions: [],
    actionItems: [],
    deadlines: [],
    unresolved: [],
    followUps: [],
    speakers: [],
    transcript: [],
  },
]

export const dashboardStats = {
  totalMeetings: meetings.length,
  pendingDecisions: 1,
  upcomingDeadlines: meetings.reduce((sum, m) => sum + m.deadlines.length, 0),
  totalActionItems: meetings.reduce((sum, m) => sum + m.actionItemsCount, 0),
}

export function getMeetingById(id) {
  return meetings.find((m) => m.id === id)
}

export function searchMeetings(query) {
  const q = query.trim().toLowerCase()
  if (!q) return []
  return meetings.filter((m) =>
    [m.title, m.summaryShort, ...m.participants].join(' ').toLowerCase().includes(q),
  )
}

export function getUpcomingDeadlines(limit = 4) {
  return meetings
    .flatMap((m) => m.deadlines.map((d) => ({ ...d, meetingId: m.id, meetingTitle: m.title })))
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(0, limit)
}
