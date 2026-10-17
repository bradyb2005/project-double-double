import { Link } from 'react-router-dom'

export default function NotFound({ title = 'Page not found', back = false }) {
  return (
    <section className="section mode-field">
      <div className="wrap stack" style={{ '--stack': 'var(--s-6)' }}>
        <title>{`${title} | Double Double`}</title>
        <span className="eyebrow"><b>#404</b>Lost</span>
        <h1 className="display">{title}</h1>
        <p className="measure">{back ? 'We could not find that.' : 'Nothing lives at this address.'}</p>
        <div className="btn-row"><Link className="btn" to="/">Back to start</Link></div>
      </div>
    </section>
  )
}
