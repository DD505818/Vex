import React, { useState } from 'react'

export const QuickActions: React.FC = () => {
  const [phrase, setPhrase] = useState('')
  const armed = phrase === 'ARM LIVE'
  return (
    <div className="panel" style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
      <button>Auto Trade</button>
      <button>Chart Only</button>
      <button style={{ background: '#ef4444', color: 'white' }}>Kill Switch</button>
      <input value={phrase} onChange={(e) => setPhrase(e.target.value)} placeholder="Type ARM LIVE" />
      <button disabled={!armed}>Hold to Confirm</button>
    </div>
  )
}
