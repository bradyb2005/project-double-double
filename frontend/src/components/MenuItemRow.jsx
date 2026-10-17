import { formatPrice } from '../api'
import { itemPhoto } from '../foodImages'
import { plateFor } from '../plate'

// `action` is the role-specific control: Add to cart for customers, Edit for owners.
export default function MenuItemRow({ item, index, category, action }) {
  const available = item.availability !== false
  const photo = itemPhoto(item)
  return (
    <li className="work" aria-disabled={!available || undefined}>
      {photo ? (
        <div className="duo"><img src={photo} alt="" loading="lazy" /></div>
      ) : (
        <div className={`plate plate--${plateFor(category.length + item.id)}`} aria-hidden="true" />
      )}
      <span className="work__idx eyebrow">{String(index + 1).padStart(2, '0')}</span>
      <div className="work__body">
        <h4 className="h3 work__title">{item.name}</h4>
        {item.description && <p className="small muted measure">{item.description}</p>}
      </div>
      <div className="work__meta">
        <p className="work__price num">{formatPrice(item.price)}</p>
        {!available && <p className="micro">//Unavailable</p>}
        {action}
      </div>
    </li>
  )
}
