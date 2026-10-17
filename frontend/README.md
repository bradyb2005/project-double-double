# Double Double frontend

React + Vite, styled with the Rubric design language (`src/rubric/`, spec in `src/rubric/DESIGN.md`).

## Run

Start the backend first (`cd backend && uvicorn app.main:app --reload`, port 8000), then:

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

In dev, Vite proxies `/api/*` to `http://127.0.0.1:8000`, so the backend needs no CORS config.
For a deployed build, set `VITE_API_URL` to the backend's URL (and add CORS middleware to the backend).

## Pages

Two roles, picked on `/`. There are no accounts yet, so either role is open to anyone.

| Route | Page | Data |
|---|---|---|
| `/customer` | Browse restaurants (search, cuisine filter, sort) | `GET /restaurants` |
| `/customer/restaurants/:id` | Restaurant and menu, add to cart | `GET /restaurants/{id}`, `GET /restaurants/{id}/menu` |
| `/customer/cart` | Cart and checkout | demo |
| `/customer/orders`, `/customer/orders/:id` | Order list and tracker | demo |
| `/owner` | Dashboard and order queue | `GET /restaurants/{id}/menu` (counts) + demo orders |
| `/owner/menu` | Menu manager | `GET /restaurants/{id}/menu` |
| `/owner/restaurants/new` | Add a restaurant | `POST /restaurants` |
| `/owner/restaurant/edit` | Edit the restaurant being run | `PUT /restaurants/update/{id}` |
| `/owner/restaurants/:id/menu/new` | Add a menu item | `POST /restaurants/{id}/menu` |
| `/owner/restaurants/:id/menu/:itemId/edit` | Edit a menu item | `PUT /restaurants/{id}/menu/{itemId}` |
| `/credits` | Photo credits | |

"Demo" means `src/demoStore.js`: the backend has no cart, orders or restaurant owners yet, so those live in this browser's
localStorage. The comment at the top of that file is the order shape to ask the backend for.

## Styling rules

Use only Rubric classes and tokens. Page-specific additions live in `src/app.css` and use tokens only.
`data-contrast="aa"` is set on `<html>` in `index.html` because this is a product people read at length.
