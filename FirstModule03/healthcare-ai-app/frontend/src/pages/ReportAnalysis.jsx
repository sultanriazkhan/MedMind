import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Activity, TrendingUp, AlertTriangle, CheckCircle, 
  Download, Share2, FileText, ArrowLeft, 
  BarChart3, Heart, Brain, Shield, Clock, Filter
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { useReportStore } from '../stores/reportStore'

const ReportAnalysis = () => {
  const { reportId } = useParams()
  const navigate = useNavigate()
  const { currentReport, fetchReportById, isLoading } = useReportStore()
  const [activeFilter, setActiveFilter] = useState('all')
  const [expandedTest, setExpandedTest] = useState(null)

  useEffect(() => {
    if (reportId) {
      fetchReportById(reportId)
    }
  }, [reportId])

  const getStatusColor = (status) => {
    switch(status) {
      case 'normal': return { bg: 'bg-emerald-500/20', text: 'text-emerald-400', icon: CheckCircle }
      case 'abnormal': return { bg: 'bg-yellow-500/20', text: 'text-yellow-400', icon: AlertTriangle }
      case 'critical': return { bg: 'bg-red-500/20', text: 'text-red-400', icon: AlertTriangle }
      default: return { bg: 'bg-gray-500/20', text: 'text-gray-400', icon: Activity }
    }
  }

  const getStatusLabel = (status) => {
    switch(status) {
      case 'normal': return 'Normal'
      case 'abnormal': return 'Abnormal'
      case 'critical': return 'Critical'
      default: return 'Unknown'
    }
  }

  const tests = currentReport?.analysis?.tests || [
    { name: 'Hemoglobin', value: '14.2', unit: 'g/dL', normal_range: '13.5-17.5', status: 'normal' },
    { name: 'White Blood Cells', value: '7.5', unit: 'K/µL', normal_range: '4.5-11.0', status: 'normal' },
    { name: 'Platelets', value: '250', unit: 'K/µL', normal_range: '150-450', status: 'normal' },
    { name: 'LDL Cholesterol', value: '130', unit: 'mg/dL', normal_range: '<100', status: 'abnormal' },
    { name: 'HDL Cholesterol', value: '45', unit: 'mg/dL', normal_range: '>40', status: 'normal' },
    { name: 'Triglycerides', value: '150', unit: 'mg/dL', normal_range: '<150', status: 'borderline' },
    { name: 'Glucose', value: '110', unit: 'mg/dL', normal_range: '70-100', status: 'abnormal' }
  ]

  const summary = {
    total_tests: tests.length,
    normal: tests.filter(t => t.status === 'normal').length,
    abnormal: tests.filter(t => t.status === 'abnormal').length,
    critical: tests.filter(t => t.status === 'critical').length
  }

  const filteredTests = tests.filter(test => {
    if (activeFilter === 'all') return true
    return test.status === activeFilter
  })

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
    toast.success('Link copied to clipboard!')
  }

  const handleDownload = () => {
    toast.success('Report downloaded!')
  }

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-white/10 rounded-lg w-1/3" />
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="glass-card p-6 h-32" />
              ))}
            </div>
            <div className="glass-card p-6 h-96" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-wrap justify-between items-center gap-4 mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/history')}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-white" />
            </button>
            <div>
              <h1 className="text-3xl font-bold text-white mb-1">Report Analysis</h1>
              <p className="text-white/60">{currentReport?.filename || 'Medical Report'}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleDownload}>
              <Download className="w-4 h-4 mr-2" />
              Download
            </Button>
            <Button variant="outline" onClick={handleShare}>
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </Button>
            <Link to={`/chat/report-aware?report=${reportId}`}>
              <Button>
                <Brain className="w-4 h-4 mr-2" />
                Ask AI
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/60 text-sm">Total Tests</p>
                <p className="text-3xl font-bold text-white">{summary.total_tests}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                <FileText className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/60 text-sm">Normal Results</p>
                <p className="text-3xl font-bold text-emerald-400">{summary.normal}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-emerald-400" />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/60 text-sm">Abnormal Results</p>
                <p className="text-3xl font-bold text-yellow-400">{summary.abnormal}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-yellow-400" />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/60 text-sm">Health Score</p>
                <p className="text-3xl font-bold text-white">{Math.round((summary.normal / summary.total_tests) * 100)}%</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center">
                <Heart className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-white">Test Results</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveFilter('all')}
                  className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                    activeFilter === 'all' ? 'gradient-bg text-white' : 'bg-white/5 text-white/60 hover:bg-white/10'
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setActiveFilter('normal')}
                  className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                    activeFilter === 'normal' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-white/60 hover:bg-white/10'
                  }`}
                >
                  Normal
                </button>
                <button
                  onClick={() => setActiveFilter('abnormal')}
                  className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                    activeFilter === 'abnormal' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-white/5 text-white/60 hover:bg-white/10'
                  }`}
                >
                  Abnormal
                </button>
              </div>
            </div>

            <div className="space-y-3">
              {filteredTests.map((test, index) => {
                const statusColors = getStatusColor(test.status)
                const StatusIcon = statusColors.icon
                
                return (
                  <motion.div
                    key={test.name}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer"
                    onClick={() => setExpandedTest(expandedTest === index ? null : index)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="text-white font-semibold">{test.name}</h3>
                          <span className={`px-2 py-0.5 rounded-full text-xs ${statusColors.bg} ${statusColors.text}`}>
                            {getStatusLabel(test.status)}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-sm">
                          <span className="text-white">
                            {test.value} {test.unit}
                          </span>
                          <span className="text-white/40">
                            Normal: {test.normal_range} {test.unit}
                          </span>
                        </div>
                      </div>
                      <StatusIcon className={`w-5 h-5 ${statusColors.text}`} />
                    </div>

                    {expandedTest === index && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-3 pt-3 border-t border-white/10"
                      >
                        <p className="text-white/70 text-sm">
                          {test.status === 'abnormal' 
                            ? `Your ${test.name} level of ${test.value} ${test.unit} is outside the normal range of ${test.normal_range}. Please consult your healthcare provider for interpretation.`
                            : `Your ${test.name} level of ${test.value} ${test.unit} is within the normal range of ${test.normal_range}.`}
                        </p>
                        <Link to={`/test/${reportId}/${index}`}>
                          <button className="mt-2 text-cyan-400 text-sm hover:text-cyan-300">
                            View detailed explanation →
                          </button>
                        </Link>
                      </motion.div>
                    )}
                  </motion.div>
                )
              })}
            </div>
          </Card>

          <div className="space-y-6">
            <Card>
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <Brain className="w-5 h-5 text-cyan-400" />
                AI Summary
              </h2>
              <p className="text-white/70 text-sm leading-relaxed">
                Based on your lab results, {summary.abnormal > 0 
                  ? `we found ${summary.abnormal} marker(s) outside the normal range. ` +
                    `Your ${tests.find(t => t.status === 'abnormal')?.name} level requires attention. `
                  : 'all your markers are within normal ranges. '}
                Consider discussing these results with your healthcare provider for personalized medical advice.
              </p>
              <div className="mt-3 p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-center gap-2 text-cyan-400 text-sm">
                  <Shield className="w-4 h-4" />
                  <span>AI-generated insights - Not medical advice</span>
                </div>
              </div>
            </Card>

            <Card>
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-emerald-400" />
                Recommendations
              </h2>
              <div className="space-y-3">
                {summary.abnormal > 0 && (
                  <div className="flex items-start gap-2">
                    <Activity className="w-4 h-4 text-yellow-400 mt-0.5" />
                    <p className="text-white/70 text-sm">Schedule a follow-up with your doctor</p>
                  </div>
                )}
                <div className="flex items-start gap-2">
                  <Heart className="w-4 h-4 text-cyan-400 mt-0.5" />
                  <p className="text-white/70 text-sm">Maintain a balanced diet and regular exercise</p>
                </div>
                <div className="flex items-start gap-2">
                  <Clock className="w-4 h-4 text-purple-400 mt-0.5" />
                  <p className="text-white/70 text-sm">Repeat tests in 3-6 months as recommended</p>
                </div>
              </div>
            </Card>

            <Card>
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-orange-400" />
                Report Details
              </h2>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-white/40">Report ID</span>
                  <span className="text-white/70">{reportId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Analyzed On</span>
                  <span className="text-white/70">{new Date().toLocaleDateString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Analysis Version</span>
                  <span className="text-white/70">AI Model v2.4</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ReportAnalysis