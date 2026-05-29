import React, { useState } from 'react';
import { loginUser } from '../services/api';
import { motion } from 'framer-motion';

const Login = ({ onLoginSuccess, onSwitchToRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const data = await loginUser(username, password);
            
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            localStorage.setItem('username', data.username);
            if (data.student_profile_id) {
                localStorage.setItem('student_profile_id', data.student_profile_id);
            }

            onLoginSuccess(data.role);
        } catch (err) {
            setError('Invalid username or password. System access denied.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div 
            className="w-full max-w-md mx-auto p-[2px] rounded-2xl animate-rgb-border"
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 300 }}
        >
            <div className="w-full p-8 glass-card rounded-2xl relative overflow-hidden">
                {/* Cyberpunk accent lines */}
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#ff0055] via-[#00ffaa] to-[#5500ff] opacity-50"></div>
                <div className="absolute bottom-0 right-0 w-full h-1 bg-gradient-to-l from-[#ff0055] via-[#00ffaa] to-[#5500ff] opacity-50"></div>

                <div className="text-center mb-8">
                    <h2 className="text-4xl font-black uppercase tracking-[0.2em] animate-rgb-text mb-2">NSP_PORTAL</h2>
                    <p className="text-[#a0aab5] font-mono text-sm tracking-widest">[ AUTH_REQUIRED ]</p>
                </div>
                
                {error && (
                    <motion.div 
                        initial={{ opacity: 0, x: -20 }} 
                        animate={{ opacity: 1, x: 0 }}
                        className="mb-6 p-3 bg-red-900/40 border-l-4 border-red-500 text-red-400 text-sm font-mono tracking-wider"
                    >
                        &gt; ERROR: {error}
                    </motion.div>
                )}
                
                <form onSubmit={handleLogin} className="flex flex-col gap-6">
                    <div className="relative group">
                        <label className="block text-xs font-mono tracking-widest text-[#00ffaa] mb-2 uppercase group-hover:text-white transition-colors">Username_</label>
                        <input 
                            type="text" 
                            className="w-full px-4 py-3 bg-[#0a0a0f]/80 border border-[#333] rounded-sm text-white font-mono focus:input-rgb-focus transition-all duration-300"
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)} 
                            required 
                            placeholder="Enter credentials..."
                            style={{ outline: 'none' }}
                        />
                    </div>
                    <div className="relative group">
                        <label className="block text-xs font-mono tracking-widest text-[#00ffaa] mb-2 uppercase group-hover:text-white transition-colors">Password_</label>
                        <input 
                            type="password" 
                            className="w-full px-4 py-3 bg-[#0a0a0f]/80 border border-[#333] rounded-sm text-white font-mono focus:input-rgb-focus transition-all duration-300"
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required 
                            placeholder="••••••••"
                            style={{ outline: 'none' }}
                        />
                    </div>
                    
                    <motion.button 
                        whileHover={{ 
                            scale: 1.05, 
                            boxShadow: "0px 0px 20px rgba(0, 255, 170, 0.8)",
                            textShadow: "0px 0px 8px rgba(255,255,255,0.8)"
                        }}
                        whileTap={{ scale: 0.95 }}
                        type="submit" 
                        disabled={loading}
                        className={`w-full py-4 mt-4 rounded-sm font-black tracking-widest uppercase transition-all duration-300 ${
                            loading ? 'bg-[#333] text-gray-500 cursor-not-allowed' : 'bg-gradient-to-r from-[#00ffaa] to-[#00bfff] text-black hover:from-[#00bfff] hover:to-[#5500ff] hover:text-white'
                        }`}
                    >
                        {loading ? 'AUTHENTICATING...' : 'INITIALIZE_LOGIN'}
                    </motion.button>
                </form>

                <div className="text-center mt-8 font-mono text-xs text-[#a0aab5]">
                    <p>UNREGISTERED ENTITY?{' '}
                        <button 
                            onClick={(e) => { e.preventDefault(); onSwitchToRegister(); }} 
                            className="text-[#ff0055] hover:text-[#00ffaa] font-bold tracking-wider hover:underline transition-colors"
                        >
                            [ CREATE_ACCOUNT ]
                        </button>
                    </p>
                </div>
            </div>
        </motion.div>
    );
};

export default Login;