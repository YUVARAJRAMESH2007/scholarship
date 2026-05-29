import React, { useEffect, useState } from 'react';
import { getPrograms, getApplications, createApplication } from '../services/api';
import { motion } from 'framer-motion';

const StudentDashboard = ({ onLogout }) => {
    const [programs, setPrograms] = useState([]);
    const [myApplications, setMyApplications] = useState([]);
    const [loading, setLoading] = useState(true);

    const studentProfileId = parseInt(localStorage.getItem('student_profile_id'));
    const username = localStorage.getItem('username');

    const fetchData = async () => {
        try {
            const programsData = await getPrograms();
            const appsData = await getApplications();
            
            setPrograms(programsData);
            const filteredApps = appsData.filter(app => app.student === studentProfileId);
            setMyApplications(filteredApps);
            
            setLoading(false);
        } catch (error) {
            console.error("Error loading dashboard data", error);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleApply = async (programId) => {
        const alreadyApplied = myApplications.some(app => app.program === programId);
        if (alreadyApplied) {
            alert("[ ERROR: DUPLICATE_ENTRY ] Application already submitted.");
            return;
        }

        try {
            const applicationPayload = {
                student: studentProfileId,
                program: programId,
                status: 'pending',
                approved_amount: "0.00"
            };
            await createApplication(applicationPayload);
            alert("[ SUCCESS ] Application transmitted to mainframe.");
            fetchData(); 
        } catch (error) {
            alert("[ ERROR ] Transmission failed.");
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <motion.div 
                    animate={{ rotate: 360, boxShadow: ["0 0 10px #00ffaa", "0 0 20px #ff0055", "0 0 10px #00ffaa"] }} 
                    transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                    className="w-16 h-16 border-t-4 border-r-4 border-[#00ffaa] border-solid rounded-full"
                />
            </div>
        );
    }

    const containerVariants = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: { staggerChildren: 0.15 }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 50, rotateX: -30 },
        show: { opacity: 1, y: 0, rotateX: 0, transition: { type: "spring", bounce: 0.4 } }
    };

    return (
        <div className="w-full max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 relative z-10">
            {/* Header Dashboard Panel */}
            <motion.div 
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col sm:flex-row justify-between items-center mb-12 p-[2px] rounded-2xl animate-rgb-border bg-transparent"
            >
                <div className="w-full flex flex-col sm:flex-row justify-between items-center p-6 glass-card rounded-2xl">
                    <div>
                        <h2 className="text-3xl font-black text-white uppercase tracking-widest">
                            SYS_USER: <span className="animate-rgb-text">{username}</span>
                        </h2>
                        <p className="text-[#00ffaa] font-mono mt-1 tracking-[0.2em] text-sm">[ SECURE_SESSION_ACTIVE ]</p>
                    </div>
                    <motion.button 
                        whileHover={{ scale: 1.05, boxShadow: "0 0 15px rgba(255, 0, 85, 0.8)" }}
                        whileTap={{ scale: 0.95 }}
                        onClick={onLogout} 
                        className="mt-4 sm:mt-0 px-8 py-3 bg-gradient-to-r from-[#ff0055] to-[#aa0000] text-white font-black uppercase tracking-widest rounded-sm transition-all"
                    >
                        TERMINATE
                    </motion.button>
                </div>
            </motion.div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                {/* Available Programs (Grid) */}
                <div className="xl:col-span-2">
                    <h3 className="text-2xl font-black mb-6 flex items-center gap-3 uppercase tracking-widest animate-rgb-text">
                        <span className="w-8 h-8 rounded-sm bg-[#5500ff] text-white flex items-center justify-center shadow-[0_0_10px_#5500ff]">_</span>
                        Available_Protocols
                    </h3>
                    <motion.div 
                        variants={containerVariants}
                        initial="hidden"
                        animate="show"
                        className="grid grid-cols-1 md:grid-cols-2 gap-6"
                    >
                        {programs.map(prog => (
                            <motion.div 
                                variants={itemVariants}
                                whileHover={{ scale: 1.03, y: -5 }}
                                key={prog.id} 
                                className="relative group p-[1px] rounded-xl bg-gradient-to-br from-[#333] to-[#111] hover:from-[#00ffaa] hover:to-[#5500ff] transition-all duration-300"
                            >
                                <div className="glass-card p-6 rounded-xl h-full flex flex-col relative z-10">
                                    <h4 className="text-xl font-bold text-white mb-2 uppercase tracking-wide">{prog.name}</h4>
                                    <p className="text-sm text-[#a0aab5] font-mono mb-4 flex-grow">{prog.description}</p>
                                    
                                    <div className="bg-black/50 border border-[#333] p-3 font-mono text-xs text-[#00ffaa] mb-5">
                                        <div className="mb-1"><span className="text-white">PARAM_1:</span> {prog.criteria1 || 'NULL'}</div>
                                        <div><span className="text-white">PARAM_2:</span> {prog.criteria2 || 'NULL'}</div>
                                    </div>
                                    
                                    <motion.button 
                                        whileHover={{ boxShadow: "0 0 20px rgba(0, 255, 170, 0.6)" }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={() => handleApply(prog.id)}
                                        className="w-full py-3 bg-[#00ffaa] text-black font-black uppercase tracking-widest rounded-sm mt-auto hover:bg-white transition-colors"
                                    >
                                        EXECUTE_APPLY
                                    </motion.button>
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>
                </div>

                {/* Applications Tracking */}
                <div>
                    <h3 className="text-2xl font-black mb-6 flex items-center gap-3 uppercase tracking-widest animate-rgb-text">
                        <span className="w-8 h-8 rounded-sm bg-[#00ffaa] text-black flex items-center justify-center shadow-[0_0_10px_#00ffaa]">X</span>
                        Active_Transmissions
                    </h3>
                    <motion.div 
                        initial={{ opacity: 0, x: 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ type: "spring", bounce: 0.3, delay: 0.3 }}
                        className="p-[1px] rounded-xl animate-rgb-border bg-transparent"
                    >
                        <div className="glass-card rounded-xl overflow-hidden h-full">
                            {myApplications.length === 0 ? (
                                <div className="p-8 text-center text-[#a0aab5] font-mono text-sm">
                                    [ NO_DATA_FOUND ]
                                </div>
                            ) : (
                                <div className="divide-y divide-[#333]">
                                    {myApplications.map((app, index) => (
                                        <motion.div 
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: 0.4 + (index * 0.1) }}
                                            key={app.id} 
                                            className="p-5 hover:bg-white/5 transition-colors group relative overflow-hidden"
                                        >
                                            {/* Hover scanline effect */}
                                            <div className="absolute top-0 left-[-100%] w-full h-[2px] bg-[#00ffaa] opacity-0 group-hover:opacity-100 group-hover:left-[100%] transition-all duration-700 ease-in-out"></div>

                                            <div className="flex justify-between items-start mb-3">
                                                <span className="text-xs font-mono text-[#a0aab5]">ID: #{app.id} [P:{app.program}]</span>
                                                <span className={`px-2 py-1 text-[10px] font-black tracking-widest uppercase border ${
                                                    app.status === 'success' || app.status === 'approved' 
                                                    ? 'text-[#00ffaa] border-[#00ffaa] shadow-[0_0_5px_#00ffaa]' 
                                                    : app.status === 'rejected' 
                                                    ? 'text-[#ff0055] border-[#ff0055] shadow-[0_0_5px_#ff0055]' 
                                                    : 'text-yellow-400 border-yellow-400 shadow-[0_0_5px_yellow]'
                                                }`}>
                                                    {app.status}
                                                </span>
                                            </div>
                                            <div className="text-xs font-mono text-[#a0aab5] mb-2">T_STAMP: {new Date(app.applied_on || Date.now()).toISOString()}</div>
                                            {app.approved_amount !== "0.00" && (
                                                <div className="mt-3 font-mono border-t border-[#333] pt-2">
                                                    <span className="text-[#a0aab5] text-xs">FUNDS_ALLOCATED: </span>
                                                    <span className="text-[#00ffaa] font-black text-lg text-shadow-glow">${app.approved_amount}</span>
                                                </div>
                                            )}
                                        </motion.div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};

export default StudentDashboard;