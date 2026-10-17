// DEMO STORE. The backend has no cart, orders or restaurant owners yet, so all of that lives here,
// in this browser's localStorage. Pages talk to this module only, so real endpoints can replace it in one file.
//
// Order shape (the spec to hand the backend):
//   {
//     id: "DD-1001",  createdAt: ISO string,
//     restaurantId, restaurantName, restaurantAddress,       // snapshotted at checkout
//     customer: { name, phone, address },
//     lines: [{ itemId, name, unitCents, qty }],             // item ids are per restaurant
//     totalCents,                                            // sum of lines; no fees or tax yet
//     status: "placed" | "preparing" | "out_for_delivery" | "delivered" | "cancelled",
//     history: [{ status, at }],
//   }
import { useSyncExternalStore } from 'react'

const KEY = 'double-double-demo'
const EMPTY = { cart: null, orders: [], seq: 1000, managedId: null }

// Orders saved while drivers existed used "ready" and "picked_up"; both now mean out for delivery.
const LEGACY = { ready: 'out_for_delivery', picked_up: 'out_for_delivery' }

function load() {
  try {
    const saved = { ...EMPTY, ...JSON.parse(localStorage.getItem(KEY)) }
    return { ...saved, orders: saved.orders.map((o) => ({ ...o, status: LEGACY[o.status] ?? o.status })) }
  } catch {
    return { ...EMPTY }
  }
}

let state = load()
const listeners = new Set()
const notify = () => listeners.forEach((l) => l())

function commit(next) {
  state = next
  try { localStorage.setItem(KEY, JSON.stringify(next)) } catch { /* private mode: state stays in memory */ }
  notify()
}

// The storage event only fires in OTHER tabs, which is what lets the owner tab see a customer's order.
addEventListener('storage', (e) => {
  if (e.key === KEY) { state = load(); notify() }
})

const subscribe = (l) => { listeners.add(l); return () => listeners.delete(l) }
export const useDemo = () => useSyncExternalStore(subscribe, () => state)

/* ---------- money ---------- */
export const toCents = (dollars) => Math.round(Number(dollars) * 100)
const cad = new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' })
export const formatCents = (c) => cad.format(c / 100)
export const cartTotal = (cart) => (cart?.lines ?? []).reduce((s, l) => s + l.unitCents * l.qty, 0)
export const cartCount = (cart) => (cart?.lines ?? []).reduce((s, l) => s + l.qty, 0)

/* ---------- order status rules: the one place that says who may move an order where ---------- */
export const STATUS_LABEL = {
  placed: 'Placed', preparing: 'Preparing', out_for_delivery: 'Out for delivery',
  delivered: 'Delivered', cancelled: 'Cancelled',
}
export const STEPS = ['placed', 'preparing', 'out_for_delivery', 'delivered']
const TRANSITIONS = {
  placed: [
    { to: 'preparing', role: 'owner', label: 'Accept' },
    { to: 'cancelled', role: 'owner', label: 'Decline' },
    { to: 'cancelled', role: 'customer', label: 'Cancel order' },
  ],
  preparing: [{ to: 'out_for_delivery', role: 'owner', label: 'Send out for delivery' }],
  out_for_delivery: [{ to: 'delivered', role: 'owner', label: 'Mark delivered' }],
}
export const actionsFor = (order, role) => (TRANSITIONS[order.status] ?? []).filter((t) => t.role === role)

export function advanceOrder(id, to, role) {
  const order = state.orders.find((o) => o.id === id)
  if (!order || !actionsFor(order, role).some((t) => t.to === to)) throw new Error('That order cannot move there.')
  const next = {
    ...order, status: to,
    history: [...order.history, { status: to, at: new Date().toISOString() }],
  }
  commit({ ...state, orders: state.orders.map((o) => (o.id === id ? next : o)) })
  return next
}

/* ---------- cart: one restaurant at a time ---------- */
export function addToCart(restaurant, item) {
  const cart = state.cart
  if (cart?.lines.length && cart.restaurant.id !== restaurant.id) return { conflict: cart.restaurant.name }
  const base = cart ?? {
    restaurant: {
      id: restaurant.id, name: restaurant.name,
      address: `${restaurant.address}, ${restaurant.location.city}`,
    },
    lines: [],
  }
  const lines = base.lines.some((l) => l.itemId === item.id)
    ? base.lines.map((l) => (l.itemId === item.id ? { ...l, qty: l.qty + 1 } : l))
    : [...base.lines, { itemId: item.id, name: item.name, unitCents: toCents(item.price), qty: 1 }]
  commit({ ...state, cart: { ...base, lines } })
  return { ok: true }
}

export function replaceCart(restaurant, item) {
  commit({ ...state, cart: null })
  return addToCart(restaurant, item)
}

export function setQty(itemId, qty) {
  const lines = state.cart.lines.map((l) => (l.itemId === itemId ? { ...l, qty } : l)).filter((l) => l.qty > 0)
  commit({ ...state, cart: lines.length ? { ...state.cart, lines } : null })
}

export const clearCart = () => commit({ ...state, cart: null })

export function placeOrder(customer) {
  const cart = state.cart
  if (!cart?.lines.length) throw new Error('Your cart is empty.')
  const seq = state.seq + 1
  const now = new Date().toISOString()
  const order = {
    id: `DD-${seq}`, createdAt: now,
    restaurantId: cart.restaurant.id, restaurantName: cart.restaurant.name, restaurantAddress: cart.restaurant.address,
    customer, lines: cart.lines, totalCents: cartTotal(cart),
    status: 'placed', history: [{ status: 'placed', at: now }],
  }
  commit({ ...state, seq, cart: null, orders: [order, ...state.orders] })
  return order
}

/* ---------- owner's chosen restaurant (there is no ownership in the backend) ---------- */
export const setManagedRestaurant = (id) => commit({ ...state, managedId: id })

/* ---------- display helpers ---------- */
export const orderSummary = (order) => order.lines.map((l) => `${l.qty} x ${l.name}`).join(', ')
export const formatWhen = (iso) =>
  new Date(iso).toLocaleString('en-CA', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })

/* ---------- selectors ---------- */
export const isActive = (o) => !['delivered', 'cancelled'].includes(o.status)
