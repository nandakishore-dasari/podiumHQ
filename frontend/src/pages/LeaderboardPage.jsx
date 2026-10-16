import React, { useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';
import { KpiCards } from '../components/KpiCards';
import { LeaderboardPodium } from '../components/LeaderboardPodium';
import { LeaderboardTable } from '../components/LeaderboardTable';

export function LeaderboardPage({ _onSelectTeamForScoring }) {
  const [rankings, setRankings] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeRound, setActiveRound] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const [lbData, statsData] = await Promise.all([
        api.getLeaderboard(),
        api.getTeamStats(),
      ]);
      setRankings(lbData.rankings || []);
      setActiveRound(lbData.active_round || 'Evaluations In Progress');
      setStats(statsData);
      setError('');
    } catch (err) {
      setError(err.message || 'Unable to connect to PodiumHQ backend API');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Auto-refresh interval
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      loadData();
    }, 10000);
    return () => clearInterval(interval);
  }, [autoRefresh, loadData]);

  return (
    <div>
      {/* KPI Cards */}
      <KpiCards stats={stats} loading={loading} />

      {error && (
        <div style={{
          padding: '1rem',
          borderRadius: '10px',
          background: 'rgba(244, 63, 94, 0.12)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          color: '#FDA4AF',
          fontSize: '0.88rem',
          marginBottom: '1.5rem',
        }}>
          <strong>Connection Alert:</strong> {error}
        </div>
      )}

      {/* Podium Showcase */}
      {!loading && rankings.length > 0 && (
        <LeaderboardPodium rankings={rankings} />
      )}

      {/* Leaderboard Rankings Table */}
      <LeaderboardTable
        rankings={rankings}
        loading={loading}
        onRefresh={loadData}
        autoRefresh={autoRefresh}
        setAutoRefresh={setAutoRefresh}
        activeRound={activeRound}
      />
    </div>
  );
}
