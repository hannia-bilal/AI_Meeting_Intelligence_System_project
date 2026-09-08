const config = {
  done: { label: 'Done', className: 'bg-olive-50 text-olive-600' },
  processing: { label: 'Processing', className: 'bg-ochre-50 text-ochre-600' },
  queued: { label: 'Queued', className: 'bg-tobacco-50 text-tobacco-600' },
  failed: { label: 'Failed', className: 'bg-oxblood-50 text-oxblood-600' },
}

export default function StatusBadge({ status }) {
  const { label, className } = config[status] || config.queued
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${className}`}>
      {label}
    </span>
  )
}
