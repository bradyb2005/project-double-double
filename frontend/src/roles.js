// Which pages belong to which role. The first URL segment picks the role.
export const ROLES = {
  customer: {
    label: 'Customer',
    nav: [
      { to: '/customer', label: 'Restaurants', end: true },
      { to: '/customer/cart', label: 'Cart' },
      { to: '/customer/orders', label: 'Orders' },
    ],
  },
  owner: {
    label: 'Owner',
    nav: [
      { to: '/owner', label: 'Dashboard', end: true },
      { to: '/owner/menu', label: 'Menu' },
      { to: '/owner/restaurants/new', label: 'Add restaurant' },
    ],
  },
}

export const roleOf = (pathname) => {
  const first = pathname.split('/')[1]
  return ROLES[first] ? first : null
}
