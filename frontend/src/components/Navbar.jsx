import { Compass, BarChart2, BookOpen, Layers, Map } from 'lucide-react'

const NAV_ITEMS = [
    { id: 'research', label: 'Research', icon: BookOpen },
    { id: 'assessment', label: 'Assessment', icon: Layers },
    { id: 'skillgap', label: 'Skill Gap', icon: BarChart2 },
    { id: 'resources', label: 'Resources', icon: BookOpen },
    { id: 'roadmap', label: 'Roadmap', icon: Map },
]

export default function Navbar({ careerGoal, page, onNav }) {
    return (
        <header className="sticky top-0 z-50 border-b border-[#1e1e2e] bg-[#09090f]/80 backdrop-blur-md">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 flex items-center justify-between h-14">
                {/* Logo */}
                <button
                    onClick={() => onNav('research')}
                    className="flex items-center gap-2 text-white font-semibold tracking-tight group"
                >
                    <div className="w-7 h-7 rounded-lg bg-[#6366f1] flex items-center justify-center group-hover:opacity-90 transition-opacity">
                        <Compass size={14} className="text-white" />
                    </div>
                    <span className="text-[15px]">CareerPilot <span className="text-[#6366f1]">AI</span></span>
                </button>

                {/* Career badge */}
                {careerGoal && (
                    <div className="hidden sm:flex items-center gap-2 text-xs text-[#8888a8] bg-[#111119] border border-[#1e1e2e] rounded-full px-3 py-1">
                        <span className="text-[#e8e8f0] font-medium">{careerGoal.career}</span>
                        {careerGoal.country && <span>• {careerGoal.country}</span>}
                        {careerGoal.timeline && <span>• {careerGoal.timeline}</span>}
                    </div>
                )}

                {/* Nav */}
                <nav className="flex items-center gap-1">
                    {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
                        <button
                            key={id}
                            onClick={() => onNav(id)}
                            aria-current={page === id ? 'page' : undefined}
                            className={`hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all
                ${page === id
                                    ? 'bg-[#6366f1]/15 text-[#818cf8]'
                                    : 'text-[#8888a8] hover:text-[#e8e8f0] hover:bg-[#1e1e2e]'
                                }`}
                        >
                            <Icon size={13} />
                            {label}
                        </button>
                    ))}
                </nav>
            </div>
        </header>
    )
}
