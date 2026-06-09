import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Loader2, Mail, MessageCircle, RefreshCw, Send, Sparkles } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const TransitCampaignsTab = ({ getAuthHeaders }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [selectedSegment, setSelectedSegment] = useState(null);
  const [form, setForm] = useState({
    subject: '',
    body: '',
    channels: ['email'],
    limit: 200,
  });

  const segments = useMemo(() => Object.entries(summary?.segments || {}), [summary]);

  const fetchSummary = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/admin/transit-segments/summary`, { headers: getAuthHeaders() });
      setSummary(res.data);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to load transit segments');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const openComposer = (segmentId, label) => {
    setSelectedSegment({ id: segmentId, label, count: summary?.segments?.[segmentId]?.count || 0 });
    setForm({
      subject: `${label} guidance from the Temple`,
      body: `Namaste,\n\nA significant transit window is active in your chart right now. Open Everyday Horoscope and review your current guidance for this phase.\n\nIn alignment,\nThe EverydayHoroscope Temple`,
      channels: ['email'],
      limit: 200,
    });
  };

  const handleSend = async () => {
    if (!selectedSegment) return;
    if (!form.subject.trim() || !form.body.trim()) {
      toast.error('Subject and body are required');
      return;
    }
    if (!form.channels.length) {
      toast.error('Select at least one channel');
      return;
    }
    setSending(true);
    try {
      const res = await axios.post(`${API}/admin/transit-campaigns/trigger`, {
        segment_id: selectedSegment.id,
        subject: form.subject,
        body: form.body,
        channels: form.channels,
        limit: Number(form.limit) || 200,
      }, { headers: getAuthHeaders() });
      toast.success(`Sent ${res.data.sent} · Failed ${res.data.failed}`);
      setSelectedSegment(null);
      fetchSummary();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send campaign');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-gold" />
            Transit Campaigns
          </h3>
          <p className="text-xs text-gray-400 mt-1">
            {summary?.computed_at ? `Computed at ${new Date(summary.computed_at).toLocaleString('en-IN')} · Refreshes every 4h` : 'Segment audience is built from consented birth profiles only.'}
          </p>
        </div>
        <Button onClick={fetchSummary} variant="outline" size="sm" className="border-gray-600 text-gray-300">
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
        </Button>
      </div>

      {loading && !summary ? (
        <Card className="p-6 bg-gray-800 border-gray-700 text-gray-400 text-sm flex items-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin" /> Computing transit audiences...
        </Card>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {segments.map(([segmentId, segment]) => (
            <Card key={segmentId} className="p-5 bg-gray-800 border-gray-700">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h4 className="text-white font-semibold">{segment.label}</h4>
                  <p className="text-2xl font-bold text-gold mt-2">{segment.count}</p>
                  <p className="text-sm text-gray-400 mt-1">users currently in this phase</p>
                  <p className="text-xs text-gray-500 mt-3 leading-relaxed">{segment.description}</p>
                </div>
                <Button
                  size="sm"
                  className="bg-gold hover:bg-gold/90 text-gray-900"
                  onClick={() => openComposer(segmentId, segment.label)}
                >
                  <Send className="h-3.5 w-3.5 mr-1.5" />
                  Send Campaign
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {selectedSegment && (
        <Card className="p-6 bg-gray-800 border-gray-700">
          <div className="flex items-center justify-between gap-3 mb-4">
            <div>
              <h4 className="text-white font-semibold">Sending to: {selectedSegment.label} ({selectedSegment.count} users)</h4>
              <p className="text-xs text-gray-400 mt-1">Only consented profiles are included.</p>
            </div>
            <Button variant="outline" size="sm" className="border-gray-600 text-gray-300" onClick={() => setSelectedSegment(null)}>
              Close
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
              <Label className="text-gray-300 text-xs mb-2 block">Max recipients</Label>
              <Input
                type="number"
                min="1"
                max="500"
                value={form.limit}
                onChange={(e) => setForm((prev) => ({ ...prev, limit: e.target.value }))}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
            <div>
              <Label className="text-gray-300 text-xs mb-2 block">Channels</Label>
              <div className="flex flex-wrap gap-4">
                {[
                  { id: 'email', label: 'Email', icon: Mail },
                  { id: 'whatsapp', label: 'WhatsApp', icon: MessageCircle },
                ].map(({ id, label, icon: Icon }) => (
                  <label key={id} className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={form.channels.includes(id)}
                      onChange={(e) => setForm((prev) => ({
                        ...prev,
                        channels: e.target.checked ? [...prev.channels, id] : prev.channels.filter((channel) => channel !== id),
                      }))}
                    />
                    <Icon className="h-3.5 w-3.5 text-gray-400" />
                    {label}
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-4">
            <Label className="text-gray-300 text-xs mb-2 block">Subject</Label>
            <Input
              value={form.subject}
              onChange={(e) => setForm((prev) => ({ ...prev, subject: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>

          <div className="mt-4">
            <Label className="text-gray-300 text-xs mb-2 block">Body</Label>
            <textarea
              rows={8}
              value={form.body}
              onChange={(e) => setForm((prev) => ({ ...prev, body: e.target.value }))}
              className="w-full bg-gray-700 border border-gray-600 rounded-md text-white text-sm p-3 resize-y focus:outline-none focus:ring-1 focus:ring-gold"
            />
          </div>

          <div className="flex gap-3 mt-5">
            <Button onClick={handleSend} disabled={sending} className="bg-gold hover:bg-gold/90 text-gray-900">
              {sending ? <Loader2 className="h-3.5 w-3.5 mr-1.5 animate-spin" /> : <Send className="h-3.5 w-3.5 mr-1.5" />}
              {sending ? 'Sending...' : 'Send Campaign'}
            </Button>
            <Button variant="outline" className="border-gray-600 text-gray-300" onClick={() => setSelectedSegment(null)}>
              Cancel
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
};
