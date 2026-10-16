import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { LeaderboardPage } from './pages/LeaderboardPage';
import { TeamsPage } from './pages/TeamsPage';
import { ScoringPage } from './pages/ScoringPage';
import { EventsRoundsPage } from './pages/EventsRoundsPage';
import { SystemHealthPage } from './pages/SystemHealthPage';

export function App() {
  const [activeTab, setActiveTab] = useState('leaderboard');
  const [selectedTeamForScoring, setSelectedTeamForScoring] = useState(null);

  const handleScoreTeam = (team) => {
    setSelectedTeamForScoring(team);
    setActiveTab('scoring');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Brand Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        liveStatus="TELEMETRY ACTIVE"
      />

      {/* Main Content Area */}
      <main style={{ flex: 1, maxWidth: '1400px', width: '100%', margin: '0 auto', padding: '1.75rem 1.5rem' }}>
        {activeTab === 'leaderboard' && (
          <LeaderboardPage onSelectTeamForScoring={handleScoreTeam} />
        )}
        {activeTab === 'teams' && (
          <TeamsPage onScoreTeam={handleScoreTeam} />
        )}
        {activeTab === 'scoring' && (
          <ScoringPage initialTeam={selectedTeamForScoring} />
        )}
        {activeTab === 'criteria' && (
          <EventsRoundsPage />
        )}
        {activeTab === 'ops' && (
          <SystemHealthPage />
        )}
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--color-border)',
        padding: '1.5rem',
        textAlign: 'center',
        fontSize: '0.8rem',
        color: '#64748B',
        background: 'rgba(7, 10, 17, 0.95)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <span>PodiumHQ &copy; 2026 DevSecOps Capstone</span>
          <span>&bull;</span>
          <span>FastAPI + React + EKS + ArgoCD GitOps</span>
          <span>&bull;</span>
          <span>Trivy Hardened & Non-Root SecurityContext</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
