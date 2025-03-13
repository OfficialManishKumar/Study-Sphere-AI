"""
Study Sphere AI - Response Template

This file provides a template for formatting responses in the Study Sphere AI bot.
It can be used to create text files with properly formatted content when Telegram's
character limit is a concern.
"""

# Header Templates
CLASS_HEADER = """
╔══════════════════════════════════════════════════════════════╗
║                     📚 STUDY SPHERE AI 📚                     ║
╚══════════════════════════════════════════════════════════════╝

"""

SUBJECT_HEADER = """
╔══════════════════════════════════════════════════════════════╗
║ {emoji} {subject} - CLASS {class_num} {emoji} ║
╚══════════════════════════════════════════════════════════════╝

"""

CHAPTER_HEADER = """
╔══════════════════════════════════════════════════════════════╗
║ 📖 CHAPTER: {chapter} 📖 ║
╚══════════════════════════════════════════════════════════════╝

"""

RESOURCE_HEADER = """
╔══════════════════════════════════════════════════════════════╗
║ {emoji} {resource_type} {difficulty_text} {emoji} ║
╚══════════════════════════════════════════════════════════════╝

"""

# Section Templates
SECTION_HEADER = """
┌──────────────────────────────────────────────────────────────┐
│ {emoji} {section_title} {emoji} │
└──────────────────────────────────────────────────────────────┘

"""

# Footer Template
FOOTER = """

╔══════════════════════════════════════════════════════════════╗
║                  🌟 STUDY SPHERE AI 🌟                       ║
║        Your AI Study Assistant for Better Learning           ║
╚══════════════════════════════════════════════════════════════╝
"""

# Resource-specific Templates
QUESTIONS_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

NOTES_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

SUMMARY_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

FORMULA_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

DIAGRAM_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

MINDMAP_TEMPLATE = """
{class_header}
{subject_header}
{chapter_header}
{resource_header}

{content}

{footer}
"""

# Helper functions
def format_response(class_num, subject, chapter, resource_type, content, difficulty=None, subsubject=None):
    """
    Format a response using the appropriate template
    
    Args:
        class_num (str): Class number
        subject (str): Subject name
        chapter (str): Chapter name
        resource_type (str): Type of resource
        content (str): Content to format
        difficulty (str, optional): Difficulty level
        subsubject (str, optional): Sub-subject name
        
    Returns:
        str: Formatted response
    """
    # Get subject emoji
    subject_emoji = get_subject_emoji(subject if not subsubject else subsubject)
    
    # Get resource emoji
    resource_emoji = get_resource_emoji(resource_type)
    
    # Format headers
    class_header = CLASS_HEADER
    
    subject_text = subject if not subsubject else f"{subject} - {subsubject}"
    subject_header = SUBJECT_HEADER.format(
        emoji=subject_emoji,
        subject=subject_text,
        class_num=class_num
    )
    
    chapter_header = CHAPTER_HEADER.format(chapter=chapter)
    
    difficulty_text = f"({difficulty.upper()})" if difficulty and difficulty != "mixed" else ""
    resource_header = RESOURCE_HEADER.format(
        emoji=resource_emoji,
        resource_type=resource_type,
        difficulty_text=difficulty_text
    )
    
    # Select template based on resource type
    if resource_type in ["Important Questions", "Previous Year Questions"]:
        template = QUESTIONS_TEMPLATE
    elif resource_type in ["Study Notes", "Quick Revision Notes"]:
        template = NOTES_TEMPLATE
    elif resource_type == "Chapter Summary":
        template = SUMMARY_TEMPLATE
    elif resource_type == "Formula Sheet":
        template = FORMULA_TEMPLATE
    elif resource_type == "Diagram Sheet":
        template = DIAGRAM_TEMPLATE
    elif resource_type == "Mind Map":
        template = MINDMAP_TEMPLATE
    else:
        template = QUESTIONS_TEMPLATE  # Default template
    
    # Format content with section headers if needed
    formatted_content = format_content_with_sections(content, resource_type)
    
    # Fill template
    return template.format(
        class_header=class_header,
        subject_header=subject_header,
        chapter_header=chapter_header,
        resource_header=resource_header,
        content=formatted_content,
        footer=FOOTER
    )

