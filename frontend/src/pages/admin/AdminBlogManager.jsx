import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import {
  Plus, Edit, Trash2, Eye, EyeOff, Save, X, BookOpen,
  Calendar, Clock, Upload, ChevronDown, ChevronUp, List
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const EMPTY_FORM = {
  title: '', slug: '', excerpt: '', content: '',
  author: 'Cosmic Wisdom', category: 'Astrology',
  tags: '', featured_image: '', video_url: '',
  published: false, scheduled_at: ''
};

const generateSlug = (title) =>
  title.toLowerCase().trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');

export const AdminBlogManager = ({ getAuthHeaders }) => {
  const [posts,       setPosts]       = useState([]);
  const [loading,     setLoading]     = useState(true);
  const [showEditor,  setShowEditor]  = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [formData,    setFormData]    = useState(EMPTY_FORM);
  const [activeView,  setActiveView]  = useState('all'); // all | scheduled | drafts

  // Bulk import state
  const [showBulk,     setShowBulk]     = useState(false);
  const [bulkJson,     setBulkJson]     = useState('');
  const [bulkParsed,   setBulkParsed]   = useState(null);
  const [bulkError,    setBulkError]    = useState('');
  const [bulkImporting,setBulkImporting]= useState(false);

  useEffect(() => { fetchPosts(); }, []);

  // Auto-publish scheduled posts that have passed their scheduled_at time
  useEffect(() => {
    const now = new Date();
    const due = posts.filter(p =>
      !p.published && p.scheduled_at && new Date(p.scheduled_at) <= now
    );
    if (due.length > 0) {
      due.forEach(p => togglePublish(p, true));
    }
  }, [posts]);

  const fetchPosts = async () => {
    try {
      const res = await axios.get(`${API}/admin/blog`, { headers: getAuthHeaders() });
      setPosts(res.data.posts);
    } catch { toast.error('Failed to load blog posts'); }
    finally { setLoading(false); }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => {
      const updated = { ...prev, [name]: type === 'checkbox' ? checked : value };
      if (name === 'title' && !editingPost) updated.slug = generateSlug(value);
      return updated;
    });
  };

  const resetForm = () => { setFormData(EMPTY_FORM); setEditingPost(null); setShowEditor(false); };

  const handleEdit = (post) => {
    setFormData({
      title: post.title, slug: post.slug, excerpt: post.excerpt,
      content: post.content, author: post.author, category: post.category,
      tags: post.tags?.join(', ') || '',
      featured_image: post.featured_image || '',
      video_url: post.video_url || '',
      published: post.published,
      scheduled_at: post.scheduled_at ? post.scheduled_at.slice(0, 16) : '',
    });
    setEditingPost(post);
    setShowEditor(true);
    setShowBulk(false);
  };

  const handleSave = async () => {
    if (!formData.title || !formData.excerpt || !formData.content) {
      toast.error('Title, excerpt, and content are required');
      return;
    }
    try {
      const payload = {
        ...formData,
        tags: formData.tags ? formData.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        scheduled_at: formData.scheduled_at ? new Date(formData.scheduled_at).toISOString() : null,
        // If scheduled and not explicitly published, keep as draft until schedule fires
        published: formData.published,
      };
      if (editingPost) {
        await axios.put(`${API}/admin/blog/${editingPost.id}`, payload, { headers: getAuthHeaders() });
        toast.success('Post updated');
      } else {
        await axios.post(`${API}/admin/blog`, payload, { headers: getAuthHeaders() });
        toast.success(formData.scheduled_at ? `Post scheduled for ${new Date(formData.scheduled_at).toLocaleString()}` : 'Post created');
      }
      fetchPosts();
      resetForm();
    } catch { toast.error('Failed to save post'); }
  };

  const handleDelete = async (postId) => {
    if (!window.confirm('Delete this post? Cannot be undone.')) return;
    try {
      await axios.delete(`${API}/admin/blog/${postId}`, { headers: getAuthHeaders() });
      toast.success('Post deleted');
      fetchPosts();
    } catch { toast.error('Failed to delete'); }
  };

  const togglePublish = async (post, forcePublish = false) => {
    try {
      await axios.put(`${API}/admin/blog/${post.id}`,
        { published: forcePublish || !post.published },
        { headers: getAuthHeaders() }
      );
      if (!forcePublish) toast.success(post.published ? 'Unpublished' : 'Published');
      fetchPosts();
    } catch { toast.error('Failed to update'); }
  };

  // ─── Bulk Import ────────────────────────────────────────────────────
  const handleBulkParse = () => {
    setBulkError('');
    try {
      const parsed = JSON.parse(bulkJson);
      if (!Array.isArray(parsed)) { setBulkError('JSON must be an array of post objects'); return; }
      // Validate each
      const invalid = parsed.filter(p => !p.title || !p.content || !p.excerpt);
      if (invalid.length > 0) {
        setBulkError(`${invalid.length} post(s) missing required fields (title, content, excerpt)`);
        return;
      }
      setBulkParsed(parsed);
      toast.success(`${parsed.length} posts parsed successfully — review and import`);
    } catch (e) {
      setBulkError(`Invalid JSON: ${e.message}`);
    }
  };

  const handleBulkImport = async () => {
    if (!bulkParsed) return;
    setBulkImporting(true);
    let success = 0, failed = 0;
    for (const post of bulkParsed) {
      try {
        await axios.post(`${API}/admin/blog`, {
          title:         post.title,
          excerpt:       post.excerpt,
          content:       post.content,
          author:        post.author || 'Cosmic Wisdom',
          category:      post.category || 'Astrology',
          tags:          Array.isArray(post.tags) ? post.tags : (post.tags ? post.tags.split(',').map(t=>t.trim()) : []),
          featured_image:post.featured_image || '',
          video_url:     post.video_url || '',
          published:     post.published || false,
          scheduled_at:  post.scheduled_at ? new Date(post.scheduled_at).toISOString() : null,
        }, { headers: getAuthHeaders() });
        success++;
      } catch { failed++; }
    }
    setBulkImporting(false);
    toast.success(`Bulk import done: ${success} imported${ failed > 0 ? `, ${failed} failed` : ''}`);
    setBulkJson(''); setBulkParsed(null); setShowBulk(false);
    fetchPosts();
  };

  // ─── Filtered views ────────────────────────────────────────────────────
  const now = new Date();
  const scheduled = posts.filter(p => !p.published && p.scheduled_at && new Date(p.scheduled_at) > now)
    .sort((a, b) => new Date(a.scheduled_at) - new Date(b.scheduled_at));
  const drafts = posts.filter(p => !p.published && (!p.scheduled_at || new Date(p.scheduled_at) <= now));
  const published = posts.filter(p => p.published);

  const viewPosts = activeView === 'scheduled' ? scheduled
    : activeView === 'drafts' ? drafts
    : activeView === 'published' ? published
    : posts;

  const fmtDate = (d) => d ? new Date(d).toLocaleString('en-IN', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' }) : '—';

  if (loading) return <div className="text-center py-8 text-gray-400">Loading blog posts...</div>;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-gold" />
          Blog Management
          <span className="text-gray-400 text-sm font-normal">({posts.length} total)</span>
        </h3>
        <div className="flex gap-2">
          {!showEditor && !showBulk && (
            <>
              <Button onClick={() => { setShowBulk(true); setShowEditor(false); }}
                variant="outline" size="sm" className="border-gray-600 text-gray-300 hover:bg-gray-700">
                <Upload className="h-3.5 w-3.5 mr-1.5" />Bulk Import
              </Button>
              <Button onClick={() => { setShowEditor(true); setShowBulk(false); }}
                size="sm" className="bg-gold hover:bg-gold/90 text-gray-900">
                <Plus className="h-3.5 w-3.5 mr-1.5" />New Post
              </Button>
            </>
          )}
        </div>
      </div>

      {/* ─── BULK IMPORT PANEL ─── */}
      {showBulk && (
        <Card className="p-6 bg-gray-800 border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-base font-semibold text-white flex items-center gap-2">
              <Upload className="h-4 w-4 text-gold" />Bulk Import (up to 50 posts)
            </h4>
            <Button variant="ghost" onClick={() => { setShowBulk(false); setBulkJson(''); setBulkParsed(null); setBulkError(''); }} className="text-gray-400">
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="mb-4 p-3 bg-gray-700/60 rounded-lg text-xs text-gray-300 space-y-1">
            <p className="text-gold font-semibold mb-2">JSON Format — paste an array of post objects:</p>
            <pre className="text-gray-400 overflow-x-auto">{`[
  {
    "title": "Post Title",
    "excerpt": "Short description",
    "content": "Full post content...",
    "category": "Astrology",
    "tags": ["zodiac", "love"],
    "author": "Cosmic Wisdom",
    "published": false,
    "scheduled_at": "2026-03-25T09:00:00"  ← optional
  },
  { ... next post ... }
]`}</pre>
            <p className="text-gray-500 mt-2">• <strong>scheduled_at</strong> is optional. Leave blank to save as draft. Set a future date/time to auto-publish on that date.</p>
            <p className="text-gray-500">• <strong>published: true</strong> publishes immediately. <strong>published: false</strong> saves as draft.</p>
          </div>

          <div className="space-y-3">
            <div>
              <Label className="text-gray-300">Paste JSON Array</Label>
              <textarea
                value={bulkJson}
                onChange={e => { setBulkJson(e.target.value); setBulkError(''); setBulkParsed(null); }}
                className="w-full h-48 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white font-mono text-xs resize-none focus:outline-none focus:ring-1 focus:ring-gold"
                placeholder='[{"title": "...", "excerpt": "...", "content": "..."}]'
              />
            </div>

            {bulkError && <p className="text-red-400 text-sm">{bulkError}</p>}

            {bulkParsed && (
              <div className="p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
                <p className="text-green-400 text-sm font-medium mb-2">✓ {bulkParsed.length} posts ready to import</p>
                <div className="space-y-1 max-h-32 overflow-y-auto">
                  {bulkParsed.map((p, i) => (
                    <div key={i} className="flex items-center justify-between text-xs">
                      <span className="text-gray-300 truncate flex-1">{i+1}. {p.title}</span>
                      <span className="text-gray-500 ml-2 flex-shrink-0">
                        {p.scheduled_at ? `📅 ${new Date(p.scheduled_at).toLocaleDateString()}` : p.published ? '• Publish now' : '• Draft'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3">
              {!bulkParsed ? (
                <Button onClick={handleBulkParse} className="bg-gold hover:bg-gold/90 text-gray-900">
                  Validate JSON
                </Button>
              ) : (
                <Button onClick={handleBulkImport} disabled={bulkImporting} className="bg-green-500 hover:bg-green-600 text-white">
                  {bulkImporting ? 'Importing...' : `Import ${bulkParsed.length} Posts`}
                </Button>
              )}
              <Button variant="outline" onClick={() => { setBulkJson(''); setBulkParsed(null); setBulkError(''); }} className="border-gray-600 text-gray-300">
                Clear
              </Button>
            </div>
          </div>
        </Card>
      )}

      {/* ─── EDITOR ─── */}
      {showEditor && (
        <Card className="p-6 bg-gray-800 border-gray-700">
          <div className="flex items-center justify-between mb-5">
            <h4 className="text-base font-semibold text-white">{editingPost ? 'Edit Post' : 'Create New Post'}</h4>
            <Button variant="ghost" onClick={resetForm} className="text-gray-400"><X className="h-4 w-4" /></Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <Label className="text-gray-300">Title *</Label>
              <Input name="title" value={formData.title} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" placeholder="Enter post title" />
            </div>

            <div>
              <Label className="text-gray-300">URL Slug (auto-generated)</Label>
              <Input name="slug" value={formData.slug} readOnly
                className="bg-gray-600 border-gray-500 text-gray-300 cursor-not-allowed" />
            </div>

            <div>
              <Label className="text-gray-300">Category</Label>
              <Input name="category" value={formData.category} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" />
            </div>

            <div>
              <Label className="text-gray-300">Author</Label>
              <Input name="author" value={formData.author} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" />
            </div>

            <div>
              <Label className="text-gray-300">Tags (comma separated)</Label>
              <Input name="tags" value={formData.tags} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" placeholder="horoscope, zodiac, love" />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Featured Image URL</Label>
              <Input name="featured_image" value={formData.featured_image} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" placeholder="https://example.com/image.jpg" />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">YouTube Video URL (optional)</Label>
              <Input name="video_url" value={formData.video_url} onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white" placeholder="https://www.youtube.com/watch?v=..." />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Excerpt * (short description)</Label>
              <textarea name="excerpt" value={formData.excerpt} onChange={handleInputChange}
                className="w-full h-20 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white resize-none"
                placeholder="Brief summary of the post..." />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Content *</Label>
              <textarea name="content" value={formData.content} onChange={handleInputChange}
                className="w-full h-56 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white resize-none font-mono text-sm"
                placeholder="Write your post content here..." />
            </div>

            {/* Schedule & Publish */}
            <div>
              <Label className="text-gray-300 flex items-center gap-1.5">
                <Clock className="h-3.5 w-3.5" />Schedule Publish Date & Time (optional)
              </Label>
              <input type="datetime-local" name="scheduled_at" value={formData.scheduled_at} onChange={handleInputChange}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white text-sm focus:outline-none focus:ring-1 focus:ring-gold" />
              <p className="text-xs text-gray-500 mt-1">Leave blank to publish manually. Set a future date to auto-publish.</p>
            </div>

            <div className="flex items-end pb-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" name="published" checked={formData.published} onChange={handleInputChange}
                  className="rounded border-gray-600 bg-gray-700 text-gold focus:ring-gold" />
                <span className="text-gray-300 text-sm">Publish immediately</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <Button variant="outline" onClick={resetForm} className="border-gray-600 text-gray-300">Cancel</Button>
            <Button onClick={handleSave} className="bg-gold hover:bg-gold/90 text-gray-900">
              <Save className="h-4 w-4 mr-2" />
              {editingPost ? 'Update Post' : formData.scheduled_at ? 'Schedule Post' : 'Create Post'}
            </Button>
          </div>
        </Card>
      )}

      {/* ─── VIEW FILTER TABS ─── */}
      <div className="flex gap-2 flex-wrap">
        {[
          { id: 'all',       label: `All (${posts.length})` },
          { id: 'published', label: `Published (${published.length})` },
          { id: 'scheduled', label: `Scheduled (${scheduled.length})`, accent: scheduled.length > 0 },
          { id: 'drafts',    label: `Drafts (${drafts.length})` },
        ].map(({ id, label, accent }) => (
          <button key={id} onClick={() => setActiveView(id)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
              activeView === id
                ? 'bg-gold text-gray-900 border-gold'
                : accent
                ? 'border-blue-500/50 text-blue-400 hover:bg-blue-500/10'
                : 'border-gray-600 text-gray-400 hover:border-gray-500'
            }`}>
            {label}
          </button>
        ))}
      </div>

      {/* ─── SCHEDULED QUEUE ─── */}
      {activeView === 'scheduled' && scheduled.length > 0 && (
        <Card className="p-4 bg-blue-500/5 border border-blue-500/20">
          <h4 className="text-sm font-semibold text-blue-400 mb-3 flex items-center gap-1.5">
            <Clock className="h-3.5 w-3.5" />Upcoming Scheduled Posts
          </h4>
          <div className="space-y-2">
            {scheduled.map((p, i) => (
              <div key={i} className="flex items-center justify-between p-2 bg-gray-800 rounded-lg">
                <div>
                  <p className="text-white text-sm font-medium">{p.title}</p>
                  <p className="text-blue-400 text-xs flex items-center gap-1 mt-0.5">
                    <Calendar className="h-3 w-3" />Publishes: {fmtDate(p.scheduled_at)}
                  </p>
                </div>
                <div className="flex gap-1">
                  <Button variant="ghost" size="sm" onClick={() => handleEdit(p)} className="text-gray-400 hover:text-white">
                    <Edit className="h-3.5 w-3.5" />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => togglePublish(p)} className="text-green-400 hover:text-green-300" title="Publish now">
                    <Eye className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* ─── POSTS LIST ─── */}
      <Card className="p-6 bg-gray-800 border-gray-700">
        <h4 className="text-sm font-semibold text-white mb-4">
          {activeView === 'all' ? 'All Posts' : activeView === 'published' ? 'Published Posts'
            : activeView === 'scheduled' ? 'Scheduled Posts' : 'Draft Posts'}
          {' '}({viewPosts.length})
        </h4>
        {viewPosts.length === 0 ? (
          <p className="text-center py-8 text-gray-500">No posts in this view</p>
        ) : (
          <div className="space-y-2">
            {viewPosts.map((post) => (
              <div key={post.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700/80 transition-colors">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h5 className="text-white text-sm font-medium truncate">{post.title}</h5>
                    <span className={`px-2 py-0.5 text-xs rounded-full ${
                      post.published ? 'bg-green-500/20 text-green-400'
                      : post.scheduled_at && new Date(post.scheduled_at) > new Date() ? 'bg-blue-500/20 text-blue-400'
                      : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {post.published ? 'Published'
                        : post.scheduled_at && new Date(post.scheduled_at) > new Date() ? '📅 Scheduled'
                        : 'Draft'}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                    <span>{post.category}</span>
                    {post.scheduled_at && !post.published && (
                      <span className="text-blue-400 flex items-center gap-1">
                        <Clock className="h-3 w-3" />{fmtDate(post.scheduled_at)}
                      </span>
                    )}
                    {post.published && (
                      <span className="flex items-center gap-1">
                        <Eye className="h-3 w-3" />{post.views || 0} views
                      </span>
                    )}
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />{new Date(post.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-1 ml-3">
                  <Button variant="ghost" size="sm" onClick={() => togglePublish(post)} className="text-gray-400 hover:text-white" title={post.published ? 'Unpublish' : 'Publish now'}>
                    {post.published ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => handleEdit(post)} className="text-gray-400 hover:text-white">
                    <Edit className="h-3.5 w-3.5" />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => handleDelete(post.id)} className="text-gray-400 hover:text-red-400">
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};
