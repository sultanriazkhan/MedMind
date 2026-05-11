import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Calendar, Clock, User, Tag, Search, TrendingUp, 
  Heart, Bookmark, Share2, Eye 
} from 'lucide-react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { useBlogStore } from '../stores/blogStore'

const categories = ['All', 'Nutrition', 'Fitness', 'Mental Health', 'Medical Research', 'Wellness Tips']

const BlogListing = () => {
  const [activeCategory, setActiveCategory] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')
  const { posts, isLoading, fetchPosts } = useBlogStore()
  const featuredPost = posts[0]
  
  useEffect(() => {
    fetchPosts()
  }, [])
  
  const filteredPosts = posts.filter(post => {
    const matchesCategory = activeCategory === 'All' || post.category === activeCategory
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          post.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })
  
  return (
    <div className="min-h-screen">
      <div className="relative h-[60vh] overflow-hidden">
        <div className="absolute inset-0 gradient-bg opacity-90" />
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1600')] bg-cover bg-center mix-blend-overlay" />
        <div className="absolute inset-0 bg-gradient-to-t from-navy-900 to-transparent" />
        
        <div className="relative h-full flex items-center justify-center text-center px-4">
          <div>
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-5xl md:text-7xl font-bold text-white mb-4"
            >
              Health Insights Blog
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-xl text-white/80 max-w-2xl"
            >
              Expert articles on nutrition, fitness, and wellness from healthcare professionals
            </motion.p>
          </div>
        </div>
      </div>
      
      <div className="container mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-8">
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setActiveCategory(category)}
                className={`px-4 py-2 rounded-full transition-all duration-300 ${
                  activeCategory === category
                    ? 'gradient-bg text-white'
                    : 'glass-card text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
          
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
            <input
              type="text"
              placeholder="Search articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>
        
        {featuredPost && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-12"
          >
            <Link to={`/blog/${featuredPost.id}`}>
              <Card className="overflow-hidden hover:scale-[1.02] transition-transform duration-300">
                <div className="grid lg:grid-cols-2 gap-6">
                  <div className="h-64 lg:h-auto">
                    <img
                      src={featuredPost.image}
                      alt={featuredPost.title}
                      className="w-full h-full object-cover rounded-xl"
                    />
                  </div>
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-xs">
                        Featured
                      </span>
                      <span className="px-2 py-1 bg-white/10 text-white/60 rounded-full text-xs">
                        {featuredPost.category}
                      </span>
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-3">{featuredPost.title}</h2>
                    <p className="text-white/70 mb-4">{featuredPost.excerpt}</p>
                    <div className="flex items-center gap-4 text-white/40 text-sm mb-4">
                      <div className="flex items-center gap-1">
                        <User className="w-3 h-3" />
                        <span>{featuredPost.author}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        <span>{new Date(featuredPost.date).toLocaleDateString()}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>{featuredPost.readTime} min read</span>
                      </div>
                    </div>
                    <Button>Read Article</Button>
                  </div>
                </div>
              </Card>
            </Link>
          </motion.div>
        )}
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPosts.slice(1).map((post, index) => (
            <motion.div
              key={post.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Link to={`/blog/${post.id}`}>
                <Card className="overflow-hidden h-full hover:scale-[1.02] transition-transform duration-300">
                  <div className="h-48 overflow-hidden">
                    <img
                      src={post.image}
                      alt={post.title}
                      className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                    />
                  </div>
                  <div className="p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="px-2 py-1 bg-white/10 text-white/60 rounded-full text-xs">
                        {post.category}
                      </span>
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2 line-clamp-2">
                      {post.title}
                    </h3>
                    <p className="text-white/60 text-sm mb-3 line-clamp-2">{post.excerpt}</p>
                    <div className="flex items-center justify-between text-white/40 text-xs">
                      <div className="flex items-center gap-3">
                        <span>{post.author}</span>
                        <span>{post.readTime} min read</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Heart className="w-3 h-3" />
                        <span>{post.likes}</span>
                        <Eye className="w-3 h-3 ml-1" />
                        <span>{post.views}</span>
                      </div>
                    </div>
                  </div>
                </Card>
              </Link>
            </motion.div>
          ))}
        </div>
        
        {filteredPosts.length === 0 && (
          <div className="text-center py-20">
            <Search className="w-20 h-20 text-white/20 mx-auto mb-4" />
            <p className="text-white/60 text-lg">No articles found matching your criteria</p>
            <Button onClick={() => { setActiveCategory('All'); setSearchQuery('') }} className="mt-4">
              Clear Filters
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

export default BlogListing