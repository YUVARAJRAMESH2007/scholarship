import React, { useState, useEffect } from 'react';
import Login from './components/login';
import Register from './components/register';
import StudentDashboard from './components/StudentDashboard';
import AdminDashboard from './components/admindashboard';
import { AnimatePresence, motion } from 'framer-motion';

function App() {
  const [role, setRole] = useState(null);
  const [authView, setAuthView] = useState('login');

  useEffect(() => {
    const savedRole = localStorage.getItem('role');
    if (savedRole) {
      setRole(savedRole);
    }
  }, []);

  const handleAuthSuccess = (userRole) => {
    setRole(userRole);
  };

  const handleLogout = () => {
    localStorage.clear();
    setRole(null);
    setAuthView('login');
  };

  const renderAuthScreen = () => {
    if (authView === 'login') {
      return (
        <Login 
          key="login"
          onLoginSuccess={handleAuthSuccess} 
          onSwitchToRegister={() => setAuthView('register')} 
        />
      );
    } else {
      return (
        <Register 
          key="register"
          onRegisterSuccess={(role) => {
            window.location.reload(); 
          }} 
          onSwitchToLogin={() => setAuthView('login')} 
        />
      );
    }
  };

  // Particles/Matrix effect wrapper
  const renderBackgroundEffects = () => (
    <div className="fixed inset-0 pointer-events-none z-[-1] overflow-hidden opacity-30">
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 bg-gradient-to-b from-transparent via-[#00ffaa] to-transparent h-32"
          initial={{
            x: Math.random() * window.innerWidth,
            y: -200,
            opacity: Math.random() * 0.5 + 0.2
          }}
          animate={{
            y: window.innerHeight + 200,
          }}
          transition={{
            duration: Math.random() * 5 + 3,
            repeat: Infinity,
            ease: "linear",
            delay: Math.random() * 5
          }}
        />
      ))}
    </div>
  );

  return (
    <div className="min-h-screen rgb-gradient-bg text-textMain font-sans flex flex-col items-center justify-center p-4 relative z-0">
      {renderBackgroundEffects()}
      
      <AnimatePresence mode="wait">
        {!role ? (
          <motion.div
            key="auth"
            initial={{ opacity: 0, rotateX: 90, z: -500 }}
            animate={{ opacity: 1, rotateX: 0, z: 0 }}
            exit={{ opacity: 0, rotateX: -90, z: -500 }}
            transition={{ duration: 0.8, type: "spring", bounce: 0.5 }}
            className="w-full max-w-md perspective-1000"
            style={{ perspective: 1000 }}
          >
            {renderAuthScreen()}
          </motion.div>
        ) : role === 'student' ? (
          <motion.div
            key="student"
            initial={{ opacity: 0, scale: 0.8, filter: 'blur(10px)' }}
            animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
            exit={{ opacity: 0, scale: 1.2, filter: 'blur(10px)' }}
            transition={{ duration: 0.6, type: "spring" }}
            className="w-full h-full"
          >
            <StudentDashboard onLogout={handleLogout} />
          </motion.div>
        ) : (
          <motion.div
            key="admin"
            initial={{ opacity: 0, scale: 0.8, filter: 'blur(10px)' }}
            animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
            exit={{ opacity: 0, scale: 1.2, filter: 'blur(10px)' }}
            transition={{ duration: 0.6, type: "spring" }}
            className="w-full h-full"
          >
            <AdminDashboard onLogout={handleLogout} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;