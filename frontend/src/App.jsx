import { useState, useCallback } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import LandingPage from './pages/LandingPage'
import AnalyzingPage from './pages/AnalyzingPage'
import ResearchPage from './pages/ResearchPage'
import AssessmentPage from './pages/AssessmentPage'
import CompletingPage from './pages/CompletingPage'
import SkillGapPage from './pages/SkillGapPage'
import ResourcesPage from './pages/ResourcesPage'
import RoadmapPage from './pages/RoadmapPage'
import Navbar from './components/Navbar'

/**
 * Top-level page states:
 * landing → analyzing → research → assessment → completing → skillgap → resources → roadmap
 */

const pageOrder = ['landing', 'analyzing', 'research', 'assessment', 'completing', 'skillgap', 'resources', 'roadmap']

export default function App() {
    const [page, setPage] = useState('landing')
    const [session, setSession] = useState({
        id: null,
        careerGoal: null,
        research: null,
        questions: null,
        skillGap: null,
        resources: null,
        roadmap: null,
    })

    const go = useCallback((p) => setPage(p), [])
    const updateSession = useCallback((patch) => setSession(s => ({ ...s, ...patch })), [])

    const showNav = page !== 'landing' && page !== 'analyzing' && page !== 'completing'
    const currentStep = pageOrder.indexOf(page)

    return (
        <div className="min-h-screen bg-[#09090f]">
            {showNav && (
                <Navbar
                    careerGoal={session.careerGoal}
                    page={page}
                    onNav={go}
                />
            )}
            <AnimatePresence mode="wait">
                {page === 'landing' && (
                    <PageWrap key="landing">
                        <LandingPage onStart={(id, cg) => {
                            updateSession({ id, careerGoal: cg })
                            go('analyzing')
                        }} />
                    </PageWrap>
                )}
                {page === 'analyzing' && (
                    <PageWrap key="analyzing">
                        <AnalyzingPage
                            sessionId={session.id}
                            onResearchDone={(research) => updateSession({ research })}
                            onQuestionsDone={(questions) => updateSession({ questions })}
                            onComplete={() => go('research')}
                            onError={() => go('landing')}
                        />
                    </PageWrap>
                )}
                {page === 'research' && (
                    <PageWrap key="research">
                        <ResearchPage
                            careerGoal={session.careerGoal}
                            research={session.research}
                            onContinue={() => go('assessment')}
                        />
                    </PageWrap>
                )}
                {page === 'assessment' && (
                    <PageWrap key="assessment">
                        <AssessmentPage
                            sessionId={session.id}
                            questions={session.questions}
                            onComplete={() => go('completing')}
                        />
                    </PageWrap>
                )}
                {page === 'completing' && (
                    <PageWrap key="completing">
                        <CompletingPage
                            sessionId={session.id}
                            onSkillGapDone={(skillGap) => updateSession({ skillGap })}
                            onResourcesDone={(resources) => updateSession({ resources })}
                            onRoadmapDone={(roadmap) => updateSession({ roadmap })}
                            onComplete={() => go('skillgap')}
                            onError={() => go('assessment')}
                        />
                    </PageWrap>
                )}
                {page === 'skillgap' && (
                    <PageWrap key="skillgap">
                        <SkillGapPage
                            careerGoal={session.careerGoal}
                            gaps={session.skillGap}
                            onContinue={() => go('resources')}
                        />
                    </PageWrap>
                )}
                {page === 'resources' && (
                    <PageWrap key="resources">
                        <ResourcesPage
                            resources={session.resources}
                            onContinue={() => go('roadmap')}
                        />
                    </PageWrap>
                )}
                {page === 'roadmap' && (
                    <PageWrap key="roadmap">
                        <RoadmapPage
                            careerGoal={session.careerGoal}
                            roadmap={session.roadmap}
                            onRestart={() => {
                                setSession({ id: null, careerGoal: null, research: null, questions: null, skillGap: null, resources: null, roadmap: null })
                                go('landing')
                            }}
                        />
                    </PageWrap>
                )}
            </AnimatePresence>
        </div>
    )
}

function PageWrap({ children }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
        >
            {children}
        </motion.div>
    )
}
