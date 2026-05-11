import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate, useLocation } from 'react-router-dom'
import { Toaster, toast } from 'sonner'
import { useState, useEffect } from 'react'

// Simple Login Component
function Login() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => {
      localStorage.setItem('token', 'demo-token')
      localStorage.setItem('user', JSON.stringify({ email, name: email.split('@')[0] }))
      toast.success('Login successful!')
      navigate('/dashboard')
      setLoading(false)
    }, 500)
  }

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', borderRadius: '20px', padding: '40px', width: '100%', maxWidth: '400px' }}>
        <h1 style={{ color: 'white', fontSize: '28px', marginBottom: '8px', textAlign: 'center' }}>Welcome Back</h1>
        <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '30px', textAlign: 'center' }}>Sign in to MediScan AI</p>
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '15px', borderRadius: '10px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', outline: 'none' }} required />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '20px', borderRadius: '10px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', outline: 'none' }} required />
          <button type="submit" disabled={loading} style={{ width: '100%', padding: '12px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', border: 'none', borderRadius: '10px', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>{loading ? 'Loading...' : 'Sign In'}</button>
        </form>
        <p style={{ color: 'rgba(255,255,255,0.6)', marginTop: '20px', textAlign: 'center' }}>Don't have an account? <Link to="/signup" style={{ color: '#00bcd4' }}>Sign Up</Link></p>
        <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(0,188,212,0.1)', borderRadius: '8px', textAlign: 'center' }}>
          <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '12px' }}>Demo: any email/password works</p>
        </div>
      </div>
    </div>
  )
}

// Simple SignUp Component
function SignUp() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => {
      localStorage.setItem('token', 'demo-token')
      localStorage.setItem('user', JSON.stringify({ email, name }))
      toast.success('Account created!')
      navigate('/dashboard')
      setLoading(false)
    }, 500)
  }

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', borderRadius: '20px', padding: '40px', width: '100%', maxWidth: '400px' }}>
        <h1 style={{ color: 'white', fontSize: '28px', marginBottom: '8px', textAlign: 'center' }}>Create Account</h1>
        <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '30px', textAlign: 'center' }}>Join MediScan AI</p>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '15px', borderRadius: '10px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', outline: 'none' }} required />
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '15px', borderRadius: '10px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', outline: 'none' }} required />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '20px', borderRadius: '10px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', outline: 'none' }} required />
          <button type="submit" disabled={loading} style={{ width: '100%', padding: '12px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', border: 'none', borderRadius: '10px', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>{loading ? 'Creating...' : 'Create Account'}</button>
        </form>
        <p style={{ color: 'rgba(255,255,255,0.6)', marginTop: '20px', textAlign: 'center' }}>Already have an account? <Link to="/login" style={{ color: '#00bcd4' }}>Login</Link></p>
      </div>
    </div>
  )
}

// Navigation Sidebar Component
function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/upload', label: 'Upload Report', icon: '📤' },
    { path: '/history', label: 'Report History', icon: '📋' },
    { path: '/profile', label: 'Health Profile', icon: '❤️' },
    { path: '/recommendations', label: 'Recommendations', icon: '✨' },
    { path: '/diet-plan', label: 'Diet Plan', icon: '🍎' },
    { path: '/exercise-plan', label: 'Exercise Plan', icon: '💪' },
    { path: '/chat', label: 'AI Chat', icon: '💬' },
    { path: '/blog', label: 'Blog', icon: '📰' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
  ]

  const handleNavigation = (path) => {
    navigate(path)
    if (onClose) onClose()
  }

  return (
    <>
      <div style={{
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        width: '260px',
        background: 'rgba(15, 23, 42, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRight: '1px solid rgba(255,255,255,0.1)',
        transform: isOpen ? 'translateX(0)' : 'translateX(-100%)',
        transition: 'transform 0.3s ease',
        zIndex: 1000,
        overflowY: 'auto'
      }}>
        <div style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '30px', paddingBottom: '20px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <div style={{ width: '40px', height: '40px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <span style={{ fontSize: '20px' }}>🏥</span>
            </div>
            <h2 style={{ color: 'white', fontSize: '18px', margin: 0 }}>MediScan AI</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            {menuItems.map((item) => (
              <button
                key={item.path}
                onClick={() => handleNavigation(item.path)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 15px',
                  background: location.pathname === item.path ? 'linear-gradient(135deg, #00bcd4, #10b981)' : 'transparent',
                  border: 'none',
                  borderRadius: '10px',
                  color: location.pathname === item.path ? 'white' : 'rgba(255,255,255,0.7)',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  fontSize: '14px',
                  fontWeight: location.pathname === item.path ? '600' : '400'
                }}
                onMouseEnter={(e) => { if (location.pathname !== item.path) e.currentTarget.style.background = 'rgba(255,255,255,0.1)' }}
                onMouseLeave={(e) => { if (location.pathname !== item.path) e.currentTarget.style.background = 'transparent' }}
              >
                <span style={{ fontSize: '18px' }}>{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
      {isOpen && (
        <div
          onClick={onClose}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.5)',
            zIndex: 999,
            display: 'none'
          }}
        />
      )}
    </>
  )
}

