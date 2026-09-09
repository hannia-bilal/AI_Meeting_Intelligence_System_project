import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UploadCloud, Mic } from 'lucide-react'
import UploadDropzone from '../components/meetings/UploadDropzone.jsx'
import RecordMeeting from '../components/meetings/RecordMeeting.jsx'
import ProcessingStages from '../components/meetings/ProcessingStages.jsx'
import PipelineDiagram from '../components/illustrations/PipelineDiagram.jsx'
import Input from '../components/ui/Input.jsx'
import Button from '../components/ui/Button.jsx'

export default function UploadMeeting() {
  const [source, setSource] = useState('file')
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [uploading, setUploading] = useState(false)
  const [stageIndex, setStageIndex] = useState(0)
  const navigate = useNavigate()

  const startProcessing = () => {
    setUploading(true)
    // Placeholder progression. Replace with real status polling against
    // GET /meetings/:id once the backend upload + background job exist.
    let step = 0
    const interval = setInterval(() => {
      step += 1
      setStageIndex(step)
      if (step >= 4) {
        clearInterval(interval)
        setTimeout(() => navigate('/meetings/m1'), 600)
      }
    }, 700)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!file) return
    startProcessing()
  }

  if (uploading) {
    return (
      <div className="max-w-md mx-auto py-10">
        <h1 className="text-xl font-semibold text-center mb-1">Processing your meeting</h1>
        <p className="text-sm text-ink-soft text-center mb-8">
          This can take a few minutes for longer recordings.
        </p>
        <div className="bg-surface border border-line rounded-lg p-6">
          <ProcessingStages currentIndex={stageIndex} />
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">New meeting</h1>
        <p className="text-sm text-ink-soft mt-1">
          Confer transcribes your recording, identifies speakers, and pulls out decisions,
          action items and deadlines automatically.
        </p>
      </div>

      <div className="bg-surface border border-line rounded-lg p-4">
        <PipelineDiagram />
      </div>

      <div className="flex bg-paper border border-line rounded-full p-1 w-fit text-sm">
        <button
          onClick={() => setSource('file')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full font-medium transition-colors ${
            source === 'file' ? 'bg-surface shadow-soft' : 'text-ink-soft'
          }`}
        >
          <UploadCloud size={15} /> Upload file
        </button>
        <button
          onClick={() => setSource('record')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full font-medium transition-colors ${
            source === 'record' ? 'bg-surface shadow-soft' : 'text-ink-soft'
          }`}
        >
          <Mic size={15} /> Record now
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {source === 'file' ? (
          <UploadDropzone file={file} onFileSelect={setFile} />
        ) : (
          <RecordMeeting onRecorded={(recorded) => setFile(recorded)} />
        )}

        {source === 'record' && file && (
          <div className="text-sm text-olive-600 bg-olive-50 rounded-md px-3 py-2">
            Recording captured — {file.name}
          </div>
        )}

        <Input
          id="title"
          label="Meeting title (optional)"
          placeholder="e.g. Q3 Product Launch Planning"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <Button type="submit" disabled={!file} className="w-full">
          Upload and analyze
        </Button>
      </form>
    </div>
  )
}
