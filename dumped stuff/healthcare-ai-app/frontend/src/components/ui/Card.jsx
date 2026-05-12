import { motion } from 'framer-motion'

const Card = ({ children, className = '', hover = true, gradient = false }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={hover ? { y: -5, transition: { duration: 0.2 } } : {}}
      className={`
        ${gradient ? 'gradient-bg' : 'glass-card-dark'} 
        rounded-2xl p-6 shadow-xl backdrop-blur-xl
        ${hover ? 'transition-all duration-300 hover:shadow-2xl' : ''}
        ${className}
      `}
    >
      {children}
    </motion.div>
  )
}

export default Card