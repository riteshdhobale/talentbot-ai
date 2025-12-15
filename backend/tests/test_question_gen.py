"""Tests for question generation module."""

import pytest
from core.question_bank import (
    categorize_tech_stack,
    parse_questions_from_response,
    _get_fallback_questions,
    format_questions_for_display
)


class TestTechStackCategorization:
    """Tests for tech stack categorization."""
    
    def test_categorize_languages(self):
        """Test categorization of programming languages."""
        stack = ["Python", "JavaScript", "Java"]
        categorized = categorize_tech_stack(stack)
        assert len(categorized["languages"]) > 0
        assert "Python" in categorized["languages"] or "JavaScript" in categorized["languages"]
    
    def test_categorize_frameworks(self):
        """Test categorization of frameworks."""
        stack = ["Django", "React", "Flask"]
        categorized = categorize_tech_stack(stack)
        assert len(categorized["frameworks"]) > 0
    
    def test_categorize_databases(self):
        """Test categorization of databases."""
        stack = ["PostgreSQL", "MongoDB", "Redis"]
        categorized = categorize_tech_stack(stack)
        assert len(categorized["databases"]) > 0
    
    def test_categorize_tools(self):
        """Test categorization of tools."""
        stack = ["Docker", "Kubernetes", "AWS"]
        categorized = categorize_tech_stack(stack)
        assert len(categorized["tools"]) > 0


class TestQuestionParsing:
    """Tests for parsing questions from LLM response."""
    
    def test_parse_questions_with_difficulty(self):
        """Test parsing questions with difficulty markers."""
        response = """1) [★] What is Python?
2) [★★] Explain Django's ORM.
3) [★★★] Design a scalable database schema."""
        
        questions = parse_questions_from_response(response)
        assert len(questions) >= 3
        assert questions[0]["difficulty"] == 1
        assert questions[1]["difficulty"] == 2
        assert questions[2]["difficulty"] == 3
    
    def test_parse_questions_numbered(self):
        """Test parsing numbered questions."""
        response = """1. What is React?
2. How does state management work?
3. Explain hooks."""
        
        questions = parse_questions_from_response(response)
        assert len(questions) >= 3
        for q in questions:
            assert "text" in q
            assert len(q["text"]) > 0
    
    def test_parse_empty_response(self):
        """Test parsing empty response."""
        questions = parse_questions_from_response("")
        assert len(questions) == 0


class TestFallbackQuestions:
    """Tests for fallback question generation."""
    
    def test_fallback_questions_count(self):
        """Test that fallback generates 3-5 questions."""
        stack = ["Python", "Django", "PostgreSQL"]
        questions = _get_fallback_questions(stack)
        assert 3 <= len(questions) <= 5
    
    def test_fallback_questions_structure(self):
        """Test fallback questions have required structure."""
        stack = ["Python"]
        questions = _get_fallback_questions(stack)
        
        for q in questions:
            assert "text" in q
            assert "difficulty" in q
            assert "difficulty_stars" in q
            assert isinstance(q["difficulty"], int)
            assert 1 <= q["difficulty"] <= 3
            assert len(q["text"]) > 10
    
    def test_fallback_questions_relevance(self):
        """Test fallback questions are relevant to tech stack."""
        stack = ["Python", "Django"]
        questions = _get_fallback_questions(stack)
        
        # At least one question should mention the tech stack
        question_texts = " ".join([q["text"] for q in questions]).lower()
        assert "python" in question_texts or "django" in question_texts


class TestQuestionFormatting:
    """Tests for question formatting."""
    
    def test_format_questions(self):
        """Test formatting questions for display."""
        questions = [
            {"text": "What is Python?", "difficulty": 1, "difficulty_stars": "★"},
            {"text": "Explain Django ORM.", "difficulty": 2, "difficulty_stars": "★★"}
        ]
        
        formatted = format_questions_for_display(questions)
        assert "1." in formatted
        assert "2." in formatted
        assert "★" in formatted
        assert "★★" in formatted
        assert "What is Python?" in formatted
    
    def test_format_empty_questions(self):
        """Test formatting empty question list."""
        formatted = format_questions_for_display([])
        assert "No questions generated" in formatted or len(formatted) == 0

