import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

const STAGE_LABELS = {
    research: 'Researching career requirements...',
    questions: 'Building your assessment...',
    skill_gap: 'Analyzing your skill gaps...',
    resources: 'Finding free learning resources...',
    roadmap: 'Creating your personalized roadmap...',
}

export default function LoadingAnalysis({ steps = {}, phase = 1 }) {
    const stageKeys = phase === 1
        ? ['research', 'questions']
        : ['skill_gap', 'resources', 'roadmap']

    return (
        <div className="space-y-3 w-full max-w-sm">
            {stageKeys.map((key) => {
                const status = steps[key] || 'pending'
                return (
                    <div key={key} className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-all
            ${status === 'running' ? 'border-[#6366f1]/40 bg-[#6366f1]/5' : status === 'done' ? 'border-[#22c55e]/30 bg-[#22c55e]/5' : 'border-[#1e1e2e] bg-[#111119]'}
          `}>
                        <div className="shrink-0">
                            {status === 'running' ? (
                                <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}>
                                    <Loader2 size={16} className="text-[#6366f1]" />
                                </motion.div>
                            ) : status === 'done' ? (
                                <span className="text-[#22c55e] text-base">✓</span>
                            ) : (
                                <span className="text-[#3a3a4e] text-base">○</span>
                            )}
                        </div>
                        <span className={`text-sm font-medium
              ${status === 'running' ? 'text-[#818cf8]' : status === 'done' ? 'text-[#22c55e]' : 'text-[#3a3a4e]'}`}>
                            {STAGE_LABELS[key]}
                        </span>
                    </div>
                )
            })}
        </div>
    )
}
