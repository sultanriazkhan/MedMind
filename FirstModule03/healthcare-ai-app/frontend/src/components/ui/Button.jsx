import { motion } from 'framer-motion'

const Button = ({ children, variant = 'primary', size = 'md', isLoading = false, disabled = false, className = '', ...props }) => {
  const variants = {
    primary: 'gradient-bg text-white shadow-lg hover:shadow-xl',
    secondary: 'glass-card text-white border-2 border-primary-400 hover:bg-white/20',
    outline: 'border-2 border-white/30 text-white hover:bg-white/10',
    ghost: 'text-white/70 hover:text-white hover:bg-white/10',
  }
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  }
  
  return (
    <motion.button
      whileHover={{ scale: disabled || isLoading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
      className={`
        ${variants[variant]} ${sizes[size]} rounded-xl font-semibold
        transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
        relative overflow-hidden animated-border ${className}
      `}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center justify-center gap-2">
          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          <span>Loading...</span>
        </div>
      ) : children}
    </motion.button>
  )
}

export default Button