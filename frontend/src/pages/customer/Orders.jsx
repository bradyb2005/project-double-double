import { isActive, useDemo } from '../../demoStore'
import DemoNote from '../../components/DemoNote'
import OrderRow from '../../components/OrderRow'
import { Empty } from '../../components/States'

export default function Orders() {
  const { orders } = useDemo()
  const groups = [
    ['#1 In progress', orders.filter(isActive)],
    ['#2 Past orders', orders.filter((o) => !isActive(o))],
  ].filter(([, list]) => list.length)

  return (
    <section className="section mode-paper">
      <title>Orders | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Orders</span>
          <h1 className="h2">Your orders</h1>
          <DemoNote />
        </div>
        {orders.length === 0 && (
          <Empty title="No orders yet" to="/customer" action="Browse restaurants">Place an order and you can follow it here.</Empty>
        )}
        {groups.map(([heading, list]) => (
          <div className="stack" style={{ '--stack': 'var(--s-4)' }} key={heading}>
            <h2 className="eyebrow">{heading}</h2>
            <ul className="work-list">
              {list.map((o) => <OrderRow key={o.id} order={o} to={`/customer/orders/${o.id}`} />)}
            </ul>
          </div>
        ))}
      </div>
    </section>
  )
}
