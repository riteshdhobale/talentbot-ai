import { cn } from "@/lib/utils";
import { Check, User, Mail, Phone, Briefcase, MapPin, Code, Clock, ChevronRight } from "lucide-react";
import { CandidateInfo } from "@/types/chat";

interface StatusCardProps {
  candidateInfo: CandidateInfo;
}

interface FieldItemProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  filled: boolean;
}

const FieldItem = ({ icon, label, value, filled }: FieldItemProps) => (
  <div className={cn(
    "group flex items-center gap-4 p-3.5 rounded-xl transition-all duration-300",
    filled ? "bg-success/10 border border-success/20" : "hover:bg-muted/60 border border-transparent hover:border-border/30"
  )}>
    <div
      className={cn(
        "w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300",
        filled 
          ? "bg-success/10 text-success" 
          : "bg-muted text-muted-foreground"
      )}
    >
      {filled ? <Check className="w-4 h-4" strokeWidth={2.5} /> : icon}
    </div>
    <div className="flex-1 min-w-0">
      <span
        className={cn(
          "text-xs font-medium transition-colors duration-300 block",
          filled ? "text-muted-foreground" : "text-muted-foreground/70"
        )}
      >
        {label}
      </span>
      {filled && (
        <span className="text-sm font-semibold text-foreground truncate block">
          {value}
        </span>
      )}
    </div>
    {filled && (
      <ChevronRight className="w-4 h-4 text-muted-foreground/50" />
    )}
  </div>
);

export const StatusCard = ({ candidateInfo }: StatusCardProps) => {
  const fields = [
    { icon: <User className="w-4 h-4" />, label: "Full Name", value: candidateInfo.fullName, filled: !!candidateInfo.fullName },
    { icon: <Mail className="w-4 h-4" />, label: "Email Address", value: candidateInfo.email, filled: !!candidateInfo.email },
    { icon: <Phone className="w-4 h-4" />, label: "Phone Number", value: candidateInfo.phone, filled: !!candidateInfo.phone },
    { icon: <Clock className="w-4 h-4" />, label: "Experience", value: `${candidateInfo.yearsOfExperience} years`, filled: !!candidateInfo.yearsOfExperience },
    { icon: <Briefcase className="w-4 h-4" />, label: "Desired Position", value: candidateInfo.desiredPositions, filled: !!candidateInfo.desiredPositions },
    { icon: <MapPin className="w-4 h-4" />, label: "Location", value: candidateInfo.currentLocation, filled: !!candidateInfo.currentLocation },
    { icon: <Code className="w-4 h-4" />, label: "Tech Stack", value: candidateInfo.techStack, filled: !!candidateInfo.techStack },
  ];

  const filledCount = fields.filter(f => f.filled).length;
  const progress = (filledCount / fields.length) * 100;

  return (
    <div className="relative bg-card/90 glass-premium rounded-2xl border border-border/50 shadow-premium overflow-hidden hover:shadow-card-hover transition-all duration-300">
      {/* Premium gradient header */}
      <div className="relative gradient-primary-subtle p-6 border-b border-border/40 overflow-hidden">
        {/* Subtle texture */}
        <div className="absolute inset-0 opacity-20" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }} />
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-foreground">Your Profile</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Complete all fields to proceed</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-gradient">{filledCount}</span>
            <span className="text-sm text-muted-foreground">/ {fields.length}</span>
          </div>
        </div>
        
        {/* Premium progress bar */}
        <div className="mt-4 h-2.5 bg-muted/60 rounded-full overflow-hidden shadow-inner relative">
          <div 
            className="h-full gradient-premium rounded-full transition-all duration-1000 ease-out relative shadow-sm"
            style={{ width: `${progress}%` }}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent animate-shimmer" />
            <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent" />
          </div>
        </div>
      </div>
      
      {/* Fields - Enhanced spacing */}
      <div className="p-4 space-y-2">
        {fields.map((field) => (
          <FieldItem key={field.label} {...field} />
        ))}
      </div>
    </div>
  );
};
