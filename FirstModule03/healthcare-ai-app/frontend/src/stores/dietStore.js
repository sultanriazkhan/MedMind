import { create } from 'zustand'

export const useDietStore = create((set, get) => ({
  dietPlan: null,
  isLoading: false,
  error: null,
  
  fetchDietPlan: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch('/api/recommendations/diet', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ dietPlan: data, isLoading: false })
      return data
    } catch (error) {
      set({ error: error.message, isLoading: false })
      throw error
    }
  },
  
  generateDietPlan: async (preferences) => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch('/api/recommendations/diet/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(preferences)
      })
      const data = await response.json()
      set({ dietPlan: data, isLoading: false })
      return data
    } catch (error) {
      set({ error: error.message, isLoading: false })
      throw error
    }
  }
}))