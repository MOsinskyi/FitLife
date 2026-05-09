import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Auth.css'

export default function RegisterMember() {
  const navigate = useNavigate()
  const { registerMember } = useAuth()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [phoneNumber, setPhoneNumber] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)

    if (password !== confirmPassword) {
      setError('Паролі не співпадають')
      return
    }

    if (password.length < 8) {
      setError('Пароль повинен містити щонайменше 8 символів')
      return
    }

    setLoading(true)

    try {
      await registerMember({
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        email: email || null,
        password,
      })
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Помилка реєстрації')
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
          <h1>Реєстрація учасника</h1>
          <p>Почніть свій шлях до здорового життя</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <div className="error-banner">{error}</div>}

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="firstName">Ім'я</label>
              <input
                id="firstName"
                type="text"
                placeholder="Іван"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="lastName">Прізвище</label>
              <input
                id="lastName"
                type="text"
                placeholder="Петренко"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
          </div>

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
            <label htmlFor="email">Email (необов'язково)</label>
            <input
              id="email"
              type="email"
              placeholder="ivan@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
            <small>Мінімум 8 символів</small>
          </div>

          <div className="form-field">
            <label htmlFor="confirmPassword">Підтвердіть пароль</label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>

          <button type="submit" className="btn-primary large full-width" disabled={loading}>
            {loading ? 'Реєстрація...' : 'Зареєструватися →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Вже маєте акаунт? <Link to="/login">Увійти</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
