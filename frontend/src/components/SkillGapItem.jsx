const GAP_STYLES = {
    Critical: { badge: 'bg-[#dc2626]/15 text-[#ef4444] border-[#dc2626]/30', bar: '#dc2626', width: '100%' },
    High: { badge: 'bg-[#f97316]/15 text-[#fb923c] border-[#f97316]/30', bar: '#f97316', width: '75%' },
    Medium: { badge: 'bg-[#f59e0b]/15 text-[#fbbf24] border-[#f59e0b]/30', bar: '#f59e0b', width: '50%' },
    Low: { badge: 'bg-[#22c55e]/15 text-[#4ade80] border-[#22c55e]/30', bar: '#22c55e', width: '25%' },
    None: { badge: 'bg-[#6366f1]/10 text-[#818cf8] border-[#6366f1]/20', bar: '#6366f1', width: '5%' },
    Unknown: { badge: 'bg-[#3a3a4e]/40 text-[#8888a8] border-[#3a3a4e]', bar: '#3a3a4e', width: '20%' },
}

export function SkillGapItem({ gap, index }) {
    const style = GAP_STYLES[gap.gap_level] || GAP_STYLES.Unknown
    return (
        <div className="py-4 border-b border-[#1e1e2e] last:border-0">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                    <span className="text-[#e8e8f0] font-semibold text-sm">{gap.requirement}</span>
                    <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${style.badge}`}>
                        {gap.gap_level}
                    </span>
                </div>
                <span className="text-xs text-[#8888a8]">
                    Your level: <span className="text-[#e8e8f0] font-medium">{gap.user_status}</span>
                </span>
            </div>
            {/* Gap bar */}
            <div className="h-1.5 w-full bg-[#1e1e2e] rounded-full mb-2 overflow-hidden">
                <div className="h-full rounded-full transition-all" style={{ width: style.width, backgroundColor: style.bar }} />
            </div>
            <p className="text-xs text-[#8888a8] leading-relaxed">{gap.explanation}</p>
        </div>
    )
}

export function SkillGapSummary({ gaps = [] }) {
    const counts = {
        Critical: gaps.filter(g => g.gap_level === 'Critical').length,
        High: gaps.filter(g => g.gap_level === 'High').length,
        Medium: gaps.filter(g => g.gap_level === 'Medium').length,
        Low: gaps.filter(g => g.gap_level === 'Low').length,
    }

    const stats = [
        { label: 'Assessed', value: gaps.length, color: 'text-[#e8e8f0]' },
        { label: 'Critical', value: counts.Critical, color: 'text-[#ef4444]' },
        { label: 'High', value: counts.High, color: 'text-[#fb923c]' },
        { label: 'Medium', value: counts.Medium, color: 'text-[#fbbf24]' },
    ]

    return (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
            {stats.map(s => (
                <div key={s.label} className="bg-[#111119] border border-[#1e1e2e] rounded-xl p-4 text-center">
                    <div className={`text-2xl font-bold mb-1 ${s.color}`}>{s.value}</div>
                    <div className="text-xs text-[#8888a8]">{s.label}</div>
                </div>
            ))}
        </div>
    )
}
