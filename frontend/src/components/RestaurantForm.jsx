import { useState } from 'react'
import { Link } from 'react-router-dom'
import Field from './Field'

const PROVINCES = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
const EMPTY_RESTAURANT = { name: '', cuisine: '', phone: '', address: '', postalcode: '', city: '', province: '' }

// Mirrors the backend rules in restaurant_service.validate_restaurant_data.
function validate(v) {
  const e = {}
  if (!v.name.trim()) e.name = 'Name is required.'
  if (!v.address.trim()) e.address = 'Address is required.'
  if (!v.city.trim()) e.city = 'City is required.'
  if (!v.province) e.province = 'Pick a province.'
  if (!/^[A-Z]\d[A-Z]\d[A-Z]\d$/.test(v.postalcode.replace(/\s/g, '').toUpperCase())) {
    e.postalcode = 'Use the format V1X 4J8.'
  }
  if (v.phone.trim() && !/^(\d{3}-\d{3}-\d{4}|\d{10})$/.test(v.phone.trim())) {
    e.phone = 'Use 250-555-0100 or ten digits.'
  }
  return e
}

// Shared by Add restaurant (POST /restaurants) and Edit restaurant (PUT /restaurants/update/{id}).
// onSubmit receives the API payload and may throw; the message is shown under the form.
export default function RestaurantForm({ initial = EMPTY_RESTAURANT, submitLabel, busyLabel, cancelTo, onSubmit }) {
  const [values, setValues] = useState(initial)
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [busy, setBusy] = useState(false)

  const bind = (key) => ({
    value: values[key],
    onChange: (e) => setValues({ ...values, [key]: e.target.value }),
    error: errors[key],
  })

  async function submit(e) {
    e.preventDefault()
    setFormError('')
    const found = validate(values)
    setErrors(found)
    if (Object.keys(found).length) return
    setBusy(true)
    try {
      await onSubmit({
        name: values.name.trim(),
        cuisine: values.cuisine.trim() || null,
        phone: values.phone.trim() || null,
        address: values.address.trim(),
        postalcode: values.postalcode.trim(),
        location: { city: values.city.trim(), province: values.province },
      })
    } catch (err) {
      setFormError(err.message)
      setBusy(false)
    }
  }

  return (
    <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
      <Field label="Name" autoComplete="off" required {...bind('name')} />
      <div className="field__row">
        <Field label="Cuisine (optional)" placeholder="Ramen" {...bind('cuisine')} />
        <Field label="Phone (optional)" type="tel" placeholder="250-555-0100" {...bind('phone')} />
      </div>
      <Field label="Address" autoComplete="street-address" required {...bind('address')} />
      <div className="field__row">
        <Field label="City" autoComplete="address-level2" required {...bind('city')} />
        <Field label="Province" as="select" required {...bind('province')}>
          <option value="">Choose</option>
          {PROVINCES.map((p) => <option key={p}>{p}</option>)}
        </Field>
      </div>
      <Field label="Postal code" autoComplete="postal-code" placeholder="V1X 4J8" required {...bind('postalcode')} />

      <div className="btn-row">
        <button className="btn" type="submit" disabled={busy}>{busy ? busyLabel : submitLabel}</button>
        {cancelTo && <Link className="btn btn--ghost" to={cancelTo}>Cancel</Link>}
      </div>
      <p className="small" role="alert">{formError}</p>
    </form>
  )
}
