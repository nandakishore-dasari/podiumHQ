import React, { useState, useEffect } from 'react';
import { X, Save, AlertCircle } from 'lucide-react';

export function TeamManagementModal({ isOpen, onClose, onSave, team, eventId }) {
  const [formData, setFormData] = useState({
    name: '',
    project_title: '',
    project_repo_url: '',
    demo_url: '',
    track: 'DevSecOps & Cloud Native',
  });
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (team) {
      setFormData({
        name: team.name || '',
        project_title: team.project_title || '',
        project_repo_url: team.project_repo_url || '',
        demo_url: team.demo_url || '',
        track: team.track || 'DevSecOps & Cloud Native',
      });
    } else {
      setFormData({
        name: '',
        project_title: '',
        project_repo_url: '',
        demo_url: '',
        track: 'DevSecOps & Cloud Native',
      });
    }
    setError('');
  }, [team, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.project_title.trim()) {
      setError('Team name and project title are required.');
      return;
    }

    setSaving(true);
    setError('');
    try {
      if (team) {
        await onSave(team.id, formData);
      } else {
        await onSave(null, { ...formData, event_id: eventId || 1 });
      }
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to save team');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 50,
      padding: '1rem',
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '520px',
        background: '#0D1322',
        border: '1px solid var(--color-border)',
        borderRadius: '16px',
        overflow: 'hidden',
        boxShadow: '0 20px 50px rgba(0, 0, 0, 0.6)',
      }}>
        {/* Modal Header */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--color-border)',
        }}>
          <h3 className="font-display" style={{ fontSize: '1.15rem', fontWeight: '700', color: '#F8FAFC' }}>
            {team ? 'Edit Team Details' : 'Register New Hackathon Team'}
          </h3>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#94A3B8',
              cursor: 'pointer',
              padding: '0.25rem',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} style={{ padding: '1.5rem' }}>
          {error && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.75rem',
              borderRadius: '8px',
              background: 'rgba(244, 63, 94, 0.12)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              color: '#FDA4AF',
              fontSize: '0.82rem',
              marginBottom: '1.25rem',
            }}>
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: '#CBD5E1', marginBottom: '0.35rem' }}>
              Team Name *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. ZeroTrust Sentinel"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--color-border)',
                color: '#F8FAFC',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: '#CBD5E1', marginBottom: '0.35rem' }}>
              Project Title *
            </label>
            <input
              type="text"
              required
              value={formData.project_title}
              onChange={(e) => setFormData({ ...formData, project_title: e.target.value })}
              placeholder="e.g. eBPF Network Policy Enforcement Engine"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--color-border)',
                color: '#F8FAFC',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: '#CBD5E1', marginBottom: '0.35rem' }}>
              Competition Track
            </label>
            <select
              value={formData.track}
              onChange={(e) => setFormData({ ...formData, track: e.target.value })}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                background: '#070A11',
                border: '1px solid var(--color-border)',
                color: '#F8FAFC',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            >
              <option value="DevSecOps & Platform Defense">DevSecOps & Platform Defense</option>
              <option value="Cloud Native AI & Autonomous SRE">Cloud Native AI & Autonomous SRE</option>
              <option value="Zero-Trust Infrastructure">Zero-Trust Infrastructure</option>
              <option value="Observability & Telemetry">Observability & Telemetry</option>
              <option value="Infrastructure Optimization">Infrastructure Optimization</option>
            </select>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: '#CBD5E1', marginBottom: '0.35rem' }}>
                GitHub Repository URL
              </label>
              <input
                type="url"
                value={formData.project_repo_url}
                onChange={(e) => setFormData({ ...formData, project_repo_url: e.target.value })}
                placeholder="https://github.com/..."
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.04)',
                  border: '1px solid var(--color-border)',
                  color: '#F8FAFC',
                  fontSize: '0.85rem',
                  outline: 'none',
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: '#CBD5E1', marginBottom: '0.35rem' }}>
                Live Demo / Ingress URL
              </label>
              <input
                type="url"
                value={formData.demo_url}
                onChange={(e) => setFormData({ ...formData, demo_url: e.target.value })}
                placeholder="https://demo.podiumhq.local"
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.04)',
                  border: '1px solid var(--color-border)',
                  color: '#F8FAFC',
                  fontSize: '0.85rem',
                  outline: 'none',
                }}
              />
            </div>
          </div>

          {/* Footer Actions */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
            <button type="button" onClick={onClose} className="btn-secondary" disabled={saving}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={saving}>
              <Save size={16} />
              <span>{saving ? 'Saving...' : team ? 'Update Team' : 'Register Team'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
