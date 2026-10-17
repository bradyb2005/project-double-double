import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { ROLES, roleOf } from '../roles'
import { cartCount, useDemo } from '../demoStore'

export default function Layout() {
  const [open, setOpen] = useState(false)
  const { pathname } = useLocation()
  const role = roleOf(pathname)
  const { cart } = useDemo()
  const count = cartCount(cart)
  const links = (role ? ROLES[role].nav : []).map((l) => ({
    ...l, label: l.to === '/customer/cart' && count ? `Cart (${count})` : l.label,
  }))

  // Keep the page behind the open panel inert. Links inside the panel close it.
  useEffect(() => {
    document.body.classList.toggle('menu-open', open)
    document.querySelectorAll('main, footer, .skip').forEach((el) => { el.inert = open })
    if (!open) return
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    const wide = matchMedia('(min-width: 1024px)')
    const onWide = (m) => m.matches && setOpen(false)
    document.addEventListener('keydown', onKey)
    wide.addEventListener('change', onWide)
    return () => {
      document.removeEventListener('keydown', onKey)
      wide.removeEventListener('change', onWide)
    }
  }, [open])

  // New route starts at the top.
  useEffect(() => { if (!window.location.hash) window.scrollTo(0, 0) }, [pathname])

  // Every role can always get back to the role chooser.
  const switchLabel = role ? 'Switch role' : 'Choose a role'

  return (
    <>
      <a className="skip" href="#main">Skip to content</a>

      <header className="header mode-field">
        <div className="wrap header__bar">
          <div className="header__brand">
            <Link className="wordmark" to="/" aria-label="Double Double, home">Double Double</Link>
            {role && <span className="micro">//{ROLES[role].label}</span>}
          </div>
          <nav aria-label="Primary">
            <div className="nav-links">
              {links.map((l) => (
                <NavLink key={l.to} to={l.to} end={l.end}>{l.label}</NavLink>
              ))}
              {role && <Link to="/">{switchLabel}</Link>}
            </div>
          </nav>
          {role ? (
            <Link className="btn btn--sm nav-links" to="/">{switchLabel}</Link>
          ) : (
            <span className="nav-links" />
          )}
          <button
            className="btn btn--ghost menu-toggle" type="button"
            aria-expanded={open} aria-controls="menu" onClick={() => setOpen(!open)}
          >
            <span className="menu-toggle__open">Menu</span>
            <span className="menu-toggle__close">Close</span>
          </button>
        </div>
        <div className="menu-panel" id="menu" hidden={!open}>
          {links.map((l, i) => (
            <Link key={l.to} className="menu-link" to={l.to} onClick={() => setOpen(false)}>{l.label} <span>0{i + 1}</span></Link>
          ))}
          <Link className="menu-link" to="/" onClick={() => setOpen(false)}>{switchLabel} <span>0{links.length + 1}</span></Link>
        </div>
      </header>

      <main id="main" tabIndex={-1}>
        <Outlet />
      </main>

      <footer>
        <div className="section mode-paper footer-solid">
          <div className="wrap">
            <div className="footer-row">
              <span className="eyebrow">Double Double / Kelowna, BC / 2026</span>
              <nav aria-label="Footer" className="footer-row" style={{ gap: 'var(--s-1) var(--s-5)' }}>
                {links.map((l) => (
                  <Link key={l.to} className="eyebrow" to={l.to}>{l.label}</Link>
                ))}
                <Link className="eyebrow" to="/">{switchLabel}</Link>
                <Link className="eyebrow" to="/credits">Photo credits</Link>
              </nav>
            </div>
          </div>
        </div>
      </footer>
    </>
  )
}
