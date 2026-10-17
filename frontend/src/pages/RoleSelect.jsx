import { Link } from 'react-router-dom'
import { ROLES } from '../roles'

const ABOUT = {
  customer: ['Browse restaurants, fill a cart, place an order and follow it to your door.', 'rings'],
  owner: ['Manage your restaurant: take orders, keep the menu current, add new dishes.', 'grid'],
}

export default function RoleSelect() {
  return (
    <>
      <title>Double Double</title>
      <section className="section mode-field hero-section" id="top">
        <div className="wrap hero hero--compact">
          <div className="hero__copy">
            <span className="eyebrow"><b>#0</b>Kelowna, BC</span>
            <h1 className="display">Pick your seat.</h1>
            <p className="measure">One kitchen, two ways in. Choose how you are using Double Double today.</p>
          </div>
        </div>
      </section>

      <section className="section mode-paper" id="roles">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <div className="grid grid--2">
            {Object.entries(ROLES).map(([key, role], i) => (
              <Link className="feature feature--link" to={`/${key}`} key={key}>
                <span className="eyebrow"><b>#{i + 1}</b>{role.label}</span>
                <h2 className="h3">{{ customer: 'I am hungry', owner: 'I run a kitchen' }[key]}</h2>
                <p className="small muted measure">{ABOUT[key][0]}</p>
                <div className={`plate plate--${ABOUT[key][1]}`} aria-hidden="true" />
              </Link>
            ))}
          </div>
          <p className="small muted measure">
            There are no accounts yet, so any seat is open to anyone. Orders, carts and the restaurant an owner manages are
            demo data saved in this browser; the restaurant list and menus come from the real backend.
          </p>
        </div>
      </section>
    </>
  )
}
