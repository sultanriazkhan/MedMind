import api from './api'

class AuthService {
  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  }
  
  async register(userData) {
    const response = await api.post('/auth/register', userData)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  }
  
  async logout() {
    await api.post('/auth/logout')
    localStorage.removeItem('access_token')
  }
  
  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  }
  
  async refreshToken() {
    const response = await api.post('/auth/refresh')
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  }
  
  async forgotPassword(email) {
    return api.post('/auth/forgot-password', { email })
  }
  
  async resetPassword(token, newPassword) {
    return api.post(`/auth/reset-password/${token}`, { new_password: newPassword })
  }
  
  async verifyEmail(token) {
    return api.get(`/auth/verify-email/${token}`)
  }
}

export default new AuthService()