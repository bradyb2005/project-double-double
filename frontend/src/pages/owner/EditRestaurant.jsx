import { useNavigate } from 'react-router-dom'
import { updateRestaurant } from '../../api'
import ManagedRestaurant from '../../components/ManagedRestaurant'
import RestaurantForm from '../../components/RestaurantForm'

function Editor({ restaurant: r }) {
  const navigate = useNavigate()

  async function save(payload) {
    await updateRestaurant(r.id, payload)
    navigate('/owner')
  }

  return (
    <section className="section mode-paper">
      <title>Edit restaurant | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#{r.id}</b>Edit restaurant</span>
          <h1 className="h2">{r.name}</h1>
          <p className="measure muted">Change the details customers see. Blank fields keep their current value.</p>
        </div>
        <RestaurantForm
          initial={{
            name: r.name, cuisine: r.cuisine ?? '', phone: r.phone ?? '', address: r.address ?? '',
            postalcode: r.postalcode ?? '', city: r.location?.city ?? '', province: r.location?.province ?? '',
          }}
          submitLabel="Save changes" busyLabel="Saving" cancelTo="/owner" onSubmit={save}
        />
      </div>
    </section>
  )
}

// Edits the restaurant the owner is currently running (the demo has no accounts).
export default function EditRestaurant() {
  return <ManagedRestaurant>{(r) => <Editor key={r.id} restaurant={r} />}</ManagedRestaurant>
}
