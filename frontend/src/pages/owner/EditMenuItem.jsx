import { useNavigate, useParams } from 'react-router-dom'
import { getMenu, updateMenuItem } from '../../api'
import { useFetch } from '../../useFetch'
import MenuItemForm from '../../components/MenuItemForm'
import { ErrorState, Loading } from '../../components/States'
import NotFound from '../NotFound'

const same = (a, b) =>
  a.name === b.name && a.price === b.price && a.category === b.category &&
  (a.image ?? '') === (b.image ?? '') && a.availability === b.availability &&
  (a.description ?? '') === (b.description ?? '')

export default function EditMenuItem() {
  const { id, itemId } = useParams()
  const menu = useFetch(() => getMenu(id), [id])
  const navigate = useNavigate()

  if (menu.error?.status === 404 || menu.error?.status === 422) {
    return <NotFound title="Restaurant not found" back />
  }
  const item = menu.data?.find((i) => String(i.id) === itemId)
  if (menu.data && !item) return <NotFound title="Menu item not found" back />

  async function save(payload) {
    // Always send the whole item: a partial PUT is easy to get wrong server-side, and this keeps the request explicit.
    await updateMenuItem(id, itemId, payload)
    // The response only echoes what was sent, so refetch to confirm the change really landed.
    const fresh = (await getMenu(id)).find((i) => String(i.id) === itemId)
    if (!fresh || !same(fresh, { ...payload })) {
      throw new Error('The server accepted the change, but the saved item did not change. Reload to see what is stored.')
    }
    navigate('/owner/menu')
  }

  return (
    <section className="section mode-paper">
      <title>Edit menu item | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Edit menu item</span>
          <h1 className="h2">{item ? item.name : 'Edit a menu item'}</h1>
        </div>
        {menu.loading && <Loading>Fetching the menu.</Loading>}
        {menu.error && !menu.loading && <ErrorState error={menu.error} onRetry={menu.reload} />}
        {item && (
          <MenuItemForm
            initial={{
              name: item.name, price: String(item.price), category: item.category,
              description: item.description ?? '', image: item.image ?? '', availability: item.availability !== false,
            }}
            submitLabel="Save changes" busyLabel="Saving" cancelTo="/owner/menu"
            onSubmit={save}
          />
        )}
      </div>
    </section>
  )
}
