import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Layers, Calendar, MapPin, Award } from 'lucide-react';

export function EventsRoundsPage() {
  const [event, setEvent] = useState(null);
  const [rounds, setRounds] = useState([]);
  const [criteria, setCriteria] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const eventsData = await api.getEvents();
        if (eventsData.items?.length > 0) {
          setEvent(eventsData.items[0]);
        }
        const [rList, cList] = await Promise.all([
          api.getRounds(),
          api.getCriteria(),
        ]);
        setRounds(rList || []);
        setCriteria(cList || []);
      } catch (err) {
        console.error('Failed to load event metadata', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
        <Layers size={32} className="pulse-green" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: '#94A3B8' }}>Loading competition criteria and rounds...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Event Overview Hero */}
      {event && (
        <div className="glass-card" style={{
          padding: '2rem',
          marginBottom: '2rem',
          background: 'linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(13, 19, 34, 0.7) 100%)',
          border: '1px solid rgba(245, 158, 11, 0.25)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <Award size={18} color="#F59E0B" />
            <span style={{ fontSize: '0.78rem', fontWeight: '700', color: '#F59E0B', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              Official Hackathon Event
            </span>
          </div>
          <h2 className="font-display" style={{ fontSize: '1.85rem', fontWeight: '800', color: '#F8FAFC' }}>
            {event.name}
          </h2>
          <p style={{ color: '#CBD5E1', fontSize: '0.92rem', maxWidth: '750px', marginTop: '0.5rem', lineHeight: '1.6' }}>
            {event.description}
          </p>

          <div style={{ display: 'flex', gap: '1.5rem', marginTop: '1.25rem', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', color: '#94A3B8' }}>
              <MapPin size={15} color="#38BDF8" />
              <span>{event.location}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', color: '#94A3B8' }}>
              <Calendar size={15} color="#10B981" />
              <span>Capacity: {event.max_teams} Teams Max</span>
            </div>
          </div>
        </div>
      )}

      {/* Judging Rounds Grid */}
      <h3 className="font-display" style={{ fontSize: '1.35rem', fontWeight: '800', color: '#F8FAFC', marginBottom: '1.25rem' }}>
        Evaluation Structure & Criteria Weights
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '1.5rem' }}>
        {rounds.map((r) => {
          const roundCriteria = criteria.filter((c) => c.round_id === r.id);

          return (
            <div key={r.id} className="glass-card" style={{ padding: '1.5rem', borderTop: '3px solid #F59E0B' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.06)', color: '#CBD5E1', marginBottom: '0.35rem' }}>
                    Stage #{r.round_number}
                  </span>
                  <h4 className="font-display" style={{ fontSize: '1.15rem', fontWeight: '700', color: '#F8FAFC' }}>
                    {r.name}
                  </h4>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94A3B8', textTransform: 'uppercase' }}>Multiplier</div>
                  <div className="font-mono" style={{ fontSize: '1.15rem', fontWeight: '800', color: '#FBBF24' }}>
                    {r.weight}x
                  </div>
                </div>
              </div>

              {/* Criteria List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {roundCriteria.map((crit) => (
                  <div
                    key={crit.id}
                    style={{
                      padding: '0.85rem 1rem',
                      borderRadius: '8px',
                      background: 'rgba(255, 255, 255, 0.02)',
                      border: '1px solid var(--color-border)',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: '600', fontSize: '0.86rem', color: '#F8FAFC' }}>
                        {crit.name}
                      </span>
                      <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#34D399', fontSize: '0.7rem' }}>
                        {(crit.weight * 100).toFixed(0)}% Weight
                      </span>
                    </div>
                    {crit.description && (
                      <p style={{ fontSize: '0.78rem', color: '#94A3B8', marginTop: '0.35rem', lineHeight: '1.4' }}>
                        {crit.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
