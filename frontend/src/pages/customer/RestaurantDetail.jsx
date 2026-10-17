import { useMemo } from 'react'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getMenu, formatRating, getRestaurant } from '../../api'
import { restaurantPhoto } from '../../foodImages'
import { addToCart, replaceCart, useDemo } from '../../demoStore'
import { useFetch } from '../../useFetch'
import MenuItemRow from '../../components/MenuItemRow'
import { Empty, ErrorState, Loading } from '../../components/States'
import NotFound from '../NotFound'

export default function RestaurantDetail() {
  const { id } = useParams()
  const restaurant = useFetch(() => getRestaurant(id), [id])
  const { cart } = useDemo()
  const [swap, setSwap] = useState(null)   // an add that needs the cart replaced first
  const menu = useFetch(() => getMenu(id), [id])

  // Group by category in first-seen order; the backend gives no category order.
  const groups = useMemo(() => {
    const map = new Map()
    for (const item of menu.data ?? []) {
      if (!map.has(item.category)) map.set(item.category, [])
      map.get(item.category).push(item)
    }
    return [...map]
  }, [menu.data])

  if (restaurant.error?.status === 404 || restaurant.error?.status === 422) {
    return <NotFound title="Restaurant not found" back />
  }

  const r = restaurant.data
  const inCart = (itemId) => (cart?.restaurant.id === r?.id ? cart.lines.find((l) => l.itemId === itemId)?.qty : 0)
  const add = (item) => { const res = addToCart(r, item); if (res.conflict) setSwap(item) }
  const addButton = (item) =>
    item.availability === false || !r ? null : (
      <button className="btn btn--sm" type="button" onClick={() => add(item)} aria-label={`Add ${item.name} to cart`}>
        {inCart(item.id) ? `Add another (${inCart(item.id)})` : 'Add to cart'}
      </button>
    )
  return (
    <>
      {r && <title>{`${r.name} | Double Double`}</title>}
      <section className="section mode-field">
        <div className="wrap stack" style={{ '--stack': 'var(--s-7)' }}>
          {restaurant.loading && <Loading>Fetching the restaurant.</Loading>}
          {restaurant.error && !restaurant.loading && <ErrorState error={restaurant.error} onRetry={restaurant.reload} />}
          {r && (
            <div className="hero hero--compact">
              <div className="hero__copy">
                <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
                  <span className="eyebrow"><b>#{r.id}</b>{r.cuisine ?? 'Restaurant'}</span>
                  <h1 className="display">{r.name}</h1>
                </div>
                <dl className="grid" style={{ gap: 'var(--s-4) var(--s-5)' }}>
                  <div className="fact"><dt className="micro">Address</dt><dd>{r.address}<br />{r.location.city}, {r.location.province} {r.postalcode}</dd></div>
                  <div className="fact"><dt className="micro">Phone</dt><dd className="num">{r.phone ?? 'Not listed'}</dd></div>
                  <div className="fact"><dt className="micro">Rating</dt><dd className="num">{formatRating(r.rating)}</dd></div>
                </dl>
              </div>
              {restaurantPhoto(r) && (
                <figure>
                  <div className="duo duo--inv"><img src={restaurantPhoto(r)} alt="" width="900" height="675" /></div>
                  <figcaption className="caption micro"><span>Fig. 1</span><span><Link className="link" to="/credits">Photo credit</Link></span></figcaption>
                </figure>
              )}
            </div>
          )}
        </div>
      </section>

      <section className="section mode-paper" id="menu-section">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
            <span className="eyebrow"><b>#1</b>Menu</span>
            <h2 className="h2">What is on offer</h2>
            {cart?.lines.length > 0 && (
              <div className="btn-row">
                <Link className="btn" to="/customer/cart">View cart from {cart.restaurant.name}</Link>
              </div>
            )}
          </div>

          {menu.loading && <Loading>Fetching the menu.</Loading>}
          {menu.error && !menu.loading && <ErrorState error={menu.error} onRetry={menu.reload} />}
          {menu.data?.length === 0 && (
            <Empty title="No menu items yet">This restaurant has not published a menu.</Empty>
          )}

          {swap && (
            <div className="note stack" style={{ '--stack': 'var(--s-3)' }} role="alert">
              <p className="small">
                Your cart has items from {cart.restaurant.name}. Start a new cart with {swap.name} from {r?.name}?
              </p>
              <div className="btn-row btn-row--tight">
                <button className="btn btn--sm" type="button" onClick={() => { replaceCart(r, swap); setSwap(null) }}>Replace cart</button>
                <button className="btn btn--sm btn--ghost" type="button" onClick={() => setSwap(null)}>Keep my cart</button>
              </div>
            </div>
          )}

          {groups.map(([category, items], g) => (
            <div className="stack" style={{ '--stack': 'var(--s-4)' }} key={category}>
              <h3 className="eyebrow"><b>#{g + 1}</b>{category}</h3>
              <ul className="work-list">
                {items.map((item, i) => (
                  <MenuItemRow key={`${id}-${item.id}`} item={item} index={i} category={category} action={addButton(item)} />
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}
