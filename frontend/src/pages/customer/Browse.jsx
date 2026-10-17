import { useMemo, useState } from 'react'
import { getRestaurants } from '../../api'
import { useFetch } from '../../useFetch'
import RestaurantCard from '../../components/RestaurantCard'
import { Empty, ErrorState, Loading } from '../../components/States'

const byRating = (a, b) => Number(b.rating ?? 0) - Number(a.rating ?? 0)
const byName = (a, b) => a.name.localeCompare(b.name)

export default function Browse() {
  const { data, error, loading, reload } = useFetch(getRestaurants, [])
  const [query, setQuery] = useState('')
  const [cuisine, setCuisine] = useState('')
  const [sort, setSort] = useState('name')

  const cuisines = useMemo(
    () => [...new Set((data ?? []).map((r) => r.cuisine).filter(Boolean))].sort(),
    [data],
  )
  const shown = useMemo(() => {
    const q = query.trim().toLowerCase()
    return (data ?? [])
      .filter((r) => !cuisine || r.cuisine === cuisine)
      .filter((r) => !q || [r.name, r.cuisine, r.location.city].some((s) => s?.toLowerCase().includes(q)))
      .sort(sort === 'rating' ? byRating : byName)
  }, [data, query, cuisine, sort])

  return (
    <>
      <title>Double Double</title>
      <section className="section mode-field hero-section" id="top">
        <div className="wrap hero">
          <div className="hero__copy">
            <span className="eyebrow"><b>#0</b>Kelowna, BC</span>
            <h1 className="display">Dinner, sorted.</h1>
            <p className="measure">Pick a local kitchen, read the whole menu, and see what it costs before you decide.</p>
            <div className="btn-row">
              <a className="btn" href="#restaurants">Browse restaurants</a>
            </div>
          </div>
          <figure>
            <div className="plate plate--rings" role="img" aria-label="Concentric rings, like a plate seen from above" />
            <figcaption className="caption micro">
              <span>Fig. 1</span>
              <span>{data ? `${data.length} kitchens on the list` : 'Loading the list'}</span>
            </figcaption>
          </figure>
        </div>
      </section>

      <section className="section mode-paper" id="restaurants">
        <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
          <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
            <span className="eyebrow"><b>#1</b>Restaurants</span>
            <h2 className="h2">Who is cooking</h2>
          </div>

          {loading && <Loading>Fetching restaurants.</Loading>}
          {error && <ErrorState error={error} onRetry={reload} />}

          {data && (
            <>
              <form className="filters" role="search" onSubmit={(e) => e.preventDefault()}>
                <div className="field">
                  <label className="label" htmlFor="q">Search</label>
                  <input
                    className="input" id="q" type="search" value={query}
                    placeholder="Name, cuisine or city" onChange={(e) => setQuery(e.target.value)}
                  />
                </div>
                <div className="field">
                  <label className="label" htmlFor="cuisine">Cuisine</label>
                  <select className="input" id="cuisine" value={cuisine} onChange={(e) => setCuisine(e.target.value)}>
                    <option value="">All cuisines</option>
                    {cuisines.map((c) => <option key={c}>{c}</option>)}
                  </select>
                </div>
                <div className="field">
                  <label className="label" htmlFor="sort">Sort by</label>
                  <select className="input" id="sort" value={sort} onChange={(e) => setSort(e.target.value)}>
                    <option value="name">Name</option>
                    <option value="rating">Rating</option>
                  </select>
                </div>
              </form>

              <p className="small muted" role="status" aria-live="polite">
                Showing <span className="num">{shown.length}</span> of <span className="num">{data.length}</span>
              </p>

              {data.length === 0 ? (
                <Empty title="No restaurants yet">
                  Nobody is on the list yet. Restaurant owners can add one from their dashboard.
                </Empty>
              ) : shown.length === 0 ? (
                <Empty title="Nothing matches">Try a different search or clear the cuisine filter.</Empty>
              ) : (
                <div className="grid grid--3">
                  {shown.map((r, i) => <RestaurantCard key={r.id} restaurant={r} index={i} />)}
                </div>
              )}
            </>
          )}
        </div>
      </section>
    </>
  )
}
