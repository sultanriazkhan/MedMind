import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Menu, Bell, User, Settings, LogOut, Sun, Moon,
  Search, ChevronDown, Heart, Activity, FileText
} from 'lucide-react'
import { toast } from 'sonner'
import { useAuthStore } from '../../stores/authStore'
import { useThemeStore } from '../../stores/themeStore'

const Header = ({ toggleSidebar }) => {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const { isDarkMode, toggleTheme } = useThemeStore()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [notifications, setNotifications] = useState([
    { id: 1, title: 'Report Analysis Complete', message: 'Your blood test results are ready', time: '5 min ago', read: false },
    { id: 2, title: 'AI Recommendation', message: 'New diet plan available', time: '1 hour ago', read: false },
    { id: 3, title: 'Health Tip', message: 'Remember to stay hydrated', time: '2 hours ago', read: true },
  ])
  const [showNotifications, setShowNotifications] = useState(false)

  const unreadCount = notifications.filter(n => !n.read).length

  const handleLogout = async () => {
    await logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const markAsRead = (id) => {
    setNotifications(notifications.map(n => 
      n.id === id ? { ...n, read: true } : n
    ))
  }

  const markAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })))
    toast.success('All notifications marked as read')
  }

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest('.user-menu') && !e.target.closest('.notifications-menu')) {
        setShowUserMenu(false)
        setShowNotifications(false)
      }
    }
    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [])

  return (
    <header className="fixed top-0 right-0 left-0 lg:left-[280px] z-30 glass-card rounded-none rounded-b-2xl">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="lg:hidden p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <Menu className="w-5 h-5 text-white" />
          </button>
          <div className="hidden lg:flex items-center gap-2">
            <div className="gradient-bg w-8 h-8 rounded-lg flex items-center justify-center">
              <Heart className="w-4 h-4 text-white" />
            </div>
            <h1 className="text-xl font-bold text-white">MediScan AI</h1>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative notifications-menu">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <Bell className="w-5 h-5 text-white/60" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-white text-xs flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            <AnimatePresence>
              {showNotifications && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="absolute right-0 top-full mt-2 w-80 glass-card rounded-xl overflow-hidden z-50"
                >
                  <div className="flex items-center justify-between p-4 border-b border-white/10">
                    <h3 className="text-white font-semibold">Notifications</h3>
                    <button
                      onClick={markAllAsRead}
                      className="text-xs text-cyan-400 hover:text-cyan-300"
                    >
                      Mark all as read
                    </button>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {notifications.length > 0 ? (
                      notifications.map((notification) => (
                        <div
                          key={notification.id}
                          onClick={() => markAsRead(notification.id)}
                          className={`p-4 border-b border-white/10 cursor-pointer transition-colors hover:bg-white/5 ${
                            !notification.read ? 'bg-cyan-500/10' : ''
                          }`}
                        >
                          <p className="text-white text-sm font-medium">{notification.title}</p>
                          <p className="text-white/40 text-xs mt-1">{notification.message}</p>
                          <p className="text-white/30 text-xs mt-2">{notification.time}</p>
                        </div>
                      ))
                    ) : (
                      <div className="p-8 text-center">
                        <Bell className="w-12 h-12 text-white/20 mx-auto mb-3" />
                        <p className="text-white/40">No notifications</p>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            {isDarkMode ? <Sun className="w-5 h-5 text-white/60" /> : <Moon className="w-5 h-5 text-white/60" />}
          </button>

          <div className="relative user-menu">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <div className="w-8 h-8 rounded-full gradient-bg flex items-center justify-center">
                <span className="text-white text-sm font-semibold">
                  {user?.full_name?.charAt(0) || 'U'}
                </span>
              </div>
              <ChevronDown className="w-4 h-4 text-white/60" />
            </button>

            <AnimatePresence>
              {showUserMenu && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="absolute right-0 top-full mt-2 w-56 glass-card rounded-xl overflow-hidden z-50"
                >
                  <div className="p-4 border-b border-white/10">
                    <p className="text-white font-semibold">{user?.full_name || 'User'}</p>
                    <p className="text-white/40 text-sm">{user?.email || 'user@example.com'}</p>
                  </div>
                  <div className="py-2">
                    <Link to="/profile" onClick={() => setShowUserMenu(false)}>
                      <div className="flex items-center gap-3 px-4 py-2 hover:bg-white/10 transition-colors">
                        <User className="w-4 h-4 text-white/60" />
                        <span className="text-white text-sm">Profile</span>
                      </div>
                    </Link>
                    <Link to="/settings" onClick={() => setShowUserMenu(false)}>
                      <div className="flex items-center gap-3 px-4 py-2 hover:bg-white/10 transition-colors">
                        <Settings className="w-4 h-4 text-white/60" />
                        <span className="text-white text-sm">Settings</span>
                      </div>
                    </Link>
                    <hr className="border-white/10 my-2" />
                    <button
                      onClick={() => {
                        setShowUserMenu(false)
                        handleLogout()
                      }}
                      className="w-full flex items-center gap-3 px-4 py-2 hover:bg-red-500/10 transition-colors"
                    >
                      <LogOut className="w-4 h-4 text-red-400" />
                      <span className="text-red-400 text-sm">Logout</span>
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header