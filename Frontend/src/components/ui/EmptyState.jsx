export default function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 px-6 border border-dashed border-line rounded-lg bg-surface">
      {Icon && (
        <div className="w-12 h-12 rounded-full bg-walnut-50 text-walnut-500 flex items-center justify-center mb-4">
          <Icon size={22} />
        </div>
      )}
      <h3 className="font-display font-semibold text-base">{title}</h3>
      {description && <p className="text-sm text-ink-soft mt-1.5 max-w-sm">{description}</p>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  )
}
