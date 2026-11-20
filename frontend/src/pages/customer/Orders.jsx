import { Link } from 'react-router-dom'
import {
  formatOrderTime, formatPrice, getAuthenticatedUserId, getOrders, getRestaurants,
  isOrderActive, orderItemSummary, orderStatusLabel,
} from '../../api'
import { useFetch } from '../../useFetch'
import { Empty, ErrorState, Loading } from '../../components/States'

async function loadOrders(userId) {
  if (!userId) return null
  const [orders, restaurants] = await Promise.all([getOrders(userId), getRestaurants().catch(() => [])])
  const names = new Map(restaurants.map((r) => [r.id, r.name]))
  return orders.map((o) => ({ ...o, restaurantName: names.get(o.restaurant_id) ?? `Restaurant ${o.restaurant_id}` }))
}

function OrderLine({ order }) {
  return (
    <li className="order-item">
      <Link className="work work--text" to={`/customer/orders/${order.id}`}>
        <span className="work__idx eyebrow">#{order.id}</span>
        <div className="work__body">
          <h3 className="h3 work__title">{order.restaurantName}</h3>
          <p className="small muted measure">{orderItemSummary(order)}</p>
          <p className="micro muted">{formatOrderTime(order.created_at)}</p>
        </div>
        <div className="work__meta">
          <p className="work__price num">{formatPrice(order.total_price)}</p>
          <p className="micro">//{orderStatusLabel(order.status)}</p>
        </div>
      </Link>
    </li>
  )
}

export default function Orders() {
  const userId = getAuthenticatedUserId()
  const { data: orders, error, loading, reload } = useFetch(() => loadOrders(userId), [userId])

  let body
  if (!userId) {
    body = <Empty title="Sign in to see your orders" to="/login" action="Sign in">Your order history is saved to your account.</Empty>
  } else if (error?.status === 401) {
    body = <Empty title="Your session has expired" to="/login" action="Sign in">Sign in again to see your orders.</Empty>
  } else if (error) {
    body = <ErrorState error={error} onRetry={reload} />
  } else if (loading || !orders) {
    body = <Loading>Fetching your orders.</Loading>
  } else if (orders.length === 0) {
    body = <Empty title="No orders yet" to="/customer" action="Browse restaurants">Place an order and it will show up here.</Empty>
  } else {
    const groups = [
      ['In progress', orders.filter(isOrderActive)],
      ['Past orders', orders.filter((o) => !isOrderActive(o))],
    ].filter(([, list]) => list.length)
    body = groups.map(([heading, list], i) => (
      <div className="stack" style={{ '--stack': 'var(--s-4)' }} key={heading}>
        <h2 className="eyebrow"><b>#{i + 1}</b>{heading}</h2>
        <ul className="work-list">
          {list.map((o) => <OrderLine key={o.id} order={o} />)}
        </ul>
      </div>
    ))
  }

  return (
    <section className="section mode-paper">
      <title>Orders | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Orders</span>
          <h1 className="h2">Your orders</h1>
        </div>
        {body}
      </div>
    </section>
  )
}
