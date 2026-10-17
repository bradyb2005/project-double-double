// All backend calls go through here. In dev, Vite proxies /api to the FastAPI server.
const BASE = import.meta.env.VITE_API_URL ?? '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

// FastAPI sends {detail: "text"} for HTTPException and {detail: [{loc, msg}]} for 422.
function detailMessage(body, fallback) {
  const d = body?.detail
  if (typeof d === 'string') return d
  if (Array.isArray(d)) return d.map((e) => e.msg).join('. ')
  return fallback
}

async function request(path, options) {
  let res
  try {
    res = await fetch(`${BASE}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch {
    throw new ApiError('Cannot reach the server. Is the backend running?', 0)
  }
  const body = await res.json().catch(() => null)
  if (res.status >= 500) throw new ApiError('The server hit an error and could not save that. Try again later.', res.status)
  if (!res.ok) throw new ApiError(detailMessage(body, `Request failed (${res.status})`), res.status)
  return body
}

export const getRestaurants = () => request('/restaurants')
export const getRestaurant = (id) => request(`/restaurants/${id}`)
export const getMenu = (id) => request(`/restaurants/${id}/menu`)
export const createRestaurant = (data) =>
  request('/restaurants', { method: 'POST', body: JSON.stringify(data) })
// Every service-level error here, validation included, comes back as 404 with a readable detail. Show it as is.
// Returns the full updated restaurant.
export const updateRestaurant = (id, data) =>
  request(`/restaurants/update/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const createMenuItem = (id, data) =>
  request(`/restaurants/${id}/menu`, { method: 'POST', body: JSON.stringify(data) })
// The PUT response holds only the fields that were sent, so callers should refetch the menu.
export const updateMenuItem = (id, itemId, data) =>
  request(`/restaurants/${id}/menu/${itemId}`, { method: 'PUT', body: JSON.stringify(data) })

export const MENU_CATEGORIES = [
  'Starters', 'Pizza', 'Pasta', 'Mains', 'Vegetarian', 'Dim Sum', 'Rolls', 'Nigiri',
  'Burgers', 'Sides', 'Bread', 'Tacos', 'Burritos', 'Dessert', 'Drinks',
]

const money = new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' })
export const formatPrice = (n) => money.format(n)

// The backend default of 0 means nobody has rated the restaurant. rating is a number (older data used strings).
export const hasRating = (r) => r != null && r !== '' && Number(r) > 0
export const formatRating = (r) => (hasRating(r) ? `${Number(r).toFixed(1)} of 5` : 'Not rated yet')
