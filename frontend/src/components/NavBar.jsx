import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ThemeToggle } from './ThemeToggle';
import { UserAccountMenu } from './UserAccountMenu';
import { Button } from './ui/button';
import {
  Menu, X, Home, Star, FileText, BookOpen, Tag, Phone,
  ChevronDown, ChevronRight, Sparkles, LogIn, User,
  Sun, Moon as MoonIcon, Calendar, Gem, Hash, Globe,
  Heart, Briefcase, Shield, Leaf, Zap, Crown,
  BookMarked, Layers
} from 'lucide-react';

// ── Stars Logo ─────────────────────────────────────────────────────────────────
const StarsLogo = ({ size = 56 }) => (
  <img
    src="/Logo.png"
    alt="Everyday Horoscope"
    width={size}
    height={size}
    style={{ width: size, height: size, objectFit: 'contain', display: 'block' }}
  />
);

const NAV = [
  { label: 'Home', icon: Home, path: '/home' },
  {
    label: 'Panchang', icon: Calendar,
    children: [
      { label: 'Daily Panchang',      path: '/panchang/today',     icon: Sun },
      { label: 'Calendar',            path: `/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`, icon: Calendar },
      { label: 'Hindi Panchang',      path: '/panchang/hindi',     icon: Globe },
      { label: 'Telugu Panchang',     path: '/panchang/telugu',    icon: Globe },
      { label: 'Malayalam Panchang',  path: '/panchang/malayalam', icon: Globe },
      { label: 'Kannada Panchang',    path: '/panchang/kannada',   icon: Globe },
      { label: 'Tamil Panchang',      path: '/panchang/tamil',     icon: Globe },
      { label: 'Shubh Muhurat',       path: '/panchang/muhurat',   icon: Star },
      { label: 'Nakshatra',           path: '/panchang/nakshatra', icon: Sparkles },
      { label: 'Choghadiya',          path: '/panchang/choghadiya',icon: Zap },
      { label: 'Festivals',           path: '/panchang/festivals', icon: Sparkles },
      { label: 'Rahu Kalam',          path: '/panchang/rahukaal',  icon: Shield },
    ],
  },
  {
    label: 'Horoscope', icon: Star,
    children: [
      { label: 'Daily Horoscope',   path: '/horoscope/daily',   icon: Sun },
      { label: 'Weekly Horoscope',  path: '/horoscope/weekly',  icon: Star },
      { label: 'Monthly Horoscope', path: '/horoscope/monthly', icon: Calendar },
    ],
  },
  {
    label: 'Reports', icon: FileText,
    children: [
      { label: 'My Reports',        path: '/my-reports',    icon: FileText },
      { label: 'Birth Chart',       path: '/birth-chart',     icon: Sparkles },
      { label: 'Lagna Kundali',     path: '/lagna-kundali',   icon: Gem },
      { label: 'Kundali Milan',     path: '/kundali-milan',   icon: Heart },
      { label: 'Brihat Kundli Pro', path: '/brihat-kundli', icon: Crown },
      { label: 'Ask 1 Question',    path: '/ask-question',  icon: Hash },
      { label: 'Love Report',       path: '/love-report',   icon: Heart },
      { label: 'Career Plus',       path: '/career-plus',   icon: Briefcase },
      { label: 'Hasta Rekha',       path: '/palmistry',     icon: Layers },
    ],
  },
  {
    // Remedies: all sub-items point to /remedies (Coming Soon) until module is built
    label: 'Remedies', icon: Gem,
    children: [
      { label: 'Gemstones',       path: '/remedies', icon: Gem },
      { label: 'Mantras',         path: '/remedies', icon: BookMarked },
      { label: 'Yantras',         path: '/remedies', icon: Shield },
      { label: 'Feng Shui',       path: '/remedies', icon: Leaf },
      { label: 'Crystal Therapy', path: '/remedies', icon: Zap },
    ],
  },
  { label: 'Numerology', icon: Hash,      path: '/numerology' },
  { label: 'Palmistry',  icon: Layers,    path: '/palmistry' },
  { label: 'Tarot',      icon: BookOpen,  path: '/tarot' },
  { label: 'Pricing',    icon: Tag,       path: '/pricing' },
  { label: 'Blog',       icon: BookOpen,  path: '/blog' },
  { label: 'Contact',    icon: Phone,     path: '/contact' },
];

const BOTTOM_NAV = [
  { label: 'Home',       icon: Home,     path: '/home' },
  { label: 'Horoscope',  icon: Star,     path: '/horoscope/daily' },
  { label: 'My Reports', icon: FileText, path: '/my-reports' },
  { label: 'Account',    icon: User,     path: '/account' },
];

