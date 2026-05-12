import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ToggleLeft, ToggleRight, FileText, X, Activity, 
  TrendingUp, AlertTriangle, CheckCircle, Brain 
} from 'lucide-react'
import HealthAIChat from './HealthAIChat'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { useReportStore } from '../stores/reportStore'
import { useChatStore } from '../stores/chatStore'

const ReportAwareChat = () => {
  const [contextEnabled, setContextEnabled] = useState(false)
  const [selectedReport, setSelectedReport] = useState(null)
  const { reports, fetchReports } = useReportStore()
  const { setReportContext } = useChatStore()
  
  useEffect(() => {
    fetchReports()
  }, [])
  
  const handleToggleContext = () => {
    const newState = !contextEnabled
    setContextEnabled(newState)
    setReportContext(newState ? selectedReport : null)
  }
  
  const handleSelectReport = (report) => {
    setSelectedReport(report)
    if (contextEnabled) {
      setReportContext(report)
    }
  }
  
  const getAbnormalitySummary = (report) => {
    if (!report.analysis) return { total: 0, abnormal: 0, critical: 0 }
    const tests = report.analysis.tests || []
    const abnormal = tests.filter(t => t.status === 'abnormal').length
    const critical = tests.filter(t => t.status === 'critical').length
    return { total: tests.length, abnormal, critical }
  }
  
  return (
    <div className="h-screen flex">
      <div className="w-80 glass-card m-4 rounded-2xl overflow-hidden flex flex-col">
        <div className="p-4 border-b border-white/10">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-white font-semibold">Report Context</h3>
            <button
              onClick={handleToggleContext}
              className="flex items-center gap-2"
            >
              {contextEnabled ? (
                <ToggleRight className="w-8 h-8 text-cyan-400" />
              ) : (
                <ToggleLeft className="w-8 h-8 text-white/40" />
              )}
              <span className={`text-sm ${contextEnabled ? 'text-cyan-400' : 'text-white/40'}`}>
                {contextEnabled ? 'ON' : 'OFF'}
              </span>
            </button>
          </div>
          
          {contextEnabled && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="space-y-3"
            >
              <p className="text-white/60 text-sm">Select a report for AI to reference:</p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {reports.map((report) => {
                  const summary = getAbnormalitySummary(report)
                  return (
                    <motion.button
                      key={report.id}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => handleSelectReport(report)}
                      className={`w-full text-left p-3 rounded-xl transition-all ${
                        selectedReport?.id === report.id
                          ? 'gradient-bg'
                          : 'glass-card hover:bg-white/10'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <FileText className="w-4 h-4 text-cyan-400" />
                        {summary.abnormal > 0 && (
                          <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-500/20 text-yellow-400">
                            {summary.abnormal} abnormal
                          </span>
                        )}
                      </div>
                      <p className="text-white text-sm font-medium mb-1 truncate">
                        {report.filename}
                      </p>
                      <p className="text-white/40 text-xs">
                        {new Date(report.created_at).toLocaleDateString()}
                      </p>
                    </motion.button>
                  )
                })}
              </div>
            </motion.div>
          )}
        </div>
        
        {selectedReport && contextEnabled && (
          <div className="p-4 bg-cyan-500/10 border-t border-cyan-500/20">
            <div className="flex items-start gap-2">
              <Activity className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-white text-sm font-medium">Active Report Context</p>
                <p className="text-white/60 text-xs truncate">{selectedReport.filename}</p>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <div className="flex-1">
        <HealthAIChat />
      </div>
    </div>
  )
}

export default ReportAwareChat