import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import Field from '../components/Field'
import { loginUser, saveAccessToken } from '../api'

const TEST_ACCOUNTS = [
  { label: 'Fill customer test account', email: 'customer.test@example.com', password: 'SecurePassword123!' },
  { label: 'Fill restaurant test account', email: 'restaurant.test@example.com', password: 'SecurePassword123!' },
  { label: 'Fill admin test account', email: 'admin.test@example.com', password: 'SecurePassword123!' },
]

export default function Login() {
  const location = useLocation()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function fillAccount(account) {
    setEmail(account.email)
    setPassword(account.password)
    setError('')
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const response = await loginUser({ email, password })
      saveAccessToken(response.access_token)
      navigate('/customer/account')
    } catch (requestError) {
      setError(requestError.message)
      setBusy(false)
    }
  }

  return (
    <section className="section mode-field">
      <title>Sign in | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Sign in</span>
          <h1 className="h2">Welcome back.</h1>
          <p className="measure">Sign in to view your account and keep ordering without re-entering your details.</p>
        </div>
        {location.state?.registered && <p className="note" role="status">Account created. Sign in to continue.</p>}
        <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
          <Field label="Email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <Field label="Password" type="password" autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
          <div className="btn-row">
            <button className="btn" type="submit" disabled={busy}>{busy ? 'Signing in' : 'Sign in'}</button>
            <Link className="btn btn--ghost" to="/register">Create an account</Link>
          </div>
          <p className="small" role="alert">{error}</p>
        </form>
        <div className="stack form-narrow" style={{ '--stack': 'var(--s-3)' }}>
          <span className="eyebrow">Testing shortcuts</span>
          <p className="small muted">Fill a seeded test account, then submit the form.</p>
          <div className="btn-row">
            {TEST_ACCOUNTS.map((account) => (
              <button className="btn btn--ghost btn--sm" type="button" key={account.email} onClick={() => fillAccount(account)}>
                {account.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