// ─── Desktop Dropdown ──────────────────────────────────────────────────────────
const DesktopDropdown = ({ item, isActive }) => {
  const [open, setOpen] = useState(false);
  const _navigate = useNavigate();
  const navigate = (path) => { window.scrollTo(0, 0); _navigate(path); };
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  if (!item.children) {
    return (
      <button
        onClick={() => navigate(item.path)}
        className={`flex items-center gap-1.5 px-3 py-2 rounded-sm text-sm font-medium transition-colors
          ${isActive ? 'text-gold' : 'text-muted-foreground hover:text-foreground'}`}
      >
        {item.label}
      </button>
    );
  }

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`flex items-center gap-1 px-3 py-2 rounded-sm text-sm font-medium transition-colors
          ${open ? 'text-gold' : 'text-muted-foreground hover:text-foreground'}`}
      >
        {item.label}
        <ChevronDown className={`h-3.5 w-3.5 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute top-full left-0 mt-1 w-52 bg-card border border-border rounded-sm shadow-xl z-50 py-1 overflow-hidden">
          <div className="h-0.5 bg-gradient-to-r from-gold/60 via-gold to-gold/60 mb-1" />
          {item.children.map((child) => (
            <button
              key={child.label}
              onClick={() => { navigate(child.path); setOpen(false); }}
              className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-muted-foreground hover:text-foreground hover:bg-gold/5 transition-colors text-left"
            >
              <child.icon className="h-3.5 w-3.5 text-gold/60 flex-shrink-0" />
              {child.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// ─── Sidebar Item ──────────────────────────────────────────────────────────────
const SidebarItem = ({ item, onNavigate, depth = 0 }) => {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const isActive = item.path && location.pathname === item.path;

  if (!item.children) {
    return (
      <button
        onClick={() => onNavigate(item.path)}
        className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors text-left rounded-sm mx-1
          ${isActive
            ? 'text-gold bg-gold/10 border-l-2 border-gold pl-3.5'
            : 'text-muted-foreground hover:text-foreground hover:bg-muted/40'}`}
        style={{ paddingLeft: depth > 0 ? '2.5rem' : undefined }}
      >
        <item.icon className={`h-4 w-4 flex-shrink-0 ${isActive ? 'text-gold' : 'text-muted-foreground/60'}`} />
        {item.label}
      </button>
    );
  }

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between gap-3 px-4 py-3 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors text-left rounded-sm mx-1"
      >
        <div className="flex items-center gap-3">
          <item.icon className="h-4 w-4 flex-shrink-0 text-muted-foreground/60" />
          {item.label}
        </div>
        <ChevronRight className={`h-3.5 w-3.5 transition-transform ${open ? 'rotate-90' : ''}`} />
      </button>
      {open && (
        <div className="ml-2 border-l border-gold/20 pl-1 my-0.5">
          {item.children.map((child) => (
            <SidebarItem key={child.label} item={child} onNavigate={onNavigate} depth={1} />
          ))}
        </div>
      )}
    </div>
  );
};

// ─── Brand Wordmark ────────────────────────────────────────────────────────────
const BrandWordmark = () => (
  <span className="font-playfair font-bold text-[1.15rem] leading-tight tracking-tight">
    Everyday{' '}
    <span className="text-gold">Horoscope</span>
  </span>
);

