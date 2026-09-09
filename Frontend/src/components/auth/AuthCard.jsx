import Logo from '../ui/Logo.jsx'
import BriefingIllustration from '../illustrations/BriefingIllustration.jsx'

export default function AuthCard({ title, subtitle, children, footer }) {
  return (
    <div className="min-h-screen bg-paper flex">
      {/* Left: illustration panel — hidden on small screens */}
      <div className="hidden lg:flex lg:w-1/2 bg-sidebar border-r border-line flex-col justify-between p-12 relative overflow-hidden">
        <Logo size={30} />

        <div className="flex-1 flex items-center justify-center py-8">
          <BriefingIllustration />
        </div>

        <div className="max-w-sm">
          <p className="font-display font-semibold text-xl leading-snug">
            Every meeting, turned into a brief you can act on.
          </p>
          <p className="text-sm text-ink-soft mt-2">
            Upload a recording — Confer transcribes it, finds the decisions and
            action items, and lets you ask it questions afterward.
          </p>
        </div>
      </div>

      {/* Right: form panel */}
      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="lg:hidden flex justify-center mb-8">
            <Logo size={30} />
          </div>

          <h1 className="font-display font-semibold text-2xl">{title}</h1>
          {subtitle && <p className="text-sm text-ink-soft mt-1.5">{subtitle}</p>}
          <div className="mt-7">{children}</div>

          {footer && <div className="text-center mt-6 text-sm text-ink-soft">{footer}</div>}
        </div>
      </div>
    </div>
  )
}
