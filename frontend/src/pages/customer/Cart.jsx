import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { checkout, formatPrice, getAuthenticatedUserId, getMenu, getRestaurant, getUser } from '../../api'
import { emptyCart, refreshCart, setQuantity, useServerCart } from '../../cartStore'
import { useFetch } from '../../useFetch'
import { Empty, ErrorState, Loading } from '../../components/States'

// The backend's messages are accurate but written for developers, so translate the common ones.
const FRIENDLY = [
  [/empty cart|has no cart/i, 'Your cart is empty. Add something from a menu before placing an order.'],
  [/unavailable|not available/i, 'An item in your cart is unavailable right now. Remove it and try again.'],
  [/not found/i, 'Something in your cart is no longer on the menu. Remove it and try again.'],
  [/not active|inactive/i, 'This account is deactivated, so it cannot place orders.'],
]

function checkoutMessage(error) {
  if (error.status === 401) return 'Your session has expired. Sign in again to place your order.'
  if (error.status === 403) return 'You can only place orders from your own cart.'
  const match = FRIENDLY.find(([pattern]) => pattern.test(error.message))
  return match ? match[1] : error.message
}

export default function Cart() {
  const navigate = useNavigate()
  const userId = getAuthenticatedUserId()
  const { cart, loaded } = useServerCart()
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const restaurantId = cart?.items?.[0]?.restaurant_id ?? null
  const menu = useFetch(() => (restaurantId ? getMenu(restaurantId) : Promise.resolve([])), [restaurantId])
  const restaurant = useFetch(() => (restaurantId ? getRestaurant(restaurantId) : Promise.resolve(null)), [restaurantId])

  useEffect(() => {
    if (!userId) return
    refreshCart().catch((e) => setError(e.message))
    getUser(userId).then(setUser).catch((e) => setError(e.message))
  }, [userId])

  // The cart stores ids and quantities only, so names and prices come from the menu.
  const lines = (cart?.items ?? []).map((item) => {
    const menuItem = menu.data?.find((m) => m.id === item.item_id)
    const unitCents = menuItem ? Math.round(Number(menuItem.price) * 100) : 0
    return { ...item, menuItem, unitCents, lineCents: unitCents * item.quantity }
  })
  const totalCents = lines.reduce((sum, l) => sum + l.lineCents, 0)
  const problem = lines.some((l) => !l.menuItem || l.menuItem.availability === false)
  const address = user?.address?.street

  async function run(action) {
    setBusy(true)
    setError('')
    try { await action() } catch (e) { setError(e.message) } finally { setBusy(false) }
  }

  async function placeOrder() {
    setBusy(true)
    setError('')
    try {
      const order = await checkout(userId)
      // Kept so the confirmation page survives a refresh. Replace with a fetch once order retrieval (#63) exists.
      sessionStorage.setItem(`order-confirmation-${order.id}`, JSON.stringify(order))
      await refreshCart().catch(() => {})
      navigate(`/customer/orders/confirmation/${order.id}`)
    } catch (e) {
      setError(checkoutMessage(e))
    } finally {
      setBusy(false)
    }
  }

  let body
  if (!userId) {
    body = <Empty title="Sign in to see your cart" to="/login" action="Sign in">Your cart is saved to your account.</Empty>
  } else if (!loaded) {
    body = error ? null : <Loading>Fetching your cart.</Loading>
  } else if (lines.length === 0) {
    body = (
      <Empty title="Your cart is empty" to="/customer" action="Browse restaurants">
        Add something from a restaurant menu and it will show up here.
      </Empty>
    )
  } else if (menu.error) {
    body = <ErrorState error={menu.error} onRetry={menu.reload} />
  } else if (menu.loading) {
    body = <Loading>Fetching prices.</Loading>
  } else {
    body = (
      <div className="parts-grid">
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow">Items</span>
          <ul>
            {lines.map((l) => (
              <li className="step" key={l.item_id}>
                <div className="stack" style={{ '--stack': 'var(--s-2)' }}>
                  <p>{l.menuItem?.name ?? `Item ${l.item_id}`}</p>
                  {l.menuItem
                    ? <p className="small muted num">{formatPrice(l.unitCents / 100)} each</p>
                    : <p className="small">This item is no longer on the menu.</p>}
                  {l.menuItem?.availability === false && <p className="small">Currently unavailable.</p>}
                  <div className="qty">
                    <button className="btn btn--sm btn--ghost" type="button" disabled={busy} aria-label="Remove one" onClick={() => run(() => setQuantity(l.item_id, l.quantity - 1))}>-</button>
                    <span className="num" aria-live="polite">{l.quantity}</span>
                    <button className="btn btn--sm btn--ghost" type="button" disabled={busy} aria-label="Add one" onClick={() => run(() => setQuantity(l.item_id, l.quantity + 1))}>+</button>
                  </div>
                </div>
                <p className="work__price num">{formatPrice(l.lineCents / 100)}</p>
              </li>
            ))}
          </ul>
          <div className="step">
            <span className="eyebrow">Subtotal</span>
            <p className="work__price num">{formatPrice(totalCents / 100)}</p>
          </div>
          <div className="step small">
            <div className="step">
              <span>GST (5%)</span>
              <p className="num">{formatPrice((totalCents * 0.05) / 100)}</p>
            </div>
            <div className="step">
              <span>PST (7%)</span>
              <p className="num">{formatPrice((totalCents * 0.07) / 100)}</p>
            </div>
            <div className="step">
              <span>Service charge (10%)</span>
              <p className="num">{formatPrice((totalCents * 0.10) / 100)}</p>
            </div>
          </div>
          <div className="step">
            <span className="eyebrow">Total</span>
            <p className="work__price num">{formatPrice((totalCents * 1.22) / 100)}</p>
          </div>
          <div className="btn-row btn-row--tight">
            <Link className="btn btn--ghost btn--sm" to={`/customer/restaurants/${restaurantId}`}>Add more</Link>
            <button className="btn btn--ghost btn--sm" type="button" disabled={busy} onClick={() => run(emptyCart)}>Empty cart</button>
          </div>
        </div>

        <div className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }}>
          <span className="eyebrow">Delivery</span>
          {user && (
            <div className="stack" style={{ '--stack': 'var(--s-2)' }}>
              <p>{`${user.firstname} ${user.lastname}`.trim()}</p>
              <p className="small muted">{address ? `${user.address.street}, ${user.address.city}` : 'No delivery address on file.'}</p>
              <p className="small muted num">{user.phone || 'No phone number on file'}</p>
            </div>
          )}
          <p className="small muted">
            Delivery details come from your account. <Link className="link" to="/customer/account">Edit them</Link>
          </p>
          {user && !address && <p className="small" role="alert">Add a delivery address to your account before ordering.</p>}
          {problem && <p className="small" role="alert">Remove unavailable items to continue.</p>}
          <div className="btn-row">
            <button className="btn" type="button" onClick={placeOrder} disabled={busy || problem || !address}>
              {busy ? 'Working...' : 'Place order'}
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <section className="section mode-paper">
      <title>Cart | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Your cart</span>
          <h1 className="h2">{restaurant.data?.name ?? 'Checkout'}</h1>
        </div>
        {error && <ErrorState error={{ message: error }} />}
        {body}
      </div>
    </section>
  )
}