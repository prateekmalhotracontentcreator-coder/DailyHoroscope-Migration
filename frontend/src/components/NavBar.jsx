import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ThemeToggle } from './ThemeToggle';
import { UserAccountMenu } from './UserAccountMenu';
import { Button } from './ui/button';
import {
  Menu, X, Home, Star, FileText, BookOpen, Tag, Phone,
  ChevronDown, ChevronRight, Sparkles, LogIn, User,
  Sun, Moon as MoonIcon, Calendar, Gem, Hash,
  Heart, Briefcase, Shield, Leaf, Zap, Crown,
  BookMarked, Layers
} from 'lucide-react';

// ── Stars Logo ─────────────────────────────────────────────────────────────────
const StarsLogo = ({ size = 28 }) => {
  // Pre-compute petal positions (16 petals)
  const petals = Array.from({ length: 16 }, (_, i) => i);
  // Pre-compute dot ring (16 dots on r=38)
  const dots = Array.from({ length: 16 }, (_, i) => {
    const angle = (i * 22.5 - 90) * Math.PI / 180;
    return { cx: 50 + 38 * Math.cos(angle), cy: 50 + 38 * Math.sin(angle) };
  });
  // Diamond gems at cardinal points (N/S/E/W) on r=44
  const diamonds = [
    { cx: 50,    cy: 6  }, // N
    { cx: 94,    cy: 50 }, // E
    { cx: 50,    cy: 94 }, // S
    { cx: 6,     cy: 50 }, // W
  ];
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Rounded-square background */}
      <rect x="2" y="2" width="96" height="96" rx="22" ry="22" fill="#FEFCF7" />
      <rect x="2" y="2" width="96" height="96" rx="22" ry="22" fill="url(#logoGrad)" opacity="0.12" />

      {/* Outer petal ring — 16 petals (mandala / lotus) */}
      {petals.map(i => (
        <ellipse key={i}
          cx="50" cy="50"
          rx="4.5" ry="16"
          fill="#C5A059"
          opacity="0.65"
          transform={`rotate(${i * 22.5} 50 50)`}
        />
      ))}

      {/* Diamond gems at N/S/E/W */}
      {diamonds.map((d, i) => (
        <polygon key={i}
          points={`${d.cx},${d.cy - 4} ${d.cx + 3},${d.cy} ${d.cx},${d.cy + 4} ${d.cx - 3},${d.cy}`}
          fill="#E8C97A"
          opacity="0.95"
        />
      ))}

      {/* Inner beaded/dot ring — 16 dots on r=38 */}
      {dots.map((d, i) => (
        <circle key={i} cx={d.cx} cy={d.cy} r="1.6" fill="#C5A059" opacity="0.9" />
      ))}

      {/* Centre 4-point sparkle star (main) */}
      <path
        d="M50 32 L52.8 47.2 L68 50 L52.8 52.8 L50 68 L47.2 52.8 L32 50 L47.2 47.2 Z"
        fill="#C5A059"
      />
      {/* Highlight on main star */}
      <path
        d="M50 36 L51.8 47.8 L50 50 L48.2 47.8 Z"
        fill="#E8C97A"
        opacity="0.7"
      />

      {/* Small sparkle star — upper right */}
      <path
        d="M65 30 L66 33.5 L69.5 34.5 L66 35.5 L65 39 L64 35.5 L60.5 34.5 L64 33.5 Z"
        fill="#E8C97A"
        opacity="0.85"
      />

      {/* Small sparkle star — lower left */}
      <path
        d="M33 60 L33.8 62.6 L36.4 63.4 L33.8 64.2 L33 66.8 L32.2 64.2 L29.6 63.4 L32.2 62.6 Z"
        fill="#C5A059"
        opacity="0.75"
      />

      {/* Tiny sparkle dot — upper left */}
      <path
        d="M30 34 L30.5 35.8 L32.3 36.3 L30.5 36.8 L30 38.6 L29.5 36.8 L27.7 36.3 L29.5 35.8 Z"
        fill="#C5A059"
        opacity="0.6"
      />

      <defs>
        <radialGradient id="logoGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#E8C97A" />
          <stop offset="100%" stopColor="#C5A059" />
        </radialGradient>
      </defs>
    </svg>
  );
};

const NAV = [
  { label: 'Home', icon: Home, path: '/home' },
  {
    label: 'Panchang', icon: Calendar,
    children: [
      { label: "Today's Panchang",    path: '/panchang/today',     icon: Sun },
      { label: "Tomorrow's Panchang", path: '/panchang/tomorrow',  icon: Sun },
      { label: 'Tithi',               path: '/panchang/tithi',     icon: MoonIcon },
      { label: 'Shubh Muhurat',       path: '/panchang/muhurat',   icon: Star },
      { label: 'Nakshatra',           path: '/panchang/nakshatra', icon: Sparkles },
      { label: 'Choghadiya',          path: '/panchang/choghadiya',icon: Zap },
      { label: 'Rahu Kaal',           path: '/panchang/rahukaal',  icon: Shield },
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
      { label: 'Birth Chart',       path: '/birth-chart',   icon: Sparkles },
      { label: 'Kundali Milan',     path: '/kundali-milan', icon: Heart },
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
    { code: 'hi', label: 'हिंदी',   active: false },
    { code: 'en', label: 'English', active: true  },
    { code: 'ta', label: 'தமிழ்',   active: false },
    { code: 'te', label: 'తెలుగు',  active: false },
    { code: 'kn', label: 'ಕನ್ನಡ',   active: false },
  ];

  return (
    <>
      {/* TOP BAR */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-md border-b border-border">
        <div className="flex items-center justify-between h-14 px-4">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 rounded-sm hover:bg-muted/50 transition-colors" aria-label="Open menu">
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
          <div className="flex items-center gap-1 h-8 px-4 min-w-max">
            {LANGUAGES.map((lang, idx) => (
              <React.Fragment key={lang.code}>
                {idx > 0 && <span className="text-border/80 text-[10px] select-none">|</span>}
                <button
                  onClick={() => {
                    if (!lang.active) console.log(`Language switch to ${lang.code} — coming soon`);
                  }}
                  className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors whitespace-nowrap
                    ${lang.active
                      ? 'text-gold font-semibold'
                      : 'text-muted-foreground hover:text-foreground'
                    }`}
                  aria-current={lang.active ? 'true' : undefined}
                >
                  {lang.label}
                </button>
              </React.Fragment>
            ))}
          </div>
        </div>
      </header>

      {/* MOBILE SIDEBAR */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden" onClick={() => setSidebarOpen(false)}>
          <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" />
          <div className="absolute left-0 top-0 bottom-0 w-72 bg-card border-r border-border shadow-2xl flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between px-4 py-4 border-b border-border">
              <div className="flex items-center gap-2.5">
                <StarsLogo size={24} />
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
