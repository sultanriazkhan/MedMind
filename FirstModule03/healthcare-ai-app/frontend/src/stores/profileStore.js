import { create } from 'zustand'

export const useProfileStore = create((set, get) => ({
  profile: null,
  statistics: null,
  healthProfile: null,
  isLoading: false,
  
  fetchProfile: async () => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/profile/profile', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ profile: data, isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },
  
  fetchStatistics: async () => {
    try {
      const response = await fetch('/api/profile/statistics', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ statistics: data })
      return data
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
    }
  },
  
  fetchHealthProfile: async () => {
    try {
      const response = await fetch('/api/profile/health', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ healthProfile: data })
      return data
    } catch (error) {
      console.error('Failed to fetch health profile:', error)
    }
  },
  
  saveProfile: async (profileData) => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/profile/health', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(profileData)
      })
      const data = await response.json()
      set({ healthProfile: data.profile, isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },
  
  updateProfile: async (userData) => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/profile/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(userData)
      })
      const data = await response.json()
      set({ profile: data.user, isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  }
}))