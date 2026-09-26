import { motion } from 'framer-motion'

function parsePhases(roadmapText) {
    if (!roadmapText) return []

    // Split on Phase headings: "Phase 1", "## Phase", "Month 1", etc.
    const lines = roadmapText.split('\n')
    const phases = []
    let current = null

    for (const line of lines) {
        const trimmed = line.trim()

        // Detect phase/month headings
        const isHeading = (
            /^#{1,3}\s/.test(trimmed) ||
            /^(phase|month|week|step|stage)\s*\d+/i.test(trimmed) ||
            /^\*\*(phase|month|week|step|stage)\s*\d+/i.test(trimmed)
        )

        if (isHeading && trimmed.length > 2) {
            if (current) phases.push(current)
            const title = trimmed.replace(/^#{1,3}\s*/, '').replace(/\*\*/g, '').trim()
            current = { title, content: [] }
        } else if (current && trimmed) {
            const cleaned = trimmed.replace(/^[\*\-]\s*/, '').replace(/\*\*/g, '').trim()
            if (cleaned) current.content.push(cleaned)
        } else if (!current && trimmed) {
            // Content before first heading
            if (phases.length === 0) {
                current = { title: 'Overview', content: [trimmed.replace(/^[\*\-]\s*/, '').replace(/\*\*/g, '').trim()] }
            }
        }
    }
    if (current) phases.push(current)
    return phases.filter(p => p.content.length > 0 || p.title !== 'Overview')
}

const PHASE_COLORS = [
    ['#6366f1', '#818cf8'],
    ['#8b5cf6', '#a78bfa'],
    ['#ec4899', '#f472b6'],
    ['#0ea5e9', '#38bdf8'],
    ['#14b8a6', '#2dd4bf'],
    ['#f59e0b', '#fcd34d'],
    ['#22c55e', '#4ade80'],
]

function RoadmapPhase({ phase, index, total }) {
    const [dot, line] = PHASE_COLORS[index % PHASE_COLORS.length]
    const isLast = index === total - 1

    return (
        <motion.div
            initial={{ opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.07 }}
            className="flex gap-5"
        >
            {/* Timeline spine */}
            <div className="flex flex-col items-center shrink-0">
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
                    style={{ backgroundColor: dot }}>
                    {index + 1}
                </div>
                {!isLast && <div className="w-0.5 flex-1 mt-2 mb-0 rounded-full" style={{ backgroundColor: `${line}33`, minHeight: '32px' }} />}
            </div>

            {/* Content */}
            <div className={`pb-8 flex-1 min-w-0 ${isLast ? '' : ''}`}>
                <h3 className="text-[#e8e8f0] font-semibold text-base mb-3">{phase.title}</h3>
                <div className="space-y-1.5">
                    {phase.content.map((line, i) => {
                        // Detect if this is a sub-heading (short, no period)
                        const isSub = line.length < 60 && !line.endsWith('.') && /^[A-Z]/.test(line) && !line.startsWith('-')
                        return (
                            <div key={i} className={isSub
                                ? 'text-xs font-semibold text-[#818cf8] uppercase tracking-wide mt-3 mb-1'
                                : 'flex items-start gap-2 text-sm text-[#8888a8]'}>
                                {!isSub && <span className="text-[#3a3a4e] mt-1 shrink-0">•</span>}
                                <span>{line}</span>
                            </div>
                        )
                    })}
                </div>
            </div>
        </motion.div>
    )
}

export default function RoadmapTimeline({ roadmap }) {
    const phases = parsePhases(roadmap)

    if (!phases.length) {
        return (
            <div className="py-8 text-center text-[#8888a8] text-sm">
                No roadmap phases found in the backend output.
            </div>
        )
    }

    return (
        <div>
            {phases.map((phase, i) => (
                <RoadmapPhase key={i} phase={phase} index={i} total={phases.length} />
            ))}
        </div>
    )
}
