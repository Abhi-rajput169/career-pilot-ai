import { useState, useEffect } from 'react'
import { AnimatePresence } from 'framer-motion'
import { ArrowRight, Loader2 } from 'lucide-react'
import AssessmentQuestion from '../components/AssessmentQuestion'
import { api } from '../api'

export default function AssessmentPage({ sessionId, questions: propQuestions = [], onComplete }) {
    const [current, setCurrent] = useState(0)
    const [answers, setAnswers] = useState({})
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState('')
    const [questions, setQuestions] = useState(propQuestions)
    const [loading, setLoading] = useState(false)

    // If questions weren't delivered via SSE, fetch them from the session API
    useEffect(() => {
        console.log('[AssessmentPage] propQuestions:', propQuestions)
        if (propQuestions && propQuestions.length > 0) {
            setQuestions(propQuestions)
            return
        }
        if (!sessionId) return
        setLoading(true)
        api.session(sessionId)
            .then(data => {
                console.log('[AssessmentPage] fetched session:', data)
                if (data.questions && data.questions.length > 0) {
                    setQuestions(data.questions)
                }
            })
            .catch(e => console.error('[AssessmentPage] session fetch failed:', e))
            .finally(() => setLoading(false))
    }, [sessionId, propQuestions])

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 size={24} className="animate-spin text-[#6366f1]" />
            </div>
        )
    }

    if (!questions || questions.length === 0) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-[#8888a8]">No assessment questions were generated.</p>
            </div>
        )
    }

    const q = questions[current]
    const val = answers[current] ?? ''
    const isLast = current === questions.length - 1
    const canProceed = val !== '' && val !== null && val !== undefined

    const next = async () => {
        if (!canProceed) return
        if (!isLast) {
            setCurrent(c => c + 1)
            return
        }
        // Submit all answers
        setSubmitting(true)
        setError('')
        const payload = questions.map((q, i) => {
            let ans = answers[i] ?? ''
            // Format number answers with "years"
            if (q.question_type === 'number' && ans !== '') {
                const n = parseFloat(ans)
                if (!isNaN(n)) ans = Number.isInteger(n) ? `${n} years` : `${n} years`
            }
            return {
                question: q.question,
                requirement: q.requirement,
                category: q.category,
                question_type: q.question_type,
                answer: String(ans),
            }
        })
        try {
            await api.submitAnswers(sessionId, payload)
            onComplete()
        } catch (e) {
            setError(e.message)
            setSubmitting(false)
        }
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
            <div className="w-full max-w-xl">
                <div className="text-center mb-10">
                    <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">Let's understand your current level</h1>
                    <p className="text-[#8888a8] text-sm">Answer a few questions so CareerPilot can identify where you should focus.</p>
                </div>

                <div className="bg-[#111119] border border-[#1e1e2e] rounded-2xl p-6 sm:p-8 mb-4">
                    <AnimatePresence mode="wait">
                        <AssessmentQuestion
                            key={current}
                            question={q}
                            index={current + 1}
                            total={questions.length}
                            value={val}
                            onChange={(v) => setAnswers(a => ({ ...a, [current]: v }))}
                        />
                    </AnimatePresence>
                </div>

                {error && <p className="text-[#f87171] text-sm mb-4">{error}</p>}

                <div className="flex items-center justify-between">
                    {current > 0 ? (
                        <button onClick={() => setCurrent(c => c - 1)} className="text-sm text-[#8888a8] hover:text-[#e8e8f0] transition-colors">
                            ← Back
                        </button>
                    ) : <span />}

                    <button
                        onClick={next}
                        disabled={!canProceed || submitting}
                        className="flex items-center gap-2 px-6 py-2.5 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold rounded-xl text-sm transition-all disabled:opacity-40 shadow-lg shadow-[#6366f1]/20"
                    >
                        {submitting ? (
                            <><Loader2 size={15} className="animate-spin" /> Submitting...</>
                        ) : isLast ? (
                            <>Analyze My Skill Gaps <ArrowRight size={15} /></>
                        ) : (
                            <>Continue <ArrowRight size={15} /></>
                        )}
                    </button>
                </div>
            </div>
        </div>
    )
}
