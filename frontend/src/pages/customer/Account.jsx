import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Field from '../../components/Field'
import { clearAccessToken, getAuthenticatedUserId, getUser, updateUser } from '../../api'
import { ErrorState, Loading } from '../../components/States'

const EMPTY = { firstname: '', lastname: '', email: '', phone: '', street: '', city: '', province: '', postalcode: '' }
const PROVINCES = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK']

export default function Account() {
  const navigate = useNavigate()
  const id = getAuthenticatedUserId()
  const [user, setUser] = useState(null)
  const [values, setValues] = useState(EMPTY)
  const [loading, setLoading] = useState(Boolean(id))
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (!id) {
      navigate('/login', { replace: true })
      return
    }
    getUser(id).then((data) => {
      setUser(data)
      setValues({
        firstname: data.firstname, lastname: data.lastname, email: data.email,
        phone: data.phone ?? '', street: data.address?.street ?? '', city: data.address?.city ?? '',
        province: data.address?.province ?? '', postalcode: data.address?.postalcode ?? '',
      })
    }).catch((requestError) => setError(requestError.message)).finally(() => setLoading(false))
  }, [id, navigate])

  const bind = (key) => ({ value: values[key], onChange: (e) => setValues({ ...values, [key]: e.target.value }) })

  async function submit(e) {
    e.preventDefault()
    setError('')
    setSaved(false)
    setBusy(true)
    try {
      const updated = await updateUser(id, {
        firstname: values.firstname.trim(), lastname: values.lastname.trim(), email: values.email.trim(),
        phone: values.phone.replace(/\D/g, '') || null,
        address: { street: values.street.trim(), city: values.city.trim(), province: values.province, postalcode: values.postalcode.trim() },
      })
      setUser(updated)
      setSaved(true)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setBusy(false)
    }
  }

  function signOut() {
    clearAccessToken()
    navigate('/login')
  }

  if (!id) return null
  if (loading) return <section className="section mode-paper"><div className="wrap"><Loading>Loading your account.</Loading></div></section>
  if (error && !user) return <section className="section mode-paper"><div className="wrap"><ErrorState error={{ message: error }} /></div></section>

  return (
    <section className="section mode-paper">
      <title>My account | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>My account</span>
          <h1 className="h2">Your details.</h1>
          <p className="measure muted">Keep your personal and delivery details current.</p>
        </div>
        <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
          <div className="field__row">
            <Field label="First name" autoComplete="given-name" required {...bind('firstname')} />
            <Field label="Last name" autoComplete="family-name" required {...bind('lastname')} />
          </div>
          <div className="field__row">
            <Field label="Email" type="email" autoComplete="email" required {...bind('email')} />
            <Field label="Phone (optional)" type="tel" autoComplete="tel" {...bind('phone')} />
          </div>
          <Field label="Street address" autoComplete="street-address" required {...bind('street')} />
          <div className="field__row">
            <Field label="City" autoComplete="address-level2" required {...bind('city')} />
            <Field label="Province" as="select" autoComplete="address-level1" required {...bind('province')}>
              <option value="">Choose</option>
              {PROVINCES.map((province) => <option key={province}>{province}</option>)}
            </Field>
          </div>
          <Field label="Postal code" autoComplete="postal-code" required {...bind('postalcode')} />
          <div className="btn-row">
            <button className="btn" type="submit" disabled={busy}>{busy ? 'Saving' : 'Save changes'}</button>
            <button className="btn btn--ghost" type="button" onClick={signOut}>Sign out</button>
          </div>
          {saved && <p className="small" role="status">Your details are saved.</p>}
          {error && <p className="small" role="alert">{error}</p>}
        </form>
        <p className="small muted">Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'today'}.</p>
      </div>
    </section>
  )
}
