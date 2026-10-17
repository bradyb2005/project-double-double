import { Link } from 'react-router-dom'

export function Loading({ children = 'Fetching from the kitchen.' }) {
  return (
    <div className="loading" role="status" aria-live="polite">
      <span className="eyebrow">Loading</span>
      <div className="loading__bar" aria-hidden="true" />
      <p className="small muted">{children}</p>
    </div>
  )
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="empty" role="alert">
      <span className="eyebrow">#0 Error</span>
      <h3 className="h3">Something went wrong</h3>
      <p className="small muted measure">{error?.message ?? 'Unknown error.'}</p>
      {onRetry && <button className="btn" type="button" onClick={onRetry}>Try again</button>}
    </div>
  )
}

export function Empty({ title, children, to, action }) {
  return (
    <div className="empty">
      <span className="eyebrow">#0 Empty</span>
      <h3 className="h3">{title}</h3>
      <p className="small muted measure">{children}</p>
      {to && <Link className="btn" to={to}>{action}</Link>}
    </div>
  )
}
