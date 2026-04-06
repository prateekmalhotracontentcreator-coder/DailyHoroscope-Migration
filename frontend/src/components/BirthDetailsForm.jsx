import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Sparkles } from 'lucide-react';
import SharedBirthCityPicker from './SharedBirthCityPicker';

export const BirthDetailsForm = ({ onSubmit, isLoading, existingProfile = null }) => {
  const [formData, setFormData] = useState({
    name: existingProfile?.name || '',
    date_of_birth: existingProfile?.date_of_birth || '',
    time_of_birth: existingProfile?.time_of_birth || '',
    location: existingProfile?.location || '',
    city_slug: existingProfile?.city_slug || '',
    latitude: existingProfile?.latitude ?? '',
    longitude: existingProfile?.longitude ?? '',
    timezone: existingProfile?.timezone || '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="p-8 border-2 border-gold/30 bg-card">
      <div className="flex items-center space-x-3 mb-6">
        <Sparkles className="h-6 w-6 text-gold" />
        <h3 className="text-2xl font-playfair font-semibold">
          {existingProfile ? 'Your Birth Details' : 'Enter Birth Details'}
        </h3>
      </div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Label htmlFor="name">Full Name</Label>
          <Input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
            disabled={isLoading || existingProfile}
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Label htmlFor="date_of_birth">Date of Birth</Label>
            <Input
              id="date_of_birth"
              name="date_of_birth"
              type="date"
              value={formData.date_of_birth}
              onChange={handleChange}
              required
              disabled={isLoading || existingProfile}
            />
          </div>
          <div>
            <Label htmlFor="time_of_birth">Time of Birth</Label>
            <Input
              id="time_of_birth"
              name="time_of_birth"
              type="time"
              value={formData.time_of_birth}
              onChange={handleChange}
              required
              disabled={isLoading || existingProfile}
            />
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="location">Place of Birth</Label>
          <SharedBirthCityPicker
            inputId="location"
            label=""
            value={formData.city_slug}
            onChange={(city) =>
              setFormData((current) => ({
                ...current,
                location: city.city_name,
                city_slug: city.slug,
                latitude: city.latitude,
                longitude: city.longitude,
                timezone: city.timezone,
              }))
            }
            required
            disabled={Boolean(isLoading || existingProfile)}
            helpText="Search by city, country, or timezone abbreviation."
          />
        </div>
        {!existingProfile && (
          <Button type="submit" disabled={isLoading} className="w-full h-12">
            {isLoading ? 'Saving...' : 'Save Birth Details'}
          </Button>
        )}
      </form>
    </Card>
  );
};
