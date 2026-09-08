import { useEffect, useRef, useState } from 'react'
import { Mic, Square, AlertTriangle } from 'lucide-react'

function formatTime(totalSeconds) {
  const m = Math.floor(totalSeconds / 60)
  const s = totalSeconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

// Records microphone audio in the browser via MediaRecorder, with a live
// level meter driven by the Web Audio API. On stop, hands the recorded
// Blob back to the parent as a File so it can flow through the same
// upload path as a file picked from disk.
export default function RecordMeeting({ onRecorded }) {
  const [permissionError, setPermissionError] = useState('')
  const [recording, setRecording] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const [levels, setLevels] = useState(new Array(24).fill(4))

  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const streamRef = useRef(null)
  const audioCtxRef = useRef(null)
  const analyserRef = useRef(null)
  const rafRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => {
    return () => stopEverything()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const stopEverything = () => {
    clearInterval(timerRef.current)
    cancelAnimationFrame(rafRef.current)
    streamRef.current?.getTracks().forEach((t) => t.stop())
    audioCtxRef.current?.close()
  }

  const startRecording = async () => {
    setPermissionError('')
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      const audioCtx = new (window.AudioContext || window.webkitAudioContext)()
      const source = audioCtx.createMediaStreamSource(stream)
      const analyser = audioCtx.createAnalyser()
      analyser.fftSize = 64
      source.connect(analyser)
      audioCtxRef.current = audioCtx
      analyserRef.current = analyser

      const recorder = new MediaRecorder(stream)
      chunksRef.current = []
      recorder.ondataavailable = (e) => chunksRef.current.push(e.data)
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        const file = new File([blob], `recording-${Date.now()}.webm`, { type: 'audio/webm' })
        onRecorded(file)
      }
      recorder.start()
      mediaRecorderRef.current = recorder

      setRecording(true)
      setSeconds(0)
      timerRef.current = setInterval(() => setSeconds((s) => s + 1), 1000)
      tickLevels()
    } catch (err) {
      setPermissionError('Microphone access was denied or is unavailable in this browser.')
    }
  }

  const tickLevels = () => {
    const analyser = analyserRef.current
    if (!analyser) return
    const data = new Uint8Array(analyser.frequencyBinCount)
    analyser.getByteFrequencyData(data)
    const bars = Array.from({ length: 24 }, (_, i) => {
      const v = data[i * Math.floor(data.length / 24)] || 0
      return Math.max(4, Math.round((v / 255) * 32))
    })
    setLevels(bars)
    rafRef.current = requestAnimationFrame(tickLevels)
  }

  const stopRecording = () => {
    mediaRecorderRef.current?.stop()
    setRecording(false)
    stopEverything()
  }

  if (permissionError) {
    return (
      <div className="flex items-start gap-3 border border-oxblood-100 bg-oxblood-50 text-oxblood-600 rounded-lg p-4 text-sm">
        <AlertTriangle size={18} className="shrink-0 mt-0.5" />
        <p>{permissionError}</p>
      </div>
    )
  }

  return (
    <div className="border border-line rounded-lg bg-surface p-8 flex flex-col items-center">
      <div className="flex items-end gap-1 h-10 mb-6">
        {levels.map((h, i) => (
          <span
            key={i}
            className={`w-1.5 rounded-full transition-all duration-75 ${
              recording ? 'bg-walnut-500' : 'bg-line'
            }`}
            style={{ height: `${recording ? h : 4}px` }}
          />
        ))}
      </div>

      <p className="font-mono text-2xl tabular-nums mb-6">{formatTime(seconds)}</p>

      {recording ? (
        <button
          onClick={stopRecording}
          className="w-16 h-16 rounded-full bg-oxblood-500 text-white flex items-center justify-center hover:bg-oxblood-600 transition-colors"
          aria-label="Stop recording"
        >
          <Square size={20} fill="currentColor" />
        </button>
      ) : (
        <button
          onClick={startRecording}
          className="w-16 h-16 rounded-full bg-walnut-500 text-white flex items-center justify-center hover:bg-walnut-600 transition-colors"
          aria-label="Start recording"
        >
          <Mic size={22} />
        </button>
      )}

      <p className="text-xs text-ink-faint mt-4">
        {recording ? 'Recording — tap to stop and continue' : 'Tap to start recording from your microphone'}
      </p>
    </div>
  )
}
