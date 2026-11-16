import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Field from '../components/Field'
import { registerUser } from '../api'

const PROVINCES = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK']
const EMPTY = {
  firstname: '', lastname: '', email: '', phone: '', password: '',
  street: '', city: '', province: '', postalcode: '',
}

function validate(values) {
  const errors = {}
  for (const key of ['firstname', 'lastname', 'email', 'password', 'street', 'city', 'province', 'postalcode']) {
    if (!values[key].trim()) errors[key] = 'This field is required.'
  }
  if (values.password && values.password.length < 8) errors.password = 'Use at least 8 characters.'
  if (values.phone && !/^\d{10}$/.test(values.phone.replace(/\D/g, ''))) errors.phone = 'Use ten digits.'
  if (values.postalcode && !/^[A-Z]\d[A-Z]\d[A-Z]\d$/.test(values.postalcode.replace(/\s/g, '').toUpperCase())) {
    errors.postalcode = 'Use the format V1X 4J8.'
  }
  return errors
}

export default function Register() {
  const [values, setValues] = useState(EMPTY)
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()
  const bind = (key) => ({
    value: values[key],
    onChange: (e) => setValues({ ...values, [key]: e.target.value }),
    error: errors[key],
  })

  async function submit(e) {
    e.preventDefault()
    const found = validate(values)
    setErrors(found)
    setFormError('')
    if (Object.keys(found).length) return
    setBusy(true)
    try {
      await registerUser({
        firstname: values.firstname.trim(),
        lastname: values.lastname.trim(),
        email: values.email.trim(),
        phone: values.phone.replace(/\D/g, '') || null,
        password: values.password,
        address: {
          street: values.street.trim(),
          city: values.city.trim(),
          province: values.province,
          postalcode: values.postalcode.trim(),
        },
      })
      navigate('/login', { state: { registered: true } })
    } catch (error) {
      setFormError(error.message)
      setBusy(false)
    }
  }

  return (
    <section className="section mode-paper">
      <title>Register | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>New customer</span>
          <h1 className="h2">Set your table</h1>
          <p className="measure muted">Create an account to keep your details ready for every order.</p>
        </div>
        <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
          <div className="field__row">
            <Field label="First name" autoComplete="given-name" required {...bind('firstname')} />
            <Field label="Last name" autoComplete="family-name" required {...bind('lastname')} />
          </div>
          <div className="field__row">
            <Field label="Email" type="email" autoComplete="email" required {...bind('email')} />
            <Field label="Phone (optional)" type="tel" autoComplete="tel" placeholder="250-555-0100" {...bind('phone')} />
          </div>
          <Field label="Password" type="password" autoComplete="new-password" hint="At least 8 characters." required {...bind('password')} />
          <Field label="Street address" autoComplete="street-address" required {...bind('street')} />
          <div className="field__row">
            <Field label="City" autoComplete="address-level2" required {...bind('city')} />
            <Field label="Province" as="select" autoComplete="address-level1" required {...bind('province')}>
              <option value="">Choose</option>
              {PROVINCES.map((province) => <option key={province}>{province}</option>)}
            </Field>
          </div>
          <Field label="Postal code" autoComplete="postal-code" placeholder="V1X 4J8" required {...bind('postalcode')} />
          <div className="btn-row">
            <button className="btn" type="submit" disabled={busy}>{busy ? 'Creating' : 'Create account'}</button>
            <Link className="btn btn--ghost" to="/login">I already have an account</Link>
          </div>
          <p className="small" role="alert">{formError}</p>
        </form>
      </div>
    </section>
  )
}
