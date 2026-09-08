import { NavLink } from 'react-router-dom'
import { LayoutGrid, UploadCloud, ListVideo, User2 } from 'lucide-react'
import Logo from '../ui/Logo.jsx'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/upload', label: 'New Meeting', icon: UploadCloud },
  { to: '/meetings', label: 'All Meetings', icon: ListVideo },
  { to: '/profile', label: 'Profile', icon: User2 },
]

export default function Sidebar() {
  return (
    <aside className="hidden md:flex md:w-60 md:flex-col md:shrink-0 border-r border-line bg-sidebar">
      <div className="h-16 flex items-center px-6 border-b border-line">
        <Logo size={30} />
      </div>

      <nav className="flex-1 px-3 py-6 space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-walnut-50 text-walnut-600'
                  : 'text-ink-soft hover:bg-paper hover:text-ink'
              }`
            }
          >
            <Icon size={18} strokeWidth={2} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-5 border-t border-line">
        <p className="text-xs text-ink-faint leading-relaxed">
          AI Meeting Intelligence
          <br />
          v1.0.0
        </p>
      </div>
    </aside>
  )
}
