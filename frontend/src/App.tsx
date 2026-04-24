import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import RegisterMember from './pages/RegisterMember'
import RegisterCoach from './pages/RegisterCoach'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register/member" element={<RegisterMember />} />
          <Route path="/register/coach" element={<RegisterCoach />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
