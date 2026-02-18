import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { Button } from './ui/button';

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      data-testid="theme-toggle"
      onClick={toggleTheme}
      variant="ghost"
      size="icon"
      className="fixed top-6 right-6 z-50 h-12 w-12 rounded-sm border border-border bg-card hover:bg-primary hover:text-primary-foreground transition-all duration-300"
    >
      {theme === 'light' ? (
        <Moon className="h-5 w-5" />
      ) : (
        <Sun className="h-5 w-5" />
      )}
    </Button>
  );
};