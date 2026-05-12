import { z } from 'zod'

export const emailSchema = z
  .string()
  .min(1, 'Email is required')
  .email('Please enter a valid email address')

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character')

export const nameSchema = z
  .string()
  .min(2, 'Name must be at least 2 characters')
  .max(100, 'Name must be less than 100 characters')
  .regex(/^[a-zA-Z\s'-]+$/, 'Name can only contain letters, spaces, apostrophes, and hyphens')

export const ageSchema = z
  .number()
  .min(18, 'Age must be at least 18')
  .max(120, 'Age must be less than 120')

export const weightSchema = z
  .number()
  .min(20, 'Weight must be at least 20 kg')
  .max(300, 'Weight must be less than 300 kg')

export const heightSchema = z
  .number()
  .min(100, 'Height must be at least 100 cm')
  .max(250, 'Height must be less than 250 cm')

export const phoneSchema = z
  .string()
  .regex(/^\+?[\d\s-]{10,}$/, 'Please enter a valid phone number')

export const dateSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Please use YYYY-MM-DD format')

export const validateEmail = (email) => {
  const result = emailSchema.safeParse(email)
  return result.success ? null : result.error.errors[0].message
}

export const validatePassword = (password) => {
  const result = passwordSchema.safeParse(password)
  return result.success ? null : result.error.errors[0].message
}

export const validateName = (name) => {
  const result = nameSchema.safeParse(name)
  return result.success ? null : result.error.errors[0].message
}

export const validateAge = (age) => {
  const result = ageSchema.safeParse(age)
  return result.success ? null : result.error.errors[0].message
}

export const validateWeight = (weight) => {
  const result = weightSchema.safeParse(weight)
  return result.success ? null : result.error.errors[0].message
}

export const validateHeight = (height) => {
  const result = heightSchema.safeParse(height)
  return result.success ? null : result.error.errors[0].message
}

export const getPasswordStrength = (password) => {
  let strength = 0
  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  return strength
}

export const getPasswordStrengthText = (strength) => {
  const texts = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong']
  return texts[strength] || 'Very Weak'
}

export const getPasswordStrengthColor = (strength) => {
  const colors = [
    'bg-red-500',
    'bg-orange-500',
    'bg-yellow-500',
    'bg-blue-500',
    'bg-emerald-500'
  ]
  return colors[strength] || 'bg-red-500'
}

export const validateConfirmPassword = (password, confirmPassword) => {
  if (password !== confirmPassword) {
    return 'Passwords do not match'
  }
  return null
}

export const validateForm = (schema, data) => {
  const result = schema.safeParse(data)
  if (result.success) {
    return { isValid: true, errors: {} }
  }
  
  const errors = {}
  result.error.errors.forEach((err) => {
    errors[err.path[0]] = err.message
  })
  
  return { isValid: false, errors }
}

export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, 'Password is required')
})

export const registerSchema = z.object({
  full_name: nameSchema,
  email: emailSchema,
  password: passwordSchema,
  confirm_password: z.string()
}).refine((data) => data.password === data.confirm_password, {
  message: "Passwords don't match",
  path: ['confirm_password']
})

export const forgotPasswordSchema = z.object({
  email: emailSchema
})

export const resetPasswordSchema = z.object({
  password: passwordSchema,
  confirm_password: z.string()
}).refine((data) => data.password === data.confirm_password, {
  message: "Passwords don't match",
  path: ['confirm_password']
})

export const healthProfileSchema = z.object({
  age: ageSchema,
  sex: z.enum(['male', 'female', 'other'], {
    errorMap: () => ({ message: 'Please select your sex' })
  }),
  weight: weightSchema,
  height: heightSchema,
  activity_level: z.number().min(1).max(5),
  conditions: z.array(z.string()),
  dietary_restrictions: z.array(z.string()),
  goals: z.array(z.string())
})

export const reportUploadSchema = z.object({
  file: z.instanceof(File, { message: 'Please select a file' })
    .refine((file) => file.size <= 16 * 1024 * 1024, 'File size must be less than 16MB')
    .refine(
      (file) => ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'].includes(file.type),
      'Only PDF, DOCX, or TXT files are allowed'
    )
})

export const settingsSchema = z.object({
  full_name: nameSchema.optional(),
  email: emailSchema.optional(),
  notification_preferences: z.object({
    email_alerts: z.boolean(),
    push_notifications: z.boolean(),
    weekly_digest: z.boolean(),
    ai_suggestions: z.boolean()
  }).optional(),
  privacy_settings: z.object({
    data_sharing: z.boolean(),
    two_factor: z.boolean()
  }).optional(),
  ai_language: z.enum(['en', 'es', 'fr', 'de', 'zh']).optional()
})

export const chatMessageSchema = z.object({
  message: z.string().min(1, 'Message cannot be empty').max(2000, 'Message too long')
})

export const blogSearchSchema = z.object({
  query: z.string().min(1, 'Search query is required'),
  category: z.string().optional(),
  page: z.number().min(1).optional(),
  limit: z.number().min(1).max(50).optional()
})

export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$/
  return emailRegex.test(email)
}

export const isValidPhone = (phone) => {
  const phoneRegex = /^\+?[\d\s-]{10,}$/
  return phoneRegex.test(phone)
}

export const isValidUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input
  return input
    .trim()
    .replace(/[<>]/g, '')
    .slice(0, 1000)
}

export const validateReportData = (data) => {
  const required = ['name', 'value', 'unit', 'normal_range']
  const missing = required.filter(field => !data[field])
  
  if (missing.length > 0) {
    return { isValid: false, errors: missing.map(f => `${f} is required`) }
  }
  
  if (isNaN(parseFloat(data.value))) {
    return { isValid: false, errors: ['Value must be a number'] }
  }
  
  return { isValid: true, errors: [] }
}

export const formatValidationErrors = (errors) => {
  if (!errors) return {}
  
  const formatted = {}
  Object.keys(errors).forEach((key) => {
    if (errors[key]?.message) {
      formatted[key] = errors[key].message
    } else if (typeof errors[key] === 'string') {
      formatted[key] = errors[key]
    }
  })
  
  return formatted
}

export default {
  emailSchema,
  passwordSchema,
  nameSchema,
  ageSchema,
  weightSchema,
  heightSchema,
  phoneSchema,
  dateSchema,
  loginSchema,
  registerSchema,
  forgotPasswordSchema,
  resetPasswordSchema,
  healthProfileSchema,
  reportUploadSchema,
  settingsSchema,
  chatMessageSchema,
  blogSearchSchema,
  validateEmail,
  validatePassword,
  validateName,
  validateAge,
  validateWeight,
  validateHeight,
  validateConfirmPassword,
  validateForm,
  getPasswordStrength,
  getPasswordStrengthText,
  getPasswordStrengthColor,
  isValidEmail,
  isValidPhone,
  isValidUrl,
  sanitizeInput,
  validateReportData,
  formatValidationErrors
}