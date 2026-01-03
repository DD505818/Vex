import React, { useEffect, useState } from 'react'
import { HeaderBar } from '../components/HeaderBar'
import { ChartGrid } from '../components/ChartGrid'
import { PerformanceCards } from '../components/PerformanceCards'
import { PositionsOrders } from '../components/PositionsOrders'
import { ExchangePanel } from '../components/ExchangePanel'
import { WalletPanel } from '../components/WalletPanel'
import { AIInsights } from '../components/AIInsights'
import { QuickActions } from '../components/QuickActions'
import { NotificationCenter } from '../components/NotificationCenter'
import { createSocket } from '../services/ws'

export const Dashboard: React.FC = () => {
  const [mode] = useState<'PAPER' | 'LIVE'>('PAPER')
  const [ticks, setTicks] = useState<any[]>([])

  useEffect(() => {
    const ws = createSocket()
    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data)
      setTicks((prev) => [...prev.slice(-10), data])
    }
    return () => ws.close()
  }, [])

  return (
    <div style={{ padding: 16, display: 'grid', gap: 12 }}>
      <HeaderBar mode={mode} />
      <QuickActions />
      <PerformanceCards />
      <ChartGrid />
      <PositionsOrders />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
        <ExchangePanel />
        <WalletPanel />
        <AIInsights />
      </div>
      <NotificationCenter />
      <div className="panel">
        <div>Recent ticks</div>
        <ul>
          {ticks.map((t, idx) => (
            <li key={idx}>{`${t.symbol} ${t.price}`}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
