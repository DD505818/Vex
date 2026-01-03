import React from 'react'

interface Props {
  mode: 'PAPER' | 'LIVE'
}

export const HeaderBar: React.FC<Props> = ({ mode }) => {
  return (
    <div className="panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ fontWeight: 700 }}>VEX AI ELITE</div>
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <span style={{ padding: '4px 10px', borderRadius: 8, background: mode === 'LIVE' ? '#ef4444' : '#10b981' }}>{mode}</span>
        <span>{new Date().toLocaleTimeString()}</span>
      </div>
    </div>
  )
}
