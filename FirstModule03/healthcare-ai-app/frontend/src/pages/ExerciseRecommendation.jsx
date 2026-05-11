import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Dumbbell, Clock, Activity, Heart, AlertCircle, 
  CheckCircle, TrendingUp, Flame, Wind, Moon, Sun
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const ExerciseRecommendation = () => {
  const [schedule, setSchedule] = useState([])
  const [exerciseLibrary, setExerciseLibrary] = useState([])
  const [safetyWarnings, setSafetyWarnings] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedDay, setSelectedDay] = useState(null)

  useEffect(() => {
    loadExercisePlan()
  }, [])

  const loadExercisePlan = async () => {
    setTimeout(() => {
      setSchedule([
        {
          day: 'Monday',
          activities: [
            { type: 'Cardio', duration: '30 min', intensity: 'Medium', completed: false },
            { type: 'Strength Training', duration: '20 min', intensity: 'Medium', completed: false }
          ]
        },
        {
          day: 'Tuesday',
          activities: [
            { type: 'Yoga', duration: '20 min', intensity: 'Low', completed: false },
            { type: 'Walking', duration: '30 min', intensity: 'Low', completed: false }
          ]
        },
        {
          day: 'Wednesday',
          activities: [
            { type: 'HIIT', duration: '20 min', intensity: 'High', completed: false },
            { type: 'Core Workout', duration: '15 min', intensity: 'Medium', completed: false }
          ]
        },
        {
          day: 'Thursday',
          activities: [
            { type: 'Swimming', duration: '30 min', intensity: 'Medium', completed: false },
            { type: 'Stretching', duration: '15 min', intensity: 'Low', completed: false }
          ]
        },
        {
          day: 'Friday',
          activities: [
            { type: 'Cardio', duration: '25 min', intensity: 'Medium', completed: false },
            { type: 'Strength Training', duration: '25 min', intensity: 'Medium', completed: false }
          ]
        },
        {
          day: 'Saturday',
          activities: [
            { type: 'Outdoor Activity', duration: '45 min', intensity: 'Medium', completed: false },
            { type: 'Recovery', duration: '15 min', intensity: 'Low', completed: false }
          ]
        },
        {
          day: 'Sunday',
          activities: [
            { type: 'Rest Day', duration: '-', intensity: 'Rest', completed: false },
            { type: 'Light Stretching', duration: '10 min', intensity: 'Low', completed: false }
          ]
        }
      ])
      
      setExerciseLibrary([
        { name: 'Jumping Jacks', type: 'Cardio', benefits: 'Improves cardiovascular health', instructions: 'Stand with feet together, jump while spreading legs and raising arms' },
        { name: 'Push-ups', type: 'Strength', benefits: 'Builds upper body strength', instructions: 'Start in plank position, lower chest to ground, push back up' },
        { name: 'Squats', type: 'Strength', benefits: 'Strengthens legs and glutes', instructions: 'Stand with feet shoulder-width, lower hips back and down' },
        { name: 'Plank', type: 'Core', benefits: 'Core stability', instructions: 'Hold push-up position with elbows on ground' },
        { name: 'Lunges', type: 'Strength', benefits: 'Leg strength and balance', instructions: 'Step forward, lower hips until both knees are at 90 degrees' }
      ])
      
      setSafetyWarnings([
        'Consult your doctor before starting any exercise program',
        'Always warm up for 5-10 minutes before exercising',
        'Stay hydrated before, during, and after exercise',
        'Listen to your body and stop if you feel pain',
        'Use proper form to prevent injury'
      ])
      
      setLoading(false)
    }, 500)
  }

  const getIntensityColor = (intensity) => {
    switch(intensity) {
      case 'Low': return 'from-green-500 to-emerald-500'
      case 'Medium': return 'from-yellow-500 to-orange-500'
      case 'High': return 'from-red-500 to-pink-500'
      default: return 'from-gray-500 to-gray-600'
    }
  }

  const getIntensityIcon = (intensity) => {
    switch(intensity) {
      case 'Low': return <Wind className="w-4 h-4" />
      case 'Medium': return <Activity className="w-4 h-4" />
      case 'High': return <Flame className="w-4 h-4" />
      default: return <Heart className="w-4 h-4" />
    }
  }

  const toggleComplete = (dayIndex, activityIndex) => {
    const newSchedule = [...schedule]
    newSchedule[dayIndex].activities[activityIndex].completed = !newSchedule[dayIndex].activities[activityIndex].completed
    setSchedule(newSchedule)
    toast.success('Progress updated!')
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-white/10 rounded-lg w-1/3" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="glass-card p-6 h-64" />
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
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">AI Exercise Planner</h1>
          <p className="text-white/60">Personalized weekly workout schedule based on your health profile</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Dumbbell className="w-5 h-5 text-cyan-400" />
              Weekly Schedule
            </h2>
            <div className="space-y-3">
              {schedule.map((day, dayIndex) => (
                <motion.div
                  key={day.day}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: dayIndex * 0.05 }}
                  className="border border-white/10 rounded-xl overflow-hidden"
                >
                  <button
                    onClick={() => setSelectedDay(selectedDay === dayIndex ? null : dayIndex)}
                    className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors"
                  >
                    <span className="text-white font-semibold">{day.day}</span>
                    <span className="text-white/60 text-sm">{day.activities.length} activities</span>
                  </button>
                  {selectedDay === dayIndex && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="border-t border-white/10 p-4 space-y-3"
                    >
                      {day.activities.map((activity, activityIndex) => (
                        <div key={activityIndex} className="flex items-center justify-between p-2 rounded-lg bg-white/5">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-white font-medium">{activity.type}</span>
                              <div className={`px-2 py-0.5 rounded-full text-xs bg-gradient-to-r ${getIntensityColor(activity.intensity)} text-white`}>
                                {activity.intensity}
                              </div>
                            </div>
                            <div className="flex items-center gap-3 text-white/40 text-sm">
                              <div className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                <span>{activity.duration}</span>
                              </div>
                              <div className="flex items-center gap-1">
                                {getIntensityIcon(activity.intensity)}
                                <span>{activity.intensity} Intensity</span>
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => toggleComplete(dayIndex, activityIndex)}
                            className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
                              activity.completed
                                ? 'bg-emerald-500/20 text-emerald-400'
                                : 'bg-white/5 text-white/40 hover:bg-white/10'
                            }`}
                          >
                            <CheckCircle className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </div>
          </Card>

          <div className="space-y-6">
            <Card>
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-yellow-400" />
                Safety Warnings
              </h2>
              <ul className="space-y-2">
                {safetyWarnings.map((warning, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <AlertCircle className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5" />
                    <span className="text-white/70">{warning}</span>
                  </li>
                ))}
              </ul>
            </Card>

            <Card>
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <Dumbbell className="w-5 h-5 text-cyan-400" />
                Exercise Library
              </h2>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {exerciseLibrary.map((exercise, i) => (
                  <div key={i} className="p-3 rounded-lg bg-white/5">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-white font-medium">{exercise.name}</h4>
                      <span className="text-xs text-cyan-400">{exercise.type}</span>
                    </div>
                    <p className="text-white/50 text-xs mb-1">{exercise.benefits}</p>
                    <p className="text-white/30 text-xs">{exercise.instructions}</p>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-white font-semibold mb-1">Weekly Progress</h3>
              <p className="text-white/60 text-sm">Track your exercise completion</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-white">
                {Math.round(schedule.flatMap(d => d.activities).filter(a => a.completed).length / schedule.flatMap(d => d.activities).length * 100)}%
              </div>
              <div className="text-white/40 text-sm">Completion Rate</div>
            </div>
          </div>
          <div className="mt-4 h-2 bg-white/10 rounded-full overflow-hidden">
            <div 
              className="gradient-bg h-full rounded-full transition-all duration-500"
              style={{ width: `${schedule.flatMap(d => d.activities).filter(a => a.completed).length / schedule.flatMap(d => d.activities).length * 100}%` }}
            />
          </div>
        </Card>
      </div>
    </div>
  )
}

export default ExerciseRecommendation