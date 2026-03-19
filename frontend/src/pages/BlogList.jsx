import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Calendar, User, Eye, Tag, ArrowRight, BookOpen } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const BlogList = () => {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    fetchPosts();
    fetchCategories();
  }, [selectedCategory]);

  const fetchPosts = async () => {
    try {
      const url = selectedCategory 
        ? `${API}/blog?category=${selectedCategory}` 
        : `${API}/blog`;
      const response = await axios.get(url);
      setPosts(response.data.posts);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API}/blog/categories/list`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-background">

      
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-3 rounded-full bg-gold/20 mb-4">
            <BookOpen className="h-8 w-8 text-gold" />
          </div>
          <h1 className="text-4xl md:text-5xl font-playfair font-bold mb-4">
            Everyday Horoscope Blog
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Explore astrology insights, zodiac guides, and cosmic wisdom to navigate your life journey
          </p>
        </div>

        {/* Categories Filter */}
        {categories.length > 0 && (
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            <Button
              variant={selectedCategory === null ? "default" : "outline"}
              onClick={() => setSelectedCategory(null)}
              className={selectedCategory === null ? "bg-gold text-primary-foreground" : ""}
              size="sm"
            >
              All Posts
            </Button>
            {categories.map((cat) => (
              <Button
                key={cat}
                variant={selectedCategory === cat ? "default" : "outline"}
                onClick={() => setSelectedCategory(cat)}
                className={selectedCategory === cat ? "bg-gold text-primary-foreground" : ""}
                size="sm"
              >
                {cat}
              </Button>
            ))}
          </div>
        )}

        {/* Blog Posts Grid */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading articles...</p>
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-12">
            <BookOpen className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground text-lg">No articles published yet</p>
            <p className="text-muted-foreground">Check back soon for cosmic insights!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
              <Card 
                key={post.id}
                className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group"
                onClick={() => navigate(`/blog/${post.slug}`)}
                data-testid={`blog-card-${post.slug}`}
              >
                {post.featured_image && (
                  <div className="aspect-video overflow-hidden">
                    <img 
                      src={post.featured_image} 
                      alt={post.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                )}
                <div className="p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-2 py-1 text-xs rounded-full bg-gold/20 text-gold font-medium">
                      {post.category}
                    </span>
                    <span className="flex items-center text-xs text-muted-foreground">
                      <Eye className="h-3 w-3 mr-1" />
                      {post.views || 0}
                    </span>
                  </div>
                  
                  <h2 className="text-xl font-semibold mb-2 group-hover:text-gold transition-colors line-clamp-2">
                    {post.title}
                  </h2>
                  
                  <p className="text-muted-foreground text-sm mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-1" />
                      {post.author}
                    </div>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {formatDate(post.created_at)}
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-border">
                    <span className="text-gold font-medium text-sm flex items-center group-hover:underline">
                      Read More <ArrowRight className="h-4 w-4 ml-1" />
                    </span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
