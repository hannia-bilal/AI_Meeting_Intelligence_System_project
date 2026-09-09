import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { Search, LogOut, Menu, Sun, Moon } from 'lucide-react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useTheme } from '../../context/ThemeContext.jsx'

export default function Topbar() {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()

  const handleSearch = (e) => {
    e.preventDefault()
    if (!query.trim()) return
    navigate(`/search?q=${encodeURIComponent(query.trim())}`)
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const initials = (user?.name || 'U').slice(0, 1).toUpperCase()

  return (
    <header className="h-16 border-b border-line bg-surface flex items-center gap-4 px-4 md:px-8">
      <button className="md:hidden text-ink-soft" aria-label="Open menu">
        <Menu size={20} />
      </button>

      <form onSubmit={handleSearch} className="flex-1 max-w-md">
        <div className="relative">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-faint"
          />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            type="text"
            placeholder="Search meetings, decisions, people…"
            className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-line bg-paper focus:bg-surface focus:border-walnut-500 outline-none transition-colors"
          />
        </div>
      </form>

      <div className="flex items-center gap-3 ml-auto">
        <button
          onClick={toggleTheme}
          className="w-9 h-9 rounded-md border border-line text-ink-soft hover:text-ink hover:bg-paper flex items-center justify-center transition-colors shrink-0"
          aria-label={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
          title={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
        >
          {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
        </button>

        <div className="hidden sm:flex flex-col items-end leading-tight">
          <span className="text-sm font-medium">{user?.name || 'Guest'}</span>
          <span className="text-xs text-ink-faint">{user?.email}</span>
        </div>
        <div className="w-9 h-9 rounded-full bg-walnut-500 text-white flex items-center justify-center text-sm font-semibold shrink-0">
          {initials}
        </div>
        <button
          onClick={handleLogout}
          className="text-ink-soft hover:text-oxblood-600 transition-colors shrink-0"
          aria-label="Log out"
          title="Log out"
        >
          <LogOut size={18} />
        </button>
      </div>
    </header>
  )
}
