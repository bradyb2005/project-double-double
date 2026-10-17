import { useNavigate, useParams } from 'react-router-dom'
import { createMenuItem, getRestaurant } from '../../api'
import { useFetch } from '../../useFetch'
import MenuItemForm from '../../components/MenuItemForm'
import { Loading } from '../../components/States'
import NotFound from '../NotFound'

export default function AddMenuItem() {
  const { id } = useParams()
  const restaurant = useFetch(() => getRestaurant(id), [id])
  const navigate = useNavigate()

  if (restaurant.error?.status === 404 || restaurant.error?.status === 422) {
    return <NotFound title="Restaurant not found" back />
  }

  const r = restaurant.data
  return (
    <section className="section mode-paper">
      <title>Add menu item | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>New menu item</span>
          <h1 className="h2">{r ? `Add to ${r.name}` : 'Add a menu item'}</h1>
          {restaurant.loading && <Loading>Fetching the restaurant.</Loading>}
          {restaurant.error && !restaurant.loading && <p className="small" role="alert">{restaurant.error.message}</p>}
        </div>
        <MenuItemForm
          submitLabel="Add item" busyLabel="Saving" cancelTo="/owner/menu"
          onSubmit={async (payload) => {
            await createMenuItem(id, payload)
            navigate('/owner/menu')
          }}
        />
      </div>
    </section>
  )
}
