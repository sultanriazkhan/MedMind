import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useThemeStore = create(
  persist(
    (set, get) => ({
      isDarkMode: true,
      
      toggleTheme: () => {
        const newMode = !get().isDarkMode
        set({ isDarkMode: newMode })
        if (newMode) {
          document.documentElement.classList.add('dark')
        } else {
          document.documentElement.classList.remove('dark')
        }
      },
      
      setTheme: (mode) => {
        set({ isDarkMode: mode })
        if (mode) {
          document.documentElement.classList.add('dark')
        } else {
          document.documentElement.classList.remove('dark')
        }
      }
    }),
    {
      name: 'theme-storage'
    }
  )
)