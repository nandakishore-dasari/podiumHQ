import React from 'react';
import { AlertTriangle, Trash2 } from 'lucide-react';

export function DeleteConfirmModal({ isOpen, onClose, onConfirm, itemName, loading }) {
  if (!isOpen) return null;

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
        maxWidth: '440px',
        background: '#0D1322',
        border: '1px solid rgba(244, 63, 94, 0.3)',
        borderRadius: '16px',
        padding: '1.5rem',
        boxShadow: '0 20px 50px rgba(0, 0, 0, 0.7)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'rgba(244, 63, 94, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <AlertTriangle size={22} color="#F43F5E" />
          </div>
          <div>
            <h3 className="font-display" style={{ fontSize: '1.15rem', fontWeight: '700', color: '#F8FAFC' }}>
              Confirm Deletion
            </h3>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>
              This action cannot be undone
            </div>
          </div>
        </div>

        <p style={{ fontSize: '0.88rem', color: '#CBD5E1', marginBottom: '1.5rem', lineHeight: '1.5' }}>
          Are you sure you want to permanently delete <strong style={{ color: '#F8FAFC' }}>{itemName}</strong>?
          All associated scores, criteria evaluations, and telemetry data will be removed.
        </p>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button onClick={onClose} className="btn-secondary" disabled={loading}>
            Cancel
          </button>
          <button onClick={onConfirm} className="btn-danger" disabled={loading}>
            <Trash2 size={16} />
            <span>{loading ? 'Deleting...' : 'Delete Permanently'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
