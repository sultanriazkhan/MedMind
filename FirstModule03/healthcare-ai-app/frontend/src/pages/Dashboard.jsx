import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  FileText, Activity, Heart, Brain, TrendingUp, 
  Clock, MessageCircle, Bell, User, Settings,
  Upload, ChevronRight, Zap, Shield, Award
} from 'lucide-react'
import { toast } from 'sonner'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { useAuthStore } from '../stores/authStore'
import { useReportStore } from '../stores/reportStore'

const Dashboard = () => {
  const { user } = useAuthStore()
  const { reports, fetchReports } = useReportStore()
  const [stats, setStats] = useState({
    totalReports: 0,
    abnormalFindings: 0,
    aiSessions: 0,
    healthScore: 85
  })

  useEffect(() => {
    fetchReports()
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('/api/dashboard/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  const statsCards = [
    { icon: FileText, label: 'Reports', value: stats.totalReports, color: 'from-cyan-500 to-blue-500', link: '/history' },
    { icon: Activity, label: 'Abnormal', value: stats.abnormalFindings, color: 'from-orange-500 to-red-500', link: '/history' },
    { icon: MessageCircle, label: 'AI Chats', value: stats.aiSessions, color: 'from-purple-500 to-pink-500', link: '/chat' },
    { icon: Award, label: 'Health Score', value: `${stats.healthScore}%`, color: 'from-emerald-500 to-teal-500', link: '/recommendations' },
  ]

  const recentReports = reports.slice(0, 3)

  const quickActions = [
    { icon: Upload, label: 'Upload Report', path: '/upload', color: 'bg-cyan-500' },
    { icon: Brain, label: 'AI Assistant', path: '/chat', color: 'bg-purple-500' },
    { icon: Activity, label: 'Recommendations', path: '/recommendations', color: 'bg-emerald-500' },
    { icon: User, label: 'Health Profile', path: '/profile', color: 'bg-blue-500' },
  ]

  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Welcome back, {user?.full_name?.split(' ')[0] || 'User'}! 👋
            </h1>
            <p className="text-white/60">Here's your health overview and recent activity</p>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors relative">
              <Bell className="w-5 h-5 text-white/60" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
            </button>
            <Link to="/settings">
              <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                <Settings className="w-5 h-5 text-white/60" />
              </button>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsCards.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Link to={stat.link}>
                <Card className="hover:scale-105 transition-transform cursor-pointer">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/60 text-sm mb-1">{stat.label}</p>
                      <p className="text-3xl font-bold text-white">{stat.value}</p>
                    </div>
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center`}>
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </Card>
              </Link>
            </motion.div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <Card>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">Quick Actions</h2>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {quickActions.map((action, index) => (
                  <Link key={action.label} to={action.path}>
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.05 }}
                      className="glass-card p-4 rounded-xl text-center hover:scale-105 transition-all cursor-pointer group"
                    >
                      <div className={`w-12 h-12 rounded-xl ${action.color} flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform`}>
                        <action.icon className="w-6 h-6 text-white" />
                      </div>
                      <p className="text-white text-sm font-medium">{action.label}</p>
                    </motion.div>
                  </Link>
                ))}
              </div>
            </Card>
          </div>

          <Card>
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              Health Insights
            </h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-white/70">Profile Completion</span>
                  <span className="text-cyan-400">75%</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <div className="gradient-bg h-full rounded-full" style={{ width: '75%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-white/70">AI Recommendations Progress</span>
                  <span className="text-cyan-400">60%</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <div className="gradient-bg h-full rounded-full" style={{ width: '60%' }} />
                </div>
              </div>
              <div className="pt-2">
                <div className="flex items-center gap-2 text-sm text-white/70">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <span>Data is HIPAA compliant and secure</span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <Card>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-white">Recent Reports</h2>
              <Link to="/history" className="text-cyan-400 text-sm hover:text-cyan-300 flex items-center gap-1">
                View all <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
            {recentReports.length > 0 ? (
              <div className="space-y-3">
                {recentReports.map((report) => (
                  <Link key={report.id} to={`/analysis/${report.id}`}>
                    <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
                      <div className="flex items-center gap-3">
                        <FileText className="w-8 h-8 text-cyan-400" />
                        <div>
                          <p className="text-white font-medium">{report.filename}</p>
                          <p className="text-white/40 text-xs">{new Date(report.created_at).toLocaleDateString()}</p>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-white/40" />
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FileText className="w-12 h-12 text-white/20 mx-auto mb-3" />
                <p className="text-white/60">No reports yet</p>
                <Link to="/upload">
                  <Button size="sm" className="mt-3">Upload your first report</Button>
                </Link>
              </div>
            )}
          </Card>

          <Card>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-white">AI Recommendations</h2>
              <Link to="/recommendations" className="text-cyan-400 text-sm hover:text-cyan-300 flex items-center gap-1">
                View all <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="space-y-3">
              <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <p className="text-white text-sm">Based on your recent reports, consider increasing water intake</p>
              </div>
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <p className="text-white text-sm">Your activity level is good! Keep up the 30min daily walks</p>
              </div>
              <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20">
                <p className="text-white text-sm">Schedule a follow-up for your cholesterol results</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Dashboard