import { useState, useEffect, useRef } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

const COACH_EMOJIS = ['🏋️‍♀️', '⚡', '🧘‍♀️', '🔥', '💪', '🎯', '🏃‍♂️', '🤸']

interface Coach {
  id: string
  first_name: string
  last_name: string
  email: string | null
  phone_number: string
  role: string
}

const benefits = [
  { icon: '⚡', title: 'Персональний підхід', desc: 'Кожна програма адаптована під твій рівень підготовки та цілі' },
  { icon: '📊', title: 'Відстеження прогресу', desc: 'Детальна статистика тренувань і динаміка результатів щотижня' },
  { icon: '🏆', title: 'Досвідчені тренери', desc: 'Сертифіковані фахівці з багаторічним досвідом у спортивній індустрії' },
  { icon: '🔄', title: 'Гнучкий розклад', desc: 'Онлайн-бронювання занять у зручний для тебе час доби' },
  { icon: '🤝', title: 'Командний дух', desc: 'Тренуйся поруч із людьми, які мають однакові цілі та мотивацію' },
  { icon: '💡', title: 'Постійний розвиток', desc: 'Програми оновлюються та адаптуються разом із твоїм прогресом' },
]

type AuthMode = 'login' | 'register'

export default function App() {
  const [authMode, setAuthMode] = useState<AuthMode>('login')
  const [authOpen, setAuthOpen] = useState(false)
  const [phone, setPhone] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const [visible, setVisible] = useState<Set<string>>(new Set())
  const heroRef = useRef<HTMLDivElement>(null)

  const [coaches, setCoaches] = useState<Coach[]>([])
  const [coachesLoading, setCoachesLoading] = useState(true)
  const [coachesError, setCoachesError] = useState<string | null>(null)

  const fetchCoaches = async () => {
    setCoachesLoading(true)
    setCoachesError(null)
    try {
      const res = await fetch(`${API_BASE}/coaches`)
      if (!res.ok) throw new Error(`Помилка ${res.status}`)
      const data: Coach[] = await res.json()
      setCoaches(data)
    } catch (e) {
      setCoachesError(e instanceof Error ? e.message : 'Не вдалося завантажити тренерів')
    } finally {
      setCoachesLoading(false)
    }
  }

  useEffect(() => {
    fetchCoaches()
  }, [])

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setVisible((prev) => new Set([...prev, entry.target.id]))
          }
        })
      },
      { threshold: 0.15 }
    )
    document.querySelectorAll('[data-animate]').forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [coaches])

  const isVisible = (id: string) => visible.has(id)

  const openAuth = (mode: AuthMode) => {
    setAuthMode(mode)
    setAuthOpen(true)
    setMenuOpen(false)
  }

  return (
    <div className="site">
      {/* NAV */}
      <nav className="nav">
        <div className="nav-inner">
          <a href="#" className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FitLife</span>
          </a>
          <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
            <a href="#about" onClick={() => setMenuOpen(false)}>Про нас</a>
            <a href="#benefits" onClick={() => setMenuOpen(false)}>Переваги</a>
            <a href="#coaches" onClick={() => setMenuOpen(false)}>Тренери</a>
            <button className="btn-ghost" onClick={() => openAuth('login')}>Увійти</button>
            <button className="btn-primary" onClick={() => openAuth('register')}>Розпочати</button>
          </div>
          <button className="burger" onClick={() => setMenuOpen(!menuOpen)}>
            <span /><span /><span />
          </button>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero" ref={heroRef}>
        <div className="hero-grid-bg" />
        <div className="hero-glow" />
        <div className="hero-content">
          <div className="hero-badge">🏆 &nbsp;Найкраща фітнес-платформа 2025</div>
          <h1 className="hero-title">
            Тренуйся.<br />
            <span className="accent">Розвивайся.</span><br />
            Перемагай.
          </h1>
          <p className="hero-sub">
            FitLife — це не просто зал. Це система зростання, де кожне тренування наближає тебе до кращої версії себе.
          </p>
          <div className="hero-actions">
            <button className="btn-primary large" onClick={() => openAuth('register')}>
              Почати безкоштовно →
            </button>
            <a href="#about" className="btn-ghost large">Дізнатись більше</a>
          </div>
          <div className="hero-stats">
            <div className="stat"><span className="stat-num">1 200+</span><span className="stat-label">Учасників</span></div>
            <div className="stat-div" />
            <div className="stat">
              <span className="stat-num">{coachesLoading ? '…' : coaches.length}</span>
              <span className="stat-label">Тренерів</span>
            </div>
            <div className="stat-div" />
            <div className="stat"><span className="stat-num">5 000+</span><span className="stat-label">Тренувань</span></div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-ring ring1" />
          <div className="hero-ring ring2" />
          <div className="hero-ring ring3" />
          <div className="hero-center-icon">⚡</div>
        </div>
      </section>

      {/* ABOUT */}
      <section className="about section" id="about">
        <div
          id="about-content"
          data-animate
          className={`about-inner fade-up ${isVisible('about-content') ? 'in' : ''}`}
        >
          <div className="section-tag">Про нас</div>
          <h2 className="section-title">Ми змінюємо спосіб тренуватися</h2>
          <p className="about-text">
            FitLife — це сучасна платформа, що об'єднує членів і тренерів у єдину екосистему.
            Ми вірим, що кожен заслуговує на доступ до якісних тренувань, персонального підходу та
            спільноти однодумців. Наша місія — зробити здоровий спосіб життя зручним і надихаючим.
          </p>
          <div className="about-highlights">
            <div className="highlight">
              <span className="highlight-icon">🎯</span>
              <div>
                <strong>Ціль-орієнтований підхід</strong>
                <p>Кожна програма починається з визначення твоїх цілей</p>
              </div>
            </div>
            <div className="highlight">
              <span className="highlight-icon">🌐</span>
              <div>
                <strong>Онлайн та офлайн</strong>
                <p>Тренуйся де завгодно — в залі або вдома</p>
              </div>
            </div>
            <div className="highlight">
              <span className="highlight-icon">🔒</span>
              <div>
                <strong>Безпека і приватність</strong>
                <p>Твої дані захищені сучасними технологіями</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* BENEFITS */}
      <section className="benefits section" id="benefits">
        <div className="section-tag">Переваги</div>
        <h2 className="section-title">Чому обирають FitLife</h2>
        <div className="benefits-grid">
          {benefits.map((b, i) => (
            <div
              key={b.title}
              id={`benefit-${i}`}
              data-animate
              className={`benefit-card fade-up ${isVisible(`benefit-${i}`) ? 'in' : ''}`}
              style={{ transitionDelay: `${i * 80}ms` }}
            >
              <div className="benefit-icon">{b.icon}</div>
              <h3>{b.title}</h3>
              <p>{b.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* COACHES */}
      <section className="coaches section" id="coaches">
        <div className="section-tag">Команда</div>
        <h2 className="section-title">Наші тренери</h2>
        <p className="section-sub">Кожен тренер — це не просто фахівець, а натхненник твоїх змін</p>

        {coachesLoading && (
          <div className="coaches-skeleton-grid">
            {[...Array(4)].map((_, i) => <div key={i} className="coach-skeleton" />)}
          </div>
        )}

        {coachesError && (
          <div className="coaches-state">
            <span>⚠️</span>
            <p>{coachesError}</p>
            <button className="btn-ghost" onClick={fetchCoaches}>Спробувати знову</button>
          </div>
        )}

        {!coachesLoading && !coachesError && coaches.length === 0 && (
          <div className="coaches-state">
            <p>Тренерів ще немає</p>
          </div>
        )}

        {!coachesLoading && !coachesError && coaches.length > 0 && (
          <div className="coaches-grid">
            {coaches.map((c, i) => (
              <div
                key={c.id}
                id={`coach-${i}`}
                data-animate
                className={`coach-card fade-up ${isVisible(`coach-${i}`) ? 'in' : ''}`}
                style={{ transitionDelay: `${i * 100}ms` }}
              >
                <div className="coach-avatar">
                  {COACH_EMOJIS[i % COACH_EMOJIS.length]}
                </div>
                <div className="coach-info">
                  <h3>{c.first_name} {c.last_name}</h3>
                  <span className="coach-specialty">Тренер</span>
                  <div className="coach-meta">
                    {c.email && <span>✉️ {c.email}</span>}
                    <span>📞 {c.phone_number}</span>
                  </div>
                </div>
                <button className="btn-outline" onClick={() => openAuth('register')}>
                  Записатись
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* CTA */}
      <section className="cta section" id="cta-section" data-animate>
        <div className={`cta-inner fade-up ${isVisible('cta-section') ? 'in' : ''}`}>
          <div className="cta-glow" />
          <h2>Готовий почати?</h2>
          <p>Зареєструйся сьогодні і отримай перше тренування безкоштовно</p>
          <button className="btn-primary large" onClick={() => openAuth('register')}>
            Зареєструватись зараз
          </button>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FitLife</span>
            <p>Твій шлях до кращого себе починається тут.</p>
          </div>
          <div className="footer-links">
            <div>
              <strong>Навігація</strong>
              <a href="#about">Про нас</a>
              <a href="#benefits">Переваги</a>
              <a href="#coaches">Тренери</a>
            </div>
            <div>
              <strong>Акаунт</strong>
              <a href="#" onClick={() => openAuth('login')}>Увійти</a>
              <a href="#" onClick={() => openAuth('register')}>Реєстрація</a>
            </div>
            <div>
              <strong>Контакти</strong>
              <a href="mailto:hello@fitlife.ua">hello@fitlife.ua</a>
              <a href="tel:+380501234567">+38 050 123 45 67</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© 2025 FitLife. Всі права захищені.</span>
        </div>
      </footer>

      {/* AUTH MODAL */}
      {authOpen && (
        <div className="modal-overlay" onClick={() => setAuthOpen(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setAuthOpen(false)}>✕</button>
            <div className="modal-tabs">
              <button className={authMode === 'login' ? 'active' : ''} onClick={() => setAuthMode('login')}>
                Увійти
              </button>
              <button className={authMode === 'register' ? 'active' : ''} onClick={() => setAuthMode('register')}>
                Реєстрація
              </button>
            </div>
            {authMode === 'login' ? (
              <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
                <div className="form-field">
                  <label>Телефон</label>
                  <input type="tel" placeholder="+380501234567" value={phone} onChange={(e) => setPhone(e.target.value)} />
                </div>
                <div className="form-field">
                  <label>Пароль</label>
                  <input type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit" className="btn-primary large full-width">Увійти →</button>
              </form>
            ) : (
              <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
                <div className="form-row">
                  <div className="form-field">
                    <label>Ім'я</label>
                    <input type="text" placeholder="Іван" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                  </div>
                  <div className="form-field">
                    <label>Прізвище</label>
                    <input type="text" placeholder="Петренко" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                  </div>
                </div>
                <div className="form-field">
                  <label>Телефон</label>
                  <input type="tel" placeholder="+380501234567" value={phone} onChange={(e) => setPhone(e.target.value)} />
                </div>
                <div className="form-field">
                  <label>Пароль</label>
                  <input type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit" className="btn-primary large full-width">Зареєструватись →</button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
