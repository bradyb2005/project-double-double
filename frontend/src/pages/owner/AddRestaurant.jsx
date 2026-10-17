import { useNavigate } from 'react-router-dom'
import { createRestaurant } from '../../api'
import { setManagedRestaurant } from '../../demoStore'
import RestaurantForm from '../../components/RestaurantForm'

export default function AddRestaurant() {
  const navigate = useNavigate()

  async function save(payload) {
    const created = await createRestaurant(payload)
    setManagedRestaurant(created.id)
    navigate('/owner')
  }

  return (
    <section className="section mode-paper">
      <title>Add restaurant | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>New restaurant</span>
          <h1 className="h2">Put a kitchen on the list</h1>
          <p className="measure muted">Name, address and postal code are required. Everything else can wait.</p>
        </div>
        <RestaurantForm submitLabel="Add restaurant" busyLabel="Saving" onSubmit={save} />
      </div>
    </section>
  )
}
