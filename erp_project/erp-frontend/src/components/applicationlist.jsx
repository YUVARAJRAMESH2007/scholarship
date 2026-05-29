import React, { useEffect, useState } from 'react';
import { getApplications } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';

const ApplicationsList = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getApplications();
                setApplications(data);
                setLoading(false);
            } catch (err) {
                setError('Failed to load applications.');
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-40">
                <motion.div 
                    animate={{ rotate: 360 }} 
                    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    className="w-10 h-10 border-4 border-secondary border-t-transparent rounded-full"
                />
            </div>
        );
    }
    
    if (error) {
        return (
            <motion.div 
                initial={{ opacity: 0, x: -10 }} 
                animate={{ opacity: 1, x: 0 }}
                className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 font-medium mb-6"
            >
                {error}
            </motion.div>
        );
    }

    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-surface rounded-2xl shadow-glass border border-white/5 overflow-hidden mb-8"
        >
            <div className="p-6 border-b border-white/10">
                <h2 className="text-xl font-bold text-textMain flex items-center gap-2">
                    <span className="w-8 h-8 rounded-full bg-secondary/20 text-secondary flex items-center justify-center">📋</span>
                    Scholarship Applications
                </h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse min-w-[700px]">
                    <thead>
                        <tr className="bg-white/5 text-textMuted text-sm uppercase tracking-wider">
                            <th className="px-6 py-4 font-semibold border-b border-white/10">ID</th>
                            <th className="px-6 py-4 font-semibold border-b border-white/10">Student ID</th>
                            <th className="px-6 py-4 font-semibold border-b border-white/10">Program ID</th>
                            <th className="px-6 py-4 font-semibold border-b border-white/10">Status</th>
                            <th className="px-6 py-4 font-semibold border-b border-white/10">Applied On</th>
                            <th className="px-6 py-4 font-semibold border-b border-white/10">Approved Amount</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                        <AnimatePresence>
                            {applications.map((app, index) => (
                                <motion.tr 
                                    key={app.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    className="hover:bg-white/5 transition-colors"
                                >
                                    <td className="px-6 py-4 text-textMuted">#{app.id}</td>
                                    <td className="px-6 py-4 font-mono text-sm">{app.student}</td>
                                    <td className="px-6 py-4 font-mono text-sm">{app.program}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full ${
                                            app.status === 'approved' || app.status === 'success' 
                                            ? 'bg-green-500/10 text-green-400 border border-green-500/20' 
                                            : app.status === 'pending'
                                            ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                                            : 'bg-red-500/10 text-red-400 border border-red-500/20'
                                        }`}>
                                            {app.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-textMuted">{app.applied_on}</td>
                                    <td className="px-6 py-4 font-bold text-textMain">
                                        {app.approved_amount !== "0.00" ? <span className="text-green-400">${app.approved_amount}</span> : '-'}
                                    </td>
                                </motion.tr>
                            ))}
                        </AnimatePresence>
                        {applications.length === 0 && (
                            <tr>
                                <td colSpan="6" className="px-6 py-8 text-center text-textMuted">No applications found.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </motion.div>
    );
};

export default ApplicationsList;