import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate, Link } from 'react-router-dom'
import { Mail, Lock, User, Eye, EyeOff, ArrowRight, CheckCircle, XCircle } from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import { useAuthStore } from '../stores/authStore'

const schema = z.object({
  fullName: z.string().min(2, 'Full name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

const SignUp = () => {
  const navigate = useNavigate()
  const { register: signUp, isLoading } = useAuthStore()
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  })
  
  const password = watch('password', '')
  
  const getPasswordStrength = (pass) => {
    let strength = 0
    if (pass.length >= 8) strength++
    if (pass.match(/[A-Z]/)) strength++
    if (pass.match(/[a-z]/)) strength++
    if (pass.match(/[0-9]/)) strength++
    return strength
  }
  
  const strength = getPasswordStrength(password)
  const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'][strength] || 'Very Weak'
  const strengthColor = [
    'bg-red-500', 'bg-orange-500', 'bg-yellow-500', 
    'bg-blue-500', 'bg-emerald-500'
  ][strength] || 'bg-red-500'
  
  const onSubmit = async (data) => {
    try {
      await signUp({
        full_name: data.fullName,
        email: data.email,
        password: data.password
      })
      toast.success('Account created successfully! Please verify your email.')
      navigate('/dashboard')
    } catch (error) {
      toast.error(error.response?.data?.error || 'Registration failed')
    }
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl floating" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl floating" style={{ animationDelay: '2s' }} />
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="glass-card p-8 rounded-2xl backdrop-blur-xl relative z-10">
          <div className="text-center mb-8">
            <div className="gradient-bg w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <User className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
            <p className="text-white/60">Join the future of healthcare analytics</p>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              label="Full Name"
              type="text"
              icon={User}
              placeholder="John Doe"
              error={errors.fullName?.message}
              {...register('fullName')}
            />
            
            <Input
              label="Email"
              type="email"
              icon={Mail}
              placeholder="john@example.com"
              error={errors.email?.message}
              {...register('email')}
            />
            
            <div className="space-y-2">
              <Input
                label="Password"
                type="password"
                icon={Lock}
                placeholder="Create a strong password"
                error={errors.password?.message}
                {...register('password')}
              />
              
              {password && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white/60">Password strength:</span>
                    <span className={`font-medium ${strength >= 4 ? 'text-emerald-400' : strength >= 3 ? 'text-blue-400' : 'text-yellow-400'}`}>
                      {strengthText}
                    </span>
                  </div>
                  <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${(strength / 4) * 100}%` }}
                      className={`h-full ${strengthColor} rounded-full transition-all duration-300`}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {[
                      { text: '8+ characters', check: password.length >= 8 },
                      { text: 'Uppercase letter', check: /[A-Z]/.test(password) },
                      { text: 'Lowercase letter', check: /[a-z]/.test(password) },
                      { text: 'Number', check: /[0-9]/.test(password) },
                    ].map((req, i) => (
                      <div key={i} className="flex items-center gap-1 text-white/50">
                        {req.check ? 
                          <CheckCircle className="w-3 h-3 text-emerald-400" /> : 
                          <XCircle className="w-3 h-3 text-white/30" />
                        }
                        <span className={req.check ? 'text-emerald-400' : ''}>{req.text}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <Input
              label="Confirm Password"
              type="password"
              icon={Lock}
              placeholder="Confirm your password"
              error={errors.confirmPassword?.message}
              {...register('confirmPassword')}
            />
            
            <Button type="submit" isLoading={isLoading} className="w-full group">
              Create Account
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </form>
          
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 glass-card text-white/60">Or continue with</span>
              </div>
            </div>
            
            <div className="mt-6 grid grid-cols-2 gap-3">
              <button className="glass-card p-3 rounded-xl text-white hover:bg-white/10 transition-colors">
                Google
              </button>
              <button className="glass-card p-3 rounded-xl text-white hover:bg-white/10 transition-colors">
                Apple
              </button>
            </div>
          </div>
          
          <p className="text-center mt-6 text-white/60">
            Already have an account?{' '}
            <Link to="/login" className="text-cyan-400 hover:text-cyan-300 transition-colors font-semibold">
              Sign in
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}

export default SignUp