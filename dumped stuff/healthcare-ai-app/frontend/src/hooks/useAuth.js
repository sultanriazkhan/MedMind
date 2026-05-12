import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useAuthStore } from '../stores/authStore'

export const useAuth = () => {
  const navigate = useNavigate()
  const { 
    user, 
    isAuthenticated, 
    isLoading, 
    login: storeLogin, 
    signUp: storeSignUp, 
    logout: storeLogout,
    checkAuth 
  } = useAuthStore()
  
  const [error, setError] = useState(null)
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    const verifyAuth = async () => {
      setIsChecking(true)
      await checkAuth()
      setIsChecking(false)
    }
    verifyAuth()
  }, [])

  const login = useCallback(async (credentials) => {
    setError(null)
    try {
      const response = await storeLogin(credentials)
      toast.success(`Welcome back, ${response.user.full_name}!`)
      navigate('/dashboard')
      return response
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Login failed. Please check your credentials.'
      setError(errorMessage)
      toast.error(errorMessage)
      throw err
    }
  }, [storeLogin, navigate])

  const signUp = useCallback(async (userData) => {
    setError(null)
    try {
      const response = await storeSignUp(userData)
      toast.success('Account created successfully! Please complete your health profile.')
      navigate('/onboarding')
      return response
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Registration failed. Please try again.'
      setError(errorMessage)
      toast.error(errorMessage)
      throw err
    }
  }, [storeSignUp, navigate])

  const logout = useCallback(async () => {
    try {
      await storeLogout()
      toast.success('Logged out successfully')
      navigate('/login')
    } catch (err) {
      toast.error('Logout failed')
    }
  }, [storeLogout, navigate])

  const requireAuth = useCallback(() => {
    if (!isAuthenticated && !isLoading && !isChecking) {
      navigate('/login')
      toast.error('Please login to access this page')
      return false
    }
    return true
  }, [isAuthenticated, isLoading, isChecking, navigate])

  const getToken = useCallback(() => {
    return localStorage.getItem('access_token')
  }, [])

  const isTokenValid = useCallback(() => {
    const token = getToken()
    if (!token) return false
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const expired = payload.exp * 1000 < Date.now()
      return !expired
    } catch {
      return false
    }
  }, [getToken])

  return {
    user,
    isAuthenticated,
    isLoading: isLoading || isChecking,
    error,
    login,
    signUp,
    logout,
    requireAuth,
    getToken,
    isTokenValid,
    checkAuth
  }
}

export default useAuth