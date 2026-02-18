import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Heart, User } from 'lucide-react';
import { Separator } from './ui/separator';

export const KundaliMilanForm = ({ onSubmit, isLoading, existingProfiles = [] }) => {
  const [person1, setPerson1] = useState({
    name: '',
    date_of_birth: '',
    time_of_birth: '',
    location: ''
  });

  const [person2, setPerson2] = useState({
    name: '',
    date_of_birth: '',
    time_of_birth: '',
    location: ''
  });

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
      <div className="flex items-center space-x-3 mb-6">
        <Heart className="h-6 w-6 text-gold" />
        <h3 className="text-2xl font-playfair font-semibold">
          Kundali Milan - Marriage Compatibility
        </h3>
      </div>

      <p className="text-muted-foreground mb-8">
        Enter birth details for both individuals to generate a comprehensive compatibility analysis based on Vedic astrology.
      </p>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Person 1 */}
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <User className="h-5 w-5 text-gold" />
            <h4 className="text-xl font-playfair font-semibold">Person 1 Details</h4>
          </div>
          
          <div className="space-y-4 pl-7">
            <div>
              <Label htmlFor="person1_name" className="text-base font-semibold mb-2 block">
                Full Name
              </Label>
              <Input
                id="person1_name"
                name="name"
                data-testid="input-person1-name"
                value={person1.name}
                onChange={handlePerson1Change}
                placeholder="Enter name"
                required
                className="h-12 text-base border-border focus:border-gold"
                disabled={isLoading}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="person1_dob" className="text-base font-semibold mb-2 block">
                  Date of Birth
                </Label>
                <Input
                  id="person1_dob"
                  name="date_of_birth"
                  type="date"
                  data-testid="input-person1-dob"
                  value={person1.date_of_birth}
                  onChange={handlePerson1Change}
                  required
                  className="h-12 text-base border-border focus:border-gold"
                  disabled={isLoading}
                />
              </div>

              <div>
                <Label htmlFor="person1_time" className="text-base font-semibold mb-2 block">
                  Time of Birth
                </Label>
                <Input
                  id="person1_time"
                  name="time_of_birth"
                  type="time"
                  data-testid="input-person1-time"
                  value={person1.time_of_birth}
                  onChange={handlePerson1Change}
                  required
                  className="h-12 text-base border-border focus:border-gold"
                  disabled={isLoading}
                />
              </div>
            </div>

            <div>
              <Label htmlFor="person1_location" className="text-base font-semibold mb-2 block">
                Place of Birth
              </Label>
              <Input
                id="person1_location"
                name="location"
                data-testid="input-person1-location"
                value={person1.location}
                onChange={handlePerson1Change}
                placeholder="City, State, Country"
                required
                className="h-12 text-base border-border focus:border-gold"
                disabled={isLoading}
              />
            </div>
          </div>
        </div>

        <Separator className="my-8" />

        {/* Person 2 */}
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <User className="h-5 w-5 text-gold" />
            <h4 className="text-xl font-playfair font-semibold">Person 2 Details</h4>
          </div>
          
          <div className="space-y-4 pl-7">
            <div>
              <Label htmlFor="person2_name" className="text-base font-semibold mb-2 block">
                Full Name
              </Label>
              <Input
                id="person2_name"
                name="name"
                data-testid="input-person2-name"
                value={person2.name}
                onChange={handlePerson2Change}
                placeholder="Enter name"
                required
                className="h-12 text-base border-border focus:border-gold"
                disabled={isLoading}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="person2_dob" className="text-base font-semibold mb-2 block">
                  Date of Birth
                </Label>
                <Input
                  id="person2_dob"
                  name="date_of_birth"
                  type="date"
                  data-testid="input-person2-dob"
                  value={person2.date_of_birth}
                  onChange={handlePerson2Change}
                  required
                  className="h-12 text-base border-border focus:border-gold"
                  disabled={isLoading}
                />
              </div>

              <div>
                <Label htmlFor="person2_time" className="text-base font-semibold mb-2 block">
                  Time of Birth
                </Label>
                <Input
                  id="person2_time"
                  name="time_of_birth"
                  type="time"
                  data-testid="input-person2-time"
                  value={person2.time_of_birth}
                  onChange={handlePerson2Change}
                  required
                  className="h-12 text-base border-border focus:border-gold"
                  disabled={isLoading}
                />
              </div>
            </div>

            <div>
              <Label htmlFor="person2_location" className="text-base font-semibold mb-2 block">
                Place of Birth
              </Label>
              <Input
                id="person2_location"
                name="location"
                data-testid="input-person2-location"
                value={person2.location}
                onChange={handlePerson2Change}
                placeholder="City, State, Country"
                required
                className="h-12 text-base border-border focus:border-gold"
                disabled={isLoading}
              />
            </div>
          </div>
        </div>

        <Button
          type="submit"
          data-testid="submit-kundali-milan"
          disabled={isLoading}
          className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground transition-all duration-300"
        >
          {isLoading ? 'Analyzing Compatibility...' : 'Generate Compatibility Report'}
        </Button>
      </form>
    </Card>
  );
};