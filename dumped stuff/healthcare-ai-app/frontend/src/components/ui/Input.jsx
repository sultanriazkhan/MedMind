import { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const Input = ({ label, type = 'text', error, icon: Icon, ...props }) => {
  const [showPassword, setShowPassword] = useState(false)
  const isPassword = type === 'password'
  const inputType = isPassword ? (showPassword ? 'text' : 'password') : type
  
  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-white/80">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <Icon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/40" />
        )}
        <input
          type={inputType}
          className={`
            w-full px-4 py-3 bg-white/5 border rounded-xl
            text-white placeholder-white/30
            focus:outline-none focus:ring-2 focus:ring-primary-500
            transition-all duration-300
            ${Icon ? 'pl-10' : ''}
            ${isPassword ? 'pr-10' : ''}
            ${error ? 'border-red-500 focus:ring-red-500' : 'border-white/10 focus:border-primary-500'}
          `}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white/60 transition-colors"
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        )}
      </div>
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="text-sm text-red-400"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Input