import { useRef, useEffect } from "react";
// Use API-enabled hook to connect to backend
// To use local-only version, change to: import { useConversation } from "@/hooks/useConversation";
import { useConversationAPI as useConversation } from "@/hooks/useConversationAPI";
import { ChatBubble } from "./chat/ChatBubble";
import { ChatInput } from "./chat/ChatInput";
import { TypingIndicator } from "./chat/TypingIndicator";
import { ProgressStepper } from "./chat/ProgressStepper";
import { StatusCard } from "./chat/StatusCard";
import { PrivacyBanner } from "./chat/PrivacyBanner";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RefreshCw, Sparkles, ArrowRight } from "lucide-react";

export const ChatInterface = () => {
  const {
    step,
    candidateInfo,
    messages,
    isLoading,
    isCompleted,
    sendMessage,
    resetSession,
  } = useConversation();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex h-[calc(100vh-80px)] overflow-hidden">
      {/* Premium Sidebar */}
      <aside className="hidden lg:flex lg:w-[360px] xl:w-[400px] flex-col border-r border-border/50 bg-card/90 glass-premium overflow-hidden shadow-2xl">
        {/* Sidebar header - Enhanced spacing */}
        <div className="p-7 border-b border-border/40">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl gradient-premium flex items-center justify-center shadow-glow hover:scale-110 transition-transform duration-300">
              <Sparkles className="w-6 h-6 text-primary-foreground" />
            </div>
            <div className="space-y-0.5">
              <h2 className="text-lg font-bold text-foreground tracking-tight">Interview Progress</h2>
              <p className="text-xs text-muted-foreground tracking-wide">Track your application</p>
            </div>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-7 space-y-7">
          {/* Progress Stepper */}
          <div>
            <ProgressStepper currentStep={step} />
          </div>

          {/* Divider - Better spacing */}
          <div className="flex items-center gap-4 py-2">
            <div className="flex-1 h-px bg-gradient-to-r from-transparent via-border/60 to-border/60" />
            <span className="text-[10px] font-bold text-muted-foreground/60 uppercase tracking-widest px-2">Details</span>
            <div className="flex-1 h-px bg-gradient-to-l from-transparent via-border/60 to-border/60" />
          </div>

          {/* Status Card */}
          <StatusCard candidateInfo={candidateInfo} />
        </div>

        {/* Privacy Banner - Enhanced spacing */}
        <div className="p-5 border-t border-border/40 bg-card/60">
          <PrivacyBanner 
            onDeleteSession={resetSession}
            isSessionActive={messages.length > 1}
          />
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col min-w-0 bg-gradient-mesh relative overflow-hidden">
        {/* Animated background orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse-soft" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-soft" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/2 right-1/3 w-72 h-72 bg-primary/5 rounded-full blur-3xl animate-float" />
        </div>
        {/* Mobile Progress Bar - Enhanced spacing */}
        <div className="lg:hidden bg-card/95 glass-premium border-b border-border/50 px-5 py-4 shadow-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl gradient-premium flex items-center justify-center shadow-glow">
                <Sparkles className="w-5 h-5 text-primary-foreground" />
              </div>
              <div className="space-y-0.5">
                <div className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Current Step</div>
                <div className="text-base font-bold text-foreground capitalize flex items-center gap-2">
                  {step.replace(/([A-Z])/g, ' $1').trim()}
                  <ArrowRight className="w-4 h-4 text-primary" />
                </div>
              </div>
            </div>
            
            {messages.length > 1 && (
              <button
                onClick={resetSession}
                className="flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-xs font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/70 border border-border/40 hover:border-border/60 transition-all duration-300 hover:scale-105"
              >
                <RefreshCw className="w-4 h-4" />
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Messages Area - Enhanced spacing */}
        <ScrollArea className="flex-1 px-5 md:px-10 py-8 relative z-10">
          <div className="max-w-3xl mx-auto space-y-7">
            {messages.map((message, index) => (
              <ChatBubble
                key={message.id}
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
                isLatest={index === messages.length - 1}
              />
            ))}
            
            {isLoading && <TypingIndicator />}
            
            <div ref={messagesEndRef} className="h-4" />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <ChatInput
          onSend={sendMessage}
          isLoading={isLoading}
          isDisabled={isCompleted}
          placeholder={
            step === 'questions' 
              ? "Share your thoughts or type 'exit' to complete..."
              : "Type your response..."
          }
        />
      </main>
    </div>
  );
};
