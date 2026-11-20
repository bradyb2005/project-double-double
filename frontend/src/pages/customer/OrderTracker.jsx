import { Link, useParams } from 'react-router-dom'
import {
  ORDER_STEPS, formatOrderTime, formatPrice, getAuthenticatedUserId, getOrder, getRestaurant, orderStatusLabel,
} from '../../api'
import { useFetch } from '../../useFetch'
import { Empty, ErrorState, Loading } from '../../components/States'
import NotFound from '../NotFound'

async function loadOrder(userId, orderId) {
  if (!userId) return null
  const order = await getOrder(userId, orderId)
  const restaurant = await getRestaurant(order.restaurant_id).catch(() => null)
  return { ...order, restaurantName: restaurant?.name ?? `Restaurant ${order.restaurant_id}` }
}

const stepsFor = (order) => (order.status === 'cancelled' ? ['pending', 'cancelled'] : ORDER_STEPS)

function stepState(order, step) {
  const steps = stepsFor(order)
  const at = steps.indexOf(order.status)
  const i = steps.indexOf(step)
  if (i < at) return ['done', '']
  if (i === at) return ['now', 'Now']
  return ['todo', 'Waiting']
}

function Shell({ children }) {
  return (
    <section className="section mode-paper">
      <div className="wrap">{children}</div>
    </section>
  )
}

export default function OrderTracker() {
  const { orderId } = useParams()
  const userId = getAuthenticatedUserId()
  const { data: order, error, loading, reload } = useFetch(() => loadOrder(userId, orderId), [userId, orderId])

  if (!userId) return <Shell><Empty title="Sign in to see this order" to="/login" action="Sign in">Your orders are saved to your account.</Empty></Shell>
  if (error?.status === 404 || error?.status === 422) return <NotFound title="Order not found" back />
  if (error?.status === 401) return <Shell><Empty title="Your session has expired" to="/login" action="Sign in">Sign in again to see this order.</Empty></Shell>
  if (error) return <Shell><ErrorState error={error} onRetry={reload} /></Shell>
  if (loading || !order) return <Shell><Loading>Fetching your order.</Loading></Shell>

  const details = order.customer_details ?? {}
  const address = details.address

  return (
    <>
      <title>{`Order #${order.id} | Double Double`}</title>
      <section className="section mode-field">
        <div className="wrap stack" style={{ '--stack': 'var(--s-5)' }}>
          <span className="eyebrow"><b>#{order.id}</b>{order.restaurantName}</span>
          <h1 className="display" aria-live="polite">{orderStatusLabel(order.status)}</h1>
          <p className="measure">Placed {formatOrderTime(order.created_at)}</p>
        </div>
      </section>

      <section className="section mode-paper">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <div className="parts-grid">
            <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
              <span className="eyebrow">Your order</span>
              <ul>
                {order.items.map((item) => (
                  <li className="step" key={item.item_id}>
                    <div className="stack" style={{ '--stack': 'var(--s-2)' }}>
                      <p>{item.name}</p>
                      <p className="small muted num">{item.quantity} × {formatPrice(item.price)}</p>
                    </div>
                    <p className="work__price num">{formatPrice(item.price * item.quantity)}</p>
                  </li>
                ))}
              </ul>
              <div className="step">
                <span className="eyebrow">Total</span>
                <p className="work__price num">{formatPrice(order.total_price)}</p>
              </div>
            </div>

            <div className="stack" style={{ '--stack': 'var(--s-8)' }}>
              <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
                <span className="eyebrow">Progress</span>
                <ol className="steps">
                  {stepsFor(order).map((s) => {
                    const [state, note] = stepState(order, s)
                    return (
                      <li className="step" key={s} data-state={state}>
                        <span>{s === 'pending' ? 'Placed' : orderStatusLabel(s)}</span>
                        <span className="small muted">{note}</span>
                      </li>
                    )
                  })}
                </ol>
              </div>
              <div className="stack" style={{ '--stack': 'var(--s-3)' }}>
                <span className="eyebrow">Delivery</span>
                <p>{`${details.firstname ?? ''} ${details.lastname ?? ''}`.trim()}</p>
                {address && <p className="small muted">{address.street}, {address.city}, {address.province} {address.postalcode}</p>}
                <p className="small muted num">{details.phone || 'No phone number on file'}</p>
              </div>
            </div>
          </div>
          <div className="btn-row">
            <Link className="btn btn--ghost" to="/customer/orders">All orders</Link>
          </div>
        </div>
      </section>
    </>
  )
}
