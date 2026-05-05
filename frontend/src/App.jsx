import { motion } from 'framer-motion'
import NetworkDashboard from './NetworkDashboard.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-bg via-slate-900/50 to-slate-900 overflow-hidden relative">
      {/* Stars BG */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute w-full h-full bg-[radial-gradient(circle_at_20%_80%,rgba(0,200,255,0.3)_0%,transparent_50%)]"></div>
        <div className="absolute w-full h-full bg-[radial-gradient(circle_at_80%_20%,rgba(0,255,136,0.2)_0%,transparent_50%)]"></div>
      </div>
      
      <NetworkDashboard />
    </div>
  )
}
