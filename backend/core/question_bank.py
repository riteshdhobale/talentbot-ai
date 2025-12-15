"""Question generation logic for TalentScout."""

import re
from typing import List, Dict, Tuple
from core.llm import get_llm_provider
from core.prompts import get_question_gen_prompt
from core.logging_utils import logger


# Tech stack categories for question sampling
TECH_CATEGORIES = {
    "languages": ["python", "javascript", "java", "go", "rust", "c++", "c#", "ruby", "php", "swift", "kotlin"],
    "frameworks": ["django", "flask", "fastapi", "react", "vue", "angular", "express", "spring", "rails", "laravel"],
    "databases": ["postgresql", "mysql", "mongodb", "redis", "sqlite", "cassandra", "elasticsearch"],
    "tools": ["docker", "kubernetes", "git", "jenkins", "aws", "gcp", "azure", "terraform", "ansible"]
}


def categorize_tech_stack(tech_stack: List[str]) -> Dict[str, List[str]]:
    """
    Categorize technologies into groups.
    
    Args:
        tech_stack: List of technology names
    
    Returns:
        Dictionary mapping categories to technologies
    """
    categorized = {
        "languages": [],
        "frameworks": [],
        "databases": [],
        "tools": []
    }
    
    tech_lower = [tech.lower() for tech in tech_stack]
    
    for tech in tech_stack:
        tech_lower = tech.lower()
        categorized_flag = False
        
        for category, keywords in TECH_CATEGORIES.items():
            if any(keyword in tech_lower for keyword in keywords):
                categorized[category].append(tech)
                categorized_flag = True
                break
        
        # If not categorized, try to infer from name
        if not categorized_flag:
            if any(keyword in tech_lower for keyword in ["db", "database", "sql", "nosql"]):
                categorized["databases"].append(tech)
            elif any(keyword in tech_lower for keyword in ["framework", "lib", "library"]):
                categorized["frameworks"].append(tech)
            else:
                # Default to languages if unclear
                categorized["languages"].append(tech)
    
    return categorized


def parse_questions_from_response(response: str) -> List[Dict[str, str]]:
    """
    Parse questions from LLM response.
    
    Args:
        response: LLM response text containing questions
    
    Returns:
        List of question dictionaries with 'text' and 'difficulty'
    """
    questions = []
    
    # Pattern to match numbered questions with difficulty markers
    # Matches: "1) [★] Question text" or "1. [★★] Question text"
    pattern = r'(\d+)[\.\)]\s*\[([★]+)\]\s*(.+?)(?=\n\d+[\.\)]|$)'
    
    matches = re.findall(pattern, response, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        number, difficulty_stars, question_text = match
        difficulty = len(difficulty_stars)
        questions.append({
            "text": question_text.strip(),
            "difficulty": difficulty,
            "difficulty_stars": difficulty_stars
        })
    
    # Fallback: if no pattern matches, try to extract numbered items
    if not questions:
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+[\.\)]', line):
                # Extract question text (remove number and difficulty if present)
                question_text = re.sub(r'^\d+[\.\)]\s*(\[.+\]\s*)?', '', line)
                if question_text:
                    # Try to extract difficulty
                    difficulty_match = re.search(r'\[([★]+)\]', line)
                    difficulty = len(difficulty_match.group(1)) if difficulty_match else 2
                    questions.append({
                        "text": question_text,
                        "difficulty": difficulty,
                        "difficulty_stars": "★" * difficulty
                    })
    
    return questions


