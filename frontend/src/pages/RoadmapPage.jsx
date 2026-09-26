import { motion } from 'framer-motion'
import RoadmapTimeline from '../components/RoadmapTimeline'
import { RefreshCw, Download } from 'lucide-react'

export default function RoadmapPage({ careerGoal, roadmap, onRestart }) {
    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
            <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
                <span className="text-xs text-[#818cf8] font-medium uppercase tracking-widest">Personalized Roadmap</span>
                <h1 className="text-2xl sm:text-3xl font-bold text-[#e8e8f0] mt-1 mb-2">Your Career Roadmap</h1>
                <div className="flex flex-wrap gap-2">
                    {careerGoal?.career && (
                        <span className="text-xs bg-[#6366f1]/10 text-[#818cf8] px-3 py-1 rounded-full border border-[#6366f1]/20">
                            {careerGoal.career}
                        </span>
                    )}
                    {careerGoal?.country && (
                        <span className="text-xs bg-[#111119] text-[#8888a8] px-3 py-1 rounded-full border border-[#1e1e2e]">
                            {careerGoal.country}
                        </span>
                    )}
                    {careerGoal?.timeline && (
                        <span className="text-xs bg-[#111119] text-[#8888a8] px-3 py-1 rounded-full border border-[#1e1e2e]">
                            {careerGoal.timeline}
                        </span>
                    )}
                </div>
            </motion.div>

            {!roadmap ? (
                <div className="bg-[#111119] border border-[#1e1e2e] rounded-2xl px-6 py-10 text-center">
                    <p className="text-[#8888a8] text-sm">Roadmap could not be generated. Please try again.</p>
                </div>
            ) : (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="bg-[#111119] border border-[#1e1e2e] rounded-2xl px-4 sm:px-8 py-6 sm:py-8 mb-8"
                >
                    <RoadmapTimeline roadmap={roadmap} />
                </motion.div>
            )}

            {/* Actions */}
            <div className="flex flex-wrap gap-3">
                <button
                    onClick={onRestart}
                    className="flex items-center gap-2 px-5 py-2.5 border border-[#1e1e2e] bg-[#111119] text-[#8888a8] hover:text-[#e8e8f0] hover:border-[#6366f1]/40 rounded-xl text-sm font-medium transition-all"
                >
                    <RefreshCw size={14} /> Plan Another Career
                </button>
            </div>

            {/* Completion card */}
            <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="mt-10 p-6 rounded-2xl border border-[#22c55e]/20 bg-[#22c55e]/5"
            >
                <h3 className="text-[#4ade80] font-semibold text-sm mb-2">✓ CareerPilot Analysis Complete</h3>
                <p className="text-[#8888a8] text-xs leading-relaxed">
                    You now have a personalized career plan covering your skill gaps, recommended free resources, and a phased learning roadmap. Start with the Critical and High priority gaps first.
                </p>
            </motion.div>
        </div>
    )
}
