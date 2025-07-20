import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Items from './pages/Items'
import Upload from './pages/Upload'
import Home from './pages/Home'

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/upload">Upload</Link>
        <Link to="/items">Items</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="/upload" element={<Upload/>}></Route>
        <Route path="/items" element={<Items/>}></Route>
      </Routes>
    </Router>
  )
}
// from here, study router, routes and links
export default App
