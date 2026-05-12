import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, FileText, Upload, History, Heart, Activity,
  MessageCircle, Bot, BookOpen, User, Settings, LogOut,
  Apple, Dumbbell, Brain, Sparkles, Menu, X, ChevronLeft,
  ChevronRight, Newspaper, Search, Target, Shield, Zap
} from 'lucide-react'
import { useAuthStore } from '../../stores/authStore'

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const location = useLocation()
  const { logout } = useAuthStore()
  const [isCollapsed, setIsCollapsed] = useState(false)

  const menuItems = [
    { section: "Main", items: [
      { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
      { path: '/upload', icon: Upload, label: 'Upload Report' },
      { path: '/history', icon: History, label: 'Report History' },
    ]},
    { section: "Health Profile", items: [
      { path: '/onboarding', icon: Heart, label: 'Health Profile' },
      { path: '/recommendations', icon: Sparkles, label: 'Recommendations' },
      { path: '/diet-plan', icon: Apple, label: 'Diet Plan' },
      { path: '/exercise-plan', icon: Dumbbell, label: 'Exercise Plan' },
    ]},
    { section: "AI Features", items: [
      { path: '/chat', icon: MessageCircle, label: 'AI Chat' },
      { path: '/chat/report-aware', icon: Bot, label: 'Report Chat' },
    ]},
    { section: "Resources", items: [
      { path: '/blog', icon: Newspaper, label: 'Blog' },
      { path: '/blog/search', icon: Search, label: 'Search Blogs' },
    ]},
    { section: "Account", items: [
      { path: '/profile', icon: User, label: 'Profile' },
      { path: '/settings', icon: Settings, label: 'Settings' },
    ]},
  ]

  const isActive = (path) => location.pathname === path

  return (
    <>
      <motion.div
        initial={{ width: isCollapsed ? 80 : 280 }}
        animate={{ width: isCollapsed ? 80 : 280 }}
        transition={{ duration: 0.3 }}
        className="fixed left-0 top-0 h-full glass-card-dark rounded-r-2xl z-40 overflow-hidden"
        style={{ backdropFilter: 'blur(20px)' }}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b border-white/10 flex items-center justify-between">
            {!isCollapsed && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-2"
              >
                <div className="gradient-bg w-8 h-8 rounded-lg flex items-center justify-center">
                  <Heart className="w-4 h-4 text-white" />
                </div>
                <span className="text-white font-bold text-lg">MediScan AI</span>
              </motion.div>
            )}
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4 text-white" /> : <ChevronLeft className="w-4 h-4 text-white" />}
            </button>
          </div>

          <div className="flex-1 overflow-y-auto py-4 custom-scrollbar">
            {menuItems.map((section, idx) => (
              <div key={idx} className="mb-6">
                {!isCollapsed && (
                  <p className="px-4 text-xs font-semibold text-white/40 uppercase tracking-wider mb-2">
                    {section.section}
                  </p>
                )}
                {section.items.map((item) => (
                  <Link to={item.path} key={item.path}>
                    <motion.div
                      whileHover={{ x: 5 }}
                      className={`relative flex items-center gap-3 px-4 py-3 mx-2 rounded-xl transition-all duration-200 cursor-pointer group ${
                        isActive(item.path)
                          ? 'gradient-bg text-white shadow-lg'
                          : 'text-white/60 hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <item.icon className="w-5 h-5 flex-shrink-0" />
                      {!isCollapsed && (
                        <span className="text-sm font-medium">{item.label}</span>
                      )}
                      {isCollapsed && (
                        <div className="absolute left-full ml-2 px-2 py-1 bg-navy-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
                          {item.label}
                        </div>
                      )}
                    </motion.div>
                  </Link>
                ))}
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-white/10">
            <button
              onClick={() => logout()}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-400 hover:bg-red-500/10 transition-colors"
            >
              <LogOut className="w-5 h-5" />
              {!isCollapsed && <span className="text-sm font-medium">Logout</span>}
            </button>
          </div>
        </div>
      </motion.div>

      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleSidebar}
            className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          />
        )}
      </AnimatePresence>
    </>
  )
}

export default Sidebar