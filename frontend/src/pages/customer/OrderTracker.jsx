import { useParams } from 'react-router-dom'
import { STATUS_LABEL, STEPS, actionsFor, advanceOrder, formatCents, formatWhen, useDemo } from '../../demoStore'
import DemoNote from '../../components/DemoNote'
import NotFound from '../NotFound'

export default function OrderTracker() {
  const { orderId } = useParams()
  const { orders } = useDemo()
  const order = orders.find((o) => o.id === orderId)
  if (!order) return <NotFound title="Order not found" back />

  const reached = (s) => order.history.find((h) => h.status === s)
  const cancel = actionsFor(order, 'customer')[0]

  return (
    <>
      <title>{`${order.id} | Double Double`}</title>
      <section className="section mode-field">
        <div className="wrap stack" style={{ '--stack': 'var(--s-5)' }}>
          <span className="eyebrow"><b>{order.id}</b>{order.restaurantName}</span>
          <h1 className="display" aria-live="polite">{STATUS_LABEL[order.status]}</h1>
          <p className="measure">
            {order.status === 'delivered' ? 'Enjoy.' : order.status === 'cancelled' ? 'This order will not be made.' : `Delivering to ${order.customer.address}.`}
          </p>
        </div>
      </section>

      <section className="section mode-paper">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <DemoNote />
          <div className="parts-grid">
            <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
              <span className="eyebrow">Progress</span>
              <ol className="steps">
                {(order.status === 'cancelled' ? ['placed', 'cancelled'] : STEPS).map((s) => (
                  <li className="step" key={s} data-state={reached(s) ? 'done' : 'todo'}>
                    <span>{STATUS_LABEL[s]}</span>
                    <span className="small muted num">{reached(s) ? formatWhen(reached(s).at) : 'Waiting'}</span>
                  </li>
                ))}
              </ol>
              {cancel && (
                <div className="btn-row">
                  <button className="btn btn--ghost" type="button" onClick={() => advanceOrder(order.id, cancel.to, 'customer')}>{cancel.label}</button>
                </div>
              )}
            </div>
            <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
              <span className="eyebrow">Your order</span>
              <ul>
                {order.lines.map((l) => (
                  <li className="step" key={l.itemId}>
                    <span>{l.qty} x {l.name}</span>
                    <span className="num">{formatCents(l.unitCents * l.qty)}</span>
                  </li>
                ))}
                <li className="step"><span className="eyebrow">Total</span><span className="num">{formatCents(order.totalCents)}</span></li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
