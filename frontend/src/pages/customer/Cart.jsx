import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { cartTotal, clearCart, formatCents, placeOrder, setQty, useDemo } from '../../demoStore'
import DemoNote from '../../components/DemoNote'
import Field from '../../components/Field'
import { Empty } from '../../components/States'

export default function Cart() {
  const { cart } = useDemo()
  const navigate = useNavigate()
  const [values, setValues] = useState({ name: '', phone: '', address: '' })
  const [errors, setErrors] = useState({})

  const bind = (key, label) => ({
    label, value: values[key], error: errors[key],
    onChange: (e) => setValues({ ...values, [key]: e.target.value }),
  })

  function submit(e) {
    e.preventDefault()
    const found = {}
    if (!values.name.trim()) found.name = 'Name is required.'
    if (!values.address.trim()) found.address = 'Delivery address is required.'
    if (values.phone.trim() && !/^(\d{3}-\d{3}-\d{4}|\d{10})$/.test(values.phone.trim())) found.phone = 'Use 250-555-0100 or ten digits.'
    setErrors(found)
    if (Object.keys(found).length) return
    const order = placeOrder({ name: values.name.trim(), phone: values.phone.trim(), address: values.address.trim() })
    navigate(`/customer/orders/${order.id}`)
  }

  return (
    <section className="section mode-paper">
      <title>Cart | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Your cart</span>
          <h1 className="h2">{cart ? cart.restaurant.name : 'Nothing yet'}</h1>
          <DemoNote />
        </div>

        {!cart ? (
          <Empty title="Your cart is empty" to="/customer" action="Browse restaurants">
            Add something from a restaurant menu and it will show up here.
          </Empty>
        ) : (
          <div className="parts-grid">
            <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
              <span className="eyebrow">Items</span>
              <ul>
                {cart.lines.map((l) => (
                  <li className="step" key={l.itemId}>
                    <div className="stack" style={{ '--stack': 'var(--s-2)' }}>
                      <p>{l.name}</p>
                      <p className="small muted num">{formatCents(l.unitCents)} each</p>
                      <div className="qty">
                        <button className="btn btn--sm btn--ghost" type="button" aria-label={`Remove one ${l.name}`} onClick={() => setQty(l.itemId, l.qty - 1)}>-</button>
                        <span className="num" aria-live="polite">{l.qty}</span>
                        <button className="btn btn--sm btn--ghost" type="button" aria-label={`Add one ${l.name}`} onClick={() => setQty(l.itemId, l.qty + 1)}>+</button>
                      </div>
                    </div>
                    <p className="work__price num">{formatCents(l.unitCents * l.qty)}</p>
                  </li>
                ))}
              </ul>
              <div className="step">
                <span className="eyebrow">Total</span>
                <p className="work__price num">{formatCents(cartTotal(cart))}</p>
              </div>
              <div className="btn-row btn-row--tight">
                <Link className="btn btn--ghost btn--sm" to={`/customer/restaurants/${cart.restaurant.id}`}>Add more</Link>
                <button className="btn btn--ghost btn--sm" type="button" onClick={clearCart}>Empty cart</button>
              </div>
            </div>

            <form className="stack form-narrow" style={{ '--stack': 'var(--s-5)' }} onSubmit={submit} noValidate>
              <span className="eyebrow">Delivery</span>
              <Field autoComplete="name" required {...bind('name', 'Name')} />
              <Field type="tel" autoComplete="tel" placeholder="250-555-0100" {...bind('phone', 'Phone (optional)')} />
              <Field autoComplete="street-address" required {...bind('address', 'Delivery address')} />
              <div className="btn-row"><button className="btn" type="submit">Place order</button></div>
            </form>
          </div>
        )}
      </div>
    </section>
  )
}
