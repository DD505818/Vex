import React from 'react'

export const PositionsOrders: React.FC = () => {
  return (
    <div className="panel">
      <div style={{ fontWeight: 600 }}>Positions & Orders</div>
      <table style={{ width: '100%', marginTop: 8 }}>
        <thead>
          <tr><th>Symbol</th><th>Side</th><th>Size</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr><td colSpan={4} style={{ textAlign: 'center', opacity: 0.6 }}>No positions</td></tr>
        </tbody>
      </table>
    </div>
  )
}
