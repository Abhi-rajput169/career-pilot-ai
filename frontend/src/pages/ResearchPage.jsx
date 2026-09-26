import { motion } from 'framer-motion'
import RequirementList from '../components/RequirementList'
import { ArrowRight, Globe, Clock, Briefcase } from 'lucide-react'

export default function ResearchPage({ careerGoal, research, onContinue }) {
    if (!research) return <div className="p-8 text-[#8888a8]">No research data available.</div>

    const info = research.career_information || {}

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
            {/* Header */}
            <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
                <div className="flex flex-wrap items-center gap-2 mb-2">
                    <span className="text-xs text-[#818cf8] font-medium uppercase tracking-widest">Career Intelligence</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-bold text-[#e8e8f0] mb-1">{careerGoal?.career}</h1>
                {careerGoal?.country && <p className="text-[#8888a8] text-sm">{careerGoal.country}{careerGoal?.timeline ? ` • ${careerGoal.timeline}` : ''}</p>}
            </motion.div>

            {/* Overview */}
            <Section title="Overview">
                <p className="text-[#8888a8] text-sm leading-relaxed">{research.career_overview}</p>
            </Section>

            {/* Career info */}
            {(info.salary_range || info.job_outlook || info.typical_responsibilities || info.work_environment) && (
                <Section title="Career Information">
                    <div className="grid sm:grid-cols-2 gap-3">
                        {info.salary_range && <InfoCard icon={<span>💰</span>} label="Salary Range" value={info.salary_range} />}
                        {info.job_outlook && <InfoCard icon={<span>📈</span>} label="Job Outlook" value={info.job_outlook} />}
                        {info.typical_responsibilities && <InfoCard icon={<Briefcase size={14} />} label="Responsibilities" value={info.typical_responsibilities} />}
                        {info.work_environment && <InfoCard icon={<Globe size={14} />} label="Work Environment" value={info.work_environment} />}
                    </div>
                </Section>
            )}

            {/* Requirements */}
            <Section title={`Requirements (${research.requirements?.length || 0})`}>
                <RequirementList requirements={research.requirements || []} />
            </Section>

            <div className="mt-8">
                <button
                    onClick={onContinue}
                    className="flex items-center gap-2 px-6 py-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-[#6366f1]/20"
                >
                    Start Assessment <ArrowRight size={16} />
                </button>
            </div>
        </div>
    )
}

function Section({ title, children }) {
    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
            <h2 className="text-xs font-semibold text-[#3a3a4e] uppercase tracking-widest mb-4">{title}</h2>
            <div className="bg-[#111119] border border-[#1e1e2e] rounded-2xl px-4 sm:px-6 py-4 sm:py-5">
                {children}
            </div>
        </motion.div>
    )
}

function InfoCard({ icon, label, value }) {
    return (
        <div className="p-3 rounded-xl bg-[#09090f] border border-[#1e1e2e]">
            <div className="flex items-center gap-1.5 mb-1 text-[#8888a8]">
                {icon}
                <span className="text-[10px] font-semibold uppercase tracking-wide">{label}</span>
            </div>
            <p className="text-[#e8e8f0] text-xs leading-relaxed">{value}</p>
        </div>
    )
}
