import React from 'react';
import { Crown } from 'lucide-react';

export function LeaderboardPodium({ rankings }) {
  if (!rankings || rankings.length === 0) return null;

  const top1 = rankings[0];
  const top2 = rankings.length > 1 ? rankings[1] : null;
  const top3 = rankings.length > 2 ? rankings[2] : null;

  return (
    <div style={{
      marginBottom: '2.5rem',
      padding: '2rem 1.5rem',
      borderRadius: '18px',
      background: 'radial-gradient(ellipse at 50% 20%, rgba(245, 158, 11, 0.08) 0%, rgba(13, 19, 34, 0.6) 80%)',
      border: '1px solid rgba(245, 158, 11, 0.2)',
    }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(245, 158, 11, 0.12)',
          border: '1px solid rgba(245, 158, 11, 0.3)',
          color: '#FBBF24',
          fontSize: '0.75rem',
          fontWeight: '700',
          padding: '0.2rem 0.75rem',
          borderRadius: '9999px',
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
          marginBottom: '0.5rem',
        }}>
          <Crown size={14} color="#F59E0B" />
          <span>Championship Podium</span>
        </div>
        <h2 className="font-display" style={{ fontSize: '1.85rem', fontWeight: '800', color: '#F8FAFC' }}>
          Current Event Standings
        </h2>
        <p style={{ color: '#94A3B8', fontSize: '0.88rem', maxWidth: '500px', margin: '0.25rem auto 0' }}>
          Evaluated across multi-round criteria with automated tie-breaking hierarchy.
        </p>
      </div>

      {/* Podium Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        alignItems: 'end',
        gap: '1.5rem',
        maxWidth: '1050px',
        margin: '0 auto',
      }}>
        {/* Silver - 2nd Place */}
        {top2 ? (
          <div className="podium-rank-2" style={{
            borderRadius: '16px',
            padding: '1.75rem 1.25rem',
            textAlign: 'center',
            position: 'relative',
          }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #CBD5E1 0%, #64748B 100%)',
              color: '#070A11',
              fontWeight: '900',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '-42px auto 0.75rem',
              boxShadow: '0 4px 14px rgba(203, 213, 225, 0.4)',
              border: '2px solid #070A11',
            }}>
              2
            </div>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#CBD5E1', letterSpacing: '0.06em' }}>
              SILVER PODIUM
            </div>
            <div className="font-display" style={{ fontSize: '1.25rem', fontWeight: '800', color: '#F8FAFC', marginTop: '0.25rem' }}>
              {top2.team_name}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#94A3B8', marginTop: '0.2rem', minHeight: '38px' }}>
              {top2.project_title}
            </div>
            <div style={{ margin: '0.85rem 0', display: 'flex', justifyContent: 'center' }}>
              <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.08)', color: '#CBD5E1' }}>
                {top2.track}
              </span>
            </div>
            <div className="font-mono" style={{ fontSize: '1.75rem', fontWeight: '800', color: '#F8FAFC' }}>
              {top2.composite_score.toFixed(2)}
              <span style={{ fontSize: '0.85rem', color: '#94A3B8', fontWeight: '400', marginLeft: '0.2rem' }}>pts</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#64748B', marginTop: '0.35rem' }}>
              {top2.total_evaluations} evaluations submitted
            </div>
          </div>
        ) : <div />}

        {/* Gold - 1st Place */}
        <div className="podium-rank-1" style={{
          borderRadius: '16px',
          padding: '2.25rem 1.5rem',
          textAlign: 'center',
          position: 'relative',
          transform: 'translateY(-12px)',
        }}>
          <div style={{
            position: 'absolute',
            top: '-26px',
            left: '50%',
            transform: 'translateX(-50%)',
          }}>
            <Crown size={28} color="#F59E0B" strokeWidth={2.5} />
          </div>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
            color: '#070A11',
            fontWeight: '900',
            fontSize: '1.35rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '-46px auto 0.75rem',
            boxShadow: '0 6px 20px rgba(245, 158, 11, 0.5)',
            border: '2px solid #070A11',
          }}>
            1
          </div>
          <div style={{ fontSize: '0.75rem', fontWeight: '800', color: '#F59E0B', letterSpacing: '0.08em' }}>
            GOLD CHAMPION
          </div>
          <div className="font-display" style={{ fontSize: '1.45rem', fontWeight: '800', color: '#F8FAFC', marginTop: '0.25rem' }}>
            {top1.team_name}
          </div>
          <div style={{ fontSize: '0.84rem', color: '#CBD5E1', marginTop: '0.25rem', minHeight: '40px' }}>
            {top1.project_title}
          </div>
          <div style={{ margin: '0.85rem 0', display: 'flex', justifyContent: 'center' }}>
            <span className="badge" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#FDE68A', border: '1px solid rgba(245, 158, 11, 0.35)' }}>
              {top1.track}
            </span>
          </div>
          <div className="font-mono" style={{ fontSize: '2.25rem', fontWeight: '800', color: '#FBBF24', textShadow: '0 0 20px rgba(245, 158, 11, 0.4)' }}>
            {top1.composite_score.toFixed(2)}
            <span style={{ fontSize: '0.9rem', color: '#CBD5E1', fontWeight: '400', marginLeft: '0.2rem' }}>pts</span>
          </div>
          <div style={{ fontSize: '0.74rem', color: '#FDE68A', marginTop: '0.35rem', fontWeight: '600' }}>
            Leading by {top2 ? (top1.composite_score - top2.composite_score).toFixed(2) : '0.00'} pts
          </div>
        </div>

        {/* Bronze - 3rd Place */}
        {top3 ? (
          <div className="podium-rank-3" style={{
            borderRadius: '16px',
            padding: '1.75rem 1.25rem',
            textAlign: 'center',
            position: 'relative',
          }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #D97706 0%, #78350F 100%)',
              color: '#F8FAFC',
              fontWeight: '900',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '-42px auto 0.75rem',
              boxShadow: '0 4px 14px rgba(217, 119, 6, 0.4)',
              border: '2px solid #070A11',
            }}>
              3
            </div>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#D97706', letterSpacing: '0.06em' }}>
              BRONZE PODIUM
            </div>
            <div className="font-display" style={{ fontSize: '1.25rem', fontWeight: '800', color: '#F8FAFC', marginTop: '0.25rem' }}>
              {top3.team_name}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#94A3B8', marginTop: '0.2rem', minHeight: '38px' }}>
              {top3.project_title}
            </div>
            <div style={{ margin: '0.85rem 0', display: 'flex', justifyContent: 'center' }}>
              <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.08)', color: '#CBD5E1' }}>
                {top3.track}
              </span>
            </div>
            <div className="font-mono" style={{ fontSize: '1.75rem', fontWeight: '800', color: '#F8FAFC' }}>
              {top3.composite_score.toFixed(2)}
              <span style={{ fontSize: '0.85rem', color: '#94A3B8', fontWeight: '400', marginLeft: '0.2rem' }}>pts</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#64748B', marginTop: '0.35rem' }}>
              {top3.total_evaluations} evaluations submitted
            </div>
          </div>
        ) : <div />}
      </div>
    </div>
  );
}
