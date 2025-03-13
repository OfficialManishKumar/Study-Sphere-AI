"""
Study Sphere AI - Content Generator Module
This module handles content generation for the Study Sphere AI bot
"""

import re
from deepseek_api import DeepSeekAPI
from response_template import format_response, save_response_to_file
import os

class ContentGenerator:
    """
    Class to handle content generation for the Study Sphere AI bot
    """
    
    def __init__(self, api_key, base_url, model):
        """
        Initialize the ContentGenerator class
        
        Args:
            api_key (str): Deep Seek API key
            base_url (str): Base URL for API calls
            model (str): Model to use for API calls
        """
        self.api = DeepSeekAPI(api_key, base_url, model)

    def generate_content(self, hierarchy, resource_type, difficulty=None):
        """
        Generate content based on hierarchy and resource type
        
        Args:
            hierarchy (list): List containing [class_num, subject, (optional) subsubject, chapter]
            resource_type (str): Type of resource to generate
            difficulty (str, optional): Difficulty level
            
        Returns:
            str: Generated content
        """
        # Extract hierarchy components
        class_num = hierarchy[0]
        subject = hierarchy[1]
        
        # Determine if we have a sub-subject
        if len(hierarchy) >= 4:  # class, subject, subsubject, chapter
            subsubject = hierarchy[2]
            chapter = hierarchy[3]
        else:  # class, subject, chapter
            subsubject = None
            chapter = hierarchy[2]
        
        # Generate study material
        content = self.api.generate_study_material(
            class_num, 
            subject, 
            chapter, 
            resource_type, 
            difficulty, 
            subsubject
        )
        
        # If content is empty after API call, use fallback

        if not content:
            fallback_method = self.api.fallback_content.get(resource_type, self.api._generate_fallback_generic)
            content = fallback_method(
                class_num, 
                subject, 
                chapter, 
                difficulty, 
                subsubject
            )

        # Format content with enhanced styling
        formatted_content = self._format_content(content, resource_type)
        
        # Create a text file version for longer content
        if len(formatted_content) > 3000:
            self._create_text_file_response(
                class_num, 
                subject, 
                chapter, 
                resource_type, 
                content, 
                difficulty, 
                subsubject
            )
        
        return formatted_content
    
    def _format_content(self, content, resource_type):
        """
        Format content with enhanced styling
        
        Args:
            content (str): Raw content
            resource_type (str): Type of resource
            
        Returns:
            str: Formatted content
        """
        # Add decorative header based on resource type
        header = self._get_resource_header(resource_type)
        
        # Add decorative footer
        footer = "\n\n🌟 Study Sphere AI - Your AI Study Assistant 🌟"
        
        # Format content based on resource type
        if resource_type in ["Important Questions", "Previous Year Questions"]:
            formatted_content = self._format_questions(content)
        elif resource_type == "Sample Paper":
            formatted_content = self._format_sample_paper(content)
        elif resource_type == "Chapter Summary":
            formatted_content = self._format_summary(content)
        elif resource_type == "Study Notes":
            formatted_content = self._format_notes(content)
        elif resource_type == "Formula Sheet":
            formatted_content = self._format_formulas(content)
        elif resource_type == "Diagram Sheet":
            formatted_content = self._format_diagrams(content)
        elif resource_type == "Mind Map":
            formatted_content = self._format_mindmap(content)
        elif resource_type == "Quick Revision Notes":
            formatted_content = self._format_revision(content)
        else:
            formatted_content = content
        
        # Combine header, formatted content, and footer
        return f"{header}\n\n{formatted_content}{footer}"
    
    def _get_resource_header(self, resource_type):
        """
        Get decorative header for resource type
        
        Args:
            resource_type (str): Type of resource
            
        Returns:
            str: Decorative header
        """
        emoji = self._get_resource_emoji(resource_type)
        
        header = f"{'═' * 40}\n"
        header += f"{emoji} {resource_type.upper()} {emoji}\n"
        header += f"{'═' * 40}"
        
        return header
    
    def _get_resource_emoji(self, resource_type):
        """
        Get appropriate emoji for resource type
        
        Args:
            resource_type (str): Type of resource
            
        Returns:
            str: Emoji for resource type
        """
        resource_emojis = {
            "Important Questions": "❓",
            "Previous Year Questions": "📆",
            "Sample Paper": "📄",
            "Chapter Summary": "📋",
            "Study Notes": "📝",
            "Formula Sheet": "➗",
            "Diagram Sheet": "📊",
            "Mind Map": "🧠",
            "Quick Revision Notes": "⚡"
        }
        
        return resource_emojis.get(resource_type, "📚")
    
    def _format_questions(self, content):
        """
        Format questions with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted questions
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Question number counter
        question_number = 0
        
        # Process each line
        for line in lines:
            # Check if line is a question (starts with a number followed by period)
            if re.match(r'^\d+\.', line):
                # Extract question number
                match = re.match(r'^(\d+)\.', line)
                if match:
                    question_number = int(match.group(1))
                
                # Get question emoji based on number
                question_emoji = self._get_question_emoji(question_number)
                
                # Format question with emoji and bold
                formatted_line = f"{question_emoji} <b>Question {question_number}:</b> {line[line.find('.')+1:].strip()}"
                formatted_lines.append(formatted_line)
            else:
                # For non-question lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _get_question_emoji(self, number):
        """
        Get varied emoji for question number
        
        Args:
            number (int): Question number
            
        Returns:
            str: Emoji for question
        """
        # List of question-related emojis
        question_emojis = ["❓", "❔", "🤔", "📝", "✏️", "📌", "🔍", "💭", "📊", "📈"]
        
        # Use modulo to cycle through emojis
        return question_emojis[number % len(question_emojis)]
    
    def _format_sample_paper(self, content):
        """
        Format sample paper with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted sample paper
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Track current section
        current_section = None
        
        # Process each line
        for line in lines:
            # Check if line is a section header
            if re.match(r'^SECTION [A-Z]', line.upper()) or "SECTION" in line.upper():
                # Format as section header
                current_section = line.strip()
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"📝 <b>{current_section}</b> 📝")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line is a question (starts with number)
            elif re.match(r'^\d+\.', line):
                # Extract question number
                match = re.match(r'^(\d+)\.', line)
                if match:
                    question_number = int(match.group(1))
                    question_emoji = self._get_question_emoji(question_number)
                    
                    # Format question with emoji and bold
                    formatted_line = f"{question_emoji} <b>Q{question_number}.</b> {line[line.find('.')+1:].strip()}"
                    formatted_lines.append(formatted_line)
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_summary(self, content):
        """
        Format chapter summary with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted summary
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"📌 <b>{heading}</b> 📌")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format bullet point
                formatted_lines.append(f"  {line.strip()}")
            # Check if line is a key concept (contains important keywords)
            elif any(keyword in line.lower() for keyword in ['key', 'important', 'essential', 'critical', 'fundamental']):
                # Highlight key concept
                formatted_lines.append(f"🔑 <b>{line.strip()}</b>")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_notes(self, content):
        """
        Format study notes with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted notes
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"📝 <b>{heading}</b> 📝")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line starts with number followed by period (numbered list)
            elif re.match(r'^\d+\.', line):
                # Format numbered list item
                formatted_lines.append(f"  {line.strip()}")
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format bullet point
                formatted_lines.append(f"  {line.strip()}")
            # Check if line contains definition (contains "is defined as" or similar)
            elif any(phrase in line.lower() for phrase in ['is defined as', 'refers to', 'is a', 'means']):
                # Highlight definition
                formatted_lines.append(f"📌 <b>{line.strip()}</b>")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_formulas(self, content):
        """
        Format formula sheet with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted formula sheet
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"➗ <b>{heading}</b> ➗")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line contains a formula (contains = or other math symbols)
            elif '=' in line or '+' in line or '-' in line or '×' in line or '÷' in line:
                # Format formula
                formatted_lines.append(f"📐 <b>{line.strip()}</b>")
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format bullet point
                formatted_lines.append(f"  {line.strip()}")
            # Check if line contains "application" or "example"
            elif 'application' in line.lower() or 'example' in line.lower():
                # Highlight application/example
                formatted_lines.append(f"💡 {line.strip()}")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_diagrams(self, content):
        """
        Format diagram sheet with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted diagram sheet
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"📊 <b>{heading}</b> 📊")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line contains "component" or "part"
            elif 'component' in line.lower() or 'part' in line.lower():
                # Highlight component
                formatted_lines.append(f"🔍 <b>{line.strip()}</b>")
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format bullet point
                formatted_lines.append(f"  {line.strip()}")
            # Check if line contains "function" or "purpose"
            elif 'function' in line.lower() or 'purpose' in line.lower():
                # Highlight function/purpose
                formatted_lines.append(f"⚙️ {line.strip()}")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_mindmap(self, content):
        """
        Format mind map with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted mind map
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"🧠 <b>{heading}</b> 🧠")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line starts with "│" or "├" or "└" (mind map structure)
            elif any(char in line for char in ['│', '├', '└', '─']):
                # Keep mind map structure as is
                formatted_lines.append(line)
            # Check if line contains a concept name followed by colon
            elif ':' in line and len(line.split(':')[0].strip()) > 0:
                # Split into concept and description
                parts = line.split(':', 1)
                concept = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
                
                # Format concept and description
                if description:
                    formatted_lines.append(f"🔵 <b>{concept}:</b> {description}")
                else:
                    formatted_lines.append(f"🔵 <b>{concept}</b>")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _format_revision(self, content):
        """
        Format quick revision notes with enhanced styling
        
        Args:
            content (str): Raw content
            
        Returns:
            str: Formatted revision notes
        """
        # Split content into lines
        lines = content.split('\n')
        formatted_lines = []
        
        # Process each line
        for line in lines:
            # Check if line is a heading (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as heading
                heading = line.strip().rstrip(':')
                formatted_lines.append(f"\n{'─' * 30}")
                formatted_lines.append(f"⚡ <b>{heading}</b> ⚡")
                formatted_lines.append(f"{'─' * 30}\n")
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format bullet point
                formatted_lines.append(f"  {line.strip()}")
            # Check if line starts with "□" (checklist item)
            elif line.strip().startswith('□'):
                # Format checklist item
                formatted_lines.append(f"✅ {line.strip()[1:].strip()}")
            # Check if line contains important keywords
            elif any(keyword in line.lower() for keyword in ['remember', 'important', 'key', 'critical', 'essential']):
                # Highlight important point
                formatted_lines.append(f"🔑 <b>{line.strip()}</b>")
            else:
                # For other lines, just add them as is
                formatted_lines.append(line)
        
        # Join lines back together
        return '\n'.join(formatted_lines)
    
    def _create_text_file_response(self, class_num, subject, chapter, resource_type, content, difficulty=None, subsubject=None):
        """
        Create a text file response for longer content
        
        Args:
            class_num (str): Class number
            subject (str): Subject name
            chapter (str): Chapter name
            resource_type (str): Type of resource
            content (str): Content to format
            difficulty (str, optional): Difficulty level
            subsubject (str, optional): Sub-subject name
            
        Returns:
            str: Path to created text file
        """
        # Format response using template
        formatted_response = format_response(
            class_num, 
            subject, 
            chapter, 
            resource_type, 
            content, 
            difficulty, 
            subsubject
        )
        
        # Create filename
        filename = f"Class{class_num}_{subject.replace(' ', '')}"
        if subsubject:
            filename += f"_{subsubject.replace(' ', '')}"
        filename += f"_{chapter.replace(' ', '')}_{resource_type.replace(' ', '')}"
        if difficulty:
            filename += f"_{difficulty}"
        filename += ".txt"
        
        # Ensure directory exists
        os.makedirs("/tmp/study_sphere", exist_ok=True)
        
        # Save to file
        file_path = f"/tmp/study_sphere/{filename}"
        save_response_to_file(formatted_response, file_path)
        
        return file_path
