import React, { useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';
import { TeamManagementModal } from '../components/TeamManagementModal';
import { DeleteConfirmModal } from '../components/DeleteConfirmModal';
import {
  Search,
  Plus,
  Filter,
  Edit2,
  Trash2,
  ExternalLink,
  Github,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';

export function TeamsPage({ _onScoreTeam }) {
  const [teams, setTeams] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(8);
  const [totalPages, setTotalPages] = useState(1);
  const [statusFilter, setStatusFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [actionError, setActionError] = useState('');

  // Modals state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTeam, setEditingTeam] = useState(null);
  const [deletingTeam, setDeletingTeam] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const fetchTeams = useCallback(async () => {
    setLoading(true);
    setActionError('');
    try {
      const data = await api.getTeams({
        status: statusFilter || null,
        search: searchQuery || null,
        page,
        pageSize,
      });
      setTeams(data.items || []);
      setTotal(data.total || 0);
      setTotalPages(data.pages || 1);
    } catch (err) {
      setActionError(err.message || 'Failed to fetch teams');
    } finally {
      setLoading(false);
    }
  }, [statusFilter, searchQuery, page, pageSize]);

  useEffect(() => {
    fetchTeams();
  }, [fetchTeams]);

  const handleCreateOrUpdate = async (teamId, payload) => {
    if (teamId) {
      await api.updateTeam(teamId, payload);
    } else {
      await api.createTeam(payload);
    }
    fetchTeams();
  };

  const handleStatusChange = async (teamId, newStatus) => {
    setActionError('');
    try {
      await api.updateTeamStatus(teamId, newStatus);
      fetchTeams();
    } catch (err) {
      setActionError(err.message || 'Status transition rejected by server.');
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deletingTeam) return;
    setIsDeleting(true);
    try {
      await api.deleteTeam(deletingTeam.id);
      setDeletingTeam(null);
      fetchTeams();
    } catch (err) {
      setActionError(err.message || 'Failed to delete team');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div>
      {/* Header Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        marginBottom: '1.5rem',
      }}>
        <div>
          <h2 className="font-display" style={{ fontSize: '1.65rem', fontWeight: '800', color: '#F8FAFC' }}>
            Registered Teams & Projects
          </h2>
          <div style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
            Manage participant lifecycle, project submissions, and status transitions.
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={() => { setEditingTeam(null); setIsModalOpen(true); }}
            className="btn-primary"
          >
            <Plus size={16} />
            <span>Register Team</span>
          </button>
        </div>
      </div>

      {actionError && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.85rem 1.1rem',
          borderRadius: '10px',
          background: 'rgba(244, 63, 94, 0.12)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          color: '#FDA4AF',
          fontSize: '0.85rem',
          marginBottom: '1.25rem',
        }}>
          <AlertCircle size={18} />
          <span>{actionError}</span>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="glass-card" style={{
        padding: '1rem 1.25rem',
        marginBottom: '1.25rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        {/* Search */}
        <div style={{
          position: 'relative',
          flex: '1',
          minWidth: '240px',
        }}>
          <Search size={16} color="#64748B" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder="Search teams, projects, or tracks..."
            value={searchQuery}
            onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
            style={{
              width: '100%',
              padding: '0.55rem 0.85rem 0.55rem 2.25rem',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--color-border)',
              color: '#F8FAFC',
              fontSize: '0.86rem',
              outline: 'none',
            }}
          />
        </div>

        {/* Status Filter */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Filter size={15} color="#94A3B8" />
          <span style={{ fontSize: '0.8rem', color: '#94A3B8' }}>Status:</span>
          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
            style={{
              padding: '0.5rem 0.75rem',
              borderRadius: '8px',
              background: '#070A11',
              border: '1px solid var(--color-border)',
              color: '#F8FAFC',
              fontSize: '0.82rem',
              outline: 'none',
            }}
          >
            <option value="">All Statuses ({total})</option>
            <option value="registered">Registered</option>
            <option value="submitted">Submitted</option>
            <option value="under_review">Under Review</option>
            <option value="scored">Scored</option>
            <option value="disqualified">Disqualified</option>
          </select>
        </div>
      </div>

      {/* Teams Data Table */}
      <div className="glass-card" style={{ padding: '0', overflow: 'hidden', marginBottom: '1.5rem' }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{
                background: 'rgba(255, 255, 255, 0.02)',
                borderBottom: '1px solid var(--color-border)',
                color: 'var(--text-muted)',
                fontSize: '0.74rem',
                letterSpacing: '0.06em',
                textTransform: 'uppercase',
              }}>
                <th style={{ padding: '0.85rem 1.25rem' }}>Team & Track</th>
                <th style={{ padding: '0.85rem 1rem' }}>Project Title & Links</th>
                <th style={{ padding: '0.85rem 1rem' }}>Lifecycle Status</th>
                <th style={{ padding: '0.85rem 1rem' }}>Advance State</th>
                <th style={{ padding: '0.85rem 1.25rem', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading && teams.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ padding: '3rem', textAlign: 'center', color: '#94A3B8' }}>
                    <RefreshCw size={24} className="pulse-green" style={{ margin: '0 auto 0.5rem' }} />
                    <div>Loading teams...</div>
                  </td>
                </tr>
              ) : teams.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ padding: '3rem', textAlign: 'center', color: '#94A3B8' }}>
                    No teams found matching the active filter criteria.
                  </td>
                </tr>
              ) : (
                teams.map((t) => (
                  <tr key={t.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }} className="bg-surface-hover">
                    {/* Team & Track */}
                    <td style={{ padding: '0.9rem 1.25rem' }}>
                      <div className="font-display" style={{ fontWeight: '700', fontSize: '0.95rem', color: '#F8FAFC' }}>
                        {t.name}
                      </div>
                      <div style={{ marginTop: '0.2rem' }}>
                        <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.06)', color: '#CBD5E1', fontSize: '0.68rem' }}>
                          {t.track}
                        </span>
                      </div>
                    </td>

                    {/* Project & Repos */}
                    <td style={{ padding: '0.9rem 1rem' }}>
                      <div style={{ fontSize: '0.85rem', color: '#CBD5E1', fontWeight: '500' }}>
                        {t.project_title}
                      </div>
                      <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.35rem' }}>
                        {t.project_repo_url && (
                          <a
                            href={t.project_repo_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.25rem',
                              fontSize: '0.72rem',
                              color: '#38BDF8',
                              textDecoration: 'none',
                            }}
                          >
                            <Github size={12} />
                            <span>Repository</span>
                          </a>
                        )}
                        {t.demo_url && (
                          <a
                            href={t.demo_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.25rem',
                              fontSize: '0.72rem',
                              color: '#10B981',
                              textDecoration: 'none',
                            }}
                          >
                            <ExternalLink size={12} />
                            <span>Live Demo</span>
                          </a>
                        )}
                      </div>
                    </td>

                    {/* Status Badge */}
                    <td style={{ padding: '0.9rem 1rem' }}>
                      <span className={`badge badge-${t.status}`}>
                        {t.status.replace('_', ' ')}
                      </span>
                    </td>

                    {/* Status State Transition Select */}
                    <td style={{ padding: '0.9rem 1rem' }}>
                      <select
                        value={t.status}
                        onChange={(e) => handleStatusChange(t.id, e.target.value)}
                        style={{
                          padding: '0.35rem 0.65rem',
                          borderRadius: '6px',
                          background: '#070A11',
                          border: '1px solid var(--color-border)',
                          color: '#CBD5E1',
                          fontSize: '0.75rem',
                          outline: 'none',
                        }}
                      >
                        <option value="registered">Registered</option>
                        <option value="submitted">Submitted</option>
                        <option value="under_review">Under Review</option>
                        <option value="scored">Scored</option>
                        <option value="disqualified">Disqualified</option>
                      </select>
                    </td>

                    {/* Actions */}
                    <td style={{ padding: '0.9rem 1.25rem', textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
                        <button
                          onClick={() => { setEditingTeam(t); setIsModalOpen(true); }}
                          title="Edit Team"
                          style={{
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid var(--color-border)',
                            color: '#CBD5E1',
                            padding: '0.4rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                          }}
                        >
                          <Edit2 size={14} />
                        </button>
                        <button
                          onClick={() => setDeletingTeam(t)}
                          title="Delete Team"
                          style={{
                            background: 'rgba(244, 63, 94, 0.1)',
                            border: '1px solid rgba(244, 63, 94, 0.25)',
                            color: '#FDA4AF',
                            padding: '0.4rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                          }}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.85rem 1.25rem',
          borderTop: '1px solid var(--color-border)',
          background: 'rgba(255, 255, 255, 0.01)',
          fontSize: '0.8rem',
          color: '#94A3B8',
        }}>
          <div>
            Showing {teams.length} of {total} teams (Page {page} of {totalPages})
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="btn-secondary"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
            >
              <ChevronLeft size={14} />
              <span>Previous</span>
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="btn-secondary"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
            >
              <span>Next</span>
              <ChevronRight size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Modals */}
      <TeamManagementModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleCreateOrUpdate}
        team={editingTeam}
      />

      <DeleteConfirmModal
        isOpen={Boolean(deletingTeam)}
        onClose={() => setDeletingTeam(null)}
        onConfirm={handleDeleteConfirm}
        itemName={deletingTeam?.name}
        loading={isDeleting}
      />
    </div>
  );
}
