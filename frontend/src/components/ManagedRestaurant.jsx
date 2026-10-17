import { getRestaurant } from '../api'
import { useDemo } from '../demoStore'
import { useFetch } from '../useFetch'
import { ErrorState, Loading } from './States'
import RestaurantPicker from './RestaurantPicker'

// Gate for owner pages: shows the picker until a restaurant is chosen, then renders children(restaurant).
export default function ManagedRestaurant({ children }) {
  const { managedId } = useDemo()
  const { data, error, loading, reload } = useFetch(
    () => (managedId ? getRestaurant(managedId) : Promise.resolve(null)), [managedId],
  )
  if (!managedId || error?.status === 404) {
    return (
      <section className="section mode-paper">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <span className="eyebrow"><b>#1</b>Owner</span>
          <h1 className="h2">Choose your restaurant</h1>
          <RestaurantPicker />
        </div>
      </section>
    )
  }
  if (loading) return <section className="section mode-paper"><div className="wrap"><Loading>Fetching your restaurant.</Loading></div></section>
  if (error) return <section className="section mode-paper"><div className="wrap"><ErrorState error={error} onRetry={reload} /></div></section>
  return data ? children(data) : null
}
