import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, FileText, Activity, BarChart3, CheckCircle, 
  Loader2, Zap, Microscope, Heart, Clock, Sparkles
} from 'lucide-react'
import { toast } from 'sonner'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'

const ProcessingScreen = () => {
  const { reportId } = useParams()
  const navigate = useNavigate()
  const [currentStage, setCurrentStage] = useState(0)
  const [progress, setProgress] = useState(0)
  const [estimatedTime, setEstimatedTime] = useState(30)

  const stages = [
    { name: 'Parsing Document', icon: FileText, description: 'Reading and extracting text from your report' },
    { name: 'Extracting Tests', icon: Microscope, description: 'Identifying medical tests and values' },
    { name: 'Analyzing Results', icon: Activity, description: 'Comparing against normal ranges' },
    { name: 'Generating Insights', icon: Brain, description: 'Creating AI-powered explanations' }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 2
        const newStage = Math.floor(newProgress / 25)
        
        if (newStage !== currentStage && newStage < stages.length) {
          setCurrentStage(newStage)
          setEstimatedTime(prev => Math.max(5, prev - 8))
        }
        
        if (newProgress >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            toast.success('Analysis complete!')
            navigate(`/analysis/${reportId}`)
          }, 500)
        }
        
        return Math.min(newProgress, 100)
      })
    }, 200)

    return () => clearInterval(interval)
  }, [currentStage, reportId, navigate])

  const getStageStatus = (index) => {
    if (index < currentStage) return 'completed'
    if (index === currentStage) return 'active'
    return 'pending'
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl floating" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl floating" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-128 h-128 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-2xl relative z-10"
      >
        <Card className="p-8">
          <div className="text-center mb-8">
            <div className="relative inline-block">
              <div className="gradient-bg w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-10 h-10 text-white animate-pulse" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-cyan-400 rounded-full animate-ping" />
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">AI Analyzing Your Report</h1>
            <p className="text-white/60">Our advanced AI is processing your medical report</p>
          </div>

          <div className="mb-8">
            <div className="flex justify-between text-sm text-white/60 mb-2">
              <span>Overall Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className="gradient-bg h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>

          <div className="space-y-4 mb-8">
            {stages.map((stage, index) => {
              const status = getStageStatus(index)
              const Icon = stage.icon
              
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`flex items-center gap-4 p-4 rounded-xl transition-all ${
                    status === 'active' ? 'bg-cyan-500/10 border border-cyan-500/20' : 'bg-white/5'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                    status === 'completed' ? 'gradient-bg' :
                    status === 'active' ? 'bg-cyan-500/20 animate-pulse' : 'bg-white/10'
                  }`}>
                    {status === 'completed' ? (
                      <CheckCircle className="w-5 h-5 text-white" />
                    ) : (
                      <Icon className={`w-5 h-5 ${status === 'active' ? 'text-cyan-400' : 'text-white/40'}`} />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className={`font-semibold ${
                        status === 'active' ? 'text-cyan-400' : 
                        status === 'completed' ? 'text-white' : 'text-white/40'
                      }`}>
                        {stage.name}
                      </h3>
                      {status === 'active' && (
                        <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
                      )}
                    </div>
                    <p className={`text-sm ${
                      status === 'active' ? 'text-white/70' : 'text-white/40'
                    }`}>
                      {stage.description}
                    </p>
                  </div>
                </motion.div>
              )
            })}
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-white/10">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-white/40" />
              <span className="text-white/40 text-sm">Estimated time: {estimatedTime}s</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />
              <span className="text-white/60 text-sm">AI Processing</span>
            </div>
          </div>
        </Card>

        <div className="mt-6 text-center">
          <p className="text-white/40 text-sm">
            Please don't close or refresh this page while processing
          </p>
        </div>
      </motion.div>
    </div>
  )
}

export default ProcessingScreen