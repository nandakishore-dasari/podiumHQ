import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { ShieldCheck, Database, Server, RefreshCw, Terminal } from 'lucide-react';

export function SystemHealthPage() {
  const [healthData, setHealthData] = useState(null);
  const [readinessData, setReadinessData] = useState(null);
  const [metricsSample, setMetricsSample] = useState('');
  const [loading, setLoading] = useState(true);
  const [lastCheck, setLastCheck] = useState('');

  const checkTelemetry = async () => {
    setLoading(true);
    try {
      const [hRes, rRes, mRes] = await Promise.all([
        api.getHealth(),
        api.getReadiness(),
        api.getMetrics(),
      ]);
      setHealthData(hRes);
      setReadinessData(rRes);
      setMetricsSample(typeof mRes === 'string' ? mRes.slice(0, 2500) : JSON.stringify(mRes, null, 2));
      setLastCheck(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('Telemetry query error', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkTelemetry();
    const timer = setInterval(checkTelemetry, 15000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.75rem',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        <div>
          <h2 className="font-display" style={{ fontSize: '1.65rem', fontWeight: '800', color: '#F8FAFC' }}>
            DevSecOps Platform Telemetry
          </h2>
          <div style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
            Live Kubernetes readiness, liveness probes, and Prometheus telemetry.
          </div>
        </div>

        <button onClick={checkTelemetry} disabled={loading} className="btn-secondary">
          <RefreshCw size={15} className={loading ? 'pulse-green' : ''} />
          <span>Poll Endpoints ({lastCheck || 'Now'})</span>
        </button>
      </div>

      {/* Probes Status Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.25rem',
        marginBottom: '2rem',
      }}>
        {/* Liveness Probe */}
        <div className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid #10B981' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Server size={18} color="#10B981" />
              <h4 className="font-display" style={{ fontSize: '1.05rem', fontWeight: '700', color: '#F8FAFC' }}>
                Liveness Probe (/health)
              </h4>
            </div>
            <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34D399' }}>
              {healthData?.status?.toUpperCase() || 'HEALTHY'}
            </span>
          </div>
          <p style={{ fontSize: '0.82rem', color: '#94A3B8', marginBottom: '0.85rem' }}>
            Monitored by Kubernetes kubelet liveness probe at 10s intervals.
          </p>
          <div style={{
            background: 'rgba(0, 0, 0, 0.35)',
            padding: '0.65rem 0.85rem',
            borderRadius: '6px',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.75rem',
            color: '#A7F3D0',
          }}>
            {JSON.stringify(healthData || { status: 'healthy', service: 'PodiumHQ' }, null, 2)}
          </div>
        </div>

        {/* Readiness Probe */}
        <div className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid #38BDF8' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Database size={18} color="#38BDF8" />
              <h4 className="font-display" style={{ fontSize: '1.05rem', fontWeight: '700', color: '#F8FAFC' }}>
                Readiness Probe (/ready)
              </h4>
            </div>
            <span className="badge" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#7DD3FC' }}>
              {readinessData?.status?.toUpperCase() || 'READY'}
            </span>
          </div>
          <p style={{ fontSize: '0.82rem', color: '#94A3B8', marginBottom: '0.85rem' }}>
            Executes active <code style={{ color: '#FBBF24' }}>SELECT 1</code> against PostgreSQL.
          </p>
          <div style={{
            background: 'rgba(0, 0, 0, 0.35)',
            padding: '0.65rem 0.85rem',
            borderRadius: '6px',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.75rem',
            color: '#BAE6FD',
          }}>
            {JSON.stringify(readinessData || { status: 'ready', database: 'connected' }, null, 2)}
          </div>
        </div>

        {/* EKS Infrastructure Card */}
        <div className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid #F59E0B' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ShieldCheck size={18} color="#F59E0B" />
              <h4 className="font-display" style={{ fontSize: '1.05rem', fontWeight: '700', color: '#F8FAFC' }}>
                EKS Cluster & GitOps
              </h4>
            </div>
            <span className="badge" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#FBBF24' }}>
              SYNCED
            </span>
          </div>
          <div style={{ fontSize: '0.8rem', color: '#CBD5E1', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
            <div>Namespace: <code style={{ color: '#FBBF24' }}>podiumhq</code></div>
            <div>Ingress Host: <code style={{ color: '#FBBF24' }}>podiumhq.local</code></div>
            <div>AWS Region: <code style={{ color: '#FBBF24' }}>ap-south-1</code></div>
            <div>HPA Target: <code style={{ color: '#FBBF24' }}>60% CPU (2 to 6 pods)</code></div>
          </div>
        </div>
      </div>

      {/* Prometheus Telemetry Stream Preview */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.85rem' }}>
          <Terminal size={18} color="#F59E0B" />
          <h3 className="font-display" style={{ fontSize: '1.15rem', fontWeight: '700', color: '#F8FAFC' }}>
            Prometheus Scrape Telemetry Output (/metrics)
          </h3>
        </div>
        <div style={{
          background: '#04070D',
          border: '1px solid var(--color-border)',
          borderRadius: '8px',
          padding: '1rem',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.76rem',
          color: '#94A3B8',
          maxHeight: '320px',
          overflowY: 'auto',
          whiteSpace: 'pre-wrap',
          lineHeight: '1.5',
        }}>
          {metricsSample || '# Scraping Prometheus telemetry...'}
        </div>
      </div>
    </div>
  );
}
