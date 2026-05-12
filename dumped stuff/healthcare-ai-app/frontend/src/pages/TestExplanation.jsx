import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ArrowLeft, Activity, AlertTriangle, CheckCircle, 
  Brain, Heart, Droplet, Wind, Thermometer, 
  Microscope, Clock, BookOpen, Share2, Download,
  ChevronDown, ChevronUp, Info, Lightbulb, Shield
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const TestExplanation = () => {
  const { reportId, testId } = useParams()
  const navigate = useNavigate()
  const [expandedSections, setExpandedSections] = useState({
    causes: true,
    recommendations: true,
    relatedTests: false
  })
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTestData()
  }, [testId])

  const loadTestData = () => {
    setTimeout(() => {
      const testData = {
        id: parseInt(testId),
        name: "LDL Cholesterol",
        fullName: "Low-Density Lipoprotein Cholesterol",
        abbreviation: "LDL-C",
        value: "130",
        unit: "mg/dL",
        normalRange: "<100",
        optimalRange: "<100",
        borderlineRange: "100-129",
        highRange: "130-159",
        veryHighRange: "≥160",
        status: "abnormal",
        category: "Lipid Panel",
        description: "LDL cholesterol is often called 'bad cholesterol' because it contributes to fatty buildup (plaque) in your arteries. This plaque can narrow arteries and increase the risk of heart attack, stroke, and peripheral artery disease.",
        interpretation: "Your LDL cholesterol level of 130 mg/dL falls in the 'high' range. This indicates an increased risk of cardiovascular disease. Lifestyle modifications and possibly medication may be recommended to lower your levels.",
        causes: [
          "Diet high in saturated fats and trans fats",
          "Lack of physical activity",
          "Excess body weight or obesity",
          "Genetics and family history",
          "Certain medical conditions (diabetes, hypothyroidism)",
          "Smoking and excessive alcohol consumption"
        ],
        symptoms: "High LDL cholesterol typically has no symptoms. It's often called a 'silent' condition that requires blood testing for detection.",
        recommendations: [
          "Reduce saturated fats found in red meat and full-fat dairy products",
          "Eat more soluble fiber from oats, beans, lentils, and fruits",
          "Increase physical activity to at least 30 minutes daily",
          "Maintain a healthy weight",
          "Consider plant sterols and stanols",
          "Quit smoking if applicable"
        ],
        foodsToEat: [
          "Oats and barley",
          "Beans and lentils",
          "Eggplants and okra",
          "Nuts (walnuts, almonds)",
          "Fatty fish (salmon, mackerel)",
          "Avocados",
          "Olive oil",
          "Berries and citrus fruits"
        ],
        foodsToAvoid: [
          "Fried foods",
          "Processed meats",
          "Baked goods (cookies, cakes)",
          "Fast food",
          "Butter and margarine",
          "Full-fat dairy",
          "Red meat"
        ],
        relatedTests: [
          { name: "HDL Cholesterol", relationship: "HDL is 'good cholesterol' that helps remove LDL from arteries" },
          { name: "Triglycerides", relationship: "Often elevated along with LDL in metabolic syndrome" },
          { name: "Total Cholesterol", relationship: "Combined measure of all cholesterol types" }
        ],
        medicalReview: "If your LDL remains high after lifestyle changes, your doctor may prescribe statins or other cholesterol-lowering medications. Regular monitoring every 3-6 months is recommended.",
        lastUpdated: "2024-01-15",
        confidence: 94
      }
      setTest(testData)
      setLoading(false)
    }, 300)
  }

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const getStatusIcon = () => {
    switch(test?.status) {
      case 'normal': return <CheckCircle className="w-8 h-8 text-emerald-400" />
      case 'abnormal': return <AlertTriangle className="w-8 h-8 text-yellow-400" />
      case 'critical': return <AlertTriangle className="w-8 h-8 text-red-400" />
      default: return <Activity className="w-8 h-8 text-cyan-400" />
    }
  }

  const getStatusColor = () => {
    switch(test?.status) {
      case 'normal': return 'from-emerald-500 to-teal-500'
      case 'abnormal': return 'from-yellow-500 to-orange-500'
      case 'critical': return 'from-red-500 to-pink-500'
      default: return 'from-cyan-500 to-blue-500'
    }
  }

  const getRiskLevel = () => {
    const value = parseInt(test?.value)
    if (value < 100) return { level: 'Optimal', color: 'text-emerald-400' }
    if (value < 130) return { level: 'Borderline High', color: 'text-yellow-400' }
    if (value < 160) return { level: 'High', color: 'text-orange-400' }
    return { level: 'Very High', color: 'text-red-400' }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-white/10 rounded-lg w-1/3" />
            <div className="glass-card p-8">
              <div className="h-8 bg-white/10 rounded-lg w-1/2 mb-4" />
              <div className="h-32 bg-white/10 rounded-lg mb-6" />
              <div className="space-y-3">
                <div className="h-4 bg-white/10 rounded-lg w-full" />
                <div className="h-4 bg-white/10 rounded-lg w-3/4" />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const risk = getRiskLevel()

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => navigate(`/analysis/${reportId}`)}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-white" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-white">{test?.name}</h1>
            <p className="text-white/60">{test?.fullName}</p>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <Card className="overflow-hidden">
            <div className={`gradient-bg bg-gradient-to-r ${getStatusColor()} p-6`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm">Test Result</p>
                  <div className="flex items-baseline gap-2">
                    <span className="text-5xl font-bold text-white">{test?.value}</span>
                    <span className="text-white/80">{test?.unit}</span>
                  </div>
                  <p className="text-white/80 text-sm mt-1">Normal Range: {test?.normalRange} {test?.unit}</p>
                </div>
                {getStatusIcon()}
              </div>
            </div>
            
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <p className="text-white/40 text-sm">Risk Level</p>
                  <p className={`text-xl font-bold ${risk.color}`}>{risk.level}</p>
                </div>
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <p className="text-white/40 text-sm">AI Confidence</p>
                  <p className="text-xl font-bold text-white">{test?.confidence}%</p>
                </div>
              </div>

              <div className="mb-6">
                <h2 className="text-xl font-semibold text-white mb-3">What This Means</h2>
                <p className="text-white/70 leading-relaxed">{test?.interpretation}</p>
              </div>

              <div className="mb-6 p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <p className="text-white/70 text-sm">{test?.description}</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <button
              onClick={() => toggleSection('causes')}
              className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors rounded-xl"
            >
              <div className="flex items-center gap-3">
                <Microscope className="w-5 h-5 text-cyan-400" />
                <h2 className="text-xl font-semibold text-white">Common Causes</h2>
              </div>
              {expandedSections.causes ? <ChevronUp className="w-5 h-5 text-white/40" /> : <ChevronDown className="w-5 h-5 text-white/40" />}
            </button>
            <AnimatePresence>
              {expandedSections.causes && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-4 pt-0 space-y-2">
                    {test?.causes.map((cause, i) => (
                      <div key={i} className="flex items-start gap-2 p-2 rounded-lg hover:bg-white/5">
                        <div className="w-2 h-2 rounded-full bg-cyan-400 mt-2" />
                        <span className="text-white/70">{cause}</span>
                      </div>
                    ))}
                    <div className="mt-3 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
                      <p className="text-white/60 text-sm">{test?.symptoms}</p>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </Card>

          <Card>
            <button
              onClick={() => toggleSection('recommendations')}
              className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors rounded-xl"
            >
              <div className="flex items-center gap-3">
                <Lightbulb className="w-5 h-5 text-yellow-400" />
                <h2 className="text-xl font-semibold text-white">Recommendations</h2>
              </div>
              {expandedSections.recommendations ? <ChevronUp className="w-5 h-5 text-white/40" /> : <ChevronDown className="w-5 h-5 text-white/40" />}
            </button>
            <AnimatePresence>
              {expandedSections.recommendations && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-4 pt-0">
                    <div className="mb-4">
                      <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                        <Activity className="w-4 h-4 text-emerald-400" />
                        Lifestyle Modifications
                      </h3>
                      <ul className="space-y-2">
                        {test?.recommendations.map((rec, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                            <span className="text-white/70">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                        <h3 className="text-emerald-400 font-semibold mb-2 flex items-center gap-2">
                          <Heart className="w-4 h-4" />
                          Foods to Eat
                        </h3>
                        <ul className="space-y-1">
                          {test?.foodsToEat.map((food, i) => (
                            <li key={i} className="text-white/60 text-sm">• {food}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20">
                        <h3 className="text-red-400 font-semibold mb-2 flex items-center gap-2">
                          <AlertTriangle className="w-4 h-4" />
                          Foods to Avoid
                        </h3>
                        <ul className="space-y-1">
                          {test?.foodsToAvoid.map((food, i) => (
                            <li key={i} className="text-white/60 text-sm">• {food}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </Card>

          <Card>
            <button
              onClick={() => toggleSection('relatedTests')}
              className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors rounded-xl"
            >
              <div className="flex items-center gap-3">
                <Activity className="w-5 h-5 text-purple-400" />
                <h2 className="text-xl font-semibold text-white">Related Tests</h2>
              </div>
              {expandedSections.relatedTests ? <ChevronUp className="w-5 h-5 text-white/40" /> : <ChevronDown className="w-5 h-5 text-white/40" />}
            </button>
            <AnimatePresence>
              {expandedSections.relatedTests && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-4 pt-0 space-y-3">
                    {test?.relatedTests.map((related, i) => (
                      <div key={i} className="p-3 rounded-xl bg-white/5">
                        <h3 className="text-white font-semibold">{related.name}</h3>
                        <p className="text-white/60 text-sm">{related.relationship}</p>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </Card>

          <Card>
            <div className="p-4">
              <div className="flex items-start gap-3 mb-4">
                <Shield className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-white font-semibold mb-1">Medical Disclaimer</h3>
                  <p className="text-white/50 text-sm">{test?.medicalReview}</p>
                </div>
              </div>
              <div className="flex items-center justify-between pt-3 border-t border-white/10">
                <div className="flex items-center gap-2 text-white/40 text-xs">
                  <Clock className="w-3 h-3" />
                  <span>Last updated: {test?.lastUpdated}</span>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                    <Download className="w-4 h-4 text-white/60" />
                  </button>
                  <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                    <Share2 className="w-4 h-4 text-white/60" />
                  </button>
                </div>
              </div>
            </div>
          </Card>

          <div className="flex gap-4 pt-4">
            <Link to={`/chat/report-aware?report=${reportId}&test=${testId}`}>
              <Button className="flex-1">
                <Brain className="w-4 h-4 mr-2" />
                Ask AI About This Result
              </Button>
            </Link>
            <Link to="/recommendations">
              <Button variant="outline" className="flex-1">
                <BookOpen className="w-4 h-4 mr-2" />
                View Lifestyle Plan
              </Button>
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default TestExplanation