import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Redirect from './components/Redirect'
import RoleSelect from './pages/RoleSelect'
import Credits from './pages/Credits'
import NotFound from './pages/NotFound'
import Browse from './pages/customer/Browse'
import RestaurantDetail from './pages/customer/RestaurantDetail'
import Cart from './pages/customer/Cart'
import Orders from './pages/customer/Orders'
import OrderTracker from './pages/customer/OrderTracker'
import Dashboard from './pages/owner/Dashboard'
import OwnerMenu from './pages/owner/OwnerMenu'
import AddRestaurant from './pages/owner/AddRestaurant'
import EditRestaurant from './pages/owner/EditRestaurant'
import AddMenuItem from './pages/owner/AddMenuItem'
import EditMenuItem from './pages/owner/EditMenuItem'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<RoleSelect />} />

        <Route path="customer" element={<Browse />} />
        <Route path="customer/restaurants/:id" element={<RestaurantDetail />} />
        <Route path="customer/cart" element={<Cart />} />
        <Route path="customer/orders" element={<Orders />} />
        <Route path="customer/orders/:orderId" element={<OrderTracker />} />

        <Route path="owner" element={<Dashboard />} />
        <Route path="owner/menu" element={<OwnerMenu />} />
        <Route path="owner/restaurants/new" element={<AddRestaurant />} />
        <Route path="owner/restaurant/edit" element={<EditRestaurant />} />
        <Route path="owner/restaurants/:id/menu/new" element={<AddMenuItem />} />
        <Route path="owner/restaurants/:id/menu/:itemId/edit" element={<EditMenuItem />} />


        <Route path="credits" element={<Credits />} />

        {/* URLs from before roles existed */}
        <Route path="restaurants/new" element={<Redirect to="/owner/restaurants/new" />} />
        <Route path="restaurants/:id" element={<Redirect to="/customer/restaurants/:id" />} />
        <Route path="restaurants/:id/menu/new" element={<Redirect to="/owner/restaurants/:id/menu/new" />} />
        <Route path="restaurants/:id/menu/:itemId/edit" element={<Redirect to="/owner/restaurants/:id/menu/:itemId/edit" />} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
