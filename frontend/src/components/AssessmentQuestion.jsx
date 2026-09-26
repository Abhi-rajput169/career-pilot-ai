import { motion } from 'framer-motion'

export function AnswerSelector({ questionType, value, onChange }) {
    if (questionType === 'level') {
        const levels = ['Beginner', 'Intermediate', 'Advanced']
        return (
            <div className="flex gap-3 flex-wrap">
                {levels.map((lvl) => (
                    <button
                        key={lvl}
                        onClick={() => onChange(lvl)}
                        className={`px-5 py-2.5 rounded-xl border text-sm font-medium transition-all
              ${value === lvl
                                ? 'bg-[#6366f1] border-[#6366f1] text-white shadow-lg shadow-[#6366f1]/20'
                                : 'border-[#1e1e2e] bg-[#111119] text-[#8888a8] hover:border-[#6366f1]/50 hover:text-[#e8e8f0]'
                            }`}
                    >
                        {lvl}
                    </button>
                ))}
            </div>
        )
    }

    if (questionType === 'yes_no') {
        return (
            <div className="flex gap-3">
                {['Yes', 'No'].map((opt) => (
                    <button
                        key={opt}
                        onClick={() => onChange(opt)}
                        className={`px-8 py-2.5 rounded-xl border text-sm font-medium transition-all
              ${value === opt
                                ? 'bg-[#6366f1] border-[#6366f1] text-white'
                                : 'border-[#1e1e2e] bg-[#111119] text-[#8888a8] hover:border-[#6366f1]/50 hover:text-[#e8e8f0]'
                            }`}
                    >
                        {opt}
                    </button>
                ))}
            </div>
        )
    }

    if (questionType === 'number') {
        return (
            <div className="flex items-center gap-3">
                <input
                    type="number"
                    min="0"
                    step="0.5"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder="0"
                    className="w-28 px-4 py-2.5 rounded-xl border border-[#1e1e2e] bg-[#111119] text-[#e8e8f0] text-sm
            focus:border-[#6366f1] focus:outline-none transition-colors placeholder:text-[#3a3a4e]"
                />
                <span className="text-[#8888a8] text-sm">years</span>
            </div>
        )
    }

    // text
    return (
        <textarea
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Your answer..."
            rows={3}
            className="w-full px-4 py-3 rounded-xl border border-[#1e1e2e] bg-[#111119] text-[#e8e8f0] text-sm
        focus:border-[#6366f1] focus:outline-none transition-colors placeholder:text-[#3a3a4e] resize-none"
        />
    )
}

const CATEGORY_COLORS = {
    skill: 'text-[#818cf8]',
    technology: 'text-[#38bdf8]',
    education: 'text-[#a78bfa]',
    experience: 'text-[#f472b6]',
    certification: 'text-[#2dd4bf]',
    other: 'text-[#9ca3af]',
}

export default function AssessmentQuestion({ question, index, total, value, onChange }) {
    const progress = ((index) / total) * 100

    return (
        <motion.div
            key={index}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.25 }}
            className="w-full max-w-xl mx-auto"
        >
            {/* Progress */}
            <div className="flex items-center justify-between mb-3">
                <span className="text-xs text-[#8888a8]">Question {index} of {total}</span>
                <span className={`text-xs font-medium ${CATEGORY_COLORS[question.category] || CATEGORY_COLORS.other}`}>
                    {question.category}
                </span>
            </div>
            <div className="h-1 w-full bg-[#1e1e2e] rounded-full mb-8 overflow-hidden">
                <motion.div
                    className="h-full bg-[#6366f1] rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.4 }}
                />
            </div>

            {/* Question */}
            <h2 className="text-lg sm:text-xl font-semibold text-[#e8e8f0] leading-snug mb-6">
                {question.question}
            </h2>

            <AnswerSelector
                questionType={question.question_type}
                value={value}
                onChange={onChange}
            />
        </motion.div>
    )
}
