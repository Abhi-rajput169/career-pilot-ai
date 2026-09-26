import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, Compass, Loader2 } from 'lucide-react'
import { api } from '../api'

const EXAMPLES = [
    { career: 'Data Scientist', country: 'India', timeline: '6 months' },
    { career: 'Product Manager', country: 'USA', timeline: '1 year' },
    { career: 'DevOps Engineer', country: 'UK', timeline: '8 months' },
]

export default function LandingPage({ onStart }) {
    const [career, setCareer] = useState('')
    const [country, setCountry] = useState('')
    const [timeline, setTimeline] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const fillExample = (ex) => {
        setCareer(ex.career); setCountry(ex.country); setTimeline(ex.timeline)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        if (!career.trim()) { setError('Please enter a career.'); return }
        setLoading(true)
        const parts = [career.trim(), country.trim(), timeline.trim()].filter(Boolean)
        const userInput = `I want to become a ${parts.join(' in ')}`
        try {
            const { session_id, career_goal } = await api.start(userInput)
            onStart(session_id, career_goal)
        } catch (err) {
            setError(`Could not reach CareerPilot AI backend. Is it running?\n\n${err.message}`)
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
            {/* Hero */}
            <motion.div
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-center mb-12 max-w-2xl"
            >
                <div className="inline-flex items-center gap-2 bg-[#6366f1]/10 border border-[#6366f1]/20 text-[#818cf8] rounded-full px-4 py-1.5 text-xs font-medium mb-6">
                    <Compass size={13} />
                    AI-Powered Career Intelligence
                </div>
                <h1 className="text-4xl sm:text-5xl font-extrabold text-[#e8e8f0] leading-tight tracking-tight mb-4">
                    Turn any career goal into<br />
                    <span className="text-[#6366f1]">a personalized action plan.</span>
                </h1>
                <p className="text-[#8888a8] text-base sm:text-lg leading-relaxed max-w-xl mx-auto">
                    Research your target career, assess your current skills, identify your gaps and build a personalized learning roadmap.
                </p>
            </motion.div>

            {/* Form */}
            <motion.form
                onSubmit={handleSubmit}
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="w-full max-w-lg bg-[#111119] border border-[#1e1e2e] rounded-2xl p-6 sm:p-8 shadow-2xl"
            >
                <div className="space-y-4 mb-6">
                    <Field label="Career" id="career" placeholder="e.g. Data Scientist" value={career} onChange={setCareer} required />
                    <Field label="Country" id="country" placeholder="e.g. India (optional)" value={country} onChange={setCountry} />
                    <Field label="Timeline" id="timeline" placeholder="e.g. 6 months (optional)" value={timeline} onChange={setTimeline} />
                </div>

                {error && (
                    <div className="mb-4 px-4 py-3 rounded-xl bg-[#ef4444]/10 border border-[#ef4444]/20 text-[#f87171] text-sm whitespace-pre-wrap">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold rounded-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed shadow-lg shadow-[#6366f1]/20 text-sm"
                >
                    {loading ? (
                        <><Loader2 size={16} className="animate-spin" /> Preparing your plan...</>
                    ) : (
                        <>Build My Career Plan <ArrowRight size={16} /></>
                    )}
                </button>
            </motion.form>

            {/* Examples */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="mt-8 text-center"
            >
                <p className="text-xs text-[#3a3a4e] mb-3 uppercase tracking-widest">Try an example</p>
                <div className="flex flex-wrap gap-2 justify-center">
                    {EXAMPLES.map((ex) => (
                        <button
                            key={ex.career}
                            onClick={() => fillExample(ex)}
                            className="text-xs px-3 py-1.5 rounded-full border border-[#1e1e2e] text-[#8888a8] hover:border-[#6366f1]/40 hover:text-[#818cf8] transition-all"
                        >
                            {ex.career} • {ex.country} • {ex.timeline}
                        </button>
                    ))}
                </div>
            </motion.div>

            {/* Pipeline hint */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="mt-12 flex flex-wrap gap-2 items-center justify-center text-[11px] text-[#3a3a4e]"
            >
                {['Career Goal', 'Research', 'Assessment', 'Skill Gap', 'Resources', 'Roadmap'].map((s, i, arr) => (
                    <span key={s} className="flex items-center gap-2">
                        <span className="text-[#8888a8]">{s}</span>
                        {i < arr.length - 1 && <span className="text-[#1e1e2e]">→</span>}
                    </span>
                ))}
            </motion.div>
        </div>
    )
}

function Field({ label, id, placeholder, value, onChange, required }) {
    return (
        <div>
            <label htmlFor={id} className="block text-xs font-medium text-[#8888a8] mb-1.5">{label}</label>
            <input
                id={id}
                type="text"
                placeholder={placeholder}
                value={value}
                onChange={e => onChange(e.target.value)}
                required={required}
                className="w-full px-4 py-2.5 rounded-xl border border-[#1e1e2e] bg-[#09090f] text-[#e8e8f0] text-sm
          focus:border-[#6366f1] focus:outline-none placeholder:text-[#3a3a4e] transition-colors"
            />
        </div>
    )
}
