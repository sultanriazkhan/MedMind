import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, ArrowRight, CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

const ForgotPassword = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [email, setEmail] = useState('')
  const [token, setToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSendEmail = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await fetch('http://localhost:5000/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })
      
      if (response.ok) {
        toast.success('Reset link sent to your email')
        setStep(2)
      } else {
        toast.error('Email not found')
      }
    } catch (error) {
      toast.error('Failed to send reset link')
    } finally {
      setLoading(false)
    }
  }

  const handleResetPassword = async (e) => {
    e.preventDefault()
    
    if (newPassword !== confirmPassword) {
      toast.error('Passwords do not match')
      return
    }
    
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }
    
    setLoading(true)
    
    try {
      const response = await fetch(`http://localhost:5000/api/auth/reset-password/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPassword })
      })
      
      if (response.ok) {
        toast.success('Password reset successful!')
        setStep(4)
        setTimeout(() => navigate('/login'), 3000)
      } else {
        toast.error('Invalid or expired token')
      }
    } catch (error) {
      toast.error('Failed to reset password')
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
        className="w-full max-w-md"
      >
        <div className="glass-card p-8 rounded-2xl">
          <div className="text-center mb-8">
            <div className="gradient-bg w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Lock className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Reset Password</h1>
            <p className="text-white/60">
              {step === 1 && "Enter your email to receive reset link"}
              {step === 2 && "Enter the reset code sent to your email"}
              {step === 3 && "Create your new password"}
              {step === 4 && "Password reset successful!"}
            </p>
          </div>

          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.form                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={handleSendEmail}
                className="space-y-5"
              >
                <Input
                  label="Email Address"
                  type="email"
                  icon={Mail}
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <Button type="submit" isLoading={loading} className="w-full">
                  Send Reset Link
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </motion.form>
            )}

            {step === 2 && (
              <motion.form
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={(e) => { e.preventDefault(); setStep(3) }}
                className="space-y-5"
              >
                <Input
                  label="Reset Code"
                  type="text"
                  placeholder="Enter 6-digit code"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  required
                />
                <p className="text-white/40 text-xs text-center">
                  Didn't receive code? <button className="text-cyan-400">Resend</button>
                </p>
                <Button type="submit" className="w-full">
                  Verify Code
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </motion.form>
            )}

            {step === 3 && (
              <motion.form
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={handleResetPassword}
                className="space-y-5"
              >
                <Input
                  label="New Password"
                  type="password"
                  icon={Lock}
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
                <Input
                  label="Confirm Password"
                  type="password"
                  icon={Lock}
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <Button type="submit" isLoading={loading} className="w-full">
                  Reset Password
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </motion.form>
            )}

            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center space-y-5"
              >
                <div className="w-20 h-20 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto">
                  <CheckCircle className="w-10 h-10 text-emerald-400" />
                </div>
                <p className="text-white/70">Your password has been successfully reset!</p>
                <p className="text-white/40 text-sm">Redirecting to login...</p>
                <Link to="/login">
                  <Button variant="outline" className="w-full">
                    Go to Login
                  </Button>
                </Link>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="mt-6 text-center">
            <Link to="/login" className="text-cyan-400 hover:text-cyan-300 text-sm">
              Back to Login
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default ForgotPassword