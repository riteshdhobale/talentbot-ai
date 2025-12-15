export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface CandidateInfo {
  fullName: string;
  email: string;
  phone: string;
  yearsOfExperience: string;
  desiredPositions: string;
  currentLocation: string;
  techStack: string;
}

export type ConversationStep = 
  | 'greeting'
  | 'fullName'
  | 'email'
  | 'phone'
  | 'yearsOfExperience'
  | 'desiredPositions'
  | 'currentLocation'
  | 'techStack'
  | 'generating'
  | 'questions'
  | 'completed';

export interface ConversationState {
  step: ConversationStep;
  candidateInfo: CandidateInfo;
  messages: Message[];
  generatedQuestions: string[];
  isLoading: boolean;
  isCompleted: boolean;
}

export const STEP_ORDER: ConversationStep[] = [
  'greeting',
  'fullName',
  'email',
  'phone',
  'yearsOfExperience',
  'desiredPositions',
  'currentLocation',
  'techStack',
  'generating',
  'questions',
  'completed'
];

export const STEP_LABELS: Record<ConversationStep, string> = {
  greeting: 'Welcome',
  fullName: 'Full Name',
  email: 'Email',
  phone: 'Phone',
  yearsOfExperience: 'Experience',
  desiredPositions: 'Position',
  currentLocation: 'Location',
  techStack: 'Tech Stack',
  generating: 'Generating',
  questions: 'Questions',
  completed: 'Complete'
};
