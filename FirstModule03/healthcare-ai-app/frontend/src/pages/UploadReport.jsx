import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

function UploadReport() {
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)' }}>
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', padding: '15px 20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} style={{ background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 12px', cursor: 'pointer', color: 'white', fontSize: '20px' }}>☰</button>
        <h1 style={{ color: 'white', fontSize: '20px', margin: 0 }}>Upload Report</h1>
      </div>
      <div style={{ padding: '40px', maxWidth: '600px', margin: '0 auto' }}>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '20px', padding: '40px', textAlign: 'center' }}>
          <div style={{ fontSize: '80px', marginBottom: '20px' }}>📄</div>
          <h2 style={{ color: 'white', marginBottom: '10px' }}>Upload Medical Report</h2>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '30px' }}>Support PDF, DOCX, TXT (Max 16MB)</p>
          <div style={{ border: '2px dashed rgba(255,255,255,0.3)', borderRadius: '15px', padding: '40px', marginBottom: '20px', cursor: 'pointer' }}>
            <p style={{ color: 'rgba(255,255,255,0.7)' }}>📁 Drag & drop or click to browse</p>
          </div>
          <button style={{ padding: '12px 30px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', border: 'none', borderRadius: '10px', color: 'white', cursor: 'pointer' }}>Select File</button>
          <div style={{ marginTop: '30px', padding: '15px', background: 'rgba(0,188,212,0.1)', borderRadius: '10px' }}>
            <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '12px' }}>🔒 Your data is encrypted and secure. HIPAA compliant.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadReport