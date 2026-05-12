import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  User, Mail, Calendar, FileText, MessageCircle, BookOpen, 
  Award, Activity, Heart, Settings, Edit2, Camera, 
  TrendingUp, Target, Zap, Shield, Clock, CheckCircle 
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import { useAuthStore } from '../stores/authStore'
import { useProfileStore } from '../stores/profileStore'

const UserProfile = () => {
  const { user } = useAuthStore()
  const { statistics, healthProfile, fetchStatistics, fetchHealthProfile, updateProfile } = useProfileStore()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || ''
  })
  
  useEffect(() => {
    fetchStatistics()
    fetchHealthProfile()
  }, [])
  
  const handleUpdateProfile = async () => {
    try {
      await updateProfile(formData)
      setIsEditing(false)
      toast.success('Profile updated successfully')
    } catch (error) {
      toast.error('Failed to update profile')
    }
  }
  
  const stats = [
    { icon: FileText, label: 'Reports Uploaded', value: statistics?.reports_uploaded || 0, color: 'from-cyan-500 to-blue-500' },
    { icon: MessageCircle, label: 'AI Sessions', value: statistics?.ai_sessions || 0, color: 'from-purple-500 to-pink-500' },
    { icon: BookOpen, label: 'Articles Read', value: statistics?.blogs_read || 0, color: 'from-emerald-500 to-teal-500' },
    { icon: Award, label: 'Health Score', value: statistics?.health_score || 0, color: 'from-orange-500 to-red-500' },
  ]
  
  const getHealthScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }
  
  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <Card className="text-center">
              <div className="relative inline-block">
                <div className="w-32 h-32 mx-auto rounded-full gradient-bg flex items-center justify-center text-5xl mb-4">
                  {user?.full_name?.charAt(0) || 'U'}
                </div>
                <button className="absolute bottom-0 right-8 p-2 gradient-bg rounded-full">
                  <Camera className="w-4 h-4 text-white" />
                </button>
              </div>
              {!isEditing ? (
                <>
                  <h2 className="text-2xl font-bold text-white mb-1">{user?.full_name}</h2>
                  <p className="text-white/60 mb-4">{user?.email}</p>
                  <Button onClick={() => setIsEditing(true)} variant="outline" size="sm">
                    <Edit2 className="w-4 h-4 mr-2" />
                    Edit Profile
                  </Button>
                </>
              ) : (
                <div className="space-y-4 text-left">
                  <Input
                    label="Full Name"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  />
                  <Input
                    label="Email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                  <div className="flex gap-2">
                    <Button onClick={handleUpdateProfile} size="sm">Save</Button>
                    <Button onClick={() => setIsEditing(false)} variant="outline" size="sm">Cancel</Button>
                  </div>
                </div>
              )}
            </Card>
            
            <Card>
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-cyan-400" />
                Account Security
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Email Verified</span>
                  <CheckCircle className={`w-5 h-5 ${user?.email_verified ? 'text-emerald-400' : 'text-yellow-400'}`} />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">2FA Status</span>
                  <span className="text-white/40">Disabled</span>
                </div>
                <Button variant="outline" size="sm" className="w-full">
                  Change Password
                </Button>
              </div>
            </Card>
          </div>
          
          <div className="lg:col-span-2 space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="text-center">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center mx-auto mb-3`}>
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="text-2xl font-bold text-white">{stat.value}</div>
                    <div className="text-white/60 text-sm">{stat.label}</div>
                  </Card>
                </motion.div>
              ))}
            </div>
            
            <Card>
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-white flex items-center gap-2">
                  <Heart className="w-6 h-6 text-cyan-400" />
                  Health Profile Overview
                </h3>
                <Button variant="outline" size="sm">
                  <Settings className="w-4 h-4 mr-2" />
                  Update Health Data
                </Button>
              </div>
              
              <div className="space-y-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-white/60 text-sm">Age</p>
                    <p className="text-white font-semibold text-lg">{healthProfile?.age || '-'} years</p>
                  </div>
                  <div>
                    <p className="text-white/60 text-sm">Sex</p>
                    <p className="text-white font-semibold text-lg capitalize">{healthProfile?.sex || '-'}</p>
                  </div>
                  <div>
                    <p className="text-white/60 text-sm">Weight</p>
                    <p className="text-white font-semibold text-lg">{healthProfile?.weight || '-'} kg</p>
                  </div>
                  <div>
                    <p className="text-white/60 text-sm">Height</p>
                    <p className="text-white font-semibold text-lg">{healthProfile?.height || '-'} cm</p>
                  </div>
                </div>
                
                <div>
                  <p className="text-white/60 text-sm mb-2">Activity Level</p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                      <div 
                        className="gradient-bg h-full rounded-full"
                        style={{ width: `${(healthProfile?.activity_level || 0) * 20}%` }}
                      />
                    </div>
                    <span className="text-white text-sm">{healthProfile?.activity_level || 0}/5</span>
                  </div>
                </div>
                
                {healthProfile?.conditions?.length > 0 && (
                  <div>
                    <p className="text-white/60 text-sm mb-2">Health Conditions</p>
                    <div className="flex flex-wrap gap-2">
                      {healthProfile.conditions.map(condition => (
                        <span key={condition} className="px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded-full text-xs">
                          {condition}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {healthProfile?.goals?.length > 0 && (
                  <div>
                    <p className="text-white/60 text-sm mb-2">Health Goals</p>
                    <div className="flex flex-wrap gap-2">
                      {healthProfile.goals.map(goal => (
                        <span key={goal} className="px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-xs">
                          {goal.replace('_', ' ').toUpperCase()}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Target className="w-5 h-5 text-cyan-400" />
                  Progress Overview
                </h3>
                <div className="space-y-3">
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
                      <span className="text-white/70">Health Goal Progress</span>
                      <span className="text-cyan-400">60%</span>
                    </div>
                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                      <div className="gradient-bg h-full rounded-full" style={{ width: '60%' }} />
                    </div>
                  </div>
                </div>
              </Card>
              
              <Card>
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-cyan-400" />
                  Recent Activity
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-sm">
                    <Clock className="w-4 h-4 text-white/40" />
                    <span className="text-white/70">Last report uploaded: 2 days ago</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <MessageCircle className="w-4 h-4 text-white/40" />
                    <span className="text-white/70">Last AI chat: 5 hours ago</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <BookOpen className="w-4 h-4 text-white/40" />
                    <span className="text-white/70">Read 3 articles this week</span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserProfile