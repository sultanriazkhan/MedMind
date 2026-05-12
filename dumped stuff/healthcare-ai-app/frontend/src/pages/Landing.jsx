import { useState, useEffect } from 'react'
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Activity, Brain, Heart, Stethoscope, Shield, Zap, 
  ChevronRight, Star, Menu, X, TrendingUp, Users, 
  Clock, Award, MessageCircle, FileText, Bell, 
  Sparkles, ArrowRight, Quote 
} from 'lucide-react'
import Button from '../components/ui/Button'

const Landing = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { scrollY } = useScroll()
  const opacity = useTransform(scrollY, [0, 300], [1, 0])
  const scale = useTransform(scrollY, [0, 300], [1, 0.95])
  
  const features = [
    { icon: Brain, title: 'AI-Powered Analysis', description: 'Advanced algorithms analyze medical reports with 99.9% accuracy', color: 'from-cyan-500 to-blue-500' },
    { icon: Activity, title: 'Real-time Monitoring', description: 'Track your health metrics and receive instant alerts', color: 'from-emerald-500 to-teal-500' },
    { icon: Shield, title: 'HIPAA Compliant', description: 'Enterprise-grade security for your medical data', color: 'from-purple-500 to-pink-500' },
    { icon: Zap, title: 'Instant Insights', description: 'Get actionable health recommendations in seconds', color: 'from-orange-500 to-red-500' },
  ]
  
  const testimonials = [
    { name: 'Dr. Sarah Johnson', role: 'Cardiologist', content: 'Revolutionary platform that saves hours of manual analysis daily.', avatar: '👩‍⚕️', rating: 5 },
    { name: 'Michael Chen', role: 'Patient', content: 'Finally understood my lab results! The explanations are crystal clear.', avatar: '👨', rating: 5 },
    { name: 'Dr. Emily Rodriguez', role: 'Researcher', content: 'The accuracy and speed of analysis is unparalleled in the industry.', avatar: '👩‍🔬', rating: 5 },
  ]
  
  const stats = [
    { icon: Users, value: '50K+', label: 'Active Users' },
    { icon: FileText, value: '100K+', label: 'Reports Analyzed' },
    { icon: Clock, value: '<2min', label: 'Avg Analysis Time' },
    { icon: Award, value: '99.9%', label: 'Accuracy Rate' },
  ]
  
  const faqs = [
    { q: 'How accurate is the AI analysis?', a: 'Our AI achieves 99.9% accuracy through continuous learning from millions of medical reports.' },
    { q: 'Is my data secure?', a: 'Yes, we use bank-level encryption and comply with all healthcare data protection regulations.' },
    { q: 'Can I share reports with my doctor?', a: 'Absolutely! You can easily share reports and insights with your healthcare providers.' },
    { q: 'What file formats are supported?', a: 'We support PDF, DOCX, TXT, and image formats for medical reports.' },
  ]
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900 overflow-hidden">
      <motion.nav 
        style={{ opacity, scale }}
        className="fixed top-0 left-0 right-0 z-50 glass-card m-4 rounded-2xl"
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2"
            >
              <div className="gradient-bg rounded-xl p-2">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
                MediScan AI
              </span>
            </motion.div>
            
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-white/80 hover:text-white transition-colors">Features</a>
              <a href="#testimonials" className="text-white/80 hover:text-white transition-colors">Testimonials</a>
              <a href="#faq" className="text-white/80 hover:text-white transition-colors">FAQ</a>
              <Link to="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link to="/signup">
                <Button>Get Started</Button>
              </Link>
            </div>
            
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden text-white"
            >
              {isMenuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </motion.nav>
      
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed top-24 left-4 right-4 z-40 glass-card rounded-2xl p-6 md:hidden"
          >
            <div className="flex flex-col gap-4">
              <a href="#features" className="text-white/80 hover:text-white">Features</a>
              <a href="#testimonials" className="text-white/80 hover:text-white">Testimonials</a>
              <a href="#faq" className="text-white/80 hover:text-white">FAQ</a>
              <Link to="/login" className="text-white/80 hover:text-white">Sign In</Link>
              <Link to="/signup">
                <Button className="w-full">Get Started</Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      <section className="relative min-h-screen flex items-center pt-20">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl floating" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl floating" style={{ animationDelay: '2s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-128 h-128 bg-primary-500/10 rounded-full blur-3xl" />
        </div>
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full mb-6">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span className="text-sm text-white/90">AI-Powered Healthcare Platform</span>
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold mb-6">
                <span className="bg-gradient-to-r from-cyan-400 via-emerald-400 to-cyan-400 bg-clip-text text-transparent bg-300% animate-gradient">
                  Intelligent Medical
                </span>
                <br />
                Report Analysis
              </h1>
              
              <p className="text-xl text-white/70 mb-8">
                Transform your lab reports into actionable health insights with advanced AI technology. 
                Understand your results instantly and make informed decisions about your health.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <Link to="/signup">
                  <Button size="lg" className="group">
                    Start Free Trial
                    <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="lg">Watch Demo</Button>
                </Link>
              </div>
              
              <div className="flex items-center gap-8 mt-8">
                <div className="flex -space-x-2">
                  {[1,2,3,4].map(i => (
                    <div key={i} className="w-10 h-10 rounded-full gradient-bg flex items-center justify-center text-white font-bold border-2 border-navy-800">
                      {i}
                    </div>
                  ))}
                </div>
                <div>
                  <div className="flex text-yellow-400">
                    {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
                  </div>
                  <p className="text-white/60 text-sm">Trusted by 50,000+ users</p>
                </div>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="glass-card p-6 rounded-2xl relative z-10">
                <div className="flex items-center gap-4 mb-6">
                  <div className="gradient-bg rounded-xl p-3">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-white/60 text-sm">Latest Analysis</p>
                    <p className="text-white font-semibold">Complete Blood Count</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  {['Hemoglobin', 'White Blood Cells', 'Platelets'].map((test, i) => (
                    <motion.div 
                      key={test}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex justify-between items-center p-3 bg-white/5 rounded-xl"
                    >
                      <span className="text-white">{test}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-white/80">{['14.2', '7.5', '250'][i]} {['g/dL', 'K/µL', 'K/µL'][i]}</span>
                        <div className={`px-2 py-1 rounded-lg text-xs font-semibold ${
                          i === 0 ? 'bg-emerald-500/20 text-emerald-400' : 
                          i === 1 ? 'bg-cyan-500/20 text-cyan-400' : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {['Normal', 'Normal', 'Borderline'][i]}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
              
              <div className="absolute -top-4 -right-4 w-32 h-32 gradient-bg rounded-full filter blur-2xl opacity-50" />
            </motion.div>
          </div>
        </div>
      </section>
      
      <section id="features" className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              Powerful Features
            </h2>
            <p className="text-xl text-white/70 max-w-2xl mx-auto">
              Everything you need to understand and manage your health data effectively
            </p>
          </motion.div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
                className="glass-card-dark p-6 rounded-2xl hover:shadow-2xl transition-all duration-300"
              >
                <div className={`gradient-bg w-14 h-14 rounded-xl flex items-center justify-center mb-4`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      <section className="py-20 relative">
        <div className="container mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full mb-6">
                <MessageCircle className="w-4 h-4 text-cyan-400" />
                <span className="text-sm text-white/90">AI Assistant</span>
              </div>
              <h2 className="text-4xl font-bold mb-4 text-white">
                Meet Your Personal
                <span className="gradient-bg bg-clip-text text-transparent"> Health AI</span>
              </h2>
              <p className="text-white/70 mb-6 text-lg">
                Chat with our advanced AI assistant to get instant answers about your health reports, 
                medication interactions, and lifestyle recommendations tailored just for you.
              </p>
              <div className="space-y-4">
                {['24/7 availability', 'Evidence-based responses', 'Multi-language support'].map((feature, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded-full gradient-bg flex items-center justify-center">
                      <ChevronRight className="w-4 h-4 text-white" />
                    </div>
                    <span className="text-white/80">{feature}</span>
                  </div>
                ))}
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="glass-card p-6 rounded-2xl">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 gradient-bg rounded-full flex items-center justify-center">
                    <Brain className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-semibold">AI Health Assistant</p>
                    <p className="text-white/60 text-sm">Online • Ready to help</p>
                  </div>
                </div>
                
                <div className="space-y-4 mb-6 max-h-80 overflow-y-auto">
                  <div className="flex gap-3">
                    <div className="w-8 h-8 gradient-bg rounded-full flex items-center justify-center flex-shrink-0">
                      <Brain className="w-4 h-4 text-white" />
                    </div>
                    <div className="glass-card p-3 rounded-2xl max-w-[80%]">
                      <p className="text-white text-sm">Hello! I can help you understand your medical reports. What would you like to know?</p>
                    </div>
                  </div>
                  
                  <div className="flex gap-3 justify-end">
                    <div className="glass-card-dark p-3 rounded-2xl max-w-[80%]">
                      <p className="text-white text-sm">What do my cholesterol numbers mean?</p>
                    </div>
                  </div>
                  
                  <div className="flex gap-3">
                    <div className="w-8 h-8 gradient-bg rounded-full flex items-center justify-center flex-shrink-0">
                      <Brain className="w-4 h-4 text-white" />
                    </div>
                    <div className="glass-card p-3 rounded-2xl max-w-[80%]">
                      <p className="text-white text-sm">Cholesterol consists of LDL (bad), HDL (good), and triglycerides. Optimal ranges: LDL &lt;100, HDL &gt;40, Triglycerides &lt;150. Your levels appear within normal range!</p>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-3">
                  <input 
                    type="text" 
                    placeholder="Ask about your health..."
                    className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-cyan-500"
                  />
                  <Button className="px-4">
                    <ArrowRight className="w-5 h-5" />
                  </Button>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
      
      <section id="testimonials" className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
              What Our Users Say
            </h2>
            <p className="text-xl text-white/70">Join thousands of satisfied users worldwide</p>
          </motion.div>
          
          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className="glass-card-dark p-6 rounded-2xl"
              >
                <Quote className="w-8 h-8 text-cyan-400 mb-4 opacity-50" />
                <p className="text-white/80 mb-6 leading-relaxed">{testimonial.content}</p>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 gradient-bg rounded-full flex items-center justify-center text-2xl">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <p className="text-white font-semibold">{testimonial.name}</p>
                    <p className="text-white/60 text-sm">{testimonial.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      <section className="py-20 relative">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card text-center p-6 rounded-2xl"
              >
                <stat.icon className="w-10 h-10 text-cyan-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-white/60">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      <section id="faq" className="py-20 relative">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-white/70">Everything you need to know about our platform</p>
          </motion.div>
          
          <div className="max-w-3xl mx-auto space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card-dark p-6 rounded-2xl cursor-pointer group"
              >
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-white group-hover:text-cyan-400 transition-colors">
                    {faq.q}
                  </h3>
                  <ChevronRight className="w-5 h-5 text-white/40 group-hover:rotate-90 transition-transform duration-300" />
                </div>
                <div className="mt-3 text-white/60">
                  {faq.a}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      <footer className="glass-card mt-20 mx-6 mb-6 rounded-2xl">
        <div className="container mx-auto px-6 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Heart className="w-6 h-6 text-cyan-400" />
                <span className="text-xl font-bold text-white">MediScan AI</span>
              </div>
              <p className="text-white/60">Intelligent healthcare analytics powered by AI</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2 text-white/60">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-white/60">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-white/60">
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">HIPAA</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-white/10 pt-8 text-center text-white/40">
            <p>&copy; 2024 MediScan AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Landing