import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function HealthProfile() {
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const stats = [
    { label: 'Age', value: '32', icon: '🎂' },
    { label: 'Weight', value: '72 kg', icon: '⚖️' },
    { label: 'Height', value: '175 cm', icon: '📏' },
    { label: 'BMI', value: '23.5', icon: '📊' },
  ]

  const conditions = ['None reported', 'Allergies: Seasonal', 'Blood Type: O+']
  const goals = ['Improve fitness', 'Better sleep', 'Reduce stress']

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)' }}>
      <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', padding: '15px 20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} style={{ background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '8px 12px', cursor: 'pointer', color: 'white', fontSize: '20px' }}>☰</button>
        <h1 style={{ color: 'white', fontSize: '20px', margin: 0 }}>Health Profile</h1>
      </div>
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '20px', padding: '30px', textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ width: '80px', height: '80px', background: 'linear-gradient(135deg, #00bcd4, #10b981)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px', fontSize: '40px' }}>👤</div>
          <h2 style={{ color: 'white' }}>{user.name || 'User'}</h2>
          <p style={{ color: 'rgba(255,255,255,0.6)' }}>{user.email || 'user@example.com'}</p>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '20px' }}>
          {stats.map((stat) => (
            <div key={stat.label} style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px', textAlign: 'center' }}>
              <span style={{ fontSize: '30px' }}>{stat.icon}</span>
              <h3 style={{ color: 'white', margin: '10px 0 5px' }}>{stat.value}</h3>
              <p style={{ color: 'rgba(255,255,255,0.6)', margin: 0 }}>{stat.label}</p>
            </div>
          ))}
        </div>

        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px', marginBottom: '20px' }}>
          <h3 style={{ color: 'white', marginBottom: '15px' }}>🏥 Medical Conditions</h3>
          {conditions.map((condition, i) => (
            <div key={i} style={{ padding: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
              <span style={{ color: 'rgba(255,255,255,0.7)' }}>{condition}</span>
            </div>
          ))}
        </div>

        <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '15px', padding: '20px' }}>
          <h3 style={{ color: 'white', marginBottom: '15px' }}>🎯 Health Goals</h3>
          {goals.map((goal, i) => (
            <div key={i} style={{ padding: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
              <span style={{ color: 'rgba(255,255,255,0.7)' }}>✓ {goal}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default HealthProfile