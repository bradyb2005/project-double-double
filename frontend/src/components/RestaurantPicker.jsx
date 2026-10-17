import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getRestaurants } from '../api'
import { setManagedRestaurant, useDemo } from '../demoStore'
import { useFetch } from '../useFetch'
import Field from './Field'
import { ErrorState, Loading } from './States'

// Owners pick which restaurant they run. The backend has no ownership, so this is remembered locally.
export default function RestaurantPicker({ title = 'Which restaurant do you run?' }) {
  const { data, error, loading, reload } = useFetch(getRestaurants, [])
  const [choice, setChoice] = useState('')
  const { managedId } = useDemo()

  return (
    <div className="empty">
      <span className="eyebrow">#0 Pick one</span>
      <h2 className="h3">{title}</h2>
      {loading && <Loading>Fetching restaurants.</Loading>}
      {error && <ErrorState error={error} onRetry={reload} />}
      {data && (
        <form
          className="stack form-narrow" style={{ '--stack': 'var(--s-4)', width: '100%' }}
          onSubmit={(e) => { e.preventDefault(); if (choice) setManagedRestaurant(Number(choice)) }}
        >
          <Field label="Restaurant" as="select" value={choice || (managedId ?? '')} onChange={(e) => setChoice(e.target.value)}>
            <option value="">Choose</option>
            {data.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
          </Field>
          <div className="btn-row">
            <button className="btn" type="submit" disabled={!choice}>Manage this restaurant</button>
            <Link className="btn btn--ghost" to="/owner/restaurants/new">Add a new one</Link>
          </div>
        </form>
      )}
    </div>
  )
}
