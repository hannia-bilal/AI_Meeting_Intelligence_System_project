import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthCard from '../components/auth/AuthCard.jsx'
import Input from '../components/ui/Input.jsx'
import Button from '../components/ui/Button.jsx'
import { useAuth } from '../context/AuthContext.jsx'

export default function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('')
  const [organization, setOrganization] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [agreed, setAgreed] = useState(false)
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!name || !email || !password || !confirmPassword) {
      setError('Fill in every required field to create your account.')
      return
    }
    if (password !== confirmPassword) {
      setError('Passwords don\u2019t match.')
      return
    }
    if (!agreed) {
      setError('Please accept the terms to continue.')
      return
    }
    register(name, email, { role, organization })
    navigate('/dashboard')
  }

  return (
    <AuthCard
      title="Create your account"
      subtitle="Start turning meetings into structured, actionable notes."
      footer={
        <>
          Already have an account?{' '}
          <Link to="/login" className="text-walnut-600 font-medium hover:underline">
            Log in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          id="name"
          label="Full name"
          type="text"
          placeholder="Ali Raza"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Input
          id="email"
          label="Work email"
          type="email"
          placeholder="you@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className="grid grid-cols-2 gap-3">
          <Input
            id="role"
            label="Role (optional)"
            type="text"
            placeholder="Product Manager"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
          <Input
            id="organization"
            label="Team (optional)"
            type="text"
            placeholder="Acme Inc."
            value={organization}
            onChange={(e) => setOrganization(e.target.value)}
          />
        </div>

        <Input
          id="password"
          label="Password"
          type="password"
          placeholder="At least 8 characters"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Input
          id="confirmPassword"
          label="Confirm password"
          type="password"
          placeholder="••••••••"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        {error && <p className="text-sm text-oxblood-600">{error}</p>}

        <label className="flex items-start gap-2 text-sm text-ink-soft pt-1">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="rounded border-line mt-0.5"
          />
          I agree to the Terms of Service and Privacy Policy.
        </label>

        <Button type="submit" className="w-full">
          Create account
        </Button>
      </form>
    </AuthCard>
  )
}
