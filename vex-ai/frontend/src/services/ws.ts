const wsURL = import.meta.env.VITE_WS_URL ?? 'ws://localhost:8000/ws'

export const createSocket = () => new WebSocket(wsURL)
