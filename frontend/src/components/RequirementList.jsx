const IMPORTANCE_STYLES = {
    essential: 'bg-[#ef4444]/10 text-[#ef4444] border-[#ef4444]/20',
    important: 'bg-[#f59e0b]/10 text-[#f59e0b] border-[#f59e0b]/20',
    optional: 'bg-[#3a3a4e]/40 text-[#8888a8] border-[#3a3a4e]',
}

const CATEGORY_STYLES = {
    skill: 'bg-[#6366f1]/10 text-[#818cf8]',
    technology: 'bg-[#0ea5e9]/10 text-[#38bdf8]',
    education: 'bg-[#8b5cf6]/10 text-[#a78bfa]',
    experience: 'bg-[#ec4899]/10 text-[#f472b6]',
    certification: 'bg-[#14b8a6]/10 text-[#2dd4bf]',
    license: 'bg-[#f97316]/10 text-[#fb923c]',
    exam: 'bg-[#eab308]/10 text-[#facc15]',
    other: 'bg-[#6b7280]/10 text-[#9ca3af]',
}

export function RequirementItem({ req, index }) {
    return (
        <div className="flex items-start gap-4 py-4 border-b border-[#1e1e2e] last:border-0 group">
            <span className="text-xs text-[#3a3a4e] font-mono mt-0.5 w-5 shrink-0">{String(index).padStart(2, '0')}</span>
            <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2 mb-1">
                    <span className="text-[#e8e8f0] font-medium text-sm">{req.requirement}</span>
                    <span className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full border ${IMPORTANCE_STYLES[req.importance] || IMPORTANCE_STYLES.optional}`}>
                        {req.importance}
                    </span>
                    <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${CATEGORY_STYLES[req.category] || CATEGORY_STYLES.other}`}>
                        {req.category}
                    </span>
                </div>
                <p className="text-[#8888a8] text-xs leading-relaxed">{req.explanation}</p>
            </div>
        </div>
    )
}

export default function RequirementList({ requirements = [] }) {
    if (!requirements.length) return <EmptyState message="No requirements found." />
    return (
        <div>
            {requirements.map((req, i) => (
                <RequirementItem key={i} req={req} index={i + 1} />
            ))}
        </div>
    )
}

function EmptyState({ message }) {
    return <p className="text-[#8888a8] text-sm py-6 text-center">{message}</p>
}
