import { useId } from 'react'

// A labelled control with an error line. `as` is "input" | "select" | "textarea".
export default function Field({ label, error, hint, as: Tag = 'input', children, ...props }) {
  const id = useId()
  const msg = `${id}-msg`
  return (
    <div className="field">
      <label className="label" htmlFor={id}>{label}</label>
      <Tag
        className="input" id={id} aria-describedby={msg} aria-invalid={error ? 'true' : undefined}
        {...props}
      >
        {children}
      </Tag>
      <p className="field__msg small muted" id={msg} data-state={error ? 'error' : undefined}>
        {error || hint || ''}
      </p>
    </div>
  )
}
