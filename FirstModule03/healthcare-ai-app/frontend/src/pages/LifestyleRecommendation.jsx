import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Apple, Dumbbell, Moon, RefreshCw, Clock, TrendingUp, 
  CheckCircle, AlertCircle, Flame, Droplet, Brain, Heart 
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { useRecommendationStore } from '../stores/recommendationStore'

const tabs = [
  { id: 'diet', label: 'Diet', icon: Apple },
  { id: 'exercise', label: 'Exercise', icon: Dumbbell },
  { id: 'lifestyle', label: 'Lifestyle', icon: Moon },
]

const LifestyleRecommendation = () => {
  const [activeTab, setActiveTab] = useState('diet')
  const { recommendations, isLoading, fetchRecommendations, regenerateRecommendations } = useRecommendationStore()
  const [lastUpdated, setLastUpdated] = useState(new Date())
  
  useEffect(() => {
    fetchRecommendations()
  }, [])
  
  const handleRegenerate = async () => {
    await regenerateRecommendations()
    setLastUpdated(new Date())
    toast.success('Recommendations regenerated with AI')
  }
  
  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return 'from-red-500 to-orange-500'
      case 'medium': return 'from-yellow-500 to-orange-500'
      case 'low': return 'from-green-500 to-emerald-500'
      default: return 'from-cyan-500 to-blue-500'
    }
  }
  
  const getCategoryIcon = (category) => {
    switch(category) {
      case 'diet': return Apple
      case 'exercise': return Dumbbell
      case 'lifestyle': return Brain
      default: return Heart
    }
  }
  
  const filteredRecommendations = recommendations.filter(rec => rec.category === activeTab)
  
  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">AI Health Recommendations</h1>
            <p className="text-white/60">Personalized insights based on your health profile</p>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-white/60 text-sm">Last updated</p>
              <p className="text-white text-sm">{lastUpdated.toLocaleTimeString()}</p>
            </div>
            <Button onClick={handleRegenerate} isLoading={isLoading}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Regenerate
            </Button>
          </div>
        </div>
        
        <div className="flex gap-2 mb-8 border-b border-white/10">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                flex items-center gap-2 px-6 py-3 rounded-t-xl transition-all duration-300
                ${activeTab === tab.id 
                  ? 'gradient-bg text-white' 
                  : 'text-white/60 hover:text-white hover:bg-white/5'}
              `}
            >
              <tab.icon className="w-5 h-5" />
              {tab.label}
            </button>
          ))}
        </div>
        
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid gap-6"
          >
            {filteredRecommendations.map((rec, index) => (
              <motion.div
                key={rec.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="overflow-hidden">
                  <div className="flex items-start gap-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${getPriorityColor(rec.priority)} flex items-center justify-center flex-shrink-0`}>
                      {rec.priority === 'high' ? (
                        <AlertCircle className="w-6 h-6 text-white" />
                      ) : rec.priority === 'medium' ? (
                        <TrendingUp className="w-6 h-6 text-white" />
                      ) : (
                        <CheckCircle className="w-6 h-6 text-white" />
                      )}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-semibold text-white">{rec.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold bg-gradient-to-r ${getPriorityColor(rec.priority)}`}>
                          {rec.priority.toUpperCase()} Priority
                        </span>
                      </div>
                      <p className="text-white/70 mb-3">{rec.description}</p>
                      
                      {rec.action_items && (
                        <div className="mt-3 space-y-2">
                          {rec.action_items.map((item, i) => (
                            <div key={i} className="flex items-center gap-2 text-sm">
                              <CheckCircle className="w-4 h-4 text-emerald-400" />
                              <span className="text-white/80">{item}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="text-right">
                      <div className="flex items-center gap-1 text-white/60 text-sm">
                        <Clock className="w-4 h-4" />
                        <span>Daily</span>
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </AnimatePresence>
        
        {filteredRecommendations.length === 0 && (
          <div className="text-center py-20">
            <Brain className="w-20 h-20 text-white/20 mx-auto mb-4" />
            <p className="text-white/60 text-lg">No recommendations available for this category</p>
            <Button onClick={handleRegenerate} className="mt-4">
              Generate Recommendations
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

export default LifestyleRecommendation