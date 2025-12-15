import { useState } from "react";
import { Shield, X, Trash2, Lock, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

interface PrivacyBannerProps {
  onDeleteSession: () => void;
  isSessionActive: boolean;
}

export const PrivacyBanner = ({ onDeleteSession, isSessionActive }: PrivacyBannerProps) => {
  const [isDismissed, setIsDismissed] = useState(false);

  if (isDismissed) return null;

  return (
    <div className="relative overflow-hidden rounded-2xl border border-info/20 bg-gradient-to-br from-info/5 via-info/10 to-primary/5">
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-24 h-24 gradient-primary opacity-5 blur-2xl" />
      
      <div className="relative p-4">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-xl bg-info/10 flex items-center justify-center flex-shrink-0">
            <Shield className="w-5 h-5 text-info" />
          </div>
          
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-bold text-foreground flex items-center gap-2">
              Privacy First
              <Lock className="w-3.5 h-3.5 text-info" />
            </h4>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
              Your data stays local. This demo uses simulated storage for privacy.
            </p>
            
            {/* Trust badges */}
            <div className="flex flex-wrap gap-2 mt-3">
              {['Local Storage', 'No Cloud', 'GDPR Ready'].map((badge) => (
                <span key={badge} className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-success/10 text-[10px] font-medium text-success">
                  <CheckCircle2 className="w-3 h-3" />
                  {badge}
                </span>
              ))}
            </div>
          </div>
          
          <button
            onClick={() => setIsDismissed(true)}
            className="flex-shrink-0 p-1.5 rounded-lg hover:bg-muted/50 transition-colors"
          >
            <X className="w-4 h-4 text-muted-foreground" />
          </button>
        </div>
        
        {isSessionActive && (
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <button
                className={cn(
                  "mt-4 w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl",
                  "text-sm font-semibold text-destructive",
                  "bg-destructive/5 border border-destructive/20",
                  "hover:bg-destructive/10 hover:border-destructive/30",
                  "transition-all duration-300"
                )}
              >
                <Trash2 className="w-4 h-4" />
                Clear Session Data
              </button>
            </AlertDialogTrigger>
            <AlertDialogContent className="rounded-3xl border-border/50 shadow-2xl">
              <AlertDialogHeader>
                <AlertDialogTitle className="font-display text-xl">Delete Session Data?</AlertDialogTitle>
                <AlertDialogDescription className="text-muted-foreground">
                  This will permanently delete all conversation data and reset the application. 
                  This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter className="gap-3">
                <AlertDialogCancel className="rounded-xl">Cancel</AlertDialogCancel>
                <AlertDialogAction
                  onClick={onDeleteSession}
                  className="rounded-xl bg-destructive text-destructive-foreground hover:bg-destructive/90"
                >
                  Delete Everything
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        )}
      </div>
    </div>
  );
};