// Dashboard Component
function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    if (!token) {
      navigate('/login')
    } else if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    toast.success('Logged out')
    navigate('/login')
  }

  const cards = [
    { title: 'Total Reports', value: '12', icon: '📄', color: '#00bcd4', path: '/history' },
    { title: 'Health Score', value: '85%', icon: '❤️', color: '#10b981', path: '/profile' },
    { title: 'AI Chats', value: '8', icon: '💬', color: '#8b5cf6', path: '/chat' },
    { title: 'Recommendations', value: '5', icon: '✨', color: '#f59e0b', path: '/recommendations' },
  ]

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)' }}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      {/* Header */}
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', padding: '15px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginLeft: '0px' }}>
        <button onClick={() => setSidebarOpen(true)} style={{ background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 12px', cursor: 'pointer', color: 'white', fontSize: '20px' }}>☰</button>
        <h1 style={{ color: 'white', fontSize: '20px', margin: 0 }}>Dashboard</h1>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ color: 'white' }}>👋 {user?.name || 'User'}</span>
          <button onClick={handleLogout} style={{ background: 'rgba(239,68,68,0.2)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: '#ef4444', cursor: 'pointer' }}>Logout</button>
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: '20px', marginLeft: '0px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
          {cards.map((card) => {
            return (
              <div 
                key={card.title} 
                onClick={() => navigate(card.path)} 
                style={{ 
                  background: 'rgba(255,255,255,0.1)', 
                  borderRadius: '15px', 
                  padding: '20px', 
                  cursor: 'pointer', 
                  transition: 'transform 0.2s' 
                }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'} 
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                  <span style={{ fontSize: '30px' }}>{card.icon}</span>
                  <span style={{ fontSize: '24px', fontWeight: 'bold', color: card.color }}>{card.value}</span>
                </div>
                <h3 style={{ color: 'white', margin: 0, fontSize: '14px', opacity: 0.7 }}>{card.title}</h3>
              </div>
            )
          })}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
          <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px' }}>
            <h3 style={{ color: 'white', marginBottom: '15px' }}>Quick Actions</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <button onClick={() => navigate('/upload')} style={{ padding: '12px', background: 'rgba(0,188,212,0.2)', border: 'none', borderRadius: '10px', color: '#00bcd4', cursor: 'pointer' }}>📤 Upload New Report</button>
              <button onClick={() => navigate('/chat')} style={{ padding: '12px', background: 'rgba(139,92,246,0.2)', border: 'none', borderRadius: '10px', color: '#8b5cf6', cursor: 'pointer' }}>💬 Chat with AI</button>
              <button onClick={() => navigate('/recommendations')} style={{ padding: '12px', background: 'rgba(245,158,11,0.2)', border: 'none', borderRadius: '10px', color: '#f59e0b', cursor: 'pointer' }}>✨ View Recommendations</button>
            </div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px' }}>
            <h3 style={{ color: 'white', marginBottom: '15px' }}>Recent Activity</h3>
            <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '14px', textAlign: 'center', padding: '30px 0' }}>No recent activity</div>
          </div>
        </div>
      </div>
    </div>
  )
}
// Simple Upload Page
function UploadReport() {
  const navigate = useNavigate()
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', padding: '20px' }}>
      <div style={{ maxWidth: '600px', margin: '0 auto', background: 'rgba(255,255,255,0.1)', borderRadius: '20px', padding: '40px', textAlign: 'center' }}>
        <button onClick={() => navigate('/dashboard')} style={{ position: 'absolute', top: '20px', left: '20px', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: 'white', cursor: 'pointer' }}>← Back</button>
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Upload Medical Report</h1>
        <div style={{ border: '2px dashed rgba(255,255,255,0.3)', borderRadius: '15px', padding: '60px', marginBottom: '20px' }}>
          <span style={{ fontSize: '50px' }}>📄</span>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '10px' }}>Drag & drop your report here</p>
          <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: '12px' }}>PDF, DOCX, TXT (Max 16MB)</p>
        </div>
        <button style={{ padding: '12px 30px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', border: 'none', borderRadius: '10px', color: 'white', cursor: 'pointer' }}>Select File</button>
      </div>
    </div>
  )
}

