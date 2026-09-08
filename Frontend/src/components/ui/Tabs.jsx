export default function Tabs({ tabs, active, onChange }) {
  return (
    <div className="border-b border-line flex gap-6 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`relative pb-3 text-sm font-medium whitespace-nowrap transition-colors ${
            active === tab.key ? 'text-walnut-600' : 'text-ink-soft hover:text-ink'
          }`}
        >
          {tab.label}
          {active === tab.key && (
            <span className="absolute left-0 right-0 -bottom-px h-0.5 bg-walnut-500 rounded-full" />
          )}
        </button>
      ))}
    </div>
  )
}
