import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Calendar, User, Clock, Heart, Eye, Filter, X } from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const BlogSearch = () => {
  const [searchParams, setSearchParams] = useSearchParams()
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [showFilters, setShowFilters] = useState(false)

  const categories = ['All', 'Nutrition', 'Fitness', 'Mental Health', 'Medical Research', 'Wellness Tips']

  useEffect(() => {
    if (searchQuery) {
      performSearch()
    }
  }, [searchQuery, selectedCategory])

  const performSearch = async () => {
    setLoading(true)
    setTimeout(() => {
      const mockResults = [
        {
          id: 1,
          title: "Understanding Your Blood Test Results",
          excerpt: "A comprehensive guide to interpreting common blood markers...",
          category: "Medical Research",
          author: "Dr. Sarah Johnson",
          date: "2024-01-15",
          readTime: 8,
          likes: 245,
          views: 3421,
          image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400"
        },
        {
          id: 2,
          title: "10 Simple Nutrition Tips for Better Health",
          excerpt: "Easy dietary changes that can transform your wellbeing...",
          category: "Nutrition",
          author: "Maria Garcia",
          date: "2024-01-10",
          readTime: 6,
          likes: 189,
          views: 2156,
          image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400"
        },
        {
          id: 3,
          title: "Morning Exercise Routine for Beginners",
          excerpt: "Start your day with these simple effective exercises...",
          category: "Fitness",
          author: "John Smith",
          date: "2024-01-08",
          readTime: 5,
          likes: 312,
          views: 4567,
          image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400"
        }
      ].filter(item => 
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
      ).filter(item => 
        selectedCategory === '' || selectedCategory === 'All' || item.category === selectedCategory
      )
      
      setResults(mockResults)
      setLoading(false)
    }, 500)
  }

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      setSearchParams({ q: searchQuery })
      performSearch()
    } else {
      toast.error('Please enter a search term')
    }
  }

  const clearFilters = () => {
    setSelectedCategory('')
    setSearchQuery('')
    setSearchParams({})
    setResults([])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-white mb-4">Search Articles</h1>
          <p className="text-white/60 mb-8">Find health insights and medical information</p>

          <form onSubmit={handleSearch} className="mb-8">
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/40" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for articles..."
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-cyan-500"
                />
              </div>
              <Button type="submit">Search</Button>
              <Button type="button" variant="outline" onClick={() => setShowFilters(!showFilters)}>
                <Filter className="w-4 h-4 mr-2" />
                Filters
              </Button>
            </div>
          </form>

          {showFilters && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="glass-card p-4 rounded-xl mb-8"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-white font-semibold">Categories</h3>
                <button onClick={clearFilters} className="text-white/40 hover:text-white text-sm">
                  Clear all
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category === 'All' ? '' : category)}
                    className={`px-3 py-1 rounded-full text-sm transition-all ${
                      (category === 'All' && selectedCategory === '') || selectedCategory === category
                        ? 'gradient-bg text-white'
                        : 'bg-white/10 text-white/70 hover:bg-white/20'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </motion.div>
          )}

          {loading ? (
            <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="animate-pulse glass-card p-4 rounded-xl">
                  <div className="h-48 bg-white/10 rounded-lg mb-4" />
                  <div className="h-6 bg-white/10 rounded-lg w-3/4 mb-2" />
                  <div className="h-4 bg-white/10 rounded-lg w-full mb-2" />
                  <div className="h-4 bg-white/10 rounded-lg w-2/3" />
                </div>
              ))}
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-6">
              <p className="text-white/60">Found {results.length} results for "{searchQuery}"</p>
              {results.map((post, index) => (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Link to={`/blog/${post.id}`}>
                    <Card className="overflow-hidden hover:scale-[1.02] transition-transform duration-300">
                      <div className="grid md:grid-cols-3 gap-4">
                        <div className="h-48 md:h-full">
                          <img src={post.image} alt={post.title} className="w-full h-full object-cover rounded-lg" />
                        </div>
                        <div className="md:col-span-2 p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-xs">
                              {post.category}
                            </span>
                          </div>
                          <h3 className="text-xl font-semibold text-white mb-2">{post.title}</h3>
                          <p className="text-white/60 text-sm mb-3">{post.excerpt}</p>
                          <div className="flex items-center gap-4 text-white/40 text-xs">
                            <div className="flex items-center gap-1">
                              <User className="w-3 h-3" />
                              <span>{post.author}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              <span>{new Date(post.date).toLocaleDateString()}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="w-3 h-3" />
                              <span>{post.readTime} min read</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </Card>
                  </Link>
                </motion.div>
              ))}
            </div>
          ) : searchQuery && (
            <div className="text-center py-20">
              <Search className="w-20 h-20 text-white/20 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No results found</h3>
              <p className="text-white/60 mb-4">We couldn't find any articles matching "{searchQuery}"</p>
              <Button onClick={clearFilters}>Clear Search</Button>
            </div>
          )}

          {!searchQuery && !loading && results.length === 0 && (
            <div className="text-center py-20">
              <Search className="w-20 h-20 text-white/20 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Search for health articles</h3>
              <p className="text-white/60">Enter keywords above to find relevant health information</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default BlogSearch