def generate_questions(tech_stack: List[str]) -> List[Dict[str, str]]:
    """
    Generate 3-5 technical questions based on tech stack.
    
    Args:
        tech_stack: List of technologies
    
    Returns:
        List of question dictionaries with 'text', 'difficulty', and 'difficulty_stars'
    """
    if not tech_stack:
        logger.warning("Empty tech stack provided for question generation")
        return []
    
    try:
        llm_provider = get_llm_provider()
        
        if not llm_provider.is_available():
            logger.error("LLM provider not available for question generation")
            return _get_fallback_questions(tech_stack)
        
        # Get question generation prompt
        prompt = get_question_gen_prompt(tech_stack)
        
        # Prepare messages for LLM
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Generate response
        response = llm_provider.generate_response(
            messages=messages,
            temperature=0.8,
            max_tokens=800
        )
        
        if not response:
            logger.warning("Empty response from LLM, using fallback questions")
            return _get_fallback_questions(tech_stack)
        
        # Parse questions from response
        questions = parse_questions_from_response(response)
        
        # Ensure we have 3-5 questions
        if len(questions) < 3:
            logger.warning(f"Only {len(questions)} questions generated, supplementing with fallback")
            fallback = _get_fallback_questions(tech_stack)
            questions.extend(fallback[:5 - len(questions)])
        elif len(questions) > 5:
            questions = questions[:5]
        
        # Validate questions
        questions = [q for q in questions if q.get("text") and len(q["text"].strip()) > 10]
        
        if len(questions) < 3:
            return _get_fallback_questions(tech_stack)
        
        logger.info(f"Generated {len(questions)} questions for tech stack: {tech_stack}")
        return questions[:5]
    
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        return _get_fallback_questions(tech_stack)


def _get_fallback_questions(tech_stack: List[str]) -> List[Dict[str, str]]:
    """
    Get fallback questions if LLM generation fails.
    
    Args:
        tech_stack: List of technologies
    
    Returns:
        List of generic question dictionaries
    """
    categorized = categorize_tech_stack(tech_stack)
    
    questions = []
    
    # Generate questions based on categories
    if categorized["languages"]:
        lang = categorized["languages"][0]
        questions.append({
            "text": f"Explain the key differences between {lang} and another language you know. What are the main use cases for {lang}?",
            "difficulty": 1,
            "difficulty_stars": "★"
        })
    
    if categorized["frameworks"]:
        framework = categorized["frameworks"][0]
        questions.append({
            "text": f"Describe the architecture of {framework}. How does it handle routing and middleware?",
            "difficulty": 2,
            "difficulty_stars": "★★"
        })
    
    if categorized["databases"]:
        db = categorized["databases"][0]
        questions.append({
            "text": f"What are the advantages and trade-offs of using {db}? When would you choose it over other database solutions?",
            "difficulty": 2,
            "difficulty_stars": "★★"
        })
    
    if categorized["tools"]:
        tool = categorized["tools"][0]
        questions.append({
            "text": f"How would you use {tool} in a production environment? What are the best practices?",
            "difficulty": 3,
            "difficulty_stars": "★★★"
        })
    
    # Generic questions if needed
    if len(questions) < 3:
        questions.append({
            "text": "Describe a challenging technical problem you've solved recently. What was your approach?",
            "difficulty": 2,
            "difficulty_stars": "★★"
        })
    
    if len(questions) < 4:
        questions.append({
            "text": "How do you ensure code quality and maintainability in your projects?",
            "difficulty": 2,
            "difficulty_stars": "★★"
        })
    
    if len(questions) < 5:
        questions.append({
            "text": "Explain your experience with version control and collaborative development workflows.",
            "difficulty": 1,
            "difficulty_stars": "★"
        })
    
    return questions[:5]


def format_questions_for_display(questions: List[Dict[str, str]]) -> str:
    """
    Format questions for display in the UI.
    
    Args:
        questions: List of question dictionaries
    
    Returns:
        Formatted string with questions
    """
    if not questions:
        return "No questions generated."
    
    formatted = []
    for i, q in enumerate(questions, 1):
        difficulty = q.get("difficulty_stars", "★" * q.get("difficulty", 2))
        text = q.get("text", "")
        formatted.append(f"{i}. [{difficulty}] {text}")
    
    return "\n\n".join(formatted)

