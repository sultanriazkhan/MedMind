import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

console.log('App starting...')

const rootElement = document.getElementById('root')
console.log('Root element:', rootElement)

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
  console.log('App rendered successfully')
} else {
  console.error('Root element not found!')
  document.body.innerHTML = '<h1 style="color:red">Error: Root element not found</h1>'
}