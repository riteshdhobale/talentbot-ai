import { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Send, Loader2, Sparkles, MessageSquare } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  isDisabled: boolean;
  placeholder?: string;
}

export const ChatInput = ({ 
  onSend, 
  isLoading, 
  isDisabled,
  placeholder = "Type your response..." 
}: ChatInputProps) => {
  const [input, setInput] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading && !isDisabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 140)}px`;
    }
  }, [input]);

  useEffect(() => {
    if (!isDisabled) {
      textareaRef.current?.focus();
    }
  }, [isDisabled]);

  return (
    <div className="relative">
      {/* Gradient border effect */}
      <div className="absolute inset-0 gradient-primary rounded-t-3xl opacity-5" />
      
      <div className="relative p-6 bg-card/95 glass-premium border-t border-border/50 shadow-2xl">
        {/* Helper text */}
        {!isDisabled && (
          <div className="flex items-center justify-center gap-2 mb-4">
            <MessageSquare className="w-3.5 h-3.5 text-muted-foreground" />
            <p className="text-xs font-medium text-muted-foreground">
              Type <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-bold">exit</kbd>, 
              <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-bold mx-1">bye</kbd>, or 
              <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-bold ml-1">quit</kbd> to end
            </p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="relative">
          {/* Input container with glow effect */}
          <div className={cn(
            "relative rounded-2xl transition-all duration-300",
            isFocused && !isDisabled && "shadow-premium"
          )}>
            {/* Animated border gradient */}
            {isFocused && !isDisabled && (
              <div className="absolute -inset-[2px] gradient-premium rounded-2xl opacity-60 blur-sm animate-pulse-soft" />
            )}
            
            <div className="relative bg-card/80 rounded-2xl border-2 border-border/50 overflow-hidden shadow-inner transition-all duration-300 hover:border-primary/40">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder={isDisabled ? "Conversation ended — refresh to start again" : placeholder}
                disabled={isLoading || isDisabled}
                rows={1}
                className={cn(
                  "w-full resize-none bg-transparent",
                  "px-5 py-4 pr-16 text-[15px] text-foreground placeholder:text-muted-foreground/60",
                  "focus:outline-none",
                  "disabled:opacity-50 disabled:cursor-not-allowed",
                  "transition-all duration-200"
                )}
              />
              
              {/* Send button */}
              <div className="absolute right-3 bottom-3">
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading || isDisabled}
                  className={cn(
                    "relative p-3 rounded-xl transition-all duration-300",
                    "disabled:opacity-40 disabled:cursor-not-allowed disabled:scale-100",
                    input.trim() && !isLoading && !isDisabled
                      ? "gradient-premium text-primary-foreground shadow-glow hover:shadow-2xl hover:shadow-glow hover:scale-110 active:scale-95 transition-all duration-300"
                      : "bg-muted text-muted-foreground"
                  )}
                >
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                  
                  {/* Sparkle effect on hover */}
                  {input.trim() && !isLoading && !isDisabled && (
                    <Sparkles className="absolute -top-1 -right-1 w-3 h-3 text-warning animate-pulse-soft" />
                  )}
                </button>
              </div>
            </div>
          </div>
        </form>
        
        {/* Powered by badge */}
        <div className="flex items-center justify-center gap-2 mt-4">
          <Sparkles className="w-3 h-3 text-primary/50" />
          <span className="text-[10px] font-medium text-muted-foreground/50 tracking-wide uppercase">
            Powered by TalentScout AI
          </span>
        </div>
      </div>
    </div>
  );
};
