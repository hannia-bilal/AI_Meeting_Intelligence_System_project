import { createContext, useContext, useEffect, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('mi_user')
    if (stored) setUser(JSON.parse(stored))
    setReady(true)
  }, [])

  const login = (email) => {
    const fakeUser = { name: email.split('@')[0] || 'User', email }
    localStorage.setItem('mi_user', JSON.stringify(fakeUser))
    setUser(fakeUser)
  }

  const register = (name, email, extra = {}) => {
    const newUser = { name, email, role: extra.role || '', organization: extra.organization || '' }
    localStorage.setItem('mi_user', JSON.stringify(newUser))
    setUser(newUser)
  }

  const updateProfile = (updates) => {
    setUser((prev) => {
      const next = { ...prev, ...updates }
      localStorage.setItem('mi_user', JSON.stringify(next))
      return next
    })
  }

  const logout = () => {
    localStorage.removeItem('mi_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, ready, login, register, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
