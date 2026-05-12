import { create } from 'zustand'

export const useSettingsStore = create((set, get) => ({
  settings: {
    notifications: {
      email_alerts: true,
      push_notifications: true,
      weekly_digest: false,
      ai_suggestions: true
    },
    privacy: {
      data_sharing: false,
      two_factor: false
    }
  },
  isLoading: false,
  
  updateSettings: async (newSettings) => {
    set({ settings: { ...get().settings, ...newSettings }, isLoading: true })
    try {
      const response = await fetch('/api/profile/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(newSettings)
      })
      const data = await response.json()
      set({ isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },
  
  changePassword: async (currentPassword, newPassword) => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/profile/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
      })
      const data = await response.json()
      set({ isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  }
}))