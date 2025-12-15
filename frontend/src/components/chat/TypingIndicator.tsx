import { Bot, Sparkles } from "lucide-react";

export const TypingIndicator = () => {
  return (
    <div className="flex gap-4 animate-fade-in">
      {/* Avatar */}
      <div className="relative flex-shrink-0">
        <div className="absolute -inset-1 gradient-primary rounded-2xl blur-sm opacity-30 animate-pulse-soft" />
        <div className="relative w-10 h-10 rounded-2xl bg-card border-2 border-primary/20 flex items-center justify-center shadow-lg">
          <Bot className="w-5 h-5 text-primary" />
        </div>
        <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full gradient-accent flex items-center justify-center shadow-sm animate-bounce-gentle">
          <Sparkles className="w-2.5 h-2.5 text-accent-foreground" />
        </div>
      </div>
      
      {/* Typing bubble */}
      <div className="relative px-6 py-4 rounded-3xl rounded-tl-lg glass bg-card/95 border border-border/50 shadow-lg">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            {[0, 1, 2].map((i) => (
              <div 
                key={i}
                className="w-2.5 h-2.5 rounded-full gradient-primary animate-typing"
                style={{ 
                  animationDelay: `${i * 200}ms`,
                  animationDuration: '1.2s'
                }} 
              />
            ))}
          </div>
          <span className="text-xs font-medium text-muted-foreground ml-2">
            AI is thinking...
          </span>
        </div>
      </div>
    </div>
  );
};
