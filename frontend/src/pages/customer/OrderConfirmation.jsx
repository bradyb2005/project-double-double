import { Link, useParams } from 'react-router-dom'
import { formatPrice } from '../../api'
import { Empty } from '../../components/States'

const STATUS_TEXT = {
  pending: 'Pending', preparing: 'Preparing', out_for_delivery: 'Out for delivery',
  delivered: 'Delivered', cancelled: 'Cancelled',
}

// The cart page saves the checkout response here. Swap for a fetch by order id once #63 (order retrieval) exists.
function loadOrder(orderId) {
  try { return JSON.parse(sessionStorage.getItem(`order-confirmation-${orderId}`)) } catch { return null }
}

const when = (iso) =>
  new Date(iso).toLocaleString('en-CA', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })

export default function OrderConfirmation() {
  const { orderId } = useParams()
  const order = loadOrder(orderId)

  if (!order) {
    return (
      <section className="section mode-paper">
        <div className="wrap">
          <Empty title="We could not find that order" to="/customer" action="Browse restaurants">
            Order details are only available right after you place an order.
          </Empty>
        </div>
      </section>
    )
  }

  const details = order.customer_details ?? {}
  const address = details.address
  return (
    <section className="section mode-paper">
      <title>Order confirmed | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#{order.id}</b>Order confirmed</span>
          <h1 className="h2">Thanks, your order has been placed.</h1>
          <p className="small muted">
            Status: <strong>{STATUS_TEXT[order.status] ?? order.status}</strong> · Placed {when(order.created_at)}
          </p>
        </div>

        <div className="parts-grid">
          <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
            <span className="eyebrow">Items</span>
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

          <div className="stack" style={{ '--stack': 'var(--s-3)' }}>
            <span className="eyebrow">Delivery</span>
            <p>{`${details.firstname ?? ''} ${details.lastname ?? ''}`.trim()}</p>
            {address && <p className="small muted">{address.street}, {address.city}, {address.province} {address.postalcode}</p>}
            <p className="small muted num">{details.phone || 'No phone number on file'}</p>
            <div className="btn-row"><Link className="btn" to="/customer">Keep browsing</Link></div>
          </div>
        </div>
      </div>
    </section>
  )
}