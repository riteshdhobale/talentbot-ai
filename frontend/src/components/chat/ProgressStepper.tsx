import { cn } from "@/lib/utils";
import { Check, Circle, Loader2, Sparkles, Zap, MessageSquare, User, Code2 } from "lucide-react";
import { ConversationStep, STEP_ORDER } from "@/types/chat";

interface ProgressStepperProps {
  currentStep: ConversationStep;
}

const VISIBLE_STEPS: { step: ConversationStep; icon: React.ElementType; label: string }[] = [
  { step: 'greeting', icon: MessageSquare, label: 'Welcome' },
  { step: 'fullName', icon: User, label: 'Your Details' },
  { step: 'techStack', icon: Code2, label: 'Tech Stack' },
  { step: 'questions', icon: Zap, label: 'AI Questions' },
  { step: 'completed', icon: Sparkles, label: 'Complete' },
];

export const ProgressStepper = ({ currentStep }: ProgressStepperProps) => {
  const currentIndex = STEP_ORDER.indexOf(currentStep);

  const getStepStatus = (step: ConversationStep) => {
    const stepIndex = STEP_ORDER.indexOf(step);

    if (step === 'fullName') {
      if (currentIndex > STEP_ORDER.indexOf('techStack')) return 'completed';
      if (currentIndex >= STEP_ORDER.indexOf('fullName') && currentIndex <= STEP_ORDER.indexOf('techStack')) return 'active';
      return 'pending';
    }

    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'active';
    if (step === 'questions' && currentStep === 'generating') return 'active';
    return 'pending';
  };

  return (
    <div className="space-y-2">
      {VISIBLE_STEPS.map((item, index) => {
        const status = getStepStatus(item.step);
        const isLast = index === VISIBLE_STEPS.length - 1;
        const Icon = item.icon;

        return (
          <div key={item.step} className="flex items-start gap-4">
            {/* Step indicator */}
            <div className="flex flex-col items-center">
              <div className="relative">
                {/* Glow effect for active/completed */}
                {(status === 'completed' || status === 'active') && (
                  <div className={cn(
                    "absolute -inset-1 rounded-xl blur-md transition-opacity duration-500",
                    status === 'completed' ? "bg-success/30" : "bg-primary/30 animate-pulse-soft"
                  )} />
                )}

                <div
                  className={cn(
                    "relative w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-500",
                    status === 'completed' && "bg-success shadow-glow-accent hover:scale-110",
                    status === 'active' && "gradient-premium shadow-glow hover:scale-110",
                    status === 'pending' && "bg-muted/50 border-2 border-border/60"
                  )}
                >
                  {status === 'completed' ? (
                    <Check className="w-5 h-5 text-success-foreground" strokeWidth={2.5} />
                  ) : status === 'active' ? (
                    currentStep === 'generating' && item.step === 'questions' ? (
                      <Loader2 className="w-5 h-5 text-primary-foreground animate-spin" />
                    ) : (
                      <Icon className="w-5 h-5 text-primary-foreground" />
                    )
                  ) : (
                    <Icon className="w-5 h-5 text-muted-foreground/50" />
                  )}
                </div>
              </div>

              {/* Connector line */}
              {!isLast && (
                <div className="relative w-0.5 h-6 my-1">
                  <div className="absolute inset-0 bg-border rounded-full" />
                  <div
                    className={cn(
                      "absolute inset-0 rounded-full transition-all duration-700 origin-top",
                      status === 'completed' ? "gradient-accent scale-y-100 shadow-sm" : "scale-y-0"
                    )}
                  >
                    <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent rounded-full" />
                  </div>
                </div>
              )}
            </div>

            {/* Step label */}
            <div className="pt-2.5">
              <span
                className={cn(
                  "text-sm font-semibold transition-colors duration-300",
                  status === 'completed' && "text-success",
                  status === 'active' && "text-foreground",
                  status === 'pending' && "text-muted-foreground/60"
                )}
              >
                {item.label}
              </span>
              {status === 'active' && (
                <p className="text-xs text-muted-foreground mt-0.5">In progress...</p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
