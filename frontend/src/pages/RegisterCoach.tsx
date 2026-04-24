import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Specialization, Emoji } from '../types'
import './Auth.css'

const specializationOptions = [
  { value: Specialization.YOGA, label: 'Йога', emoji: Emoji.YOGA },
  { value: Specialization.CROSSFIT, label: 'Кросфіт', emoji: Emoji.CROSSFIT },
  { value: Specialization.AEROBICS, label: 'Аеробіка', emoji: Emoji.AEROBICS },
  { value: Specialization.STRENGTH_TRAINING, label: 'Силові тренування', emoji: Emoji.STRENGTH_TRAINING },
  { value: Specialization.CARDIO, label: 'Кардіо', emoji: Emoji.CARDIO },
  { value: Specialization.MEDITATION, label: 'Медитація', emoji: Emoji.MEDITATION },
]

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
  const [specialization, setSpecialization] = useState<Specialization>(Specialization.STRENGTH_TRAINING)
  const [experience, setExperience] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const selectedOption = specializationOptions.find(opt => opt.value === specialization)

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
      await registerCoach({
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        email: email || null,
        password,
        specialization,
        emoji: selectedOption?.emoji || Emoji.STRENGTH_TRAINING,
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

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="specialization">Спеціалізація</label>
              <select
                id="specialization"
                value={specialization}
                onChange={(e) => setSpecialization(e.target.value as Specialization)}
                required
              >
                {specializationOptions.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.emoji} {opt.label}
                  </option>
                ))}
              </select>
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

          <button type="submit" className="btn-primary large full-width" disabled={loading}>
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
