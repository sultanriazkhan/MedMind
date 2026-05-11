import { create } from 'zustand'

export const useBlogStore = create((set, get) => ({
  posts: [],
  currentPost: null,
  isLoading: false,
  
  fetchPosts: async () => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/blog/posts')
      const data = await response.json()
      set({ posts: data.posts || [], isLoading: false })
    } catch (error) {
      console.error('Failed to fetch posts:', error)
      set({ isLoading: false })
    }
  },
  
  fetchPostById: async (id) => {
    set({ isLoading: true })
    try {
      const response = await fetch(`/api/blog/posts/${id}`)
      const data = await response.json()
      set({ currentPost: data.post, isLoading: false })
      return data.post
    } catch (error) {
      console.error('Failed to fetch post:', error)
      set({ isLoading: false })
    }
  },
  
  searchPosts: async (query) => {
    set({ isLoading: true })
    try {
      const response = await fetch(`/api/blog/search?q=${query}`)
      const data = await response.json()
      set({ posts: data.posts || [], isLoading: false })
      return data.posts
    } catch (error) {
      console.error('Failed to search posts:', error)
      set({ isLoading: false })
    }
  }
}))