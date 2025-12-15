import { useState, useCallback, useEffect } from "react";
import { 
  Message, 
  CandidateInfo, 
  ConversationState, 
  ConversationStep,
  STEP_ORDER 
} from "@/types/chat";
import {
  validateEmail,
  validatePhone,
  validateYearsOfExperience,
  validateName,
  validateTechStack,
  validatePosition,
  validateLocation,
  isExitKeyword,
} from "@/lib/validators";
import {
  GREETING_MESSAGE,
  getFieldPrompt,
  getValidationErrorMessage,
  getConfirmationMessage,
  getSummaryMessage,
  QUESTIONS_INTRO_MESSAGE,
  EXIT_MESSAGE,
  FALLBACK_MESSAGE,
} from "@/lib/prompts";
import { generateQuestions } from "@/lib/questionGenerator";

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

const FIELD_ORDER: (keyof CandidateInfo)[] = [
  'fullName',
  'email',
  'phone',
  'yearsOfExperience',
  'desiredPositions',
  'currentLocation',
  'techStack',
];

const VALIDATORS: Record<keyof CandidateInfo, (value: string) => boolean> = {
  fullName: validateName,
  email: validateEmail,
  phone: validatePhone,
  yearsOfExperience: validateYearsOfExperience,
  desiredPositions: validatePosition,
  currentLocation: validateLocation,
  techStack: validateTechStack,
};

export const useConversation = () => {
  const [state, setState] = useState<ConversationState>(() => {
    // Try to load from localStorage
    const saved = localStorage.getItem('talentscout_session');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // Restore dates
        parsed.messages = parsed.messages.map((m: Message) => ({
          ...m,
          timestamp: new Date(m.timestamp),
        }));
        return parsed;
      } catch {
        // Invalid data, use initial state
      }
    }
    return INITIAL_STATE;
  });

  // Save to localStorage on state change
  useEffect(() => {
    localStorage.setItem('talentscout_session', JSON.stringify(state));
  }, [state]);

  // Initialize with greeting on first load
  useEffect(() => {
    if (state.messages.length === 0 && state.step === 'greeting') {
      const greetingMessage = createMessage('assistant', GREETING_MESSAGE);
      setState(prev => ({
        ...prev,
        step: 'fullName',
        messages: [greetingMessage],
      }));
    }
  }, []);

  const getCurrentField = useCallback((): keyof CandidateInfo | null => {
    const fieldSteps: ConversationStep[] = [
      'fullName', 'email', 'phone', 'yearsOfExperience', 
      'desiredPositions', 'currentLocation', 'techStack'
    ];
    if (fieldSteps.includes(state.step as ConversationStep)) {
      return state.step as keyof CandidateInfo;
    }
    return null;
  }, [state.step]);

  const getNextStep = useCallback((currentStep: ConversationStep): ConversationStep => {
    const currentIndex = STEP_ORDER.indexOf(currentStep);
    if (currentIndex < STEP_ORDER.length - 1) {
      return STEP_ORDER[currentIndex + 1];
    }
    return currentStep;
  }, []);

  const handleUserMessage = useCallback(async (userInput: string) => {
    // Add user message
    const userMessage = createMessage('user', userInput);
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
    }));

    // Simulate thinking delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 500));

    // Check for exit keywords
    if (isExitKeyword(userInput)) {
      const exitMessage = createMessage('assistant', EXIT_MESSAGE);
      setState(prev => ({
        ...prev,
        step: 'completed',
        messages: [...prev.messages, exitMessage],
        isLoading: false,
        isCompleted: true,
      }));
      return;
    }

    const currentField = getCurrentField();

    // If we're in a field collection step
    if (currentField) {
      const validator = VALIDATORS[currentField];
      const isValid = validator(userInput);

      if (!isValid) {
        // Validation failed
        const errorMessage = createMessage(
          'assistant', 
          getValidationErrorMessage(currentField)
        );
        setState(prev => ({
          ...prev,
          messages: [...prev.messages, errorMessage],
          isLoading: false,
        }));
        return;
      }

      // Valid input - update candidate info
      const updatedInfo = {
        ...state.candidateInfo,
        [currentField]: userInput.trim(),
      };

      const currentFieldIndex = FIELD_ORDER.indexOf(currentField);
      const isLastField = currentFieldIndex === FIELD_ORDER.length - 1;

      if (isLastField) {
        // All fields collected - show summary and generate questions
        const summaryMessage = createMessage('assistant', getSummaryMessage(updatedInfo));
        
        setState(prev => ({
          ...prev,
          step: 'generating',
          candidateInfo: updatedInfo,
          messages: [...prev.messages, summaryMessage],
          isLoading: true,
        }));

        // Generate questions with a slight delay
        await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));

        const questions = generateQuestions(updatedInfo.techStack);
        const questionsContent = `${QUESTIONS_INTRO_MESSAGE}\n\n${questions.map((q, i) => `${i + 1}. ${q}`).join('\n\n')}`;
        const questionsMessage = createMessage('assistant', questionsContent);
        
        const followUpMessage = createMessage(
          'assistant',
          `These questions are designed to assess your proficiency in your declared tech stack. Take your time to think through each one.\n\n**What would you like to do next?**\n- Type your thoughts or questions about any of the above\n- Type **"exit"** or **"bye"** to complete your screening`
        );

        setState(prev => ({
          ...prev,
          step: 'questions',
          generatedQuestions: questions,
          messages: [...prev.messages, questionsMessage, followUpMessage],
          isLoading: false,
        }));
      } else {
        // Move to next field
        const nextField = FIELD_ORDER[currentFieldIndex + 1];
        const confirmation = getConfirmationMessage(currentField, userInput.trim());
        const nextPrompt = getFieldPrompt(nextField);
        const responseMessage = createMessage('assistant', confirmation + nextPrompt);

        setState(prev => ({
          ...prev,
          step: nextField as ConversationStep,
          candidateInfo: updatedInfo,
          messages: [...prev.messages, responseMessage],
          isLoading: false,
        }));
      }
    } else if (state.step === 'questions') {
      // Handle conversation after questions are shown
      const followUpResponse = createMessage(
        'assistant',
        `Thank you for sharing! If you have any other questions or would like to discuss further, feel free to ask. Otherwise, type **"exit"** or **"bye"** to complete your screening and we'll be in touch soon.`
      );
      
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, followUpResponse],
        isLoading: false,
      }));
    } else {
      // Fallback for unexpected states
      const fallbackMessage = createMessage('assistant', FALLBACK_MESSAGE('information'));
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, fallbackMessage],
        isLoading: false,
      }));
    }
  }, [state, getCurrentField, getNextStep]);

  const resetSession = useCallback(() => {
    localStorage.removeItem('talentscout_session');
    const greetingMessage = createMessage('assistant', GREETING_MESSAGE);
    setState({
      ...INITIAL_STATE,
      step: 'fullName',
      messages: [greetingMessage],
    });
  }, []);

  return {
    ...state,
    sendMessage: handleUserMessage,
    resetSession,
  };
};
