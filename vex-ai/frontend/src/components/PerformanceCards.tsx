import React from 'react'

export const PerformanceCards: React.FC = () => {
  const metrics = [
    { label: 'Net PnL', value: '$0.0' },
    { label: 'Win Rate', value: '0%' },
    { label: 'Drawdown', value: '0%' },
    { label: 'Execution Tax', value: 'bps 0' }
  ]
  return (
    <div className="panel" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
      {metrics.map((m) => (
        <div key={m.label} className="panel">
          <div style={{ fontSize: 12, opacity: 0.8 }}>{m.label}</div>
          <div style={{ fontSize: 20, fontWeight: 700 }}>{m.value}</div>
        </div>
      ))}
    </div>
  )
}