// ─── Main NavBar ───────────────────────────────────────────────────────────────
export const NavBar = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, loading } = useAuth();

  const handleNavigate = (path) => { navigate(path); setSidebarOpen(false); };

  useEffect(() => { setSidebarOpen(false); }, [location.pathname]);

  useEffect(() => {
    document.body.style.overflow = sidebarOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [sidebarOpen]);

  const LANGUAGES = [
    { code: 'en', label: 'English', route: '/panchang/today'       },
    { code: 'hi', label: 'हिंदी',   route: '/panchang/hindi'       },
    { code: 'ta', label: 'தமிழ்',   route: '/panchang/tamil'       },
    { code: 'te', label: 'తెలుగు',  route: '/panchang/telugu'      },
    { code: 'ml', label: 'മലയാളം', route: '/panchang/malayalam'   },
    { code: 'kn', label: 'ಕನ್ನಡ',   route: '/panchang/kannada'     },
  ];

  const activeLangCode = location.pathname === '/panchang/tamil'    ? 'ta'
                       : location.pathname === '/panchang/telugu'   ? 'te'
                       : location.pathname === '/panchang/malayalam'? 'ml'
                       : location.pathname === '/panchang/kannada'  ? 'kn'
                       : location.pathname === '/panchang/hindi'    ? 'hi'
                       : 'en';

  return (
    <>
      {/* TOP BAR */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-md border-b border-border">
        <div className="flex items-center justify-between h-14 px-4">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)} className="p-2 rounded-sm hover:bg-muted/50 transition-colors text-foreground" aria-label="Open menu">
              <Menu className="h-5 w-5" />
            </button>
            <button onClick={() => navigate(user ? '/home' : '/')} className="flex items-center gap-2.5" data-testid="header-logo">
              <StarsLogo size={28} />
              <BrandWordmark />
            </button>
          </div>

          <nav className="hidden lg:flex items-center gap-0.5">
            {NAV.map((item) => (
              <DesktopDropdown key={item.label} item={item} isActive={item.path && location.pathname === item.path} />
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <ThemeToggle />
            {loading ? (
              <div className="h-8 w-8 rounded-full bg-muted animate-pulse" />
            ) : user ? (
              <UserAccountMenu />
            ) : (
              <Button data-testid="header-login-btn" onClick={() => navigate('/login')} size="sm"
                className="bg-gold hover:bg-gold/90 text-primary-foreground h-8 px-3 text-xs font-semibold">
                <LogIn className="h-3.5 w-3.5 mr-1.5" /> Sign In
              </Button>
            )}
          </div>
        </div>

        {/* LANGUAGE BAR — second tier */}
        <div className="border-t border-border/60 bg-muted/30 overflow-x-auto">
          <div className="flex items-center justify-end gap-1 h-8 px-4 min-w-max ml-auto">
            {LANGUAGES.map((lang, idx) => {
              const isActive = lang.code === activeLangCode;
              return (
                <React.Fragment key={lang.code}>
                  {idx > 0 && <span className="text-border/80 text-[10px] select-none">|</span>}
                  <button
                    onClick={() => navigate(lang.route)}
                    className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors whitespace-nowrap
                      ${isActive
                        ? 'text-gold font-semibold'
                        : 'text-muted-foreground hover:text-foreground'
                      }`}
                    aria-current={isActive ? 'true' : undefined}
                  >
                    {lang.label}
                  </button>
                </React.Fragment>
              );
            })}
          </div>
        </div>
      </header>

      {/* MOBILE SIDEBAR */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50" onClick={() => setSidebarOpen(false)}>
          <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" />
          <div className="absolute left-0 top-0 bottom-0 w-72 bg-card border-r border-border shadow-2xl flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between px-4 py-4 border-b border-border">
              <div className="flex items-center gap-2.5">
                <StarsLogo size={44} />
                <BrandWordmark />
              </div>
              <button onClick={() => setSidebarOpen(false)} className="p-1.5 rounded-sm hover:bg-muted/50 transition-colors">
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="h-px bg-gradient-to-r from-transparent via-gold/50 to-transparent" />
            <nav className="flex-1 overflow-y-auto py-3 space-y-0.5">
              {NAV.map((item) => (
                <SidebarItem key={item.label} item={item} onNavigate={handleNavigate} />
              ))}
            </nav>
            <div className="border-t border-border p-4">
              {user ? (
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-gold/20 flex items-center justify-center">
                    <User className="h-4 w-4 text-gold" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{user.name || user.email}</p>
                    <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                  </div>
                </div>
              ) : (
                <Button onClick={() => handleNavigate('/login')} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground" size="sm">
                  <LogIn className="h-4 w-4 mr-2" /> Sign In
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* BOTTOM TAB BAR */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-zinc-900 border-t border-gray-200 dark:border-zinc-700 shadow-lg">
        <div className="flex items-stretch h-16">
          {BOTTOM_NAV.map((item) => {
            const isActive =
              location.pathname === item.path ||
              (item.path === '/horoscope/daily' && location.pathname.startsWith('/horoscope')) ||
              (item.path === '/my-reports' && location.pathname === '/my-reports') ||
              (item.path === '/account' && location.pathname === '/account');
            return (
              <button
                key={item.label}
                onClick={() => navigate(item.path)}
                className={`flex-1 flex flex-col items-center justify-center gap-1 py-2 transition-colors
                  ${isActive ? 'text-amber-500' : 'text-gray-500 dark:text-gray-400'}`}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                <span className="text-xs font-medium leading-none">{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Bottom spacer so content clears the bottom nav */}
      <div className="lg:hidden h-20" />
    </>
  );
};
