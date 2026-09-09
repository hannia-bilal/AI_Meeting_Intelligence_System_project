
export default function BriefingIllustration() {
  return (
    <svg
      viewBox="0 0 480 520"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-full max-w-md"
      role="img"
      aria-label="A meeting recording being turned into a structured summary with action items"
    >
      {/* backdrop shapes */}
      <circle cx="380" cy="90" r="70" className="fill-walnut-100" fillOpacity="0.5" />
      <circle cx="60" cy="440" r="90" className="fill-ochre-100" fillOpacity="0.5" />

      {/* recording card */}
      <g transform="translate(40,60)">
        <rect width="220" height="150" rx="16" className="fill-surface" stroke="currentColor" strokeOpacity="0.08" />
        <circle cx="28" cy="28" r="6" className="fill-oxblood-500" />
        <rect x="46" y="23" width="80" height="10" rx="5" className="fill-ink" fillOpacity="0.12" />
        {/* waveform */}
        {[8, 22, 14, 30, 18, 26, 10, 20, 30, 16, 24, 12].map((h, i) => (
          <rect
            key={i}
            x={20 + i * 16}
            y={95 - h}
            width="7"
            height={h * 2}
            rx="3.5"
            className={i % 3 === 0 ? 'fill-walnut-500' : 'fill-walnut-400'}
            fillOpacity={i % 3 === 0 ? 1 : 0.6}
          />
        ))}
        <rect x="20" y="122" width="60" height="8" rx="4" className="fill-ink" fillOpacity="0.1" />
      </g>

      {/* connecting arrow */}
      <path
        d="M270 150 C 320 150, 320 230, 270 250"
        stroke="currentColor"
        strokeOpacity="0.2"
        strokeWidth="2.5"
        strokeDasharray="1 8"
        strokeLinecap="round"
        fill="none"
      />
      <path d="M262 244 L272 251 L262 258" stroke="currentColor" strokeOpacity="0.35" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />

      {/* summary card */}
      <g transform="translate(120,260)">
        <rect width="260" height="200" rx="16" className="fill-surface" stroke="currentColor" strokeOpacity="0.08" />
        <rect x="24" y="26" width="120" height="12" rx="6" className="fill-ink" fillOpacity="0.85" />
        <rect x="24" y="50" width="180" height="8" rx="4" className="fill-ink" fillOpacity="0.15" />
        <rect x="24" y="64" width="150" height="8" rx="4" className="fill-ink" fillOpacity="0.15" />

        {/* decision chip */}
        <rect x="24" y="88" width="150" height="24" rx="12" className="fill-olive-100" />
        <circle cx="38" cy="100" r="5" className="fill-olive-600" />
        <rect x="50" y="96" width="110" height="8" rx="4" className="fill-olive-600" fillOpacity="0.7" />

        {/* action item row */}
        <rect x="24" y="126" width="14" height="14" rx="4" className="fill-ochre-100" stroke="currentColor" strokeOpacity="0.15" />
        <rect x="46" y="129" width="140" height="8" rx="4" className="fill-ink" fillOpacity="0.5" />
        <rect x="46" y="143" width="70" height="7" rx="3.5" className="fill-ink" fillOpacity="0.25" />

        {/* deadline pill */}
        <rect x="190" y="126" width="50" height="20" rx="10" className="fill-oxblood-100" />
        <rect x="198" y="133" width="34" height="6" rx="3" className="fill-oxblood-600" fillOpacity="0.8" />

        <rect x="24" y="164" width="212" height="1" className="fill-line" />
        <circle cx="34" cy="182" r="10" className="fill-walnut-100" />
        <circle cx="54" cy="182" r="10" className="fill-ochre-100" />
        <circle cx="74" cy="182" r="10" className="fill-olive-100" />
      </g>
    </svg>
  )
}
