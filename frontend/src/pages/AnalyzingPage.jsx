import { useEffect, useRef, useState } from 'react'
import { subscribeSSE } from '../api'
import LoadingAnalysis from '../components/LoadingAnalysis'
import { Compass } from 'lucide-react'

export default function AnalyzingPage({ sessionId, onResearchDone, onQuestionsDone, onComplete, onError }) {
    const [steps, setSteps] = useState({})
    const [errorMsg, setErrorMsg] = useState('')
    const started = useRef(false)
    // Store data in refs so they're always available when done fires
    const researchRef = useRef(null)
    const questionsRef = useRef(null)

    useEffect(() => {
        if (!sessionId || started.current) return
        started.current = true

        const unsub = subscribeSSE(
            `/analyze/${sessionId}`,
            (msg) => {
                if (msg.event === 'step') {
                    setSteps(s => ({ ...s, [msg.step]: msg.status }))
                    if (msg.step === 'research' && msg.status === 'done' && msg.data) {
                        researchRef.current = msg.data
                        onResearchDone(msg.data)
                    }
                    if (msg.step === 'questions' && msg.status === 'done' && msg.data) {
                        questionsRef.current = msg.data
                        onQuestionsDone(msg.data)
                    }
                }
                if (msg.event === 'done') {
                    // Flush any data that may not have been saved yet
                    if (researchRef.current) onResearchDone(researchRef.current)
                    if (questionsRef.current) onQuestionsDone(questionsRef.current)
                    setTimeout(onComplete, 1200)
                }
                if (msg.event === 'error') {
                    setErrorMsg(msg.message || 'Analysis failed.')
                }
            },
            (err) => setErrorMsg(err.message || 'Connection failed.')
        )
        return unsub
    }, [sessionId])

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
            <div className="w-8 h-8 rounded-lg bg-[#6366f1] flex items-center justify-center mb-8">
                <Compass size={16} className="text-white" />
            </div>

            {errorMsg ? (
                <div className="max-w-sm text-center">
                    <h2 className="text-[#ef4444] font-semibold mb-2">Something went wrong</h2>
                    <p className="text-[#8888a8] text-sm mb-6">{errorMsg}</p>
                    <button onClick={onError} className="text-sm text-[#818cf8] underline">← Try again</button>
                </div>
            ) : (
                <>
                    <h1 className="text-xl font-bold text-[#e8e8f0] mb-2">Analyzing your career goal</h1>
                    <p className="text-[#8888a8] text-sm mb-10 text-center">
                        This usually takes 1–2 minutes while the AI researches your career.<br />Please keep this page open.
                    </p>
                    <LoadingAnalysis steps={steps} phase={1} />
                </>
            )}
        </div>
    )
}
