import { useSyncExternalStore } from 'react'
import {
  addCartItem, clearServerCart, getAuthenticatedUserId, getCart, removeCartItem, updateCartItem,
} from './api'

// The customer's cart lives on the backend. This keeps the latest copy so the nav badge and the
// pages stay in step. It holds ids and quantities only; prices come from the menu.
let state = { cart: null, loaded: false }
const listeners = new Set()
const set = (cart) => { state = { cart, loaded: true }; listeners.forEach((l) => l()) }
const subscribe = (l) => { listeners.add(l); return () => listeners.delete(l) }
export const useServerCart = () => useSyncExternalStore(subscribe, () => state)

export const cartCount = (cart) => (cart?.items ?? []).reduce((sum, i) => sum + i.quantity, 0)
export const cartRestaurantId = (cart) => cart?.items?.[0]?.restaurant_id ?? null

export async function refreshCart() {
  const id = getAuthenticatedUserId()
  if (!id) { set(null); return null }
  const cart = await getCart(id)
  set(cart)
  return cart
}

function userId() {
  const id = getAuthenticatedUserId()
  if (!id) throw new Error('Sign in to use your cart.')
  return id
}

// Change the cart, then refetch it so the screen never depends on a partial response.
async function mutate(action) {
  await action(userId())
  return refreshCart()
}

export const addItem = (restaurantId, itemId, quantity = 1) =>
  mutate((id) => addCartItem(id, { item_id: itemId, restaurant_id: restaurantId, quantity }))
export const setQuantity = (itemId, quantity) =>
  mutate((id) => (quantity > 0 ? updateCartItem(id, itemId, quantity) : removeCartItem(id, itemId)))
export const emptyCart = () => mutate((id) => clearServerCart(id))