import React from 'react'

export const ChartGrid: React.FC = () => {
  return (
    <div className="panel" style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
      {[1, 2, 3, 4].map((id) => (
        <div key={id} className="panel" style={{ minHeight: 120 }}>
          <div>Chart {id}</div>
        </div>
      ))}
    </div>
  )
}
