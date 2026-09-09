export default function Input({ label, id, className = '', ...props }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-ink">
          {label}
        </label>
      )}
      <input
        id={id}
        className={`px-3 py-2.5 text-sm rounded-md border border-line bg-surface focus:border-walnut-500 outline-none transition-colors ${className}`}
        {...props}
      />
    </div>
  )
}
