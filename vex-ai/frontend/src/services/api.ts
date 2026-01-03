import axios from 'axios'

const client = axios.create({ baseURL: 'http://localhost:8000' })

export const getHealth = async () => (await client.get('/health')).data
