import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import authService from '../services/authService'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      
      login: async (credentials) => {
        set({ isLoading: true })
        try {
          const response = await authService.login(credentials)
          set({ user: response.user, isAuthenticated: true, isLoading: false })
          return response
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },
      
      signUp: async (userData) => {
        set({ isLoading: true })
        try {
          const response = await authService.register(userData)
          set({ user: response.user, isAuthenticated: true, isLoading: false })
          return response
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },
      
      logout: async () => {
        set({ isLoading: true })
        try {
          await authService.logout()
          set({ user: null, isAuthenticated: false, isLoading: false })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },
      
      checkAuth: async () => {
        const token = localStorage.getItem('access_token')
        if (token && !get().isAuthenticated) {
          try {
            const user = await authService.getCurrentUser()
            set({ user, isAuthenticated: true })
          } catch (error) {
            set({ user: null, isAuthenticated: false })
          }
        }
      }
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage,
    }
  )
)