/**
 * API-enabled conversation hook
 * This version connects to the FastAPI backend
 */

import { useState, useCallback, useEffect } from "react";
import { 
  Message, 
  CandidateInfo, 
  ConversationState, 
  ConversationStep,
} from "@/types/chat";
import { apiClient } from "@/lib/api";

const INITIAL_STATE: ConversationState = {
  step: 'greeting',
  candidateInfo: {
    fullName: '',
    email: '',
    phone: '',
    yearsOfExperience: '',
    desiredPositions: '',
    currentLocation: '',
    techStack: '',
  },
  messages: [],
  generatedQuestions: [],
  isLoading: false,
  isCompleted: false,
};

const createMessage = (role: 'user' | 'assistant', content: string): Message => ({
  id: `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
  role,
  content,
  timestamp: new Date(),
});

// Map backend field names to frontend field names
const FIELD_MAPPING: Record<string, keyof CandidateInfo> = {
  'full_name': 'fullName',
  'email': 'email',
  'phone': 'phone',
  'years_experience': 'yearsOfExperience',
  'desired_position': 'desiredPositions',
  'current_location': 'currentLocation',
  'tech_stack': 'techStack',
};

// Map frontend field names to backend field names
const REVERSE_FIELD_MAPPING: Record<keyof CandidateInfo, string> = {
  'fullName': 'full_name',
  'email': 'email',
  'phone': 'phone',
  'yearsOfExperience': 'years_experience',
  'desiredPositions': 'desired_position',
  'currentLocation': 'current_location',
  'techStack': 'tech_stack',
};

// Map backend conversation stages to frontend steps
const mapStageToStep = (stage: string): ConversationStep => {
  const stageMap: Record<string, ConversationStep> = {
    'greeting': 'greeting',
    'collection': 'fullName',
    'questions': 'questions',
    'exit': 'completed',
  };
  return stageMap[stage] || 'greeting';
};

// Map backend collected fields to frontend candidate info
const mapFieldsToCandidateInfo = (fields: Record<string, any>): CandidateInfo => {
  const info: CandidateInfo = {
    fullName: '',
    email: '',
    phone: '',
    yearsOfExperience: '',
    desiredPositions: '',
    currentLocation: '',
    techStack: '',
  };

  for (const [backendKey, value] of Object.entries(fields)) {
    const frontendKey = FIELD_MAPPING[backendKey];
    if (frontendKey) {
      if (backendKey === 'tech_stack' && Array.isArray(value)) {
        info[frontendKey] = value.join(', ');
      } else {
        info[frontendKey] = String(value || '');
      }
    }
  }

  return info;
};

export const useConversationAPI = () => {
  const [state, setState] = useState<ConversationState>(INITIAL_STATE);
  const [sessionId, setSessionId] = useState<string | null>(() => {
    // Try to load session ID from localStorage
    return localStorage.getItem('talentscout_session_id');
  });
  const [isInitializing, setIsInitializing] = useState(true);

  // Initialize session on mount
  useEffect(() => {
    const initializeSession = async () => {
      try {
        let session;
        
        if (sessionId) {
          // Try to restore existing session
          try {
            session = await apiClient.getSession(sessionId);
          } catch (error) {
            // Session not found, create new one
            session = await apiClient.createSession();
            setSessionId(session.session_id);
            localStorage.setItem('talentscout_session_id', session.session_id);
          }
        } else {
          // Create new session
          session = await apiClient.createSession();
          setSessionId(session.session_id);
          localStorage.setItem('talentscout_session_id', session.session_id);
        }

        // Convert backend session to frontend state
        const candidateInfo = mapFieldsToCandidateInfo(session.collected_fields);
        const messages: Message[] = session.chat_history.map((msg, index) => ({
          id: `msg-${index}`,
          role: msg.role as 'user' | 'assistant',
          content: msg.content,
          timestamp: new Date(),
        }));

        setState({
          step: mapStageToStep(session.conversation_stage),
          candidateInfo,
          messages,
          generatedQuestions: [],
          isLoading: false,
          isCompleted: session.conversation_stage === 'exit',
        });
      } catch (error) {
        console.error('Failed to initialize session:', error);
        // Fallback to initial state
        setState(INITIAL_STATE);
      } finally {
        setIsInitializing(false);
      }
    };

    initializeSession();
  }, []);

  const handleUserMessage = useCallback(async (userInput: string) => {
    if (!sessionId) {
      console.error('No session ID available');
      return;
    }

    // Add user message immediately
    const userMessage = createMessage('user', userInput);
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
    }));

    try {
      // Send message to backend
      const response = await apiClient.sendMessage(sessionId, userInput);

      // Convert backend response to frontend state
      const candidateInfo = mapFieldsToCandidateInfo(response.fields_collected);
      const assistantMessage = createMessage('assistant', response.response);
      
      // Extract questions if present
      const questions = response.questions?.map(q => q.text) || [];

      setState(prev => ({
        ...prev,
        step: mapStageToStep(response.conversation_stage),
        candidateInfo,
        messages: [...prev.messages, assistantMessage],
        generatedQuestions: questions.length > 0 ? questions : prev.generatedQuestions,
        isLoading: false,
        isCompleted: response.conversation_stage === 'exit',
      }));
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = createMessage(
        'assistant',
        'I apologize, but I encountered an error processing your request. Please try again.'
      );
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
      }));
    }
  }, [sessionId]);

  const resetSession = useCallback(async () => {
    try {
      // Create new session
      const session = await apiClient.createSession();
      setSessionId(session.session_id);
      localStorage.setItem('talentscout_session_id', session.session_id);

      // Reset state
      const candidateInfo = mapFieldsToCandidateInfo(session.collected_fields);
      const messages: Message[] = session.chat_history.map((msg, index) => ({
        id: `msg-${index}`,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        timestamp: new Date(),
      }));

      setState({
        step: mapStageToStep(session.conversation_stage),
        candidateInfo,
        messages,
        generatedQuestions: [],
        isLoading: false,
        isCompleted: false,
      });
    } catch (error) {
      console.error('Failed to reset session:', error);
    }
  }, []);

  return {
    ...state,
    sendMessage: handleUserMessage,
    resetSession,
    isInitializing,
  };
};

