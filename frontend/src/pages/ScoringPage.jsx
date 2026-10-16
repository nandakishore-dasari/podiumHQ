import React, { useState, useEffect, useMemo } from 'react';
import { api } from '../api/client';
import { Scale, CheckCircle2, AlertCircle, Sparkles, Send, Lock } from 'lucide-react';

export function ScoringPage() {
  const [judges, setJudges] = useState([]);
  const [teams, setTeams] = useState([]);
  const [rounds, setRounds] = useState([]);
  const [criteria, setCriteria] = useState([]);

  const [selectedJudgeId, setSelectedJudgeId] = useState('');
  const [selectedTeamId, setSelectedTeamId] = useState('');
  const [selectedRoundId, setSelectedRoundId] = useState('');

  const [scoresMap, setScoresMap] = useState({});
  const [feedbackMap, setFeedbackMap] = useState({});

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [alertMessage, setAlertMessage] = useState({ type: '', text: '' });

  // Initial data load
  useEffect(() => {
    async function initData() {
      try {
        const [jList, tList, rList] = await Promise.all([
          api.getJudges(),
          api.getTeams({ pageSize: 50 }),
          api.getRounds(),
        ]);
        setJudges(jList || []);
        setTeams(tList.items || []);
        setRounds(rList || []);

        if (jList.length > 0) setSelectedJudgeId(jList[0].id.toString());
        if (tList.items?.length > 0) setSelectedTeamId(tList.items[0].id.toString());
        if (rList.length > 0) setSelectedRoundId(rList[0].id.toString());
      } catch (err) {
        setAlertMessage({ type: 'error', text: err.message || 'Error loading scoring parameters' });
      } finally {
        setLoading(false);
      }
    }
    initData();
  }, []);

  // Fetch criteria when selected round changes
  useEffect(() => {
    if (!selectedRoundId) return;
    async function loadCriteria() {
      try {
        const critList = await api.getCriteria(parseInt(selectedRoundId, 10));
        setCriteria(critList || []);

        // Initialize default scores
        const initialScores = {};
        const initialFeedbacks = {};
        (critList || []).forEach((c) => {
          initialScores[c.id] = 8.5;
          initialFeedbacks[c.id] = '';
        });
        setScoresMap(initialScores);
        setFeedbackMap(initialFeedbacks);
      } catch (err) {
        setAlertMessage({ type: 'error', text: 'Failed to load round criteria.' });
      }
    }
    loadCriteria();
  }, [selectedRoundId]);

  // Selected entities
  const activeRound = useMemo(() => {
    return rounds.find((r) => r.id.toString() === selectedRoundId);
  }, [rounds, selectedRoundId]);

  const activeTeam = useMemo(() => {
    return teams.find((t) => t.id.toString() === selectedTeamId);
  }, [teams, selectedTeamId]);

  // Real-time weighted preview calculation
  const calculatedPreview = useMemo(() => {
    if (!criteria.length) return { roundScore: 0, compositeContribution: 0 };
    const totalWeights = criteria.reduce((acc, c) => acc + c.weight, 0) || 1.0;
    let roundScore = 0.0;

    criteria.forEach((c) => {
      const raw = parseFloat(scoresMap[c.id] || 0.0);
      roundScore += raw * (c.weight / totalWeights);
    });

    const roundWeight = activeRound?.weight || 1.0;
    const compositeContribution = roundScore * roundWeight;

    return {
      roundScore: roundScore.toFixed(2),
      compositeContribution: compositeContribution.toFixed(2),
    };
  }, [criteria, scoresMap, activeRound]);

  const handleScoreChange = (criterionId, val) => {
    const num = Math.min(10.0, Math.max(0.0, parseFloat(val) || 0.0));
    setScoresMap((prev) => ({ ...prev, [criterionId]: num }));
  };

  const handleFeedbackChange = (criterionId, text) => {
    setFeedbackMap((prev) => ({ ...prev, [criterionId]: text }));
  };

  const handleSubmitEvaluation = async (e) => {
    e.preventDefault();
    if (!selectedJudgeId || !selectedTeamId || !selectedRoundId) {
      setAlertMessage({ type: 'error', text: 'Please ensure Judge, Team, and Round are selected.' });
      return;
    }

    if (activeRound?.status === 'closed') {
      setAlertMessage({ type: 'error', text: `Scoring is locked. Round '${activeRound.name}' is closed.` });
      return;
    }

    setSubmitting(true);
    setAlertMessage({ type: '', text: '' });

    try {
      const payload = {
        judge_id: parseInt(selectedJudgeId, 10),
        team_id: parseInt(selectedTeamId, 10),
        round_id: parseInt(selectedRoundId, 10),
        scores: criteria.map((c) => ({
          criterion_id: c.id,
          raw_score: parseFloat(scoresMap[c.id] || 0.0),
          feedback: feedbackMap[c.id] || 'Evaluated via judge console',
        })),
      };

      await api.submitBatchScores(payload);
      setAlertMessage({
        type: 'success',
        text: `Evaluation successfully recorded for '${activeTeam?.name}'! Live leaderboard updated.`,
      });
    } catch (err) {
      setAlertMessage({
        type: 'error',
        text: err.message || 'Evaluation rejected. You may have already scored this team.',
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
        <Scale size={32} className="pulse-green" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: '#94A3B8' }}>Loading judging matrix and criteria...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '1.75rem' }}>
        <h2 className="font-display" style={{ fontSize: '1.65rem', fontWeight: '800', color: '#F8FAFC' }}>
          Judge Evaluation Console
        </h2>
        <p style={{ fontSize: '0.86rem', color: '#94A3B8' }}>
          Score participating hackathon projects against weighted criteria with real-time composite preview.
        </p>
      </div>

      {alertMessage.text && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.65rem',
          padding: '0.9rem 1.25rem',
          borderRadius: '10px',
          background: alertMessage.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(244, 63, 94, 0.12)',
          border: alertMessage.type === 'success' ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(244, 63, 94, 0.3)',
          color: alertMessage.type === 'success' ? '#6EE7B7' : '#FDA4AF',
          fontSize: '0.88rem',
          marginBottom: '1.5rem',
        }}>
          {alertMessage.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
          <span>{alertMessage.text}</span>
        </div>
      )}

      {/* Selectors Bar */}
      <div className="glass-card" style={{
        padding: '1.5rem',
        marginBottom: '1.75rem',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '1.25rem',
      }}>
        {/* Judge Select */}
        <div>
          <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: '700', color: '#CBD5E1', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Evaluating Judge
          </label>
          <select
            value={selectedJudgeId}
            onChange={(e) => setSelectedJudgeId(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              background: '#070A11',
              border: '1px solid var(--color-border)',
              color: '#F8FAFC',
              fontSize: '0.88rem',
              outline: 'none',
            }}
          >
            {judges.map((j) => (
              <option key={j.id} value={j.id}>
                {j.name} ({j.organization})
              </option>
            ))}
          </select>
        </div>

        {/* Team Select */}
        <div>
          <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: '700', color: '#CBD5E1', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Target Team & Project
          </label>
          <select
            value={selectedTeamId}
            onChange={(e) => setSelectedTeamId(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              background: '#070A11',
              border: '1px solid var(--color-border)',
              color: '#F8FAFC',
              fontSize: '0.88rem',
              outline: 'none',
            }}
          >
            {teams.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} — {t.project_title.slice(0, 32)}...
              </option>
            ))}
          </select>
        </div>

        {/* Round Select */}
        <div>
          <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: '700', color: '#CBD5E1', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Judging Round
          </label>
          <select
            value={selectedRoundId}
            onChange={(e) => setSelectedRoundId(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              background: '#070A11',
              border: '1px solid var(--color-border)',
              color: '#F8FAFC',
              fontSize: '0.88rem',
              outline: 'none',
            }}
          >
            {rounds.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} (w={r.weight}) {r.status === 'closed' ? '🔒 [CLOSED]' : ''}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Target Project Summary Banner */}
      {activeTeam && (
        <div style={{
          padding: '1.25rem 1.5rem',
          borderRadius: '12px',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid var(--color-border)',
          marginBottom: '1.75rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
        }}>
          <div>
            <div style={{ fontSize: '0.74rem', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Project under evaluation
            </div>
            <div className="font-display" style={{ fontSize: '1.15rem', fontWeight: '700', color: '#F8FAFC' }}>
              {activeTeam.project_title}
            </div>
            <div style={{ fontSize: '0.78rem', color: '#F59E0B' }}>
              Team: {activeTeam.name} | Track: {activeTeam.track}
            </div>
          </div>

          {activeRound?.status === 'closed' && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.4rem 0.85rem',
              borderRadius: '6px',
              background: 'rgba(244, 63, 94, 0.15)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              color: '#FDA4AF',
              fontSize: '0.82rem',
              fontWeight: '700',
            }}>
              <Lock size={14} />
              <span>ROUND CLOSED (SCORING LOCKED)</span>
            </div>
          )}
        </div>
      )}

      {/* Criteria Sliders & Matrix */}
      <form onSubmit={handleSubmitEvaluation}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '2rem' }}>
          {criteria.map((c) => {
            const currentScore = scoresMap[c.id] ?? 8.0;

            return (
              <div
                key={c.id}
                className="glass-card"
                style={{
                  padding: '1.5rem',
                  borderLeft: '4px solid #F59E0B',
                }}
              >
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '0.75rem',
                  flexWrap: 'wrap',
                  gap: '0.5rem',
                }}>
                  <div>
                    <h4 className="font-display" style={{ fontSize: '1.05rem', fontWeight: '700', color: '#F8FAFC' }}>
                      {c.name}
                    </h4>
                    <p style={{ fontSize: '0.8rem', color: '#94A3B8', marginTop: '0.15rem', maxWidth: '600px' }}>
                      {c.description}
                    </p>
                  </div>

                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}>
                    <span className="badge" style={{ background: 'rgba(245, 158, 11, 0.12)', color: '#FBBF24' }}>
                      Weight: {(c.weight * 100).toFixed(0)}%
                    </span>
                    <div className="font-mono" style={{
                      fontSize: '1.35rem',
                      fontWeight: '800',
                      color: '#FBBF24',
                      minWidth: '55px',
                      textAlign: 'right',
                    }}>
                      {parseFloat(currentScore).toFixed(1)}
                    </div>
                  </div>
                </div>

                {/* Range Slider */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.85rem' }}>
                  <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: 'var(--font-mono)' }}>0.0</span>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    step="0.1"
                    value={currentScore}
                    onChange={(e) => handleScoreChange(c.id, e.target.value)}
                    disabled={activeRound?.status === 'closed'}
                    style={{
                      flex: 1,
                      accentColor: '#F59E0B',
                      cursor: activeRound?.status === 'closed' ? 'not-allowed' : 'pointer',
                    }}
                  />
                  <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: 'var(--font-mono)' }}>10.0</span>
                </div>

                {/* Qualitative Feedback */}
                <input
                  type="text"
                  placeholder="Optional evaluator qualitative notes..."
                  value={feedbackMap[c.id] || ''}
                  onChange={(e) => handleFeedbackChange(c.id, e.target.value)}
                  disabled={activeRound?.status === 'closed'}
                  style={{
                    width: '100%',
                    padding: '0.5rem 0.75rem',
                    borderRadius: '6px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--color-border)',
                    color: '#CBD5E1',
                    fontSize: '0.8rem',
                    outline: 'none',
                  }}
                />
              </div>
            );
          })}
        </div>

        {/* Live Calculation Preview & Submit Bar */}
        <div className="glass-card" style={{
          padding: '1.25rem 1.75rem',
          position: 'sticky',
          bottom: '1rem',
          background: 'rgba(13, 19, 34, 0.95)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(245, 158, 11, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1.25rem',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.7)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Sparkles size={20} color="#F59E0B" />
              <div>
                <div style={{ fontSize: '0.72rem', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Weighted Round Score
                </div>
                <div className="font-mono" style={{ fontSize: '1.35rem', fontWeight: '800', color: '#F8FAFC' }}>
                  {calculatedPreview.roundScore} <span style={{ fontSize: '0.8rem', color: '#94A3B8' }}>/ 10.0</span>
                </div>
              </div>
            </div>

            <div style={{ borderLeft: '1px solid var(--color-border)', paddingLeft: '1.5rem' }}>
              <div style={{ fontSize: '0.72rem', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Composite Contribution (w={activeRound?.weight})
              </div>
              <div className="font-mono" style={{ fontSize: '1.35rem', fontWeight: '800', color: '#FBBF24' }}>
                +{calculatedPreview.compositeContribution} pts
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting || activeRound?.status === 'closed'}
            className="btn-primary"
            style={{
              padding: '0.75rem 1.75rem',
              fontSize: '0.95rem',
              opacity: activeRound?.status === 'closed' ? 0.5 : 1,
            }}
          >
            <Send size={16} />
            <span>{submitting ? 'Submitting Evaluation...' : 'Submit Evaluation'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
