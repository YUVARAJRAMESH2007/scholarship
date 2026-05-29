import React, { useState } from 'react';
import { createApplication } from '../services/api';
import { motion } from 'framer-motion';

const ApplicationForm = ({ onApplicationAdded }) => {
    const [formData, setFormData] = useState({
        student: '',
        program: '',
        approved_amount: '',
        status: 'pending'
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await createApplication(formData);
            alert('Application submitted successfully!');
            setFormData({ student: '', program: '', approved_amount: '', status: 'pending' });
            if (onApplicationAdded) onApplicationAdded();
        } catch (error) {
            alert('Failed to submit application. Please check console for details.');
        } finally {
            setLoading(false);
        }
    };

    const inputClasses = "w-full px-4 py-2 bg-background/50 border border-white/10 rounded-lg text-textMain focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-200";

    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-surface p-6 rounded-2xl shadow-glass border border-white/5 mb-8"
        >
            <h3 className="text-xl font-bold text-textMain mb-6 flex items-center gap-2">
                <span className="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center">➕</span>
                Create New Application
            </h3>
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-4 gap-6 items-end">
                <div>
                    <label className="block text-sm font-medium text-textMuted mb-1.5">Student ID</label>
                    <input 
                        type="number" 
                        name="student" 
                        className={inputClasses}
                        value={formData.student} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-textMuted mb-1.5">Program ID</label>
                    <input 
                        type="number" 
                        name="program" 
                        className={inputClasses}
                        value={formData.program} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-textMuted mb-1.5">Amount ($)</label>
                    <input 
                        type="number" 
                        name="approved_amount" 
                        className={inputClasses}
                        value={formData.approved_amount} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <motion.button 
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="submit" 
                    disabled={loading}
                    className={`w-full py-2 rounded-lg font-semibold text-white shadow-lg transition-colors duration-200 h-[42px] ${
                        loading ? 'bg-primary/70 cursor-not-allowed' : 'bg-primary hover:bg-primary/90'
                    }`}
                >
                    {loading ? 'Submitting...' : 'Submit'}
                </motion.button>
            </form>
        </motion.div>
    );
};

export default ApplicationForm;