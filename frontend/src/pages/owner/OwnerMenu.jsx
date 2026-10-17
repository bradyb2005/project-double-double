import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { getMenu } from '../../api'
import { useFetch } from '../../useFetch'
import ManagedRestaurant from '../../components/ManagedRestaurant'
import MenuItemRow from '../../components/MenuItemRow'
import { Empty, ErrorState, Loading } from '../../components/States'

function MenuManager({ restaurant }) {
  const menu = useFetch(() => getMenu(restaurant.id), [restaurant.id])
  const groups = useMemo(() => {
    const map = new Map()
    for (const item of menu.data ?? []) {
      if (!map.has(item.category)) map.set(item.category, [])
      map.get(item.category).push(item)
    }
    return [...map]
  }, [menu.data])

  return (
    <section className="section mode-paper">
      <title>Menu | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>{restaurant.name}</span>
          <h1 className="h2">Your menu</h1>
          <div className="btn-row">
            <Link className="btn" to={`/owner/restaurants/${restaurant.id}/menu/new`}>Add menu item</Link>
          </div>
        </div>
        {menu.loading && <Loading>Fetching the menu.</Loading>}
        {menu.error && !menu.loading && <ErrorState error={menu.error} onRetry={menu.reload} />}
        {menu.data?.length === 0 && (
          <Empty title="No menu items yet" to={`/owner/restaurants/${restaurant.id}/menu/new`} action="Add the first item">
            Customers cannot order until you add something.
          </Empty>
        )}
        {groups.map(([category, items], g) => (
          <div className="stack" style={{ '--stack': 'var(--s-4)' }} key={category}>
            <h2 className="eyebrow"><b>#{g + 1}</b>{category}</h2>
            <ul className="work-list">
              {items.map((item, i) => (
                <MenuItemRow
                  key={`${restaurant.id}-${item.id}`} item={item} index={i} category={category}
                  action={<Link className="link small" to={`/owner/restaurants/${restaurant.id}/menu/${item.id}/edit`} aria-label={`Edit ${item.name}`}>Edit</Link>}
                />
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  )
}

export default function OwnerMenu() {
  return <ManagedRestaurant>{(r) => <MenuManager restaurant={r} />}</ManagedRestaurant>
}
