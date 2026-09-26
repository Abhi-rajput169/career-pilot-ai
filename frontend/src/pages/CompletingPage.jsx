import { useEffect, useRef, useState } from 'react'
import { subscribeSSE } from '../api'
import LoadingAnalysis from '../components/LoadingAnalysis'
import { Compass } from 'lucide-react'

export default function CompletingPage({
    sessionId,
    onSkillGapDone,
    onResourcesDone,
    onRoadmapDone,
    onComplete,
    onError,
}) {
    const [steps, setSteps] = useState({})
    const [errorMsg, setErrorMsg] = useState('')
    const started = useRef(false)

    useEffect(() => {
        if (!sessionId || started.current) return
        started.current = true

        const unsub = subscribeSSE(
            `/complete/${sessionId}`,
            (msg) => {
                if (msg.event === 'step') {
                    setSteps(s => ({ ...s, [msg.step]: msg.status }))
                    if (msg.step === 'skill_gap' && msg.status === 'done' && msg.data) onSkillGapDone(msg.data)
                    if (msg.step === 'resources' && msg.status === 'done' && msg.data) onResourcesDone(msg.data)
                    if (msg.step === 'roadmap' && msg.status === 'done' && msg.data) onRoadmapDone(msg.data)
                }
                if (msg.event === 'done') setTimeout(onComplete, 800)
                if (msg.event === 'error') setErrorMsg(msg.message || 'Completion failed.')
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
                    <button onClick={onError} className="text-sm text-[#818cf8] underline">← Go back</button>
                </div>
            ) : (
                <>
                    <h1 className="text-xl font-bold text-[#e8e8f0] mb-2">Building your career plan</h1>
                    <p className="text-[#8888a8] text-sm mb-10 text-center">
                        Analyzing your skill gaps, finding resources and creating your roadmap.<br />This takes 2–4 minutes.
                    </p>
                    <LoadingAnalysis steps={steps} phase={2} />
                </>
            )}
        </div>
    )
}
