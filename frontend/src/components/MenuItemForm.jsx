import { useState } from 'react'
import { Link } from 'react-router-dom'
import { MENU_CATEGORIES } from '../api'
import Field from './Field'

const EMPTY_ITEM = { name: '', price: '', category: '', description: '', image: '', availability: true }

// Shared by the add and edit pages. `onSubmit(payload)` may throw; its message is shown under the form.
export default function MenuItemForm({ initial = EMPTY_ITEM, submitLabel, busyLabel, cancelTo, onSubmit }) {
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
    const found = {}
    if (!values.name.trim()) found.name = 'Name is required.'
    if (!(Number(values.price) > 0)) found.price = 'Price must be greater than 0.'
    if (!values.category) found.category = 'Pick a category.'
    setErrors(found)
    if (Object.keys(found).length) return
    setBusy(true)
    try {
      await onSubmit({
        name: values.name.trim(),
        price: Number(values.price),
        category: values.category,
        image: values.image.trim(),
        availability: values.availability,
        description: values.description.trim() || null,
      })
    } catch (err) {
      setFormError(err.message)
      setBusy(false)
    }
  }

  return (
    <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
      <Field label="Name" required {...bind('name')} />
      <div className="field__row">
        <Field label="Price (CAD)" type="number" inputMode="decimal" min="0" step="0.01" placeholder="9.50" required {...bind('price')} />
        <Field label="Category" as="select" required {...bind('category')}>
          <option value="">Choose</option>
          {MENU_CATEGORIES.map((c) => <option key={c}>{c}</option>)}
        </Field>
      </div>
      <Field label="Description (optional)" as="textarea" rows={4} {...bind('description')} />
      <Field label="Image URL (optional)" type="url" placeholder="https://" {...bind('image')} />
      <label className="check">
        <input
          type="checkbox" checked={values.availability}
          onChange={(e) => setValues({ ...values, availability: e.target.checked })}
        />
        <span className="small">Available to order</span>
      </label>

      <div className="btn-row">
        <button className="btn" type="submit" disabled={busy}>{busy ? busyLabel : submitLabel}</button>
        <Link className="btn btn--ghost" to={cancelTo}>Cancel</Link>
      </div>
      <p className="small" role="alert">{formError}</p>
    </form>
  )
}
