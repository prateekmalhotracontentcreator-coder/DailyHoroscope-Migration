import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Heart, User } from 'lucide-react';
import { Separator } from './ui/separator';
import SharedBirthCityPicker from './SharedBirthCityPicker';

function defaultPersonState() {
  return {
    name: '',
    date_of_birth: '',
    time_of_birth: '',
    location: '',
    city_slug: '',
    latitude: '',
    longitude: '',
    timezone: '',
  };
}

export const KundaliMilanForm = ({ onSubmit, isLoading, existingProfiles = [] }) => {
  const [person1, setPerson1] = useState(defaultPersonState());
  const [person2, setPerson2] = useState(defaultPersonState());

  const handlePerson1Change = (e) => {
    setPerson1({ ...person1, [e.target.name]: e.target.value });
  };

  const handlePerson2Change = (e) => {
    setPerson2({ ...person2, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ person1, person2 });
  };

  return (
    <Card className="p-8 border-2 border-gold/30 bg-card">
      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <User className="h-5 w-5 text-gold" />
            <h3 className="text-xl font-playfair font-semibold">Person 1</h3>
          </div>
          <div className="grid gap-6">
            <div>
              <Label htmlFor="person1_name">Full Name</Label>
              <Input
                id="person1_name"
                name="name"
                value={person1.name}
                onChange={handlePerson1Change}
                required
                disabled={isLoading}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label htmlFor="person1_date_of_birth">Date of Birth</Label>
                <Input
                  id="person1_date_of_birth"
                  name="date_of_birth"
                  type="date"
                  value={person1.date_of_birth}
                  onChange={handlePerson1Change}
                  required
                  disabled={isLoading}
                />
              </div>
              <div>
                <Label htmlFor="person1_time_of_birth">Time of Birth</Label>
                <Input
                  id="person1_time_of_birth"
                  name="time_of_birth"
                  type="time"
                  value={person1.time_of_birth}
                  onChange={handlePerson1Change}
                  required
                  disabled={isLoading}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="person1_location">Place of Birth</Label>
              <SharedBirthCityPicker
                inputId="person1_location"
                label=""
                value={person1.city_slug}
                onChange={(city) =>
                  setPerson1((current) => ({
                    ...current,
                    location: city.city_name,
                    city_slug: city.slug,
                    latitude: city.latitude,
                    longitude: city.longitude,
                    timezone: city.timezone,
                  }))
                }
                required
                disabled={isLoading}
                helpText="Search by city, country, or timezone abbreviation."
              />
            </div>
          </div>
        </div>

        <Separator />

        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <Heart className="h-5 w-5 text-gold" />
            <h3 className="text-xl font-playfair font-semibold">Person 2</h3>
          </div>
          <div className="grid gap-6">
            <div>
              <Label htmlFor="person2_name">Full Name</Label>
              <Input
                id="person2_name"
                name="name"
                value={person2.name}
                onChange={handlePerson2Change}
                required
                disabled={isLoading}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label htmlFor="person2_date_of_birth">Date of Birth</Label>
                <Input
                  id="person2_date_of_birth"
                  name="date_of_birth"
                  type="date"
                  value={person2.date_of_birth}
                  onChange={handlePerson2Change}
                  required
                  disabled={isLoading}
                />
              </div>
              <div>
                <Label htmlFor="person2_time_of_birth">Time of Birth</Label>
                <Input
                  id="person2_time_of_birth"
                  name="time_of_birth"
                  type="time"
                  value={person2.time_of_birth}
                  onChange={handlePerson2Change}
                  required
                  disabled={isLoading}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="person2_location">Place of Birth</Label>
              <SharedBirthCityPicker
                inputId="person2_location"
                label=""
                value={person2.city_slug}
                onChange={(city) =>
                  setPerson2((current) => ({
                    ...current,
                    location: city.city_name,
                    city_slug: city.slug,
                    latitude: city.latitude,
                    longitude: city.longitude,
                    timezone: city.timezone,
                  }))
                }
                required
                disabled={isLoading}
                helpText="Search by city, country, or timezone abbreviation."
              />
            </div>
          </div>
        </div>

        <Button type="submit" disabled={isLoading} className="w-full h-12">
          {isLoading ? 'Analyzing Compatibility...' : 'Generate Compatibility Report'}
        </Button>
      </form>
    </Card>
  );
};
