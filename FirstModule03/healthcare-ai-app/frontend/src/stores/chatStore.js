import { create } from 'zustand'

export const useChatStore = create((set, get) => ({
  messages: [],
  isLoading: false,
  suggestions: [],
  reportContext: null,
  
  sendMessage: async (message) => {
    const newMessages = [...get().messages, { role: 'user', content: message }]
    set({ messages: newMessages, isLoading: true })
    
    try {
      const response = await fetch('/api/chat/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          message,
          report_context: !!get().reportContext,
          report_id: get().reportContext?.id
        })
      })
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ''
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue
            try {
              const parsed = JSON.parse(data)
              assistantMessage += parsed.content
              set({ 
                messages: [...newMessages, { role: 'assistant', content: assistantMessage }],
                isLoading: false
              })
            } catch (e) {}
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error)
      set({ isLoading: false })
    }
  },
  
  fetchSuggestions: async () => {
    try {
      const response = await fetch('/api/chat/suggestions', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      const data = await response.json()
      set({ suggestions: data.suggestions })
    } catch (error) {
      console.error('Failed to fetch suggestions:', error)
    }
  },
  
  clearChat: async () => {
    try {
      await fetch('/api/chat/clear', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      set({ messages: [] })
    } catch (error) {
      console.error('Failed to clear chat:', error)
    }
  },
  
  setReportContext: (report) => {
    set({ reportContext: report })
  }
}))