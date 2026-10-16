import React, { useState } from 'react';
import { RefreshCw, ArrowUp, ArrowDown, Minus, ChevronDown, ChevronUp, Layers } from 'lucide-react';

export function LeaderboardTable({
  rankings,
  loading,
  onRefresh,
  autoRefresh,
  setAutoRefresh,
  activeRound,
}) {
  const [expandedTeamId, setExpandedTeamId] = useState(null);

  const toggleExpand = (id) => {
    setExpandedTeamId(expandedTeamId === id ? null : id);
  };

  return (
    <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
      {/* Header with Auto-refresh & Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        marginBottom: '1.25rem',
        paddingBottom: '1rem',
        borderBottom: '1px solid var(--color-border)',
      }}>
        <div>
          <h3 className="font-display" style={{ fontSize: '1.25rem', fontWeight: '700', color: '#F8FAFC' }}>
            Live Leaderboard Standings
          </h3>
          <div style={{ fontSize: '0.8rem', color: '#94A3B8' }}>
            Active Stage: <span style={{ color: '#F59E0B', fontWeight: '600' }}>{activeRound || 'Round 1 & 2 Evaluations'}</span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Auto Refresh Toggle */}
          <label style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.8rem',
            color: autoRefresh ? '#34D399' : '#94A3B8',
            cursor: 'pointer',
            padding: '0.4rem 0.75rem',
            borderRadius: '6px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--color-border)',
          }}>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              style={{ cursor: 'pointer', accentColor: '#10B981' }}
            />
            <span>Auto-Refresh (10s)</span>
          </label>

          {/* Manual Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={loading}
            className="btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}
          >
            <RefreshCw size={14} className={loading ? 'pulse-green' : ''} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{
              borderBottom: '1px solid var(--color-border)',
              color: 'var(--text-muted)',
              fontSize: '0.75rem',
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
            }}>
              <th style={{ padding: '0.75rem 0.5rem', width: '70px', textAlign: 'center' }}>Rank</th>
              <th style={{ padding: '0.75rem 0.5rem', width: '80px', textAlign: 'center' }}>Delta</th>
              <th style={{ padding: '0.75rem 1rem' }}>Team & Project</th>
              <th style={{ padding: '0.75rem 0.75rem' }}>Track</th>
              <th style={{ padding: '0.75rem 0.75rem' }}>Status</th>
              <th style={{ padding: '0.75rem 0.75rem', textAlign: 'right' }}>Weighted Score</th>
              <th style={{ padding: '0.75rem 0.5rem', width: '60px', textAlign: 'center' }}>Details</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((team) => {
              const isExpanded = expandedTeamId === team.team_id;

              return (
                <React.Fragment key={team.team_id}>
                  <tr
                    onClick={() => toggleExpand(team.team_id)}
                    style={{
                      borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                      cursor: 'pointer',
                      transition: 'background 0.15s ease',
                      background: team.rank === 1
                        ? 'rgba(245, 158, 11, 0.05)'
                        : isExpanded
                        ? 'rgba(255, 255, 255, 0.03)'
                        : 'transparent',
                    }}
                    className="bg-surface-hover"
                  >
                    {/* Rank */}
                    <td style={{ padding: '0.9rem 0.5rem', textAlign: 'center' }}>
                      <span className="font-display" style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '28px',
                        height: '28px',
                        borderRadius: '6px',
                        fontSize: '0.9rem',
                        fontWeight: '800',
                        color: team.rank === 1 ? '#F59E0B' : team.rank === 2 ? '#CBD5E1' : team.rank === 3 ? '#D97706' : '#94A3B8',
                        background: team.rank <= 3 ? 'rgba(255, 255, 255, 0.06)' : 'transparent',
                        border: team.rank <= 3 ? '1px solid rgba(255, 255, 255, 0.12)' : 'none',
                      }}>
                        #{team.rank}
                      </span>
                    </td>

                    {/* Rank Delta Badge */}
                    <td style={{ padding: '0.9rem 0.5rem', textAlign: 'center' }}>
                      {team.rank_delta > 0 ? (
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.15rem',
                          color: '#34D399',
                          background: 'rgba(16, 185, 129, 0.12)',
                          padding: '0.2rem 0.45rem',
                          borderRadius: '4px',
                          fontSize: '0.74rem',
                          fontWeight: '700',
                          fontFamily: 'var(--font-mono)',
                        }}>
                          <ArrowUp size={12} />
                          <span>+{team.rank_delta}</span>
                        </span>
                      ) : team.rank_delta < 0 ? (
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.15rem',
                          color: '#FDA4AF',
                          background: 'rgba(244, 63, 94, 0.12)',
                          padding: '0.2rem 0.45rem',
                          borderRadius: '4px',
                          fontSize: '0.74rem',
                          fontWeight: '700',
                          fontFamily: 'var(--font-mono)',
                        }}>
                          <ArrowDown size={12} />
                          <span>{team.rank_delta}</span>
                        </span>
                      ) : (
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.15rem',
                          color: '#64748B',
                          fontSize: '0.75rem',
                          fontFamily: 'var(--font-mono)',
                        }}>
                          <Minus size={12} />
                          <span>0</span>
                        </span>
                      )}
                    </td>

                    {/* Team & Project */}
                    <td style={{ padding: '0.9rem 1rem' }}>
                      <div className="font-display" style={{ fontWeight: '700', fontSize: '0.95rem', color: '#F8FAFC' }}>
                        {team.team_name}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: '#94A3B8', marginTop: '0.1rem' }}>
                        {team.project_title}
                      </div>
                    </td>

                    {/* Track */}
                    <td style={{ padding: '0.9rem 0.75rem' }}>
                      <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: '#CBD5E1', fontSize: '0.7rem' }}>
                        {team.track}
                      </span>
                    </td>

                    {/* Status */}
                    <td style={{ padding: '0.9rem 0.75rem' }}>
                      <span className={`badge badge-${team.status}`}>
                        {team.status.replace('_', ' ')}
                      </span>
                    </td>

                    {/* Weighted Score */}
                    <td style={{ padding: '0.9rem 0.75rem', textAlign: 'right' }}>
                      <span className="font-mono" style={{
                        fontSize: '1.25rem',
                        fontWeight: '800',
                        color: team.rank === 1 ? '#FBBF24' : '#F8FAFC',
                      }}>
                        {team.composite_score.toFixed(2)}
                      </span>
                      <span style={{ fontSize: '0.72rem', color: '#94A3B8', marginLeft: '0.2rem' }}>pts</span>
                    </td>

                    {/* Expand Toggle */}
                    <td style={{ padding: '0.9rem 0.5rem', textAlign: 'center', color: '#64748B' }}>
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </td>
                  </tr>

                  {/* Expanded Breakdown Drawer */}
                  {isExpanded && (
                    <tr style={{ background: 'rgba(10, 15, 27, 0.8)' }}>
                      <td colSpan="7" style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--color-border)' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
                          {/* Round Contributions */}
                          <div>
                            <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: '0.4rem',
                              fontSize: '0.78rem',
                              fontWeight: '700',
                              color: '#F59E0B',
                              marginBottom: '0.5rem',
                              textTransform: 'uppercase',
                              letterSpacing: '0.05em',
                            }}>
                              <Layers size={14} />
                              <span>Round Score Contributions</span>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                              {team.rounds_breakdown?.map((rb, idx) => (
                                <div key={idx} style={{
                                  display: 'flex',
                                  justifyContent: 'space-between',
                                  padding: '0.4rem 0.65rem',
                                  background: 'rgba(255, 255, 255, 0.03)',
                                  borderRadius: '6px',
                                  fontSize: '0.78rem',
                                }}>
                                  <span style={{ color: '#CBD5E1' }}>{rb.round_name} (w={rb.weight})</span>
                                  <span className="font-mono" style={{ fontWeight: '700', color: '#F8FAFC' }}>
                                    {rb.score.toFixed(2)} / 10
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Criteria Averages */}
                          <div>
                            <div style={{
                              fontSize: '0.78rem',
                              fontWeight: '700',
                              color: '#34D399',
                              marginBottom: '0.5rem',
                              textTransform: 'uppercase',
                              letterSpacing: '0.05em',
                            }}>
                              Criterion Breakdown (Judge Average)
                            </div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                              {Object.entries(team.criteria_scores || {}).map(([cName, cScore], idx) => (
                                <div key={idx} style={{
                                  padding: '0.35rem 0.6rem',
                                  borderRadius: '6px',
                                  background: 'rgba(16, 185, 129, 0.08)',
                                  border: '1px solid rgba(16, 185, 129, 0.2)',
                                  fontSize: '0.75rem',
                                }}>
                                  <span style={{ color: '#94A3B8' }}>{cName}: </span>
                                  <span className="font-mono" style={{ fontWeight: '700', color: '#6EE7B7' }}>
                                    {cScore.toFixed(1)}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
