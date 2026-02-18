import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Sparkles } from 'lucide-react';

export const BirthDetailsForm = ({ onSubmit, isLoading, existingProfile = null }) => {
  const [formData, setFormData] = useState({
    name: existingProfile?.name || '',
    date_of_birth: existingProfile?.date_of_birth || '',
    time_of_birth: existingProfile?.time_of_birth || '',
    location: existingProfile?.location || ''
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
          <Label htmlFor="name" className="text-base font-semibold mb-2 block">
            Full Name
          </Label>
          <Input
            id="name"
            name="name"
            data-testid="input-name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
            className="h-12 text-base border-border focus:border-gold focus:ring-gold"
            disabled={isLoading || existingProfile}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Label htmlFor="date_of_birth" className="text-base font-semibold mb-2 block">
              Date of Birth
            </Label>
            <Input
              id="date_of_birth"
              name="date_of_birth"
              type="date"
              data-testid="input-dob"
              value={formData.date_of_birth}
              onChange={handleChange}
              required
              className="h-12 text-base border-border focus:border-gold focus:ring-gold"
              disabled={isLoading || existingProfile}
            />
          </div>

          <div>
            <Label htmlFor="time_of_birth" className="text-base font-semibold mb-2 block">
              Time of Birth
            </Label>
            <Input
              id="time_of_birth"
              name="time_of_birth"
              type="time"
              data-testid="input-time"
              value={formData.time_of_birth}
              onChange={handleChange}
              required
              className="h-12 text-base border-border focus:border-gold focus:ring-gold"
              disabled={isLoading || existingProfile}
            />
          </div>
        </div>

        <div>
          <Label htmlFor="location" className="text-base font-semibold mb-2 block">
            Place of Birth
          </Label>
          <Input
            id="location"
            name="location"
            data-testid="input-location"
            value={formData.location}
            onChange={handleChange}
            placeholder="City, State, Country"
            required
            className="h-12 text-base border-border focus:border-gold focus:ring-gold"
            disabled={isLoading || existingProfile}
          />
        </div>

        {!existingProfile && (
          <Button
            type="submit"
            data-testid="submit-birth-details"
            disabled={isLoading}
            className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground transition-all duration-300"
          >
            {isLoading ? 'Saving...' : 'Save Birth Details'}
          </Button>
        )}
      </form>
    </Card>
  );
};