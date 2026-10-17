import { Link } from 'react-router-dom'
import { formatRating } from '../api'
import { restaurantPhoto } from '../foodImages'
import { plateFor } from '../plate'


export default function RestaurantCard({ restaurant: r, index }) {
  const photo = restaurantPhoto(r)
  return (
    <Link className="feature feature--link" to={`/customer/restaurants/${r.id}`}>
      <span className="eyebrow"><b>#{index + 1}</b>{r.cuisine ?? 'Restaurant'}</span>
      <h3 className="h3">{r.name}</h3>
      <p className="small muted">
        {r.location.city}, {r.location.province}
        {' / '}
        <span className="num">{formatRating(r.rating)}</span>
      </p>
      {photo ? (
        <div className="duo"><img src={photo} alt="" width="900" height="675" loading="lazy" /></div>
      ) : (
        <div className={`plate plate--${plateFor(r.id)}`} aria-hidden="true" />
      )}
    </Link>
  )
}
