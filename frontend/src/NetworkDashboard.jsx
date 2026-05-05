import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { io } from 'socket.io-client'
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadialBarChart, RadialBar, 
} from 'recharts'

const NetworkDashboard = () => {
  const [stats, setStats] = useState({})
  const [chartData, setChartData] = useState([])
  const [logs, setLogs] = useState([])
  const [isConnected, setIsConnected] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [intervalMs, setIntervalMs] = useState(3000)
  const socketRef = useRef()

  useEffect(() => {
    // Connect Socket.IO
    socketRef.current = io('http://localhost:8000', { path: '/socket.io', transports: ['websocket'] })
    
    socketRef.current.on('connect', () => {
      setIsConnected(true)
      socketRef.current.emit('join_stats')
    })
    
    socketRef.current.on('disconnect', () => setIsConnected(false))
    
    socketRef.current.on('network_update', (data) => {
      setStats(data)
      // Chart data: time series net io
      const time = new Date().toLocaleTimeString()
      setChartData(prev => {
        const newData = [...prev, { time, upload: data.total_bytes_sent / 1e6, download: data.total_bytes_recv / 1e6 }]
        return newData.slice(-60) // Last 60 points
      })
    })
    
    return () => socketRef.current?.disconnect()
  }, [])

  const toggleRefresh = () => {
    setAutoRefresh(!autoRefresh)
    if (socketRef.current) {
      socketRef.current.emit('toggle_refresh', !autoRefresh)
    }
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <motion.header initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
        <h1 className="text-5xl font-black bg-gradient-to-r from-white via-cyan to-green bg-clip-text text-transparent mb-2">
          VaultX Network
        </h1>
        <p className="text-xl text-muted font-mono tracking-wider">Live diagnostics • {isConnected ? '🟢 Connected' : '🔴 Disconnected'}</p>
      </motion.header>

      {/* Controls */}
      <div className="flex gap-4 mb-8">
        <motion.button 
          whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          onClick={toggleRefresh}
          className="px-6 py-2 bg-card border border-cyan/30 text-cyan font-mono rounded-xl hover:bg-cyan/5 transition-all"
        >
          {autoRefresh ? '⏸️ Pause Auto' : '▶️ Resume Auto'}
        </motion.button>
        <div className="text-sm text-muted font-mono">Interval: {intervalMs/1000}s</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
        {/* Stats Cards */}
        <motion.div className="stat-card p-8 col-span-1" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <div className="text-4xl mb-2">🟢 {stats.status || 'Loading...'}</div>
          <div className="text-3xl font-black text-cyan">{stats.cpu_percent || 0}% CPU</div>
          <div className="w-full bg-muted/20 rounded-full h-3 mt-4">
            <div className="progress-fill" style={{ width: `${stats.cpu_percent || 0}%` }} />
          </div>
        </motion.div>

        <motion.div className="stat-card p-8 col-span-1" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <div className="text-3xl font-black text-violet">{stats.memory_percent || 0}% RAM</div>
          <div className="w-full bg-muted/20 rounded-full h-3 mt-4">
            <div className="h-full bg-gradient-to-r from-violet to-purple-500 rounded-full" style={{ width: `${stats.memory_percent || 0}%` }} />
          </div>
          <div className="text-xs text-muted mt-2 font-mono">{stats.total_files || 0} files</div>
        </motion.div>

        <motion.div className="stat-card p-8 lg:col-span-1 xl:col-span-1" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <div className="text-xl font-mono">{stats.hostname || 'N/A'}</div>
          <div className="text-2xl font-black text-gold mb-1">{stats.uptime || '00:00:00'}</div>
          <div className="text-sm text-muted">{stats.local_ip || 'localhost'}</div>
        </motion.div>
      </div>

      {/* Network Chart */}
      <motion.div className="stat-card p-8 col-span-full mb-8" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.4 }}>
        <h2 className="text-xl font-bold mb-6 text-muted font-mono tracking-wide uppercase">Network Traffic (MB/s)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(200 20% 10% / 0.5)" />
            <XAxis dataKey="time" stroke="hsl(200 20% 60%)" fontSize={12} />
            <YAxis stroke="hsl(200 20% 60%)" fontSize={12} />
            <Tooltip />
            <Line type="monotone" dataKey="upload" stroke="#00c8ff" strokeWidth={3} dot={false} name="Upload" />
            <Line type="monotone" dataKey="download" stroke="#ff4466" strokeWidth={3} dot={false} name="Download" />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Logs (mock) */}
      <motion.div className="stat-card p-6" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }}>
        <h3 className="text-lg font-bold mb-4 text-muted font-mono">Recent Connections</h3>
        <div className="space-y-2">
          {logs.map((log, i) => (
            <div key={i} className="flex gap-4 text-sm p-3 bg-bg/50 rounded-lg">
              <span className="font-mono w-24">{log.time}</span>
              <span className="font-mono text-cyan">{log.ip}</span>
              <span className="px-2 py-0.5 bg-green/20 text-green text-xs rounded-full font-mono">{log.method}</span>
              <span>{log.path}</span>
              <span className="ml-auto font-mono text-green">200</span>
            </div>
          ))}
        </div>
        {logs.length === 0 && (
          <div className="text-center py-8 text-muted font-mono">No recent activity</div>
        )}
      </motion.div>
    </div>
  )
}

export default NetworkDashboard
