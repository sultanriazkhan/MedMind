import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Bell, Lock, Shield, Globe, Moon, Sun, Trash2, 
  Save, AlertTriangle, Mail, MessageCircle, Activity,
  Database, Eye, EyeOff, Check, X, Loader2
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import { useSettingsStore } from '../stores/settingsStore'
import { useThemeStore } from '../stores/themeStore'

const Settings = () => {
  const { isDarkMode, toggleTheme } = useThemeStore()
  const { settings, updateSettings, changePassword, isLoading } = useSettingsStore()
  const [showCurrentPassword, setShowCurrentPassword] = useState(false)
  const [showNewPassword, setShowNewPassword] = useState(false)
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState('')
  
  const handleNotificationToggle = (key) => {
    updateSettings({
      notifications: {
        ...settings.notifications,
        [key]: !settings.notifications[key]
      }
    })
  }
  
  const handlePasswordChange = async (e) => {
    e.preventDefault()
    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error('Passwords do not match')
      return
    }
    try {
      await changePassword(passwordData.current_password, passwordData.new_password)
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' })
      toast.success('Password changed successfully')
    } catch (error) {
      toast.error('Failed to change password')
    }
  }
  
  const handleDeleteAccount = () => {
    if (deleteConfirm === 'DELETE') {
      toast.error('Account deletion not implemented in demo')
      setShowDeleteModal(false)
    } else {
      toast.error('Please type DELETE to confirm')
    }
  }
  
  const notificationSections = [
    { key: 'email_alerts', label: 'Email Alerts', icon: Mail, description: 'Receive health alerts via email' },
    { key: 'push_notifications', label: 'Push Notifications', icon: Bell, description: 'Get real-time notifications' },
    { key: 'weekly_digest', label: 'Weekly Digest', icon: Activity, description: 'Weekly health summary' },
    { key: 'ai_suggestions', label: 'AI Suggestions', icon: MessageCircle, description: 'Personalized AI recommendations' },
  ]
  
  const privacySettings = [
    { key: 'data_sharing', label: 'Anonymous Data Sharing', icon: Database, description: 'Help improve AI by sharing anonymized data' },
    { key: 'two_factor', label: 'Two-Factor Authentication', icon: Shield, description: 'Add extra security to your account' },
  ]
  
  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
          <p className="text-white/60">Manage your account preferences and security</p>
        </div>
        
        <div className="space-y-6">
          <Card>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                <Bell className="w-5 h-5 text-cyan-400" />
                Notifications
              </h2>
            </div>
            <div className="space-y-4">
              {notificationSections.map((section) => (
                <div key={section.key} className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
                      <section.icon className="w-5 h-5 text-cyan-400" />
                    </div>
                    <div>
                      <p className="text-white font-medium">{section.label}</p>
                      <p className="text-white/40 text-sm">{section.description}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleNotificationToggle(section.key)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      settings.notifications?.[section.key] ? 'gradient-bg' : 'bg-white/20'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.notifications?.[section.key] ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              ))}
            </div>
          </Card>
          
          <Card>
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <Lock className="w-5 h-5 text-cyan-400" />
              Security
            </h2>
            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div className="relative">
                <Input
                  label="Current Password"
                  type={showCurrentPassword ? 'text' : 'password'}
                  value={passwordData.current_password}
                  onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                  className="absolute right-3 top-9 text-white/40 hover:text-white/60"
                >
                  {showCurrentPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              
              <div className="relative">
                <Input
                  label="New Password"
                  type={showNewPassword ? 'text' : 'password'}
                  value={passwordData.new_password}
                  onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                  required
                />
              </div>
              
              <Input
                label="Confirm New Password"
                type="password"
                value={passwordData.confirm_password}
                onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                required
              />
              
              <Button type="submit" isLoading={isLoading}>
                <Save className="w-4 h-4 mr-2" />
                Change Password
              </Button>
            </form>
          </Card>
          
          <Card>
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <Globe className="w-5 h-5 text-cyan-400" />
              Preferences
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
                    {isDarkMode ? <Moon className="w-5 h-5 text-cyan-400" /> : <Sun className="w-5 h-5 text-cyan-400" />}
                  </div>
                  <div>
                    <p className="text-white font-medium">Dark Mode</p>
                    <p className="text-white/40 text-sm">Toggle dark/light theme</p>
                  </div>
                </div>
                <button
                  onClick={toggleTheme}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    isDarkMode ? 'gradient-bg' : 'bg-white/20'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      isDarkMode ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div>
                <label className="block text-white/70 text-sm mb-2">AI Language Preference</label>
                <select className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-cyan-500">
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                  <option>German</option>
                  <option>Chinese</option>
                </select>
              </div>
            </div>
          </Card>
          
          <Card>
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <Shield className="w-5 h-5 text-cyan-400" />
              Privacy
            </h2>
            <div className="space-y-4">
              {privacySettings.map((setting) => (
                <div key={setting.key} className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
                      <setting.icon className="w-5 h-5 text-cyan-400" />
                    </div>
                    <div>
                      <p className="text-white font-medium">{setting.label}</p>
                      <p className="text-white/40 text-sm">{setting.description}</p>
                    </div>
                  </div>
                  <button
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      settings.privacy?.[setting.key] ? 'gradient-bg' : 'bg-white/20'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.privacy?.[setting.key] ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              ))}
            </div>
          </Card>
          
          <Card className="border-red-500/20">
            <h2 className="text-xl font-semibold text-red-400 mb-4 flex items-center gap-2">
              <Trash2 className="w-5 h-5" />
              Danger Zone
            </h2>
            <p className="text-white/60 mb-4 text-sm">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <Button variant="outline" onClick={() => setShowDeleteModal(true)} className="border-red-500 text-red-400 hover:bg-red-500/10">
              Delete Account
            </Button>
          </Card>
        </div>
      </div>
      
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card max-w-md w-full p-6 rounded-2xl"
          >
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle className="w-8 h-8 text-red-400" />
              <h3 className="text-xl font-bold text-white">Delete Account</h3>
            </div>
            <p className="text-white/70 mb-4">
              This action cannot be undone. This will permanently delete your account and remove all your data.
            </p>
            <p className="text-white/70 mb-4">
              Please type <span className="text-red-400 font-bold">DELETE</span> to confirm.
            </p>
            <input
              type="text"
              value={deleteConfirm}
              onChange={(e) => setDeleteConfirm(e.target.value)}
              className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white mb-4 focus:outline-none focus:border-red-500"
              placeholder="Type DELETE"
            />
            <div className="flex gap-3">
              <Button onClick={handleDeleteAccount} className="flex-1 bg-red-500 hover:bg-red-600">
                Delete Account
              </Button>
              <Button onClick={() => setShowDeleteModal(false)} variant="outline" className="flex-1">
                Cancel
              </Button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}

export default Settings