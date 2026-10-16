import React from 'react';
import { Users, FileCode, CheckCircle2, TrendingUp, Sliders } from 'lucide-react';

export function KpiCards({ stats, loading }) {
  if (loading && !stats) {
    return (
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '1rem',
        marginBottom: '1.75rem',
      }}>
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="glass-card skeleton" style={{ height: '95px' }} />
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'TOTAL TEAMS',
      value: stats?.total_teams ?? 0,
      sub: `${stats?.registered_count ?? 0} registered`,
      icon: Users,
      color: '#F59E0B',
      accentBg: 'rgba(245, 158, 11, 0.1)',
      borderAccent: 'rgba(245, 158, 11, 0.25)',
    },
    {
      title: 'PROJECTS SUBMITTED',
      value: stats?.submitted_count ?? 0,
      sub: 'Ready for evaluation',
      icon: FileCode,
      color: '#10B981',
      accentBg: 'rgba(16, 185, 129, 0.1)',
      borderAccent: 'rgba(16, 185, 129, 0.25)',
    },
    {
      title: 'EVALUATED & SCORED',
      value: stats?.scored_count ?? 0,
      sub: `${stats?.under_review_count ?? 0} under review`,
      icon: CheckCircle2,
      color: '#8B5CF6',
      accentBg: 'rgba(139, 92, 246, 0.1)',
      borderAccent: 'rgba(139, 92, 246, 0.25)',
    },
    {
      title: 'AVERAGE SCORE',
      value: `${stats?.average_score?.toFixed(1) ?? '0.0'} / 10`,
      sub: 'Normalized across rounds',
      icon: TrendingUp,
      color: '#38BDF8',
      accentBg: 'rgba(56, 189, 248, 0.1)',
      borderAccent: 'rgba(56, 189, 248, 0.25)',
    },
    {
      title: 'JUDGE AGREEMENT',
      value: `${((stats?.judge_agreement_index ?? 0.95) * 100).toFixed(0)}%`,
      sub: 'Consensus variance index',
      icon: Sliders,
      color: '#F43F5E',
      accentBg: 'rgba(244, 63, 94, 0.1)',
      borderAccent: 'rgba(244, 63, 94, 0.25)',
    },
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
      gap: '1rem',
      marginBottom: '1.75rem',
    }}>
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <div
            key={i}
            className="glass-card"
            style={{
              padding: '1.1rem 1.25rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderLeft: `4px solid ${c.color}`,
            }}
          >
            <div>
              <div style={{
                fontSize: '0.72rem',
                fontWeight: '700',
                letterSpacing: '0.06em',
                color: 'var(--text-muted)',
                marginBottom: '0.25rem',
              }}>
                {c.title}
              </div>
              <div className="font-display" style={{
                fontSize: '1.65rem',
                fontWeight: '800',
                color: '#F8FAFC',
                lineHeight: '1.2',
              }}>
                {c.value}
              </div>
              <div style={{ fontSize: '0.74rem', color: '#94A3B8', marginTop: '0.15rem' }}>
                {c.sub}
              </div>
            </div>

            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '10px',
              background: c.accentBg,
              border: `1px solid ${c.borderAccent}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <Icon size={20} color={c.color} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
