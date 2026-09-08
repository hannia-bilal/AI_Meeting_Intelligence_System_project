import { useState } from 'react'
import { Sun, Moon, Bell, ShieldCheck } from 'lucide-react'
import Avatar from '../components/ui/Avatar.jsx'
import Input from '../components/ui/Input.jsx'
import Button from '../components/ui/Button.jsx'
import { useAuth } from '../context/AuthContext.jsx'
import { useTheme } from '../context/ThemeContext.jsx'

export default function Profile() {
  const { user, updateProfile } = useAuth()
  const { theme, setTheme } = useTheme()

  const [name, setName] = useState(user?.name || '')
  const [email, setEmail] = useState(user?.email || '')
  const [role, setRole] = useState(user?.role || '')
  const [organization, setOrganization] = useState(user?.organization || '')
  const [savedProfile, setSavedProfile] = useState(false)

  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [savedPassword, setSavedPassword] = useState(false)

  const [notifyOnFinish, setNotifyOnFinish] = useState(true)
  const [weeklyDigest, setWeeklyDigest] = useState(false)

  const handleSaveProfile = (e) => {
    e.preventDefault()
    updateProfile({ name, email, role, organization })
    setSavedProfile(true)
    setTimeout(() => setSavedProfile(false), 2000)
  }

  const handleSavePassword = (e) => {
    e.preventDefault()
    setCurrentPassword('')
    setNewPassword('')
    setSavedPassword(true)
    setTimeout(() => setSavedPassword(false), 2000)
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Profile & settings</h1>
        <p className="text-sm text-ink-soft mt-1">Manage your account, preferences and notifications.</p>
      </div>

      {/* Identity header */}
      <div className="bg-surface border border-line rounded-lg p-6 flex items-center gap-4">
        <Avatar name={name || 'U'} size={56} />
        <div>
          <p className="font-display font-semibold text-base">{name || 'Your name'}</p>
          <p className="text-sm text-ink-soft">{email || 'you@company.com'}</p>
          {(role || organization) && (
            <p className="text-xs text-ink-faint mt-0.5">
              {[role, organization].filter(Boolean).join(' · ')}
            </p>
          )}
        </div>
      </div>

      {/* Personal info */}
      <form onSubmit={handleSaveProfile} className="bg-surface border border-line rounded-lg p-6 space-y-4">
        <h2 className="font-display font-semibold text-sm">Personal information</h2>
        <div className="grid sm:grid-cols-2 gap-4">
          <Input id="name" label="Full name" value={name} onChange={(e) => setName(e.target.value)} />
          <Input id="email" label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <Input id="role" label="Role" placeholder="Product Manager" value={role} onChange={(e) => setRole(e.target.value)} />
          <Input id="organization" label="Team" placeholder="Acme Inc." value={organization} onChange={(e) => setOrganization(e.target.value)} />
        </div>
        <div className="flex items-center gap-3 pt-1">
          <Button type="submit">Save changes</Button>
          {savedProfile && <span className="text-sm text-olive-600">Saved.</span>}
        </div>
      </form>

      {/* Password */}
      <form onSubmit={handleSavePassword} className="bg-surface border border-line rounded-lg p-6 space-y-4">
        <h2 className="font-display font-semibold text-sm flex items-center gap-2">
          <ShieldCheck size={16} className="text-walnut-500" /> Password
        </h2>
        <div className="grid sm:grid-cols-2 gap-4">
          <Input
            id="currentPassword"
            label="Current password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <Input
            id="newPassword"
            label="New password"
            type="password"
            placeholder="At least 8 characters"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-3 pt-1">
          <Button type="submit" variant="secondary">Update password</Button>
          {savedPassword && <span className="text-sm text-olive-600">Password updated.</span>}
        </div>
      </form>

      {/* Appearance */}
      <div className="bg-surface border border-line rounded-lg p-6 space-y-3">
        <h2 className="font-display font-semibold text-sm">Appearance</h2>
        <div className="flex bg-paper border border-line rounded-full p-1 w-fit text-sm">
          <button
            onClick={() => setTheme('light')}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full font-medium transition-colors ${
              theme === 'light' ? 'bg-surface shadow-soft' : 'text-ink-soft'
            }`}
          >
            <Sun size={14} /> Light
          </button>
          <button
            onClick={() => setTheme('dark')}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full font-medium transition-colors ${
              theme === 'dark' ? 'bg-surface shadow-soft' : 'text-ink-soft'
            }`}
          >
            <Moon size={14} /> Dark
          </button>
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-surface border border-line rounded-lg p-6 space-y-3">
        <h2 className="font-display font-semibold text-sm flex items-center gap-2">
          <Bell size={16} className="text-walnut-500" /> Notifications
        </h2>
        <label className="flex items-center gap-2 text-sm text-ink-soft">
          <input
            type="checkbox"
            checked={notifyOnFinish}
            onChange={(e) => setNotifyOnFinish(e.target.checked)}
            className="rounded border-line"
          />
          Email me when a meeting finishes processing
        </label>
        <label className="flex items-center gap-2 text-sm text-ink-soft">
          <input
            type="checkbox"
            checked={weeklyDigest}
            onChange={(e) => setWeeklyDigest(e.target.checked)}
            className="rounded border-line"
          />
          Send me a weekly digest of open action items
        </label>
      </div>
    </div>
  )
}
