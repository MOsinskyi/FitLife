import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { apiClient } from '../services/api'
import type { Coach, Gallery } from '../types'
import '../App.css'

const benefits = [
  { icon: '⚡', title: 'Персональний підхід', desc: 'Кожна програма адаптована під твій рівень підготовки та цілі' },
  { icon: '📊', title: 'Відстеження прогресу', desc: 'Детальна статистика тренувань і динаміка результатів щотижня' },
  { icon: '🏆', title: 'Досвідчені тренери', desc: 'Сертифіковані фахівці з багаторічним досвідом у спортивній індустрії' },
  { icon: '🔄', title: 'Гнучкий розклад', desc: 'Онлайн-бронювання занять у зручний для тебе час доби' },
  { icon: '🤝', title: 'Командний дух', desc: 'Тренуйся поруч із людьми, які мають однакові цілі та мотивацію' },
  { icon: '💡', title: 'Постійний розвиток', desc: 'Програми оновлюються та адаптуються разом із твоїм прогресом' },
]

export default function Home() {
  const { user, logout, isAuthenticated } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const [visible, setVisible] = useState<Set<string>>(new Set())
  const heroRef = useRef<HTMLDivElement>(null)

  const [coaches, setCoaches] = useState<Coach[]>([])
  const [coachesLoading, setCoachesLoading] = useState(true)
  const [coachesError, setCoachesError] = useState<string | null>(null)

  const [gallery, setGallery] = useState<Gallery[]>([])
  const [galleryLoading, setGalleryLoading] = useState(true)

  const fetchCoaches = async () => {
    setCoachesLoading(true)
    setCoachesError(null)
    try {
      const data = await apiClient.getCoaches()
      setCoaches(data)
    } catch (e) {
      setCoachesError(e instanceof Error ? e.message : 'Не вдалося завантажити тренерів')
    } finally {
      setCoachesLoading(false)
    }
  }

  const fetchGallery = async () => {
    setGalleryLoading(true)
    try {
      const data = await apiClient.getGallery()
      setGallery(data)
    } catch (e) {
      console.error('Failed to fetch gallery', e)
    } finally {
      setGalleryLoading(false)
    }
  }

  useEffect(() => {
    fetchCoaches()
    fetchGallery()
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

  const handleLogout = () => {
    logout()
    setMenuOpen(false)
  }

  return (
    <div className="site">
      {/* NAV */}
      <nav className="nav">
        <div className="nav-inner">
          <Link to="/" className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FitLife</span>
          </Link>
          <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
            <a href="#about" onClick={() => setMenuOpen(false)}>Про нас</a>
            <a href="#benefits" onClick={() => setMenuOpen(false)}>Переваги</a>
            <a href="#gallery" onClick={() => setMenuOpen(false)}>Галерея</a>
            <a href="#coaches" onClick={() => setMenuOpen(false)}>Тренери</a>
            {isAuthenticated ? (
              <>
                {user?.role === 'admin' && (
                  <Link to="/register/coach" className="nav-link-special" onClick={() => setMenuOpen(false)}>+ Додати тренера</Link>
                )}
                <span className="user-greeting">Привіт, {user?.first_name}!</span>
                <button className="btn-ghost" onClick={handleLogout}>Вийти</button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-ghost" onClick={() => setMenuOpen(false)}>Увійти</Link>
                <Link to="/register/member" className="btn-primary" onClick={() => setMenuOpen(false)}>Розпочати</Link>
              </>
            )}
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
            {isAuthenticated ? (
              <a href="#coaches" className="btn-primary large">
                Переглянути тренерів →
              </a>
            ) : (
              <>
                <Link to="/register/member" className="btn-primary large">
                  Почати безкоштовно →
                </Link>
                <a href="#about" className="btn-ghost large">Дізнатись більше</a>
              </>
            )}
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

      {/* GALLERY */}
      {gallery.length > 0 && (
        <section className="gallery section" id="gallery">
          <div className="gallery-inner">
            <div className="section-tag">Галерея</div>
            <h2 className="section-title">Життя у FitLife</h2>
            <p className="section-sub">Зазирни в нашу атмосферу та надихнись на зміни</p>

            <div className="gallery-grid">
              {gallery.map((item, i) => (
                <div
                  key={item.id}
                  id={`gallery-${i}`}
                  data-animate
                  className={`gallery-card fade-up ${isVisible(`gallery-${i}`) ? 'in' : ''}`}
                  style={{ transitionDelay: `${i * 100}ms` }}
                >
                  <img src={item.image_url} alt={item.title} className="gallery-img" />
                  <div className="gallery-overlay">
                    <h3>{item.title}</h3>
                    <p>{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

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
                  {c.emoji}
                </div>
                <div className="coach-info">
                  <h3>{c.first_name} {c.last_name}</h3>
                  <div className="coach-specialties">
                    {c.specializations.map((spec) => (
                      <span key={spec.id} className="coach-specialty">
                        {spec.emoji} {spec.name}
                      </span>
                    ))}
                  </div>
                  <div className="coach-meta">
                    <span>📅 {c.experience} {c.experience_label}</span>
                    {c.email && <span>✉️ {c.email}</span>}
                    <span>📞 {c.phone_number}</span>
                  </div>
                </div>
                {isAuthenticated ? (
                  <button className="btn-outline">
                    Записатись
                  </button>
                ) : (
                  <Link to="/register/member" className="btn-outline">
                    Записатись
                  </Link>
                )}
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
          {isAuthenticated ? (
            <a href="#coaches" className="btn-primary large">
              Переглянути тренерів
            </a>
          ) : (
            <Link to="/register/member" className="btn-primary large">
              Зареєструватись зараз
            </Link>
          )}
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
              <a href="#gallery">Галерея</a>
              <a href="#coaches">Тренери</a>
            </div>
            <div>
              <strong>Акаунт</strong>
              {isAuthenticated ? (
                <>
                  <span>Ви увійшли як {user?.first_name}</span>
                  <button onClick={handleLogout} className="link-button">Вийти</button>
                </>
              ) : (
                <>
                  <Link to="/login">Увійти</Link>
                  <Link to="/register/member">Реєстрація</Link>
                </>
              )}
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
    </div>
  )
}
