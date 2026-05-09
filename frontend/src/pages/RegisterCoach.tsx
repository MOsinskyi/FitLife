import { useState, useEffect } from 'react'
import type { FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { apiClient } from '../services/api'
import type { Specialization } from '../types'
import './Auth.css'

const experienceLabels = [
  { min: 1, max: 1, label: 'рік' },
  { min: 2, max: 4, label: 'роки' },
  { min: 5, max: 100, label: 'років' },
]

function getExperienceLabel(years: number): string {
  for (const { min, max, label } of experienceLabels) {
    if (years >= min && years <= max) {
      return label
    }
  }
  return 'років'
}

export default function RegisterCoach() {
  const navigate = useNavigate()
  const { registerCoach } = useAuth()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [phoneNumber, setPhoneNumber] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [specializationIds, setSpecializationIds] = useState<string[]>([])
  const [experience, setExperience] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  
  const [availableSpecializations, setAvailableSpecializations] = useState<Specialization[]>([])
  const [fetchingSpecializations, setFetchingSpecializations] = useState(true)

  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const specs = await apiClient.getSpecializations()
        setAvailableSpecializations(specs)
      } catch (err) {
        console.error('Failed to fetch specializations', err)
      } finally {
        setFetchingSpecializations(false)
      }
    }
    fetchSpecs()
  }, [])

  const handleSpecializationChange = (id: string) => {
    if (specializationIds.includes(id)) {
      setSpecializationIds(specializationIds.filter(s => s !== id))
    } else {
      setSpecializationIds([...specializationIds, id])
    }
  }

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

    if (specializationIds.length === 0) {
      setError('Оберіть хоча б одну спеціалізацію')
      return
    }

    setLoading(true)

    // Use the emoji of the first specialization as the main coach emoji
    const firstSpec = availableSpecializations.find(s => s.id === specializationIds[0])

    try {
      await registerCoach({
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        email: email || null,
        password,
        specialization_ids: specializationIds,
        emoji: firstSpec?.emoji || '💪',
        experience,
        experience_label: getExperienceLabel(experience),
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
      <div className="auth-container wide">
        <div className="auth-header">
          <Link to="/" className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FitLife</span>
          </Link>
          <h1>Реєстрація тренера</h1>
          <p>Приєднуйтесь до нашої команди професіоналів</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <div className="error-banner">{error}</div>}

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="firstName">Ім'я</label>
              <input
                id="firstName"
                type="text"
                placeholder="Тарас"
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
                placeholder="Шевченко"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-row">
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
                placeholder="taras@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="form-field">
            <label>Спеціалізації</label>
            {fetchingSpecializations ? (
              <p className="loading-text">Завантаження спеціалізацій...</p>
            ) : (
              <div className="checkbox-grid">
                {availableSpecializations.map((spec) => (
                  <label key={spec.id} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={specializationIds.includes(spec.id)}
                      onChange={() => handleSpecializationChange(spec.id)}
                    />
                    <span>{spec.emoji} {spec.name}</span>
                  </label>
                ))}
                {availableSpecializations.length === 0 && (
                  <p className="error-text small">Спеціалізації ще не додані адміністратором</p>
                )}
              </div>
            )}
          </div>

          <div className="form-field">
            <label htmlFor="experience">
              Досвід роботи: {experience} {getExperienceLabel(experience)}
            </label>
            <input
              id="experience"
              type="range"
              min="1"
              max="30"
              value={experience}
              onChange={(e) => setExperience(Number(e.target.value))}
              required
            />
          </div>

          <div className="form-row">
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
          </div>

          <button type="submit" className="btn-primary large full-width" disabled={loading || fetchingSpecializations}>
            {loading ? 'Реєстрація...' : 'Зареєструватися як тренер →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Вже маєте акаунт? <Link to="/login">Увійти</Link>
          </p>
          <p>
            Хочете зареєструватись як учасник? <Link to="/register/member">Реєстрація учасника</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
