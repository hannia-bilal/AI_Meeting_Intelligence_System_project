const palette = [
  'bg-walnut-100 text-walnut-600',
  'bg-caramel-100 text-caramel-600',
  'bg-tobacco-100 text-tobacco-600',
  'bg-olive-100 text-olive-600',
  'bg-ochre-100 text-ochre-600',
  'bg-oxblood-100 text-oxblood-600',
]

function colorFor(name) {
  const sum = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)
  return palette[sum % palette.length]
}

export default function Avatar({ name, size = 28 }) {
  const initials = name
    .split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()

  return (
    <div
      className={`rounded-full flex items-center justify-center font-medium shrink-0 ring-2 ring-surface ${colorFor(name)}`}
      style={{ width: size, height: size, fontSize: size * 0.4 }}
      title={name}
    >
      {initials}
    </div>
  )
}
