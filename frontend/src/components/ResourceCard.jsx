import { ExternalLink } from 'lucide-react'

const GAP_BADGE = {
    Critical: 'bg-[#dc2626]/15 text-[#ef4444]',
    High: 'bg-[#f97316]/15 text-[#fb923c]',
    Medium: 'bg-[#f59e0b]/15 text-[#fbbf24]',
    Low: 'bg-[#22c55e]/15 text-[#4ade80]',
    Unknown: 'bg-[#3a3a4e]/40 text-[#8888a8]',
}

export default function ResourceCard({ requirement, gap_level, resources = [] }) {
    return (
        <div className="mb-8">
            <div className="flex items-center gap-3 mb-3">
                <h3 className="text-[#e8e8f0] font-semibold">{requirement}</h3>
                <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full ${GAP_BADGE[gap_level] || GAP_BADGE.Unknown}`}>
                    {gap_level} gap
                </span>
            </div>

            {resources.length === 0 ? (
                <div className="py-4 px-4 rounded-xl border border-[#1e1e2e] bg-[#111119] text-sm text-[#8888a8]">
                    No verified free resources found for this requirement yet.
                </div>
            ) : (
                <div className="space-y-2">
                    {resources.map((r, i) => (
                        <a
                            key={i}
                            href={r.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-start gap-3 p-4 rounded-xl border border-[#1e1e2e] bg-[#111119]
                hover:border-[#6366f1]/40 hover:bg-[#6366f1]/5 transition-all group"
                        >
                            {/* YouTube thumb placeholder */}
                            <div className="w-10 h-10 rounded-lg bg-[#dc2626]/15 flex items-center justify-center shrink-0 mt-0.5">
                                <span className="text-[#dc2626] text-lg font-bold">▶</span>
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-[#e8e8f0] text-sm font-medium leading-snug mb-1 group-hover:text-[#818cf8] transition-colors">
                                    {r.title || requirement}
                                </p>
                                <p className="text-[#8888a8] text-xs leading-relaxed">{r.why_recommended}</p>
                                <div className="flex items-center gap-2 mt-2">
                                    <span className="text-[10px] bg-[#22c55e]/10 text-[#4ade80] px-2 py-0.5 rounded-full font-medium">Free</span>
                                    <span className="text-[10px] bg-[#dc2626]/10 text-[#f87171] px-2 py-0.5 rounded-full font-medium">YouTube</span>
                                </div>
                            </div>
                            <ExternalLink size={13} className="text-[#3a3a4e] group-hover:text-[#6366f1] transition-colors shrink-0 mt-1" />
                        </a>
                    ))}
                </div>
            )}
        </div>
    )
}
