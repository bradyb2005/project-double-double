import { Navigate, useParams } from 'react-router-dom'

// Old URLs (before roles) forward to their new home. `to` may use :params.
export default function Redirect({ to }) {
  const params = useParams()
  return <Navigate to={to.replace(/:(\w+)/g, (_, k) => params[k])} replace />
}
