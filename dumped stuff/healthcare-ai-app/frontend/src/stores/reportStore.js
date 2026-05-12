import { create } from 'zustand'

export const useReportStore = create((set, get) => ({
  reports: [],
  currentReport: null,
  isLoading: false,
  
  fetchReports: async () => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/reports/reports', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ reports: data.reports || [], isLoading: false })
    } catch (error) {
      console.error('Failed to fetch reports:', error)
      set({ isLoading: false })
    }
  },
  
  fetchReportById: async (id) => {
    set({ isLoading: true })
    try {
      const response = await fetch(`/api/reports/reports/${id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ currentReport: data, isLoading: false })
      return data
    } catch (error) {
      console.error('Failed to fetch report:', error)
      set({ isLoading: false })
    }
  },
  
  uploadReport: async (file) => {
    set({ isLoading: true })
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await fetch('/api/reports/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      })
      const data = await response.json()
      set({ isLoading: false })
      return data
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },
  
  deleteReport: async (id) => {
    try {
      await fetch(`/api/reports/reports/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      set({ reports: get().reports.filter(r => r.id !== id) })
    } catch (error) {
      console.error('Failed to delete report:', error)
    }
  }
}))