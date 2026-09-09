const variants = {
  primary: 'bg-walnut-500 text-white hover:bg-walnut-600',
  secondary: 'bg-surface border border-line text-ink hover:bg-paper',
  ghost: 'text-ink-soft hover:text-ink hover:bg-paper',
  danger: 'bg-oxblood-50 text-oxblood-600 hover:bg-oxblood-100',
}

export default function Button({ variant = 'primary', className = '', children, ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
