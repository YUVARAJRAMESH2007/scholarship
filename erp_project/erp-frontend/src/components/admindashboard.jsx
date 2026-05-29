import React, { useEffect, useState } from 'react';
import { getApplications, updateApplication, getStudents, deleteStudent } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';

const AdminDashboard = ({ onLogout }) => {
    const [applications, setApplications] = useState([]);
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [amounts, setAmounts] = useState({});

    const fetchAdminData = async () => {
        try {
            const appsData = await getApplications();
            const studentsData = await getStudents();
            setApplications(appsData);
            setStudents(studentsData);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching admin data", error);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAdminData();
    }, []);

    const handleAmountChange = (id, value) => {
        setAmounts({ ...amounts, [id]: value });
    };

    const handleProcessAction = async (id, nextStatus) => {
        const selectedAmount = amounts[id] || "0.00";
        if (nextStatus === 'approved' && (parseFloat(selectedAmount) <= 0 || isNaN(parseFloat(selectedAmount)))) {
            alert("Please input a valid scholarship disbursement amount before approval.");
            return;
        }

        try {
            const payload = {
                status: nextStatus,
                approved_amount: nextStatus === 'approved' ? parseFloat(selectedAmount).toFixed(2) : "0.00"
            };
            await updateApplication(id, payload);
            setAmounts({ ...amounts, [id]: '' });
            fetchAdminData();
        } catch (error) {
            alert("Failed to update application state on the server.");
        }
    };

    const handleDeleteUser = async (studentId) => {
        if (window.confirm("Are you sure you want to permanently delete this user? This cannot be undone.")) {
            try {
                await deleteStudent(studentId);
                fetchAdminData();
            } catch (error) {
                alert("Failed to delete user.");
            }
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center space-y-4">
                <motion.div 
                    animate={{ rotate: 360 }} 
                    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    className="w-12 h-12 border-4 border-secondary border-t-transparent rounded-full"
                />
                <h2 className="text-textMuted font-medium tracking-wider">Loading Admin Workspace...</h2>
            </div>
        );
    }

    const pendingApps = applications.filter(app => app.status === 'pending');
    const processedApps = applications.filter(app => app.status !== 'pending');

    const cardVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
    };

    return (
        <motion.div 
            initial="hidden"
            animate="visible"
            variants={{
                hidden: { opacity: 0 },
                visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
            }}
            className="w-full max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8"
        >
            {/* Header */}
            <motion.div variants={cardVariants} className="flex flex-col sm:flex-row justify-between items-center mb-8 pb-6 border-b border-white/10">
                <div>
                    <h2 className="text-3xl font-bold text-secondary">NSP Admin Control Center</h2>
                    <p className="text-textMuted mt-1">Manage users, applications, and disbursements</p>
                </div>
                <motion.button 
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={onLogout} 
                    className="mt-4 sm:mt-0 px-6 py-2.5 bg-red-500/10 hover:bg-red-500 hover:text-white text-red-500 border border-red-500/50 rounded-lg font-bold transition-all duration-300"
                >
                    Secure Logout
                </motion.button>
            </motion.div>

            {/* Top Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                <motion.div variants={cardVariants} whileHover={{ y: -5 }} className="bg-surface p-6 rounded-2xl shadow-glass border border-white/5">
                    <h3 className="text-sm font-semibold text-textMuted uppercase tracking-wider mb-2">Total Registered Users</h3>
                    <p className="text-4xl font-bold text-green-400">{students.length}</p>
                </motion.div>
                <motion.div variants={cardVariants} whileHover={{ y: -5 }} className="bg-surface p-6 rounded-2xl shadow-glass border border-white/5">
                    <h3 className="text-sm font-semibold text-textMuted uppercase tracking-wider mb-2">Total Applications</h3>
                    <p className="text-4xl font-bold text-secondary">{applications.length}</p>
                </motion.div>
                <motion.div variants={cardVariants} whileHover={{ y: -5 }} className="bg-surface p-6 rounded-2xl shadow-glass border border-white/5">
                    <h3 className="text-sm font-semibold text-textMuted uppercase tracking-wider mb-2">Pending Verifications</h3>
                    <p className="text-4xl font-bold text-yellow-500">{pendingApps.length}</p>
                </motion.div>
            </div>

            {/* User Management Section */}
            <motion.div variants={cardVariants} className="mb-12">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-1.5 h-6 bg-green-500 rounded-full"></div>
                    <h3 className="text-xl font-bold text-textMain">User Management</h3>
                </div>
                <div className="bg-surface rounded-2xl overflow-hidden shadow-glass border border-white/5 overflow-x-auto">
                    <table className="w-full text-left border-collapse min-w-[800px]">
                        <thead>
                            <tr className="bg-white/5 text-textMuted text-sm uppercase tracking-wider border-b border-white/10">
                                <th className="px-6 py-4 font-semibold">DB ID</th>
                                <th className="px-6 py-4 font-semibold">Full Name</th>
                                <th className="px-6 py-4 font-semibold">Student ID</th>
                                <th className="px-6 py-4 font-semibold">Email</th>
                                <th className="px-6 py-4 font-semibold">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/10">
                            <AnimatePresence>
                                {students.map((student) => (
                                    <motion.tr 
                                        key={student.id} 
                                        initial={{ opacity: 0, height: 0 }} 
                                        animate={{ opacity: 1, height: 'auto' }} 
                                        exit={{ opacity: 0, height: 0 }}
                                        className="hover:bg-white/5 transition-colors"
                                    >
                                        <td className="px-6 py-4 text-textMuted">{student.id}</td>
                                        <td className="px-6 py-4 font-semibold text-textMain">{student.name}</td>
                                        <td className="px-6 py-4 font-mono text-sm">{student.student_id}</td>
                                        <td className="px-6 py-4 text-textMuted">{student.email}</td>
                                        <td className="px-6 py-4">
                                            <motion.button 
                                                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                                                onClick={() => handleDeleteUser(student.id)}
                                                className="px-4 py-1.5 text-sm font-medium text-red-400 bg-red-400/10 hover:bg-red-400 hover:text-white rounded-md transition-colors"
                                            >
                                                Remove
                                            </motion.button>
                                        </td>
                                    </motion.tr>
                                ))}
                            </AnimatePresence>
                            {students.length === 0 && (
                                <tr>
                                    <td colSpan="5" className="px-6 py-8 text-center text-textMuted">No users found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </motion.div>

            {/* Pending Applications Section */}
            <motion.div variants={cardVariants} className="mb-12">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-1.5 h-6 bg-yellow-500 rounded-full"></div>
                    <h3 className="text-xl font-bold text-textMain">Pending Verifications</h3>
                </div>
                <div className="bg-surface rounded-2xl overflow-hidden shadow-glass border border-white/5 overflow-x-auto">
                    <table className="w-full text-left border-collapse min-w-[900px]">
                        <thead>
                            <tr className="bg-white/5 text-textMuted text-sm uppercase tracking-wider border-b border-white/10">
                                <th className="px-6 py-4 font-semibold">App ID</th>
                                <th className="px-6 py-4 font-semibold">Applicant</th>
                                <th className="px-6 py-4 font-semibold">Program</th>
                                <th className="px-6 py-4 font-semibold">Date</th>
                                <th className="px-6 py-4 font-semibold">Amount ($)</th>
                                <th className="px-6 py-4 font-semibold">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/10">
                            <AnimatePresence>
                                {pendingApps.map((app) => {
                                    const applicantName = students.find(s => s.id === app.student)?.name || 'Unknown';
                                    return (
                                    <motion.tr 
                                        key={app.id} 
                                        initial={{ opacity: 0, height: 0 }} 
                                        animate={{ opacity: 1, height: 'auto' }} 
                                        exit={{ opacity: 0, x: -100 }}
                                        className="hover:bg-white/5 transition-colors"
                                    >
                                        <td className="px-6 py-4 text-textMuted">#{app.id}</td>
                                        <td className="px-6 py-4 font-semibold text-textMain">{applicantName}</td>
                                        <td className="px-6 py-4 font-mono text-sm">{app.program}</td>
                                        <td className="px-6 py-4 text-textMuted">{app.applied_on}</td>
                                        <td className="px-6 py-4">
                                            <input 
                                                type="number" 
                                                placeholder="0.00"
                                                className="w-24 px-3 py-1.5 bg-background/50 border border-white/10 rounded-md text-textMain focus:outline-none focus:ring-1 focus:ring-secondary text-center"
                                                value={amounts[app.id] || ''}
                                                onChange={(e) => handleAmountChange(app.id, e.target.value)}
                                            />
                                        </td>
                                        <td className="px-6 py-4 flex gap-2">
                                            <motion.button 
                                                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                                                onClick={() => handleProcessAction(app.id, 'approved')}
                                                className="px-4 py-1.5 text-sm font-bold text-white bg-green-500 hover:bg-green-600 rounded-md transition-colors shadow-lg shadow-green-500/20"
                                            >
                                                Approve
                                            </motion.button>
                                            <motion.button 
                                                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                                                onClick={() => handleProcessAction(app.id, 'rejected')}
                                                className="px-4 py-1.5 text-sm font-bold text-white bg-red-500 hover:bg-red-600 rounded-md transition-colors shadow-lg shadow-red-500/20"
                                            >
                                                Reject
                                            </motion.button>
                                        </td>
                                    </motion.tr>
                                )})}
                            </AnimatePresence>
                            {pendingApps.length === 0 && (
                                <tr>
                                    <td colSpan="6" className="px-6 py-8 text-center text-textMuted">No pending applications.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </motion.div>

            {/* Processed Applications Archive */}
            <motion.div variants={cardVariants} className="mb-8">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-1.5 h-6 bg-secondary rounded-full"></div>
                    <h3 className="text-xl font-bold text-textMain">Processed Records Archive</h3>
                </div>
                <div className="bg-surface rounded-2xl overflow-hidden shadow-glass border border-white/5 overflow-x-auto">
                    <table className="w-full text-left border-collapse min-w-[800px]">
                        <thead>
                            <tr className="bg-white/5 text-textMuted text-sm uppercase tracking-wider border-b border-white/10">
                                <th className="px-6 py-4 font-semibold">App ID</th>
                                <th className="px-6 py-4 font-semibold">Applicant</th>
                                <th className="px-6 py-4 font-semibold">Program</th>
                                <th className="px-6 py-4 font-semibold">Date</th>
                                <th className="px-6 py-4 font-semibold">Status</th>
                                <th className="px-6 py-4 font-semibold">Amount</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/10">
                            <AnimatePresence>
                                {processedApps.map((app, index) => {
                                    const applicantName = students.find(s => s.id === app.student)?.name || 'Unknown';
                                    return(
                                    <motion.tr 
                                        key={app.id} 
                                        initial={{ opacity: 0, y: 10 }} 
                                        animate={{ opacity: 1, y: 0 }} 
                                        transition={{ delay: index * 0.05 }}
                                        className="hover:bg-white/5 transition-colors"
                                    >
                                        <td className="px-6 py-4 text-textMuted">#{app.id}</td>
                                        <td className="px-6 py-4 font-semibold text-textMain">{applicantName}</td>
                                        <td className="px-6 py-4 font-mono text-sm">{app.program}</td>
                                        <td className="px-6 py-4 text-textMuted">{app.applied_on}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full ${
                                                app.status === 'approved' || app.status === 'success' 
                                                ? 'bg-green-500/10 text-green-400 border border-green-500/20' 
                                                : 'bg-red-500/10 text-red-400 border border-red-500/20'
                                            }`}>
                                                {app.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 font-bold text-textMain">
                                            {app.approved_amount !== "0.00" ? <span className="text-green-400">${app.approved_amount}</span> : '-'}
                                        </td>
                                    </motion.tr>
                                )})}
                            </AnimatePresence>
                            {processedApps.length === 0 && (
                                <tr>
                                    <td colSpan="6" className="px-6 py-8 text-center text-textMuted">No applications have been processed yet.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </motion.div>
        </motion.div>
    );
};

export default AdminDashboard;