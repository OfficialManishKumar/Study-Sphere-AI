"""
Study Sphere AI - Deep Seek API Module
This module handles all Deep Seek API interactions for the Study Sphere AI bot
"""

import json
import urllib.request
import urllib.parse
import re
import time
import ssl
import random

class DeepSeekAPI:
    """
    Class to handle all Deep Seek API interactions
    """

    def __init__(self, api_key, base_url, model):
        """
        Initialize the DeepSeekAPI with API credentials
        
        Args:
            api_key (str): Deep Seek API key
            base_url (str): Base URL for API calls
            model (str): Model to use for API calls
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        
        # Create SSL context that ignores certificate verification
        # This is sometimes needed for API calls in certain environments
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Fallback content for when API fails
        self.fallback_content = {
            "Important Questions": self._generate_fallback_questions,
            "Previous Year Questions": self._generate_fallback_pyq,
            "Sample Paper": self._generate_fallback_sample_paper,
            "Chapter Summary": self._generate_fallback_summary,
            "Study Notes": self._generate_fallback_notes,
            "Formula Sheet": self._generate_fallback_formulas,
            "Diagram Sheet": self._generate_fallback_diagrams,
            "Mind Map": self._generate_fallback_mindmap,
            "Quick Revision Notes": self._generate_fallback_revision
        }
    

    def generate_content(self, prompt, max_retries=1, retry_delay=2):
        """
        Generate content using Deep Seek API
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 2048
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = json.dumps(payload).encode('utf-8')
        
        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(
                    self.base_url,
                    data=data,
                    headers=headers,
                    method='POST'
                )
                with urllib.request.urlopen(req, context=self.ssl_context) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    content = response_data['choices'][0]['message']['content']
                    cleaned_content = self.clean_response(content)
                    return cleaned_content
            except Exception as e:
                print(f"API Error: {str(e)}")
                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Using fallback content.")
                    return None
        return None

    def clean_response(self, content):
        """
        Clean the API response from unwanted formatting
        
        Args:
            content (str): Raw content from API
            
        Returns:
            str: Cleaned content
        """
        if not content:
            return "No content was generated. Please try again."
            
        # Print original content for debugging
        print(f"Original content length: {len(content)}")
        print(f"Original content preview: {content[:200]}...")
        
        # Enhanced cleaning process
        
        # Step 1: Remove all LaTeX wrappers and commands
        content = re.sub(r'\\boxed\{(.*?)\}', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{.*?\}(.*?)\\end\{.*?\}', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'\\[a-zA-Z]+(\{.*?\}|\[.*?\])?', '', content)
        
        # Step 2: Remove code blocks but keep the content inside
        content = re.sub(r'```(?:json|python|markdown|latex|math)?\n?(.*?)```', r'\1', content, flags=re.DOTALL)
        
        # Step 3: Remove Markdown formatting characters while preserving structure
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'\*(.*?)\*', r'\1', content)
        content = re.sub(r'__(.*?)__', r'\1', content)
        content = re.sub(r'_(.*?)_', r'\1', content)
        
        # Step 4: Clean up LaTeX and special characters
        content = content.replace('\\\\', '')
        
        # Step 5: Fix common formatting issues
        content = re.sub(r'(\d+)\\\. ', r'\1. ', content)
        
        # Step 6: Standardize bullet points
        content = re.sub(r'^\s*[-•●◦○*]\s+', '• ', content, flags=re.MULTILINE)
        
        # Step 7: Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = '\n'.join([line.strip() for line in content.split('\n')])
        
        # Step 8: Fix spacing after punctuation
        content = re.sub(r'([.,:;!?])([a-zA-Z])', r'\1 \2', content)
        
        # Step 9: Standardize section headers
        content = re.sub(r'^([A-Z][A-Z\s]+)$', r'\n\1\n', content, flags=re.MULTILINE)
        
        # Step 10: Remove non-ASCII characters
        content = re.sub(r'[^\x00-\x7F]+', '', content)
        
        # Step 11: Fix double spaces
        content = re.sub(r' {2,}', ' ', content)
        
        # Step 12: Ensure proper spacing around list items
        content = re.sub(r'\n(\d+\.)', r'\n\n\1', content)
        content = re.sub(r'\n(•)', r'\n\n\1', content)
        
        # Step 13: Remove any remaining LaTeX artifacts
        content = content.replace('\\boxed', '')
        content = content.replace('\\text', '')
        content = content.replace('\\frac', '')
        content = content.replace('\\sqrt', 'sqrt')
        content = content.replace('\\sum', 'sum')
        content = content.replace('\\int', 'integral')
        content = content.replace('\\infty', 'infinity')
        content = content.replace('\\approx', '≈')
        content = content.replace('\\times', '×')
        content = content.replace('\\div', '÷')
        content = content.replace('\\pm', '±')
        content = content.replace('\\cdot', '·')
        content = content.replace('\\ldots', '...')
        content = content.replace('\\rightarrow', '→')
        content = content.replace('\\leftarrow', '←')
        
        # Step 14: Clean up remaining braces
        content = re.sub(r'\{([^{}]*)\}', r'\1', content)
        content = re.sub(r'\[([^\[\]]*)\]', r'\1', content)
        
        # Step 15: Final cleanup of double spaces or excessive newlines
        content = re.sub(r' {2,}', ' ', content)
        content = re.sub(r'\n{3,}', '\n\n', content)

        content = content.replace("#"," ")
        return content

    def generate_study_material(self, class_num, subject, chapter, resource_type, difficulty=None, subsubject=None):
        """
        Generate study material based on parameters
        """
        prompt = self._build_prompt(class_num, subject, chapter, resource_type, difficulty, subsubject)
        print(f"Sending prompt to API: {prompt[:200]}...")
        
        content = self.generate_content(prompt)
        
        if not content:
            fallback_method = self.fallback_content.get(resource_type, self._generate_fallback_generic)
            content = fallback_method(class_num, subject, chapter, difficulty, subsubject)
        
        return content

    def _build_prompt(self, class_num, subject, chapter, resource_type, difficulty=None, subsubject=None):
        """
        Build a detailed prompt for the API
        
        Args:
            class_num (str): Class number
            subject (str): Subject name
            chapter (str): Chapter name
            resource_type (str): Type of resource to generate
            difficulty (str, optional): Difficulty level
            subsubject (str, optional): Sub-subject name
            
        Returns:
            str: Detailed prompt for the API
        """
        context = (
            "You are Study Sphere AI, an educational assistant that helps students prepare for exams. "
            "Your responses should be clear, concise, and educational. "
            "Format your response with headings, bullet points, and emphasis as needed. "
            "Provide detailed content in plain text without markdown or LaTeX."
        )
        
        subject_context = f"Subject: {subject}"
        if subsubject:
            subject_context += f", specifically {subsubject}"
        
        chapter_context = f"Chapter: {chapter}"
        
        resource_instructions = {
            "Important Questions": (
                f"Generate 5 important questions for Class {class_num} {subject_context}, {chapter_context}. "
                "Keep them brief and clear. "
                "Number each question."
            ),
            "Previous Year Questions": (
                f"Generate 5 previous year questions for Class {class_num} {subject_context}, {chapter_context}. "
                "Include the year and keep the questions concise. "
                "Number each question."
            ),
            "Sample Paper": (
                f"Create a sample paper for Class {class_num} {subject_context}, on {chapter_context}. "
                "Include 3 short, 3 medium, and 2 long questions with clear instructions. "
                "Keep it very concise."
            ),
            "Chapter Summary": (
                f"Provide a brief summary of {chapter_context} for Class {class_num} {subject_context}. "
                "Focus on key points and definitions."
            ),
            "Study Notes": (
                f"Create short study notes for {chapter_context} from Class {class_num} {subject_context}. "
                "Include definitions and key concepts in bullet points."
            ),
            "Formula Sheet": (
                f"List essential formulas for {chapter_context} for Class {class_num} {subject_context}. "
                "Keep each formula and its explanation very short."
            ),
            "Diagram Sheet": (
                f"Describe 2 key diagrams for {chapter_context} from Class {class_num} {subject_context}. "
                "Be brief in descriptions and list only essential labels."
            ),
            "Mind Map": (
                f"Create a short textual mind map for {chapter_context} for Class {class_num} {subject_context}. "
                "Include only main branches and key points."
            ),
            "Quick Revision Notes": (
                f"Provide very concise revision notes for {chapter_context} from Class {class_num} {subject_context}. "
                "List only the most critical definitions and formulas."
            )
        }
        
        specific_instructions = resource_instructions.get(
            resource_type, 
            f"Generate educational content about {chapter_context} for Class {class_num} {subject_context}. "
            "Keep it detailed yet concise."
        )
        
        complete_prompt = f"{context}\n\n{specific_instructions}"
        
        return complete_prompt
    
    # Fallback content generators
    def _generate_fallback_questions(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback important questions"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        diff_str = "" if not difficulty or difficulty == "mixed" else f" - {difficulty.capitalize()} Level"
        
        return f"""❓ Important Questions{diff_str} ❓

Class {class_num} - {subject_str}
Chapter: {chapter}

1. What is the key idea of {chapter}?
2. Why is {chapter} important in {subject}?
3. How does {chapter} apply in real life?
4. What is one major problem in {chapter}?
5. Summarize a core concept from {chapter}."""
    
    def _generate_fallback_pyq(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback previous year questions"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        diff_str = "" if not difficulty or difficulty == "mixed" else f" - {difficulty.capitalize()} Level"
        year = random.choice([2024, 2023, 2022])
        
        return f"""📆 Previous Year Questions{diff_str} 📆

Class {class_num} - {subject_str}
Chapter: {chapter}

1. ({year}) What is a main question on {chapter}?
2. ({year}) Explain a key concept of {chapter}.
3. ({year}) Solve a brief problem on {chapter}.
4. ({year}) Describe a significant aspect of {chapter}.
5. ({year}) Summarize an experimental question on {chapter}."""
    
    def _generate_fallback_sample_paper(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback sample paper"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        diff_str = "" if not difficulty or difficulty == "mixed" else f" - {difficulty.capitalize()} Level"
        
        return f"""📄 Sample Paper{diff_str} 📄

Class {class_num} - {subject_str}
Chapter: {chapter}

Time: 1 hour    Maximum Marks: 40

Section A (Easy):
1. Define a key term from {chapter}.

Section B (Moderate):
2. Solve a brief problem from {chapter}.

Section C (Challenging):
3. Explain a major concept from {chapter} in short."""
    
    def _generate_fallback_summary(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback chapter summary"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""📋 Chapter Summary 📋

Class {class_num} - {subject_str}
Chapter: {chapter}

• Brief introduction to {chapter}.
• Key concepts and definitions.
• Summary of applications and significance."""
    
    def _generate_fallback_notes(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback study notes"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""📝 Study Notes 📝

Class {class_num} - {subject_str}
Chapter: {chapter}

• Intro: Main idea of {chapter}.
• Core: 3 key points.
• Application: 1 example.
• Tip: Review key terms."""
    
    def _generate_fallback_formulas(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback formula sheet"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""➗ Formula Sheet ➗

Class {class_num} - {subject_str}
Chapter: {chapter}

• Formula 1: [formula] - brief use.
• Formula 2: [formula] - brief use.
• Formula 3: [formula] - brief use."""
    
    def _generate_fallback_diagrams(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback diagram sheet"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""📊 Diagram Sheet 📊

Class {class_num} - {subject_str}
Chapter: {chapter}

Diagram 1:
• Title: [Concept]
• Brief description and key labels.

Diagram 2:
• Title: [Process]
• Brief steps and labels."""
    
    def _generate_fallback_mindmap(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback mind map"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""🧠 Mind Map 🧠

Class {class_num} - {subject_str}
Chapter: {chapter}

Central: {chapter}
• Branch 1: Key idea
• Branch 2: Key idea
• Branch 3: Key idea"""
    
    def _generate_fallback_revision(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback quick revision notes"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""⚡ Quick Revision Notes ⚡

Class {class_num} - {subject_str}
Chapter: {chapter}

• 3 key definitions.
• 3 core concepts.
• 2 critical formulas.
• 1 quick checklist item."""
    
    def _generate_fallback_generic(self, class_num, subject, chapter, difficulty=None, subsubject=None):
        """Generate fallback generic content"""
        subject_str = f"{subject}" if not subsubject else f"{subject} ({subsubject})"
        
        return f"""📚 Study Material 📚

Class {class_num} - {subject_str}
Chapter: {chapter}

• Brief intro to {chapter}.
• 3 main concepts.
• Key terms and one application.
• Quick study tip."""
