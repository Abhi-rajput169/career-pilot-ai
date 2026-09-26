import { motion } from 'framer-motion'
import ResourceCard from '../components/ResourceCard'
import { ArrowRight } from 'lucide-react'

export default function ResourcesPage({ resources = [], onContinue }) {
    const hasResources = resources && resources.some(r => r.resources?.length > 0)

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
            <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
                <span className="text-xs text-[#818cf8] font-medium uppercase tracking-widest">Learning Resources</span>
                <h1 className="text-2xl sm:text-3xl font-bold text-[#e8e8f0] mt-1 mb-1">Resources for Your Gaps</h1>
                <p className="text-[#8888a8] text-sm">
                    Free resources selected based on your current level and skill gaps.
                </p>
            </motion.div>

            {!hasResources ? (
                <div className="bg-[#111119] border border-[#1e1e2e] rounded-2xl px-6 py-10 text-center">
                    <p className="text-[#8888a8] text-sm">No verified free resources found for your gaps yet.</p>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
                    {resources.map((item, i) => (
                        <ResourceCard
                            key={i}
                            requirement={item.requirement}
                            gap_level={item.gap_level}
                            resources={item.resources || []}
                        />
                    ))}
                </motion.div>
            )}

            <div className="mt-8">
                <button
                    onClick={onContinue}
                    className="flex items-center gap-2 px-6 py-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-[#6366f1]/20"
                >
                    View My Roadmap <ArrowRight size={16} />
                </button>
            </div>
        </div>
    )
}
