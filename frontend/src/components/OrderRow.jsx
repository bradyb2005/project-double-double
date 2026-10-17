import { Link } from 'react-router-dom'
import { STATUS_LABEL, formatCents, formatWhen, orderSummary } from '../demoStore'

// One order in a list. `to` makes the whole row a link; `children` are the role's action buttons.
export default function OrderRow({ order, to, title, children }) {
  const body = (
    <>
      <span className="work__idx eyebrow">{order.id}</span>
      <div className="work__body">
        <h3 className="h3 work__title">{title ?? order.restaurantName}</h3>
        <p className="small muted measure">{orderSummary(order)}</p>
        <p className="micro muted">{formatWhen(order.createdAt)}</p>
      </div>
      <div className="work__meta">
        <p className="work__price num">{formatCents(order.totalCents)}</p>
        <p className="micro">//{STATUS_LABEL[order.status]}</p>
      </div>
    </>
  )
  return (
    <li className="order-item">
      {to ? <Link className="work work--text" to={to}>{body}</Link> : <div className="work work--text">{body}</div>}
      {children && <div className="btn-row btn-row--tight order-actions">{children}</div>}
    </li>
  )
}
