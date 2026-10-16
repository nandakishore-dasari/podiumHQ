import React from 'react';
import { Award, Users, Scale, Activity, Layers, ShieldCheck } from 'lucide-react';

export function Navbar({ activeTab, setActiveTab, liveStatus }) {
  const navItems = [
    { id: 'leaderboard', label: 'Live Leaderboard', icon: Award },
    { id: 'teams', label: 'Teams & Projects', icon: Users },
    { id: 'scoring', label: 'Judge Console', icon: Scale },
    { id: 'criteria', label: 'Rounds & Criteria', icon: Layers },
    { id: 'ops', label: 'DevSecOps Telemetry', icon: Activity },
  ];

  return (
    <header style={{
      borderBottom: '1px solid var(--color-border)',
      background: 'rgba(7, 10, 17, 0.85)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 40,
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0.85rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 16px rgba(245, 158, 11, 0.4)',
          }}>
            <Award size={22} color="#070A11" strokeWidth={2.5} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="font-display" style={{ fontSize: '1.25rem', fontWeight: '800', letterSpacing: '-0.02em', color: '#F8FAFC' }}>
                PODIUM<span style={{ color: '#F59E0B' }}>HQ</span>
              </span>
              <span style={{
                background: 'rgba(245, 158, 11, 0.12)',
                border: '1px solid rgba(245, 158, 11, 0.3)',
                color: '#FBBF24',
                fontSize: '0.65rem',
                fontWeight: '700',
                padding: '0.1rem 0.45rem',
                borderRadius: '4px',
                letterSpacing: '0.05em',
              }}>
                DEVSECOPS CAPSTONE
              </span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#94A3B8' }}>
              Hackathon & Event Judging Platform
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  padding: '0.55rem 0.95rem',
                  borderRadius: '8px',
                  fontSize: '0.86rem',
                  fontWeight: isActive ? '700' : '500',
                  color: isActive ? '#070A11' : '#94A3B8',
                  background: isActive ? 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)' : 'transparent',
                  border: isActive ? '1px solid #F59E0B' : '1px solid transparent',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  boxShadow: isActive ? '0 2px 10px rgba(245, 158, 11, 0.3)' : 'none',
                }}
              >
                <Icon size={16} strokeWidth={isActive ? 2.5 : 2} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Live Cluster & Telemetry Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.35rem 0.75rem',
            borderRadius: '20px',
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            fontSize: '0.75rem',
            color: '#34D399',
            fontFamily: 'var(--font-mono)',
          }}>
            <span className="pulse-green" style={{
              width: '7px',
              height: '7px',
              borderRadius: '50%',
              backgroundColor: '#10B981',
              display: 'inline-block',
            }} />
            <span>{liveStatus || 'LIVE TELEMETRY'}</span>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem',
            padding: '0.35rem 0.65rem',
            borderRadius: '6px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--color-border)',
            fontSize: '0.72rem',
            color: '#CBD5E1',
            fontFamily: 'var(--font-mono)',
          }}>
            <ShieldCheck size={14} color="#10B981" />
            <span>EKS: ap-south-1</span>
          </div>
        </div>
      </div>
    </header>
  );
}
