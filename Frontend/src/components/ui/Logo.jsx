// Wordmark + icon for "Confer". The icon reads as a voice waveform that
// resolves into a checkmark — audio going in, a decided outcome coming out.
export default function Logo({ size = 32, withWordmark = true, className = '' }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <rect width="40" height="40" rx="11" className="fill-walnut-500" />
        <rect x="10" y="17" width="3.2" height="6" rx="1.6" fill="white" fillOpacity="0.55" />
        <rect x="15.4" y="12" width="3.2" height="16" rx="1.6" fill="white" fillOpacity="0.75" />
        <rect x="20.8" y="15.5" width="3.2" height="9" rx="1.6" fill="white" fillOpacity="0.55" />
        <path
          d="M25 22.5L27.6 25.1L32.5 18.5"
          stroke="white"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {withWordmark && (
        <span className="font-display font-semibold text-lg tracking-tight">Confer</span>
      )}
    </div>
  )
}
