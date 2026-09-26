import { motion } from 'framer-motion'
import { Check, Circle, Loader } from 'lucide-react'

const STEPS = [
    { id: 'goal', label: 'Career Goal' },
    { id: 'research', label: 'Research' },
    { id: 'questions', label: 'Assessment' },
    { id: 'skill_gap', label: 'Skill Gap' },
    { id: 'resources', label: 'Resources' },
    { id: 'roadmap', label: 'Roadmap' },
]

export default function ProgressStepper({ steps = {} }) {
    return (
        <div className="flex items-center gap-0 w-full max-w-2xl mx-auto my-6">
            {STEPS.map((step, idx) => {
                const status = steps[step.id] || 'pending'
                const isLast = idx === STEPS.length - 1
                return (
                    <div key={step.id} className="flex items-center flex-1 min-w-0">
                        <div className="flex flex-col items-center gap-1 shrink-0">
                            <motion.div
                                initial={false}
                                animate={
                                    status === 'done'
                                        ? { backgroundColor: '#22c55e', borderColor: '#22c55e' }
                                        : status === 'running'
                                            ? { borderColor: '#6366f1' }
                                            : { borderColor: '#1e1e2e' }
                                }
                                className="w-7 h-7 rounded-full border-2 flex items-center justify-center"
                            >
                                {status === 'done' && <Check size={13} className="text-white" />}
                                {status === 'running' && (
                                    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}>
                                        <Loader size={12} className="text-[#6366f1]" />
                                    </motion.div>
                                )}
                                {status === 'pending' && <Circle size={10} className="text-[#3a3a4e]" />}
                            </motion.div>
                            <span className={`text-[10px] font-medium whitespace-nowrap
                ${status === 'done' ? 'text-[#22c55e]' : status === 'running' ? 'text-[#818cf8]' : 'text-[#3a3a4e]'}`}>
                                {step.label}
                            </span>
                        </div>
                        {!isLast && (
                            <div className="flex-1 h-px mx-1 mt-[-12px]"
                                style={{ background: status === 'done' ? '#22c55e55' : '#1e1e2e' }} />
                        )}
                    </div>
                )
            })}
        </div>
    )
}
