import { motion } from 'framer-motion'
import { SkillGapSummary, SkillGapItem } from '../components/SkillGapItem'
import { ArrowRight } from 'lucide-react'

export default function SkillGapPage({ careerGoal, gaps = [], onContinue }) {
    if (!gaps || gaps.length === 0) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-[#8888a8]">No skill gap data available.</p>
            </div>
        )
    }

    // Sort: Critical → High → Medium → Low → None → Unknown
    const ORDER = { Critical: 0, High: 1, Medium: 2, Low: 3, None: 4, Unknown: 5 }
    const sorted = [...gaps].sort((a, b) => (ORDER[a.gap_level] ?? 5) - (ORDER[b.gap_level] ?? 5))

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
            <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
                <span className="text-xs text-[#818cf8] font-medium uppercase tracking-widest">Skill Gap Report</span>
                <h1 className="text-2xl sm:text-3xl font-bold text-[#e8e8f0] mt-1 mb-1">Your Skill Gap</h1>
                <p className="text-[#8888a8] text-sm">
                    Here's what is currently between you and becoming a{' '}
                    <span className="text-[#e8e8f0]">{careerGoal?.career}</span>
                    {careerGoal?.country ? ` in ${careerGoal.country}` : ''}.
                </p>
            </motion.div>

            <SkillGapSummary gaps={gaps} />

            <div className="bg-[#111119] border border-[#1e1e2e] rounded-2xl px-4 sm:px-6 py-2">
                {sorted.map((gap, i) => (
                    <SkillGapItem key={i} gap={gap} index={i + 1} />
                ))}
            </div>

            <div className="mt-8">
                <button
                    onClick={onContinue}
                    className="flex items-center gap-2 px-6 py-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-[#6366f1]/20"
                >
                    View Learning Resources <ArrowRight size={16} />
                </button>
            </div>
        </div>
    )
}
