import React, { useState } from 'react';
import { registerUser } from '../services/api';
import { motion } from 'framer-motion';

const Register = ({ onRegisterSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        student_id: '',
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');

        if (!formData.email.includes('@')) {
            setError('INVALID_EMAIL: Email address must contain "@" symbol.');
            return;
        }

        const passwordRegex = /^(?=.*[0-9]).{8,}$/;
        if (!passwordRegex.test(formData.password)) {
            setError('SECURITY_WARNING: Password must be at least 8 characters long and contain at least one number.');
            return;
        }

        setLoading(true);
        try {
            const data = await registerUser(formData);
            
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            localStorage.setItem('username', data.username); 
            
            if (data.student_profile_id) {
                localStorage.setItem('student_profile_id', data.student_profile_id); 
            }
            
            onRegisterSuccess(data.role);
        } catch (err) {
            if (err.response && err.response.data) {
                const errorMessages = Object.values(err.response.data).flat().join(' ');
                if (errorMessages.toLowerCase().includes('username') && errorMessages.toLowerCase().includes('already exists')) {
                    setError('ACCESS_DENIED: Username already exists. Please choose a different alias.');
                } else {
                    setError(errorMessages || 'Failed to register. Please check your details.');
                }
            } else {
                setError('Network error. Database connection failed.');
            }
        } finally {
            setLoading(false);
        }
    };

    const inputClasses = "w-full px-4 py-3 bg-[#0a0a0f]/80 border border-[#333] rounded-sm text-white font-mono focus:input-rgb-focus transition-all duration-300 outline-none";
    const labelClasses = "block text-xs font-mono tracking-widest text-[#00ffaa] mb-2 uppercase group-hover:text-white transition-colors";

    return (
        <motion.div 
            className="w-full max-w-lg mx-auto p-[2px] rounded-2xl animate-rgb-border"
            whileHover={{ scale: 1.01 }}
            transition={{ type: "spring", stiffness: 300 }}
        >
            <div className="w-full p-8 glass-card rounded-2xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#ff0055] via-[#00ffaa] to-[#5500ff] opacity-50"></div>
                
                <div className="text-center mb-8">
                    <h2 className="text-4xl font-black uppercase tracking-[0.2em] animate-rgb-text mb-2">NEW_ENTITY</h2>
                    <p className="text-[#a0aab5] font-mono text-sm tracking-widest">[ REGISTRATION_PROTOCOL ]</p>
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
                
                <form onSubmit={handleRegister} className="flex flex-col gap-5">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div className="relative group">
                            <label className={labelClasses}>Full_Name</label>
                            <input type="text" name="name" className={inputClasses} value={formData.name} onChange={handleChange} required placeholder="John Doe" />
                        </div>
                        <div className="relative group">
                            <label className={labelClasses}>Student_ID</label>
                            <input type="text" name="student_id" className={inputClasses} value={formData.student_id} onChange={handleChange} required placeholder="STU-001" />
                        </div>
                    </div>
                    <div className="relative group">
                        <label className={labelClasses}>Email_Address</label>
                        <input type="email" name="email" className={inputClasses} value={formData.email} onChange={handleChange} required placeholder="user@network.com" />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div className="relative group">
                            <label className={labelClasses}>Username</label>
                            <input type="text" name="username" className={inputClasses} value={formData.username} onChange={handleChange} required placeholder="Alias" />
                        </div>
                        <div className="relative group">
                            <label className={labelClasses}>Password</label>
                            <input type="password" name="password" className={inputClasses} value={formData.password} onChange={handleChange} required placeholder="••••••••" />
                        </div>
                    </div>
                    
                    <motion.button 
                        whileHover={{ 
                            scale: 1.03, 
                            boxShadow: "0px 0px 20px rgba(85, 0, 255, 0.8)",
                            textShadow: "0px 0px 8px rgba(255,255,255,0.8)"
                        }}
                        whileTap={{ scale: 0.95 }}
                        type="submit" 
                        disabled={loading}
                        className={`w-full py-4 mt-6 rounded-sm font-black tracking-widest uppercase transition-all duration-300 ${
                            loading ? 'bg-[#333] text-gray-500 cursor-not-allowed' : 'bg-gradient-to-r from-[#5500ff] to-[#ff0055] text-white hover:from-[#ff0055] hover:to-[#00ffaa] hover:text-black'
                        }`}
                    >
                        {loading ? 'PROCESSING...' : 'EXECUTE_REGISTRATION'}
                    </motion.button>
                </form>

                <div className="text-center mt-6 font-mono text-xs text-[#a0aab5]">
                    <p>EXISTING ENTITY?{' '}
                        <button onClick={onSwitchToLogin} className="text-[#00ffaa] hover:text-[#ff0055] font-bold tracking-wider hover:underline transition-colors">
                            [ RETURN_TO_LOGIN ]
                        </button>
                    </p>
                </div>
            </div>
        </motion.div>
    );
};

export default Register;