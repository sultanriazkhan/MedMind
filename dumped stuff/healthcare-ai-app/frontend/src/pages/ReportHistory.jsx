import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function ReportHistory() {
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  
  const reports = [
    { id: 1, name: 'Complete Blood Count', date: '2024-01-15', status: 'Completed', abnormal: 2 },
    { id: 2, name: 'Lipid Panel', date: '2024-01-10', status: 'Completed', abnormal: 1 },
    { id: 3, name: 'Thyroid Function Test', date: '2024-01-05', status: 'Completed', abnormal: 0 },
    { id: 4, name: 'Liver Function Test', date: '2023-12-28', status: 'Completed', abnormal: 3 },
    { id: 5, name: 'Kidney Function Test', date: '2023-12-20', status: 'Processing', abnormal: 0 },
  ]

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)' }}>
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', padding: '15px 20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} style={{ background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 12px', cursor: 'pointer', color: 'white', fontSize: '20px' }}>☰</button>
        <h1 style={{ color: 'white', fontSize: '20px', margin: 0 }}>Report History</h1>
      </div>
      <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', overflow: 'hidden' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '3fr 2fr 2fr 2fr', padding: '15px 20px', background: 'rgba(0,188,212,0.2)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <span style={{ color: 'white', fontWeight: 'bold' }}>Report Name</span>
            <span style={{ color: 'white', fontWeight: 'bold' }}>Date</span>
            <span style={{ color: 'white', fontWeight: 'bold' }}>Status</span>
            <span style={{ color: 'white', fontWeight: 'bold' }}>Abnormal</span>
          </div>
          {reports.map((report) => (
            <div key={report.id} style={{ display: 'grid', gridTemplateColumns: '3fr 2fr 2fr 2fr', padding: '15px 20px', borderBottom: '1px solid rgba(255,255,255,0.05)', cursor: 'pointer' }} onClick={() => navigate(`/analysis/${report.id}`)}>
              <span style={{ color: 'white' }}>📄 {report.name}</span>
              <span style={{ color: 'rgba(255,255,255,0.6)' }}>{report.date}</span>
              <span style={{ color: report.status === 'Completed' ? '#10b981' : '#f59e0b' }}>{report.status}</span>
              <span style={{ color: report.abnormal > 0 ? '#ef4444' : '#10b981' }}>{report.abnormal} {report.abnormal === 1 ? 'finding' : 'findings'}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ReportHistory