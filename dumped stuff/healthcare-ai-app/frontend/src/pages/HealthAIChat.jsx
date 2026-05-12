import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { 
  Send, Bot, User, Sparkles, Trash2, Lightbulb, 
  FileText, Loader2, Copy, Check, ThumbsUp, ThumbsDown 
} from 'lucide-react'
import { toast } from 'sonner'
import Button from '../components/ui/Button'
import { useChatStore } from '../stores/chatStore'

const HealthAIChat = () => {
  const [message, setMessage] = useState('')
  const [copiedId, setCopiedId] = useState(null)
  const messagesEndRef = useRef(null)
  const { messages, isLoading, sendMessage, clearChat, suggestions, fetchSuggestions } = useChatStore()
  
  useEffect(() => {
    fetchSuggestions()
    scrollToBottom()
  }, [])
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  const handleSend = async () => {
    if (!message.trim() || isLoading) return
    await sendMessage(message)
    setMessage('')
  }
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }
  
  const handleCopy = async (content, id) => {
    await navigator.clipboard.writeText(content)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
    toast.success('Copied to clipboard')
  }
  
  const handleSuggestionClick = (suggestion) => {
    setMessage(suggestion)
  }
  
  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900">
      <div className="glass-card mx-6 mt-6 rounded-2xl">
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="gradient-bg w-10 h-10 rounded-xl flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-white font-semibold">AI Health Assistant</h2>
              <p className="text-white/60 text-xs">Powered by GPT-4</p>
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={clearChat}>
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        <AnimatePresence>
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center justify-center h-full text-center"
            >
              <div className="gradient-bg w-20 h-20 rounded-2xl flex items-center justify-center mb-6">
                <Sparkles className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">How can I help you today?</h3>
              <p className="text-white/60 mb-8">Ask me anything about your health, lab results, or wellness journey</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                {suggestions.map((suggestion, i) => (
                  <motion.button
                    key={i}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="glass-card p-3 rounded-xl text-left hover:bg-white/10 transition-all"
                  >
                    <Lightbulb className="w-4 h-4 text-cyan-400 mb-2" />
                    <p className="text-white text-sm">{suggestion}</p>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                msg.role === 'user' ? 'gradient-bg' : 'glass-card'
              }`}>
                {msg.role === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-cyan-400" />
                )}
              </div>
              
              <div className={`group relative rounded-2xl p-4 ${
                msg.role === 'user' 
                  ? 'gradient-bg text-white' 
                  : 'glass-card text-white/90'
              }`}>
                {msg.role === 'assistant' ? (
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                )}
                
                {msg.role === 'assistant' && (
                  <div className="absolute -bottom-8 right-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleCopy(msg.content, index)}
                      className="p-1 glass-card rounded-lg hover:bg-white/10 transition-colors"
                    >
                      {copiedId === index ? (
                        <Check className="w-3 h-3 text-emerald-400" />
                      ) : (
                        <Copy className="w-3 h-3 text-white/60" />
                      )}
                    </button>
                    <button className="p-1 glass-card rounded-lg hover:bg-white/10 transition-colors">
                      <ThumbsUp className="w-3 h-3 text-white/60" />
                    </button>
                    <button className="p-1 glass-card rounded-lg hover:bg-white/10 transition-colors">
                      <ThumbsDown className="w-3 h-3 text-white/60" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        ))}
        
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full glass-card flex items-center justify-center">
                <Bot className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="glass-card rounded-2xl p-4">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="glass-card mx-6 mb-6 rounded-2xl p-4">
        <div className="flex gap-3">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your health..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-cyan-500 resize-none"
            rows="1"
          />
          <Button onClick={handleSend} disabled={isLoading || !message.trim()}>
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </Button>
        </div>
        <p className="text-xs text-white/40 mt-2 text-center">
          AI-generated information is not medical advice. Consult healthcare professionals for medical decisions.
        </p>
      </div>
    </div>
  )
}

export default HealthAIChat