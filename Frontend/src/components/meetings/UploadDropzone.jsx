import { useRef, useState } from 'react'
import { UploadCloud, FileAudio, X } from 'lucide-react'

const ACCEPTED = '.mp3,.wav,.m4a,.mp4,.mov,.webm'

export default function UploadDropzone({ file, onFileSelect }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const dropped = e.dataTransfer.files?.[0]
    if (dropped) onFileSelect(dropped)
  }

  if (file) {
    return (
      <div className="flex items-center justify-between border border-line rounded-lg p-4 bg-surface">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-10 h-10 rounded-md bg-walnut-50 text-walnut-500 flex items-center justify-center shrink-0">
            <FileAudio size={18} />
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium truncate">{file.name}</p>
            <p className="text-xs text-ink-faint">{(file.size / (1024 * 1024)).toFixed(1)} MB</p>
          </div>
        </div>
        <button
          onClick={() => onFileSelect(null)}
          className="text-ink-faint hover:text-oxblood-600 shrink-0"
          aria-label="Remove file"
        >
          <X size={18} />
        </button>
      </div>
    )
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`flex flex-col items-center justify-center text-center border-2 border-dashed rounded-lg py-12 px-6 cursor-pointer transition-colors ${
        dragging ? 'border-walnut-500 bg-walnut-50' : 'border-line bg-surface hover:border-walnut-400'
      }`}
    >
      <div className="w-12 h-12 rounded-full bg-walnut-50 text-walnut-500 flex items-center justify-center mb-4">
        <UploadCloud size={22} />
      </div>
      <p className="text-sm font-medium">Drag and drop your recording here</p>
      <p className="text-xs text-ink-faint mt-1">or click to browse — MP3, WAV, MP4, MOV, WEBM</p>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED}
        className="hidden"
        onChange={(e) => onFileSelect(e.target.files?.[0] || null)}
      />
    </div>
  )
}
