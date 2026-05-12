import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Apple, Coffee, Sun, Moon, Download, AlertCircle, 
  CheckCircle, XCircle, Info, Utensils, Droplet, Leaf 
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { useDietStore } from '../stores/dietStore'

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const mealIcons = { breakfast: Sun, lunch: Coffee, dinner: Moon, snacks: Apple }

const DietRecommendation = () => {
  const [mealPlan, setMealPlan] = useState(null)
  const [foodsToEat, setFoodsToEat] = useState([])
  const [foodsToAvoid, setFoodsToAvoid] = useState([])
  const [rationale, setRationale] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const { fetchDietPlan } = useDietStore()
  
  useEffect(() => {
    loadDietPlan()
  }, [])
  
  const loadDietPlan = async () => {
    setIsLoading(true)
    try {
      const data = await fetchDietPlan()
      setMealPlan(data.weekly_plan)
      setFoodsToEat(data.foods_to_eat)
      setFoodsToAvoid(data.foods_to_avoid)
      setRationale(data.nutritional_rationale)
    } catch (error) {
      toast.error('Failed to load diet plan')
    } finally {
      setIsLoading(false)
    }
  }
  
  const handleDownloadPDF = () => {
    toast.success('Downloading PDF...')
  }
  
  if (isLoading) {
    return (
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-white/10 rounded-lg w-1/3" />
            <div className="grid grid-cols-7 gap-4">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="glass-card p-4 h-96" />
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }
  
  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">7-Day AI Meal Plan</h1>
            <p className="text-white/60">Personalized nutrition recommendations for your health goals</p>
          </div>
          <Button onClick={handleDownloadPDF}>
            <Download className="w-4 h-4 mr-2" />
            Download PDF
          </Button>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-emerald-400" />
              Foods to Eat
            </h2>
            <div className="flex flex-wrap gap-2">
              {foodsToEat.map((food, i) => (
                <span key={i} className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-sm">
                  {food}
                </span>
              ))}
            </div>
          </Card>
          
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <XCircle className="w-5 h-5 text-red-400" />
              Foods to Avoid
            </h2>
            <div className="flex flex-wrap gap-2">
              {foodsToAvoid.map((food, i) => (
                <span key={i} className="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm">
                  {food}
                </span>
              ))}
            </div>
          </Card>
        </div>
        
        <Card className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-3 flex items-center gap-2">
            <Info className="w-5 h-5 text-cyan-400" />
            Nutritional Rationale
          </h2>
          <p className="text-white/80 leading-relaxed">{rationale}</p>
        </Card>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-7 gap-4">
          {mealPlan && mealPlan.map((day, index) => (
            <motion.div
              key={day.day}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass-card rounded-xl overflow-hidden"
            >
              <div className="gradient-bg p-3 text-center">
                <h3 className="text-white font-semibold">{day.day}</h3>
              </div>
              <div className="p-4 space-y-3">
                {Object.entries(day.meals).map(([mealType, meal]) => {
                  const Icon = mealIcons[mealType]
                  return (
                    <div key={mealType} className="space-y-1">
                      <div className="flex items-center gap-2 text-white/70 text-sm">
                        {Icon && <Icon className="w-3 h-3" />}
                        <span className="capitalize font-medium">{mealType}</span>
                      </div>
                      <p className="text-white text-sm leading-relaxed">{meal}</p>
                    </div>
                  )
                })}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default DietRecommendation