import { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate, Link } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

const Login = () => {
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    console.log('Login attempt with:', formData.email)
    
    // For testing - allow demo login without backend
    if (formData.email === 'demo@example.com' && formData.password === 'demo123') {
      localStorage.setItem('access_token', 'demo_token_12345')
      localStorage.setItem('user', JSON.stringify({
        id: 1,
        full_name: 'Demo User',
        email: 'demo@example.com'
      }))
      toast.success('Demo login successful!')
      setTimeout(() => {
        navigate('/dashboard')
      }, 500)
      setLoading(false)
      return
    }
    
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      const data = await response.json()
      console.log('Response:', response.status, data)
      
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        toast.success('Login successful!')
        navigate('/dashboard')
      } else {
        toast.error(data.error || 'Login failed')
      }
    } catch (error) {
      console.error('Login error:', error)
      toast.error('Cannot connect to server. Using demo mode? Try demo@example.com / demo123')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl floating" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl floating" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md relative z-10"
      >
        <div className="glass-card p-8 rounded-2xl">
          <div className="text-center mb-8">
            <div className="gradient-bg w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Mail className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-white/60">Sign in to your MediScan AI account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-white/80 text-sm mb-2">Email Address</label>
              <input
                type="email"
                placeholder="demo@example.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>

            <div>
              <label className="block text-white/80 text-sm mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="demo123"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-cyan-500"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white/60"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 rounded border-white/20 bg-white/5 accent-cyan-500" />
                <span className="text-white/60 text-sm">Remember me</span>
              </label>
              <Link to="/forgot-password" className="text-cyan-400 hover:text-cyan-300 text-sm">
                Forgot password?
              </Link>
            </div>

            <Button type="submit" isLoading={loading} className="w-full">
              Sign In
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 glass-card text-white/60">Demo Account</span>
              </div>
            </div>
            <div className="mt-4 p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
              <p className="text-white/60 text-sm text-center">
                Demo: demo@example.com / demo123
              </p>
            </div>
          </div>

          <p className="text-center mt-6 text-white/60">
            Don't have an account?{' '}
            <Link to="/signup" className="text-cyan-400 hover:text-cyan-300 font-semibold">
              Create account
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}

export default Login