import { create } from 'zustand'

export const useUIStore = create((set, get) => ({
  sidebarOpen: true,
  notifications: [],
  loadingStates: {},
  modalOpen: false,
  modalContent: null,
  toastMessage: null,
  
  toggleSidebar: () => set({ sidebarOpen: !get().sidebarOpen }),
  
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  
  addNotification: (notification) => {
    const id = Date.now()
    const newNotification = { ...notification, id, read: false, timestamp: new Date() }
    set({ notifications: [newNotification, ...get().notifications].slice(0, 50) })
    
    setTimeout(() => {
      get().removeNotification(id)
    }, 5000)
    
    return id
  },
  
  removeNotification: (id) => {
    set({ notifications: get().notifications.filter(n => n.id !== id) })
  },
  
  markNotificationAsRead: (id) => {
    set({
      notifications: get().notifications.map(n =>
        n.id === id ? { ...n, read: true } : n
      )
    })
  },
  
  clearAllNotifications: () => set({ notifications: [] }),
  
  setLoading: (key, isLoading) => {
    set({ loadingStates: { ...get().loadingStates, [key]: isLoading } })
  },
  
  isLoading: (key) => {
    return get().loadingStates[key] || false
  },
  
  openModal: (content, options = {}) => {
    set({ modalOpen: true, modalContent: content, modalOptions: options })
  },
  
  closeModal: () => {
    set({ modalOpen: false, modalContent: null, modalOptions: null })
  },
  
  showToast: (message, type = 'info') => {
    set({ toastMessage: { message, type, timestamp: Date.now() } })
    setTimeout(() => {
      if (get().toastMessage?.timestamp === Date.now()) {
        set({ toastMessage: null })
      }
    }, 3000)
  },
  
  hideToast: () => set({ toastMessage: null }),
  
  setTheme: (theme) => {
    set({ theme })
    localStorage.setItem('ui_theme', theme)
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  },
  
  toggleTheme: () => {
    const newTheme = get().theme === 'dark' ? 'light' : 'dark'
    get().setTheme(newTheme)
  },
  
  initTheme: () => {
    const savedTheme = localStorage.getItem('ui_theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light')
    get().setTheme(initialTheme)
  }
}))