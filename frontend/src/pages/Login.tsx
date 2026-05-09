import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Auth.css'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      await login({ username: phoneNumber, password })
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Помилка входу')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <Link to="/" className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FitLife</span>
          </Link>
          <h1>Вхід</h1>
          <p>Ласкаво просимо назад!</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <div className="error-banner">{error}</div>}

          <div className="form-field">
            <label htmlFor="phone">Телефон</label>
            <input
              id="phone"
              type="tel"
              placeholder="+380501234567"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
              pattern="^\+380\d{9}$"
              title="Введіть номер у форматі +380XXXXXXXXX"
            />
          </div>

          <div className="form-field">
            <label htmlFor="password">Пароль</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>

          <button type="submit" className="btn-primary large full-width" disabled={loading}>
            {loading ? 'Вхід...' : 'Увійти →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Ще не маєте акаунту?{' '}
            <Link to="/register/member">Зареєструватися</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
