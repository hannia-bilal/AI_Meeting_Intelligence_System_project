export default function StatCard({ label, value, tone = 'walnut', icon: Icon }) {
  const tones = {
    walnut: 'bg-walnut-50 text-walnut-600',
    caramel: 'bg-caramel-50 text-caramel-600',
    tobacco: 'bg-tobacco-50 text-tobacco-600',
    ochre: 'bg-ochre-50 text-ochre-600',
    olive: 'bg-olive-50 text-olive-600',
    oxblood: 'bg-oxblood-50 text-oxblood-600',
  }

  return (
    <div className="bg-surface border border-line rounded-lg p-5 flex items-center gap-4">
      <div className={`w-11 h-11 rounded-md flex items-center justify-center shrink-0 ${tones[tone]}`}>
        {Icon && <Icon size={20} />}
      </div>
      <div>
        <p className="text-2xl font-display font-semibold leading-none">{value}</p>
        <p className="text-sm text-ink-soft mt-1.5">{label}</p>
      </div>
    </div>
  )
}
