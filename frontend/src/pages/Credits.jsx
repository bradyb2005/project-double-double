import { allPhotos } from '../foodImages'

export default function Credits() {
  return (
    <section className="section mode-paper">
      <title>Photo credits | Double Double</title>
      <div className="wrap stack" style={{ '--stack': 'var(--s-8)' }}>
        <div className="stack" style={{ '--stack': 'var(--s-4)' }}>
          <span className="eyebrow"><b>#1</b>Credits</span>
          <h1 className="h2">Photo credits</h1>
          <p className="measure muted">
            Placeholder food photos from Wikimedia Commons, shown in the brand duotone. They stand in until restaurants upload their own.
          </p>
        </div>
        <ul>
          {allPhotos.map((p) => (
            <li className="credits" key={p.title}>
              <a className="link" href={p.page} target="_blank" rel="noreferrer">{p.title}</a>
              <p className="small muted">{p.author} / {p.license}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