// Simple History Page
function ReportHistory() {
  const navigate = useNavigate()
  const reports = [
    { id: 1, name: 'Blood Test Results', date: '2024-01-15', status: 'Completed' },
    { id: 2, name: 'Lipid Panel', date: '2024-01-10', status: 'Completed' },
    { id: 3, name: 'Complete Blood Count', date: '2024-01-05', status: 'Processing' },
  ]
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', padding: '20px' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <button onClick={() => navigate('/dashboard')} style={{ marginBottom: '20px', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: 'white', cursor: 'pointer' }}>← Back</button>
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Report History</h1>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', overflow: 'hidden' }}>
          {reports.map((report) => (
            <div key={report.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px 20px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
              <div><span style={{ fontSize: '20px', marginRight: '10px' }}>📄</span><span style={{ color: 'white' }}>{report.name}</span><div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '12px' }}>{report.date}</div></div>
              <span style={{ color: report.status === 'Completed' ? '#10b981' : '#f59e0b', fontSize: '12px' }}>{report.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// Simple Profile Page
function UserProfile() {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', padding: '20px' }}>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <button onClick={() => navigate('/dashboard')} style={{ marginBottom: '20px', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: 'white', cursor: 'pointer' }}>← Back</button>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '20px', padding: '40px', textAlign: 'center' }}>
          <div style={{ width: '80px', height: '80px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px', fontSize: '30px' }}>👤</div>
          <h2 style={{ color: 'white' }}>{user.name || 'User'}</h2>
          <p style={{ color: 'rgba(255,255,255,0.6)' }}>{user.email || 'user@example.com'}</p>
          <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
            <p style={{ color: 'white' }}>Health Profile</p>
            <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '14px' }}>Complete your health profile for personalized recommendations</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// Simple Settings Page
function Settings() {
  const navigate = useNavigate()
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', padding: '20px' }}>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <button onClick={() => navigate('/dashboard')} style={{ marginBottom: '20px', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: 'white', cursor: 'pointer' }}>← Back</button>
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Settings</h1>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px 0', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <span style={{ color: 'white' }}>🔔 Email Notifications</span>
            <label style={{ position: 'relative', display: 'inline-block', width: '50px', height: '24px' }}><input type="checkbox" style={{ opacity: 0, width: 0, height: 0 }} /><span style={{ position: 'absolute', cursor: 'pointer', top: 0, left: 0, right: 0, bottom: 0, background: '#ccc', borderRadius: '24px', transition: '0.3s' }}></span></label>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px 0', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <span style={{ color: 'white' }}>🌙 Dark Mode</span>
            <label style={{ position: 'relative', display: 'inline-block', width: '50px', height: '24px' }}><input type="checkbox" defaultChecked style={{ opacity: 0, width: 0, height: 0 }} /><span style={{ position: 'absolute', cursor: 'pointer', top: 0, left: 0, right: 0, bottom: 0, background: '#00bcd4', borderRadius: '24px', transition: '0.3s' }}></span></label>
          </div>
        </div>
      </div>
    </div>
  )
}

// Simple Placeholder for other pages
function PlaceholderPage({ title }) {
  const navigate = useNavigate()
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', padding: '20px' }}>
      <button onClick={() => navigate('/dashboard')} style={{ marginBottom: '20px', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 15px', color: 'white', cursor: 'pointer' }}>← Back</button>
      <div style={{ textAlign: 'center', padding: '100px 20px' }}>
        <span style={{ fontSize: '60px' }}>🚧</span>
        <h1 style={{ color: 'white', marginTop: '20px' }}>{title}</h1>
        <p style={{ color: 'rgba(255,255,255,0.6)' }}>This page is under construction</p>
      </div>
    </div>
  )
}

// Main App Component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<UploadReport />} />
        <Route path="/history" element={<ReportHistory />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/recommendations" element={<PlaceholderPage title="Recommendations" />} />
        <Route path="/diet-plan" element={<PlaceholderPage title="Diet Plan" />} />
        <Route path="/exercise-plan" element={<PlaceholderPage title="Exercise Plan" />} />
        <Route path="/chat" element={<PlaceholderPage title="AI Chat" />} />
        <Route path="/blog" element={<PlaceholderPage title="Blog" />} />
      </Routes>
      <Toaster position="top-right" richColors />
    </Router>
  )
}

export default App