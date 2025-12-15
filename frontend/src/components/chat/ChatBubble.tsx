import { cn } from "@/lib/utils";
import { Bot, User, Sparkles } from "lucide-react";
import { format } from "date-fns";
import ReactMarkdown from "react-markdown";

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isLatest?: boolean;
}

export const ChatBubble = ({ role, content, timestamp, isLatest }: ChatBubbleProps) => {
  const isUser = role === 'user';
  
  return (
    <div
      className={cn(
        "flex gap-4 animate-fade-in-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
      style={{ animationDelay: isLatest ? '0ms' : '0ms' }}
    >
      {/* Avatar */}
      <div className="relative flex-shrink-0">
        {isUser ? (
          <div className="w-10 h-10 rounded-2xl gradient-primary flex items-center justify-center shadow-lg shadow-primary/20">
            <User className="w-5 h-5 text-primary-foreground" />
          </div>
        ) : (
          <div className="relative group">
            <div className="absolute -inset-1 gradient-primary rounded-2xl blur-sm opacity-20 group-hover:opacity-40 transition-opacity" />
            <div className="relative w-10 h-10 rounded-2xl bg-card border-2 border-primary/20 flex items-center justify-center shadow-lg">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            {isLatest && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full gradient-accent flex items-center justify-center shadow-sm">
                <Sparkles className="w-2.5 h-2.5 text-accent-foreground" />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Message Content */}
      <div
        className={cn(
          "flex flex-col max-w-[80%] md:max-w-[70%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        <div
          className={cn(
            "relative px-5 py-4 shadow-xl transition-all duration-300",
            isUser
              ? "gradient-premium text-primary-foreground rounded-3xl rounded-tr-lg shadow-glow hover:shadow-2xl hover:scale-[1.02]"
              : "glass-premium bg-card/95 border border-border/50 text-card-foreground rounded-3xl rounded-tl-lg hover:shadow-card-hover hover:scale-[1.01]"
          )}
        >
          {/* Premium shine effect for user messages */}
          {isUser && (
            <>
              <div className="absolute inset-0 rounded-3xl rounded-tr-lg overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/5 to-transparent" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/5 to-transparent" />
              </div>
              <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/30 to-transparent" />
            </>
          )}
          
          {/* Subtle texture overlay */}
          <div className="absolute inset-0 rounded-3xl opacity-30 pointer-events-none" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
          }} />
          
          <div className={cn(
            "relative text-[15px] leading-relaxed prose prose-sm max-w-none",
            isUser ? "prose-invert" : ""
          )}>
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
                ul: ({ children }) => <ul className="list-disc ml-5 mb-3 space-y-1.5">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal ml-5 mb-3 space-y-1.5">{children}</ol>,
                li: ({ children }) => <li className="text-[15px] leading-relaxed">{children}</li>,
                strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                code: ({ children }) => (
                  <code className={cn(
                    "px-2 py-1 rounded-lg text-[13px] font-mono font-medium",
                    isUser ? "bg-white/20" : "bg-primary/10 text-primary"
                  )}>
                    {children}
                  </code>
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        </div>
        
        {/* Timestamp */}
        <span className={cn(
          "text-[11px] font-medium text-muted-foreground/70 mt-2 px-2",
          isUser ? "text-right" : "text-left"
        )}>
          {format(timestamp, 'h:mm a')}
        </span>
      </div>
    </div>
  );
};
