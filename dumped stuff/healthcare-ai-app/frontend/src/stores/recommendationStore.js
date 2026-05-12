import { create } from 'zustand'

export const useRecommendationStore = create((set, get) => ({
  recommendations: [],
  isLoading: false,
  
  fetchRecommendations: async () => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/recommendations/lifestyle', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ recommendations: data.recommendations || [], isLoading: false })
    } catch (error) {
      console.error('Failed to fetch recommendations:', error)
      set({ isLoading: false })
    }
  },
  
  regenerateRecommendations: async () => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/recommendations/regenerate', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ recommendations: data.recommendations || [], isLoading: false })
    } catch (error) {
      console.error('Failed to regenerate recommendations:', error)
      set({ isLoading: false })
    }
  }
}))