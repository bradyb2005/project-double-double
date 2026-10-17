import photos from './foodPhotos.json'

// The backend stores image "" for every seed item, so placeholders are matched by name here.
// A real `image` URL from the backend always wins. Anything not listed keeps its generative plate.
const ITEM_PHOTO = {
  'teen burger': 'teen-burger',
  'papa burger': 'papa-burger',
  'hand-breaded onion rings': 'onion-rings',
  'a&w root beer': 'root-beer',
  'russet thick-cut fries': 'fries',
  'tonkotsu ramen': 'tonkotsu-ramen',
  'spicy miso ramen': 'miso-ramen',
  'chicken karaage': 'karaage',
  'pork gyoza': 'gyoza',
  'donburi chicken bowl': 'chicken-bowl',
  'carne asada tacos': 'carne-asada-tacos',
  'baja fish tacos': 'fish-tacos',
  'carnitas burrito': 'carnitas-burrito',
  'chips and guacamole': 'chips-guac',
  horchata: 'horchata',
}

const RESTAURANT_PHOTO = {
  'a&w': 'teen-burger',
  'arashi ramen': 'tonkotsu-ramen',
  'cantina del centro': 'carne-asada-tacos',
}

const lookup = (table, name) => photos[table[name?.trim().toLowerCase()]]?.src ?? null

export const itemPhoto = (item) => item.image || lookup(ITEM_PHOTO, item.name)
export const restaurantPhoto = (r) => lookup(RESTAURANT_PHOTO, r.name)
export const allPhotos = Object.values(photos)
