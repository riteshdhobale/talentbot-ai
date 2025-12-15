import { useState } from "react";
import { cn } from "@/lib/utils";
import { Check, Copy, Star, Zap, Sparkles } from "lucide-react";
import { toast } from "sonner";

interface QuestionListProps {
  questions: string[];
}

const getDifficultyConfig = (stars: number) => {
  if (stars === 1) return { 
    color: "text-success", 
    bg: "bg-success/10", 
    border: "border-success/20",
    label: "Starter",
    icon: Sparkles
  };
  if (stars === 2) return { 
    color: "text-warning", 
    bg: "bg-warning/10", 
    border: "border-warning/20",
    label: "Intermediate",
    icon: Zap
  };
  return { 
    color: "text-destructive", 
    bg: "bg-destructive/10", 
    border: "border-destructive/20",
    label: "Advanced",
    icon: Star
  };
};

export const QuestionList = ({ questions }: QuestionListProps) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyQuestion = async (question: string, index: number) => {
    const cleanQuestion = question.replace(/^\[★+\]\s*/, '');
    await navigator.clipboard.writeText(cleanQuestion);
    setCopiedIndex(index);
    toast.success("Question copied to clipboard!", {
      description: "Ready to paste anywhere",
      duration: 2000,
    });
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const parseQuestion = (question: string) => {
    const starMatch = question.match(/^\[(★+)\]\s*/);
    const stars = starMatch ? starMatch[1].length : 1;
    const text = question.replace(/^\[★+\]\s*/, '');
    return { stars, text };
  };

  return (
    <div className="space-y-4">
      {questions.map((question, index) => {
        const { stars, text } = parseQuestion(question);
        const isCopied = copiedIndex === index;
        const config = getDifficultyConfig(stars);
        const DifficultyIcon = config.icon;
        
        return (
          <div
            key={index}
            className={cn(
              "group relative bg-card rounded-2xl border border-border/50 overflow-hidden",
              "shadow-card hover:shadow-card-hover transition-all duration-500",
              "animate-fade-in-up hover-lift"
            )}
            style={{ animationDelay: `${index * 150}ms` }}
          >
            {/* Accent bar */}
            <div className={cn(
              "absolute left-0 top-0 bottom-0 w-1",
              stars === 1 && "bg-success",
              stars === 2 && "bg-warning",
              stars === 3 && "bg-destructive"
            )} />
            
            <div className="p-5 pl-6">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  {/* Header */}
                  <div className="flex items-center gap-3 mb-3">
                    <span className={cn(
                      "flex items-center justify-center w-8 h-8 rounded-lg text-sm font-bold",
                      config.bg, config.color
                    )}>
                      Q{index + 1}
                    </span>
                    
                    <div className={cn(
                      "flex items-center gap-1.5 px-3 py-1 rounded-full",
                      config.bg, config.border, "border"
                    )}>
                      <DifficultyIcon className={cn("w-3.5 h-3.5", config.color)} />
                      <span className={cn("text-xs font-semibold", config.color)}>
                        {config.label}
                      </span>
                      <div className="flex items-center gap-0.5 ml-1">
                        {Array.from({ length: 3 }).map((_, i) => (
                          <Star 
                            key={i} 
                            className={cn(
                              "w-3 h-3 transition-colors",
                              i < stars ? `${config.color} fill-current` : "text-muted-foreground/20"
                            )} 
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {/* Question text */}
                  <p className="text-[15px] text-foreground leading-relaxed font-medium">
                    {text}
                  </p>
                </div>
                
                {/* Copy button */}
                <button
                  onClick={() => copyQuestion(question, index)}
                  className={cn(
                    "flex-shrink-0 p-3 rounded-xl transition-all duration-300",
                    "border border-transparent",
                    isCopied 
                      ? "bg-success/10 border-success/20" 
                      : "bg-muted/50 hover:bg-muted hover:border-border"
                  )}
                  title="Copy question"
                >
                  {isCopied ? (
                    <Check className="w-5 h-5 text-success" />
                  ) : (
                    <Copy className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                  )}
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
