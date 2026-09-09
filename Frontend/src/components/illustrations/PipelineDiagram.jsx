import { AudioLines, FileText, Users, BrainCircuit, Database, MessageCircleQuestion } from 'lucide-react'

const stages = [
  { icon: AudioLines, label: 'Audio/Video' },
  { icon: FileText, label: 'Transcript' },
  { icon: Users, label: 'Speakers' },
  { icon: BrainCircuit, label: 'LLM analysis' },
  { icon: Database, label: 'Structured data' },
  { icon: MessageCircleQuestion, label: 'Q&A' },
]

export default function PipelineDiagram() {
  return (
    <div className="flex items-center gap-1.5 overflow-x-auto py-1">
      {stages.map(({ icon: Icon, label }, i) => (
        <div key={label} className="flex items-center gap-1.5 shrink-0">
          <div className="flex flex-col items-center gap-1.5">
            <div className="w-10 h-10 rounded-md bg-walnut-50 text-walnut-500 flex items-center justify-center">
              <Icon size={17} />
            </div>
            <span className="text-[11px] text-ink-faint whitespace-nowrap">{label}</span>
          </div>
          {i < stages.length - 1 && (
            <div className="w-5 h-px bg-line mb-4" />
          )}
        </div>
      ))}
    </div>
  )
}
