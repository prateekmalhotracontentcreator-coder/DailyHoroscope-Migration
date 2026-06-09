import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { History, Loader2, RefreshCw, XCircle } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const statusChipClass = (status) => ({
  sent: 'bg-green-500/20 text-green-400',
  pending: 'bg-yellow-500/20 text-yellow-400',
  failed: 'bg-red-500/20 text-red-400',
  skipped: 'bg-gray-500/20 text-gray-400',
}[status] || 'bg-gray-500/20 text-gray-400');

const StageCell = ({ stage }) => (
  <span className={`inline-flex px-2 py-1 rounded text-xs font-medium capitalize ${statusChipClass(stage?.status)}`}>
    {stage?.status || 'pending'}
  </span>
);

export const LifecycleSequencesTab = ({ getAuthHeaders }) => {
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [sequences, setSequences] = useState([]);
  const [canceling, setCanceling] = useState(null);

  const fetchSequences = async (nextFilter = filter) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/admin/lifecycle-sequences?status=${nextFilter}&limit=100`, { headers: getAuthHeaders() });
      setSequences(res.data.sequences || []);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to load lifecycle sequences');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSequences(filter);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  const handleCancel = async (sequenceId) => {
    setCanceling(sequenceId);
    try {
      await axios.post(`${API}/admin/lifecycle-sequences/${sequenceId}/cancel`, {}, { headers: getAuthHeaders() });
      toast.success('Lifecycle sequence cancelled');
      fetchSequences(filter);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to cancel sequence');
    } finally {
      setCanceling(null);
    }
  };

  return (
    <Card className="p-5 bg-gray-800 border-gray-700">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <History className="h-4 w-4 text-gold" />
            Lifecycle Sequences
          </h3>
          <p className="text-xs text-gray-400 mt-1">Stage 1 sends immediately after verification. Stages 2 and 3 are scheduler-driven.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {[
            { id: 'all', label: 'All' },
            { id: 'active', label: 'Active' },
            { id: 'completed', label: 'Completed' },
            { id: 'cancelled', label: 'Cancelled' },
          ].map((item) => (
            <Button
              key={item.id}
              size="sm"
              variant="outline"
              onClick={() => setFilter(item.id)}
              className={filter === item.id ? 'bg-gold/20 text-gold border-gold/40' : 'border-gray-600 text-gray-300'}
            >
              {item.label}
            </Button>
          ))}
          <Button onClick={() => fetchSequences(filter)} variant="outline" size="sm" className="border-gray-600 text-gray-300">
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </div>

      {loading && !sequences.length ? (
        <div className="text-gray-400 text-sm flex items-center gap-2 py-8 justify-center">
          <Loader2 className="h-4 w-4 animate-spin" /> Loading lifecycle sequences...
        </div>
      ) : sequences.length === 0 ? (
        <p className="text-gray-500 text-sm text-center py-8">No lifecycle sequences found for this filter.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-400 border-b border-gray-700">
                <th className="py-3 pr-4">User</th>
                <th className="py-3 pr-4">Product</th>
                <th className="py-3 pr-4">Started</th>
                <th className="py-3 pr-4">Stage 1</th>
                <th className="py-3 pr-4">Stage 2</th>
                <th className="py-3 pr-4">Stage 3</th>
                <th className="py-3 pr-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {sequences.map((sequence) => (
                <tr key={sequence.sequence_id} className="border-b border-gray-800 align-top">
                  <td className="py-3 pr-4">
                    <div className="text-white">{sequence.user_name || 'Seeker'}</div>
                    <div className="text-xs text-gray-400">{sequence.user_email}</div>
                  </td>
                  <td className="py-3 pr-4 text-gray-300">{sequence.product_name}</td>
                  <td className="py-3 pr-4 text-gray-400">{new Date(sequence.started_at).toLocaleString('en-IN')}</td>
                  <td className="py-3 pr-4"><StageCell stage={sequence.stages?.stage_1} /></td>
                  <td className="py-3 pr-4"><StageCell stage={sequence.stages?.stage_2} /></td>
                  <td className="py-3 pr-4"><StageCell stage={sequence.stages?.stage_3} /></td>
                  <td className="py-3 pr-4">
                    {!sequence.cancelled && sequence.derived_status !== 'completed' ? (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCancel(sequence.sequence_id)}
                        disabled={canceling === sequence.sequence_id}
                        className="border-red-700/50 text-red-400 hover:bg-red-900/20"
                      >
                        {canceling === sequence.sequence_id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <XCircle className="h-3.5 w-3.5 mr-1.5" />}
                        Cancel
                      </Button>
                    ) : (
                      <span className="text-xs text-gray-500 capitalize">{sequence.derived_status}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
};
