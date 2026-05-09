import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { apiClient } from '../services/api'
import type { User, LoginRequest, MemberRegisterRequest, CoachRegisterRequest } from '../types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  registerMember: (data: MemberRegisterRequest) => Promise<void>
  registerCoach: (data: CoachRegisterRequest) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      if (apiClient.isAuthenticated()) {
        try {
          const currentUser = await apiClient.getCurrentUser()
          setUser(currentUser)
        } catch (error) {
          console.error('Failed to fetch current user:', error)
          apiClient.logout()
        }
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  const login = async (credentials: LoginRequest) => {
    await apiClient.login(credentials)
    const currentUser = await apiClient.getCurrentUser()
    setUser(currentUser)
  }

  const registerMember = async (data: MemberRegisterRequest) => {
    const newUser = await apiClient.registerMember(data)
    await login({ username: data.phone_number, password: data.password })
    setUser(newUser)
  }

  const registerCoach = async (data: CoachRegisterRequest) => {
    await apiClient.registerCoach(data)
  }

  const logout = () => {
    apiClient.logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        registerMember,
        registerCoach,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
