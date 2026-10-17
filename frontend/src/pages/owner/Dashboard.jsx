import { Link } from 'react-router-dom'
import { getMenu } from '../../api'
import { actionsFor, advanceOrder, setManagedRestaurant, useDemo } from '../../demoStore'
import { useFetch } from '../../useFetch'
import DemoNote from '../../components/DemoNote'
import ManagedRestaurant from '../../components/ManagedRestaurant'
import OrderRow from '../../components/OrderRow'
import { Empty } from '../../components/States'

const GROUPS = [
  ['New', ['placed']],
  ['In the kitchen', ['preparing']],
  ['Out for delivery', ['out_for_delivery']],
  ['Finished', ['delivered', 'cancelled']],
]

function Queue({ restaurant }) {
  const { orders } = useDemo()
  const menu = useFetch(() => getMenu(restaurant.id), [restaurant.id])
  const mine = orders.filter((o) => o.restaurantId === restaurant.id)
  const open = mine.filter((o) => !['delivered', 'cancelled'].includes(o.status))
  const unavailable = (menu.data ?? []).filter((i) => i.availability === false).length

  return (
    <>
      <title>{`Dashboard | Double Double`}</title>
      <section className="section mode-field">
        <div className="wrap stack" style={{ '--stack': 'var(--s-7)' }}>
          <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
            <span className="eyebrow"><b>#{restaurant.id}</b>You are running</span>
            <h1 className="display">{restaurant.name}</h1>
          </div>
          <dl className="grid grid--3" style={{ gap: 'var(--s-4) var(--s-5)' }}>
            <div className="fact"><dt className="micro">Open orders</dt><dd className="h3 num">{open.length}</dd></div>
            <div className="fact"><dt className="micro">Delivered</dt><dd className="h3 num">{mine.filter((o) => o.status === 'delivered').length}</dd></div>
            <div className="fact">
              <dt className="micro">Menu items</dt>
              <dd className="h3 num">{menu.data ? menu.data.length : '-'}{unavailable ? ` (${unavailable} unavailable)` : ''}</dd>
            </div>
          </dl>
          <div className="btn-row">
            <Link className="btn" to="/owner/menu">Manage menu</Link>
            <Link className="btn btn--ghost" to="/owner/restaurant/edit">Edit details</Link>
            <button className="btn btn--ghost" type="button" onClick={() => setManagedRestaurant(null)}>Switch restaurant</button>
          </div>
        </div>
      </section>

      <section className="section mode-paper">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
            <span className="eyebrow"><b>#1</b>Orders</span>
            <h2 className="h2">Order queue</h2>
            <DemoNote />
          </div>
          {mine.length === 0 && (
            <Empty title="No orders yet">
              When a customer orders from {restaurant.name}, it appears here. Open the customer view in another tab to place one.
            </Empty>
          )}
          {GROUPS.map(([heading, statuses]) => {
            const list = mine.filter((o) => statuses.includes(o.status))
            if (!list.length) return null
            return (
              <div className="stack" style={{ '--stack': 'var(--s-4)' }} key={heading}>
                <h3 className="eyebrow">{heading} ({list.length})</h3>
                <ul className="work-list">
                  {list.map((o) => (
                    <OrderRow key={o.id} order={o} title={o.customer.name}>
                      {actionsFor(o, 'owner').map((a) => (
                        <button
                          key={a.to} className={`btn btn--sm${a.to === 'cancelled' ? ' btn--ghost' : ''}`} type="button"
                          onClick={() => advanceOrder(o.id, a.to, 'owner')}
                        >{a.label}</button>
                      ))}
                    </OrderRow>
                  ))}
                </ul>
              </div>
            )
          })}
        </div>
      </section>
    </>
  )
}

export default function Dashboard() {
  return <ManagedRestaurant>{(r) => <Queue restaurant={r} />}</ManagedRestaurant>
}
