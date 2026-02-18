import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { 
  Plus, Edit, Trash2, Eye, EyeOff, Save, X, BookOpen, Calendar
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AdminBlogManager = ({ getAuthHeaders }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showEditor, setShowEditor] = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    author: 'Cosmic Wisdom',
    category: 'Astrology',
    tags: '',
    featured_image: '',
    published: false
  });

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const headers = getAuthHeaders();
      const response = await axios.get(`${API}/admin/blog`, { headers });
      setPosts(response.data.posts);
    } catch (error) {
      console.error('Error fetching posts:', error);
      toast.error('Failed to load blog posts');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const resetForm = () => {
    setFormData({
      title: '',
      slug: '',
      excerpt: '',
      content: '',
      author: 'Cosmic Wisdom',
      category: 'Astrology',
      tags: '',
      featured_image: '',
      published: false
    });
    setEditingPost(null);
    setShowEditor(false);
  };

  const handleEdit = (post) => {
    setFormData({
      title: post.title,
      slug: post.slug,
      excerpt: post.excerpt,
      content: post.content,
      author: post.author,
      category: post.category,
      tags: post.tags?.join(', ') || '',
      featured_image: post.featured_image || '',
      published: post.published
    });
    setEditingPost(post);
    setShowEditor(true);
  };

  const handleSave = async () => {
    if (!formData.title || !formData.excerpt || !formData.content) {
      toast.error('Please fill in title, excerpt, and content');
      return;
    }

    try {
      const headers = getAuthHeaders();
      const payload = {
        ...formData,
        tags: formData.tags ? formData.tags.split(',').map(t => t.trim()).filter(t => t) : []
      };

      if (editingPost) {
        await axios.put(`${API}/admin/blog/${editingPost.id}`, payload, { headers });
        toast.success('Post updated successfully');
      } else {
        await axios.post(`${API}/admin/blog`, payload, { headers });
        toast.success('Post created successfully');
      }

      fetchPosts();
      resetForm();
    } catch (error) {
      console.error('Error saving post:', error);
      toast.error('Failed to save post');
    }
  };

  const handleDelete = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;

    try {
      const headers = getAuthHeaders();
      await axios.delete(`${API}/admin/blog/${postId}`, { headers });
      toast.success('Post deleted successfully');
      fetchPosts();
    } catch (error) {
      console.error('Error deleting post:', error);
      toast.error('Failed to delete post');
    }
  };

  const togglePublish = async (post) => {
    try {
      const headers = getAuthHeaders();
      await axios.put(`${API}/admin/blog/${post.id}`, {
        published: !post.published
      }, { headers });
      toast.success(post.published ? 'Post unpublished' : 'Post published');
      fetchPosts();
    } catch (error) {
      console.error('Error toggling publish:', error);
      toast.error('Failed to update post');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Loading blog posts...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white flex items-center">
          <BookOpen className="h-5 w-5 mr-2 text-gold" />
          Blog Management
        </h3>
        {!showEditor && (
          <Button
            onClick={() => setShowEditor(true)}
            className="bg-gold hover:bg-gold/90 text-gray-900"
            data-testid="new-post-btn"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Post
          </Button>
        )}
      </div>

      {/* Editor */}
      {showEditor && (
        <Card className="p-6 bg-gray-800 border-gray-700">
          <div className="flex items-center justify-between mb-6">
            <h4 className="text-lg font-semibold text-white">
              {editingPost ? 'Edit Post' : 'Create New Post'}
            </h4>
            <Button variant="ghost" onClick={resetForm} className="text-gray-400">
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <Label className="text-gray-300">Title *</Label>
              <Input
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
                placeholder="Enter post title"
                data-testid="blog-title-input"
              />
            </div>

            <div>
              <Label className="text-gray-300">Slug (auto-generated if empty)</Label>
              <Input
                name="slug"
                value={formData.slug}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
                placeholder="url-friendly-slug"
              />
            </div>

            <div>
              <Label className="text-gray-300">Category</Label>
              <Input
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
                placeholder="e.g., Astrology, Zodiac, Tips"
              />
            </div>

            <div>
              <Label className="text-gray-300">Author</Label>
              <Input
                name="author"
                value={formData.author}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>

            <div>
              <Label className="text-gray-300">Tags (comma separated)</Label>
              <Input
                name="tags"
                value={formData.tags}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
                placeholder="horoscope, zodiac, love"
              />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Featured Image URL</Label>
              <Input
                name="featured_image"
                value={formData.featured_image}
                onChange={handleInputChange}
                className="bg-gray-700 border-gray-600 text-white"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Excerpt * (Short description)</Label>
              <textarea
                name="excerpt"
                value={formData.excerpt}
                onChange={handleInputChange}
                className="w-full h-20 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white resize-none"
                placeholder="Brief summary of the post..."
                data-testid="blog-excerpt-input"
              />
            </div>

            <div className="md:col-span-2">
              <Label className="text-gray-300">Content * (Supports basic formatting)</Label>
              <textarea
                name="content"
                value={formData.content}
                onChange={handleInputChange}
                className="w-full h-64 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white resize-none font-mono text-sm"
                placeholder="Write your post content here...

Use **bold** for bold text
Use *italic* for italic text
Use ## for headings
Use - for bullet points"
                data-testid="blog-content-input"
              />
            </div>

            <div className="md:col-span-2 flex items-center space-x-4">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="published"
                  checked={formData.published}
                  onChange={handleInputChange}
                  className="rounded border-gray-600 bg-gray-700 text-gold focus:ring-gold"
                />
                <span className="text-gray-300">Publish immediately</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end space-x-3 mt-6">
            <Button variant="outline" onClick={resetForm} className="border-gray-600 text-gray-300">
              Cancel
            </Button>
            <Button onClick={handleSave} className="bg-gold hover:bg-gold/90 text-gray-900">
              <Save className="h-4 w-4 mr-2" />
              {editingPost ? 'Update Post' : 'Create Post'}
            </Button>
          </div>
        </Card>
      )}

      {/* Posts List */}
      <Card className="p-6 bg-gray-800 border-gray-700">
        <h4 className="text-lg font-semibold text-white mb-4">All Posts ({posts.length})</h4>
        
        {posts.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No blog posts yet. Create your first post!
          </div>
        ) : (
          <div className="space-y-3">
            {posts.map((post) => (
              <div 
                key={post.id}
                className="flex items-center justify-between p-4 bg-gray-700/50 rounded-lg"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <h5 className="text-white font-medium truncate">{post.title}</h5>
                    <span className={`px-2 py-0.5 text-xs rounded-full ${
                      post.published 
                        ? 'bg-green-500/20 text-green-400' 
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {post.published ? 'Published' : 'Draft'}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4 mt-1 text-sm text-gray-400">
                    <span>{post.category}</span>
                    <span className="flex items-center">
                      <Calendar className="h-3 w-3 mr-1" />
                      {formatDate(post.created_at)}
                    </span>
                    <span className="flex items-center">
                      <Eye className="h-3 w-3 mr-1" />
                      {post.views || 0} views
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => togglePublish(post)}
                    className="text-gray-400 hover:text-white"
                    title={post.published ? 'Unpublish' : 'Publish'}
                  >
                    {post.published ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEdit(post)}
                    className="text-gray-400 hover:text-white"
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(post.id)}
                    className="text-gray-400 hover:text-red-400"
                  >
                    <Trash2 className="h-4 w-4" />
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
