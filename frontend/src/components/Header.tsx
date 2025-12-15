import { Sparkles, Zap } from "lucide-react";

export const Header = () => {
  return (
    <header className="relative bg-card/90 glass-premium border-b border-border/60 shadow-sm">
      {/* Premium gradient overlay */}
      <div className="absolute inset-0 gradient-mesh opacity-40 pointer-events-none" />
      {/* Subtle texture */}
      <div className="absolute inset-0 opacity-30 pointer-events-none" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
      }} />
      
      <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex items-center justify-between h-24">
          {/* Logo & Title - Enhanced spacing */}
          <div className="flex items-center gap-5">
            {/* Premium Logo - Larger size */}
            <div className="relative group">
              <div className="absolute -inset-1.5 gradient-premium rounded-2xl blur-xl opacity-60 group-hover:opacity-80 transition-opacity duration-500 animate-pulse-soft" />
              <div className="relative w-14 h-14 gradient-premium rounded-2xl flex items-center justify-center shadow-glow hover:shadow-2xl transition-all duration-300 hover:scale-110">
                <svg 
                  viewBox="0 0 24 24" 
                  className="w-6 h-6 text-primary-foreground"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
            </div>
            
            <div className="space-y-0.5">
              <h1 className="font-display text-3xl font-bold tracking-tight leading-tight">
                <span className="text-foreground">Talent</span>
                <span className="text-gradient ml-1.5">Scout</span>
              </h1>
              <p className="text-xs font-medium text-muted-foreground tracking-wider uppercase">
                AI-Powered Hiring Assistant
              </p>
            </div>
          </div>

          {/* Premium Badge - Enhanced spacing and sizing */}
          <div className="flex items-center gap-4">
            {/* Status indicator - Better spacing */}
            <div className="hidden sm:flex items-center gap-2.5 px-4 py-2 rounded-full bg-success/15 border border-success/30 shadow-sm hover:shadow-md transition-all duration-300">
              <div className="w-2.5 h-2.5 rounded-full bg-success animate-pulse shadow-glow-accent" />
              <span className="text-xs font-semibold text-success tracking-wide">Online</span>
            </div>
            
            {/* AI Badge - Larger, better spacing */}
            <div className="relative group cursor-default">
              <div className="absolute -inset-1 gradient-premium rounded-full blur-md opacity-40 group-hover:opacity-60 transition-opacity duration-300" />
              <div className="relative flex items-center gap-3 px-5 py-2.5 rounded-full bg-card/80 border border-primary/30 shadow-premium hover:shadow-glow transition-all duration-300 hover:scale-105">
                <Sparkles className="w-4.5 h-4.5 text-primary animate-pulse-soft" />
                <span className="text-sm font-bold text-gradient tracking-wide">
                  AI-Powered
                </span>
                <Zap className="w-4 h-4 text-warning animate-pulse-soft" style={{ animationDelay: '0.5s' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