def format_content_with_sections(content, resource_type):
    """
    Format content with section headers based on resource type
    
    Args:
        content (str): Content to format
        resource_type (str): Type of resource
        
    Returns:
        str: Formatted content with section headers
    """
    # Split content into lines
    lines = content.split('\n')
    
    # Initialize formatted content
    formatted_content = []
    
    # Process based on resource type
    if resource_type in ["Important Questions", "Previous Year Questions"]:
        # Add introduction
        formatted_content.append(f"Here are {resource_type} for your study:")
        formatted_content.append("")
        
        # Process each line
        for line in lines:
            # Check if line is a question (starts with number)
            if re.match(r'^\d+\.', line):
                # Format as question
                formatted_content.append(f"➤ {line}")
            else:
                formatted_content.append(line)
    
    elif resource_type == "Sample Paper":
        # Add introduction
        formatted_content.append(f"Sample Paper for your preparation:")
        formatted_content.append("")
        
        # Track current section
        current_section = None
        
        # Process each line
        for line in lines:
            # Check if line is a section header
            if re.match(r'^SECTION [A-Z]', line.upper()) or "SECTION" in line.upper():
                # Format as section header
                current_section = line.strip()
                section_emoji = "📝"
                formatted_content.append(SECTION_HEADER.format(
                    emoji=section_emoji,
                    section_title=current_section
                ))
            # Check if line is a question (starts with number)
            elif re.match(r'^\d+\.', line):
                # Format as question
                formatted_content.append(f"➤ {line}")
            else:
                formatted_content.append(line)
    
    elif resource_type in ["Study Notes", "Chapter Summary", "Quick Revision Notes"]:
        # Process each line
        current_section = None
        
        for line in lines:
            # Check if line is a potential section header (all caps or ends with colon)
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as section header
                current_section = line.strip().rstrip(':')
                section_emoji = "📌"
                formatted_content.append(SECTION_HEADER.format(
                    emoji=section_emoji,
                    section_title=current_section
                ))
            # Check if line starts with bullet point
            elif line.strip().startswith('•'):
                # Format as bullet point
                formatted_content.append(f"{line}")
            else:
                formatted_content.append(line)
    
    elif resource_type == "Formula Sheet":
        # Add introduction
        formatted_content.append(f"Essential formulas for your reference:")
        formatted_content.append("")
        
        # Track current section
        current_section = None
        
        # Process each line
        for line in lines:
            # Check if line is a section header
            if line.isupper() or (line.strip().endswith(':') and len(line.strip()) > 3):
                # Format as section header
                current_section = line.strip().rstrip(':')
                section_emoji = "🔍"
                formatted_content.append(SECTION_HEADER.format(
                    emoji=section_emoji,
                    section_title=current_section
                ))
            # Check if line contains a formula (contains = or other math symbols)
            elif '=' in line or '+' in line or '-' in line or '×' in line or '÷' in line:
                # Format as formula
                formatted_content.append(f"➤ {line}")
            else:
                formatted_content.append(line)
    
    else:
        # For other resource types, just use the content as is
        formatted_content = lines
    
    # Join lines back together
    return '\n'.join(formatted_content)

def get_subject_emoji(subject):
    """
    Get appropriate emoji for a subject
    
    Args:
        subject (str): Subject name
        
    Returns:
        str: Emoji for the subject
    """
    subject_emojis = {
        "Mathematics": "🔢",
        "Math": "🔢",
        "Physics": "⚛️",
        "Chemistry": "🧪",
        "Biology": "🧬",
        "Science": "🔬",
        "Social Science": "🌍",
        "History": "📜",
        "Geography": "🗺️",
        "Political Science": "⚖️",
        "Civics": "🏛️",
        "Economics": "📊",
        "English": "📝",
        "Hindi": "🔤",
        "Computer Science": "💻",
        "Information Technology": "💻",
        "Business Studies": "💼",
        "Accountancy": "📒",
        "Physical Education": "🏃‍♂️"
    }
    
    return subject_emojis.get(subject, "📚")

def get_resource_emoji(resource_type):
    """
    Get appropriate emoji for a resource type
    
    Args:
        resource_type (str): Resource type
        
    Returns:
        str: Emoji for the resource type
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

def save_response_to_file(formatted_response, file_path):
    """
    Save formatted response to a text file
    
    Args:
        formatted_response (str): Formatted response
        file_path (str): Path to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_response)
        return True
    except Exception as e:
        print(f"Error saving response to file: {e}")
        return False

# Import regex for content formatting
import re
