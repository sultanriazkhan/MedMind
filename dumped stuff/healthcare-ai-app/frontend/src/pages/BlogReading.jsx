import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Calendar, User, Clock, Heart, Share2, Bookmark, ArrowLeft, Facebook, Twitter, Linkedin } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const BlogReading = () => {
  const { id } = useParams()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [liked, setLiked] = useState(false)
  const [bookmarked, setBookmarked] = useState(false)
  const [readingProgress, setReadingProgress] = useState(0)

  useEffect(() => {
    fetchPost()
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleScroll = () => {
    const winScroll = document.documentElement.scrollTop
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight
    const scrolled = (winScroll / height) * 100
    setReadingProgress(scrolled)
  }

  const fetchPost = async () => {
    setTimeout(() => {
      setPost({
        id: parseInt(id),
        title: "Understanding Your Blood Test Results: A Complete Guide",
        excerpt: "Learn how to interpret common blood test markers and what they mean for your health.",
        content: `
## Introduction

Blood tests are one of the most common medical procedures, yet many people find the results confusing. This guide will help you understand the key markers.

## Complete Blood Count (CBC)

The CBC measures different components of your blood:

### Red Blood Cells (RBC)
- **Normal range**: 4.5-5.9 million cells/mcL
- **Low RBC**: May indicate anemia
- **High RBC**: Could suggest dehydration or other conditions

### White Blood Cells (WBC)
- **Normal range**: 4,500-11,000 cells/mcL
- **High WBC**: Often indicates infection or inflammation
- **Low WBC**: May suggest bone marrow issues

### Platelets
- **Normal range**: 150,000-450,000 platelets/mcL
- **Low platelets**: Bleeding risk
- **High platelets**: Clotting risk

## Lipid Panel

### LDL Cholesterol ("Bad" Cholesterol)
- **Optimal**: <100 mg/dL
- **Near optimal**: 100-129 mg/dL
- **Borderline high**: 130-159 mg/dL

### HDL Cholesterol ("Good" Cholesterol)
- **Poor**: <40 mg/dL
- **Better**: 40-59 mg/dL
- **Excellent**: >60 mg/dL

## When to Consult Your Doctor

Always discuss abnormal results with your healthcare provider. They can provide personalized interpretations based on your medical history.

## Conclusion

Understanding your lab results empowers you to take control of your health. Use this knowledge to have informed conversations with your doctor.
        `,
        category: "Medical Research",
        author: "Dr. Sarah Johnson",
        authorTitle: "Clinical Pathologist",
        authorAvatar: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100",
        date: "2024-01-15",
        readTime: 8,
        likes: 245,
        views: 3421,
        image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200",
        tags: ["Blood Tests", "Health Education", "Lab Results"]
      })
      setLoading(false)
    }, 500)
  }

  const handleLike = () => {
    setLiked(!liked)
    toast.success(liked ? 'Removed like' : 'Liked!')
  }

  const handleBookmark = () => {
    setBookmarked(!bookmarked)
    toast.success(bookmarked ? 'Removed bookmark' : 'Saved to bookmarks')
  }

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
    toast.success('Link copied to clipboard!')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse">
            <div className="h-96 bg-white/10 rounded-2xl mb-8" />
            <div className="h-10 bg-white/10 rounded-lg w-3/4 mb-4" />
            <div className="h-4 bg-white/10 rounded-lg w-1/2 mb-8" />
            <div className="space-y-3">
              <div className="h-4 bg-white/10 rounded-lg w-full" />
              <div className="h-4 bg-white/10 rounded-lg w-full" />
              <div className="h-4 bg-white/10 rounded-lg w-3/4" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
      <div className="fixed top-0 left-0 right-0 h-1 bg-white/10 z-50">
        <div className="gradient-bg h-full transition-all duration-300" style={{ width: `${readingProgress}%` }} />
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Link to="/blog" className="inline-flex items-center gap-2 text-white/60 hover:text-white mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Blog
        </Link>

        <motion.article
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-sm">
                {post.category}
              </span>
            </div>
            
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              {post.title}
            </h1>
            
            <p className="text-xl text-white/70 mb-6">
              {post.excerpt}
            </p>
            
            <div className="flex flex-wrap items-center justify-between gap-4 py-4 border-y border-white/10">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-3">
                  <img src={post.authorAvatar} alt={post.author} className="w-12 h-12 rounded-full object-cover" />
                  <div>
                    <p className="text-white font-semibold">{post.author}</p>
                    <p className="text-white/40 text-sm">{post.authorTitle}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-white/40 text-sm">
                  <div className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(post.date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>{post.readTime} min read</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={handleLike}
                  className={`p-2 rounded-lg transition-colors ${liked ? 'bg-red-500/20 text-red-400' : 'bg-white/5 text-white/60 hover:bg-white/10'}`}
                >
                  <Heart className={`w-5 h-5 ${liked ? 'fill-red-400' : ''}`} />
                </button>
                <button
                  onClick={handleBookmark}
                  className={`p-2 rounded-lg transition-colors ${bookmarked ? 'bg-yellow-500/20 text-yellow-400' : 'bg-white/5 text-white/60 hover:bg-white/10'}`}
                >
                  <Bookmark className={`w-5 h-5 ${bookmarked ? 'fill-yellow-400' : ''}`} />
                </button>
                <button
                  onClick={handleShare}
                  className="p-2 rounded-lg bg-white/5 text-white/60 hover:bg-white/10 transition-colors"
                >
                  <Share2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          <div className="relative mb-8 rounded-2xl overflow-hidden h-96">
            <img src={post.image} alt={post.title} className="w-full h-full object-cover" />
          </div>

          <div className="prose prose-invert prose-lg max-w-none">
            <ReactMarkdown>{post.content}</ReactMarkdown>
          </div>

          <div className="mt-8 pt-8 border-t border-white/10">
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag, i) => (
                <span key={i} className="px-3 py-1 bg-white/5 text-white/60 rounded-full text-sm">
                  #{tag}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-8 p-6 glass-card rounded-2xl">
            <div className="flex items-center gap-4">
              <img src={post.authorAvatar} alt={post.author} className="w-16 h-16 rounded-full object-cover" />
              <div className="flex-1">
                <h4 className="text-white font-semibold">{post.author}</h4>
                <p className="text-white/60 text-sm mb-2">{post.authorTitle}</p>
                <p className="text-white/70 text-sm">Dr. Johnson is a board-certified clinical pathologist with over 15 years of experience in laboratory medicine.</p>
              </div>
            </div>
          </div>

          <div className="mt-8 flex justify-center gap-4">
            <button className="p-3 rounded-full bg-[#1877f2]/20 text-[#1877f2] hover:bg-[#1877f2]/30 transition-colors">
              <Facebook className="w-5 h-5" />
            </button>
            <button className="p-3 rounded-full bg-[#1da1f2]/20 text-[#1da1f2] hover:bg-[#1da1f2]/30 transition-colors">
              <Twitter className="w-5 h-5" />
            </button>
            <button className="p-3 rounded-full bg-[#0077b5]/20 text-[#0077b5] hover:bg-[#0077b5]/30 transition-colors">
              <Linkedin className="w-5 h-5" />
            </button>
          </div>
        </motion.article>
      </div>
    </div>
  )
}

export default BlogReading