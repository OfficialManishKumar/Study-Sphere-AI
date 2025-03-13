"""
Study Sphere AI - User Experience Module
This module enhances the user experience with emojis, formatting, and engaging messages
"""

class UserExperience:
    """
    Class to handle user experience enhancements for the Study Sphere AI bot
    """
    
    def __init__(self):
        """
        Initialize the UserExperience class
        """
        # Dictionary of emojis for different contexts
        self.emojis = {
            # General emojis
            "welcome": "🎓",
            "success": "✅",
            "error": "❌",
            "loading": "⏳",
            "back": "🔙",
            "next": "➡️",
            "help": "❓",
            "info": "ℹ️",
            "warning": "⚠️",
            "star": "⭐",
            "book": "📚",
            "pencil": "✏️",
            "bulb": "💡",
            "rocket": "🚀",
            "clock": "🕒",
            "globe": "🌍",
            "check": "✓",
            
            # Subject-specific emojis
            "math": "🔢",
            "physics": "⚛️",
            "chemistry": "🧪",
            "biology": "🧬",
            "science": "🔬",
            "social_science": "🌍",
            "history": "📜",
            "geography": "🗺️",
            "political_science": "⚖️",
            "economics": "📊",
            "english": "📝",
            "hindi": "🔤",
            "computer_science": "💻",
            
            # Resource type emojis
            "questions": "❓",
            "previous_year": "📆",
            "sample_paper": "📄",
            "summary": "📋",
            "notes": "📝",
            "formula": "➗",
            "diagram": "📊",
            "mind_map": "🧠",
            "revision": "⚡",
            
            # Difficulty level emojis
            "easy": "⭐",
            "medium": "⭐⭐",
            "hard": "⭐⭐⭐",
            "mixed": "🔄"
        }
    
    def get_welcome_message(self):
        """
        Get a formatted welcome message
        
        Returns:
            str: Formatted welcome message
        """
        return (
            f"{self.emojis['welcome']} <b>Welcome to Study Sphere AI!</b> {self.emojis['book']}\n\n"
            f"I'm your personal study assistant designed to help you excel in your academics. "
            f"I can generate important questions, summaries, notes, and more for all your subjects.\n\n"
            f"{self.emojis['bulb']} Let's get started by selecting your class below:"
        )
    
    def get_class_selection_message(self):
        """
        Get a formatted class selection message
        
        Returns:
            str: Formatted class selection message
        """
        return (
            f"{self.emojis['book']} <b>Select Your Class</b> {self.emojis['book']}\n\n"
            f"Choose the class you're studying in:"
        )
    
    def get_subject_selection_message(self, class_num):
        """
        Get a formatted subject selection message
        
        Args:
            class_num (str): Selected class number
            
        Returns:
            str: Formatted subject selection message
        """
        return (
            f"{self.emojis['book']} <b>Class {class_num} Subjects</b> {self.emojis['book']}\n\n"
            f"Great! You've selected Class {class_num}.\n"
            f"Now, choose a subject you want to study:"
        )
    
    def get_subsubject_selection_message(self, class_num, subject):
        """
        Get a formatted sub-subject selection message
        
        Args:
            class_num (str): Selected class number
            subject (str): Selected subject
            
        Returns:
            str: Formatted sub-subject selection message
        """
        return (
            f"{self._get_subject_emoji(subject)} <b>{subject} Branches</b> {self._get_subject_emoji(subject)}\n\n"
            f"Class {class_num} > {subject}\n\n"
            f"Please select a specific branch of {subject}:"
        )
    
    def get_chapter_selection_message(self, class_num, subject, subsubject=None):
        """
        Get a formatted chapter selection message
        
        Args:
            class_num (str): Selected class number
            subject (str): Selected subject
            subsubject (str, optional): Selected sub-subject
            
        Returns:
            str: Formatted chapter selection message
        """
        emoji = self._get_subject_emoji(subsubject if subsubject else subject)
        
        if subsubject:
            return (
                f"{emoji} <b>{subsubject} Chapters</b> {emoji}\n\n"
                f"Class {class_num} > {subject} > {subsubject}\n\n"
                f"Please select a chapter to study:"
            )
        else:
            return (
                f"{emoji} <b>{subject} Chapters</b> {emoji}\n\n"
                f"Class {class_num} > {subject}\n\n"
                f"Please select a chapter to study:"
            )
    
    def get_resource_type_selection_message(self, hierarchy_description, chapter):
        """
        Get a formatted resource type selection message
        
        Args:
            hierarchy_description (str): Description of current hierarchy
            chapter (str): Selected chapter
            
        Returns:
            str: Formatted resource type selection message
        """
        return (
            f"{self.emojis['book']} <b>Study Resources for {chapter}</b> {self.emojis['book']}\n\n"
            f"{hierarchy_description}\n\n"
            f"{self.emojis['bulb']} What type of study material would you like for this chapter?"
        )
    
    def get_difficulty_selection_message(self, resource_type):
        """
        Get a formatted difficulty selection message
        
        Args:
            resource_type (str): Selected resource type
            
        Returns:
            str: Formatted difficulty selection message
        """
        emoji = self._get_resource_emoji(resource_type)
        
        return (
            f"{emoji} <b>Select Difficulty Level</b> {emoji}\n\n"
            f"You've selected: {resource_type}\n\n"
            f"{self.emojis['star']} Choose the difficulty level:"
        )
    
    def get_generating_message(self, resource_type, chapter):
        """
        Get a formatted generating message
        
        Args:
            resource_type (str): Selected resource type
            chapter (str): Selected chapter
            
        Returns:
            str: Formatted generating message
        """
        emoji = self._get_resource_emoji(resource_type)
        
        return (
            f"{self.emojis['loading']} <b>Generating {resource_type}</b>\n\n"
            f"I'm creating {resource_type.lower()} for {chapter}.\n"
            f"This may take a moment. Please wait..."
        )
    
    def get_post_response_message(self):
        """
        Get a formatted post-response message
        
        Returns:
            str: Formatted post-response message
        """
        return (
            f"{self.emojis['rocket']} <b>What would you like to do next?</b> {self.emojis['rocket']}\n\n"
            f"You can choose another chapter, select a different subject, or start over with a new class."
        )
    
    def get_error_message(self, error_type="general"):
        """
        Get a formatted error message
        
        Args:
            error_type (str): Type of error
            
        Returns:
            str: Formatted error message
        """
        if error_type == "api":
            return (
                f"{self.emojis['error']} <b>Connection Error</b>\n\n"
                f"I couldn't connect to the knowledge database at the moment. "
                f"This might be due to high traffic or temporary issues.\n\n"
                f"{self.emojis['clock']} Please try again in a few moments or choose a different option."
            )
        elif error_type == "content":
            return (
                f"{self.emojis['error']} <b>Content Generation Error</b>\n\n"
                f"I had trouble generating the content you requested. "
                f"This might be due to the complexity of the topic or temporary issues.\n\n"
                f"{self.emojis['bulb']} Please try again with a different chapter or resource type."
            )
        else:
            return (
                f"{self.emojis['error']} <b>Oops! Something went wrong</b>\n\n"
                f"I encountered an unexpected issue while processing your request.\n\n"
                f"{self.emojis['rocket']} Please try again or start over with a new selection."
            )
    
    def format_hierarchy_path(self, hierarchy):
        """
        Format hierarchy path with emojis
        
        Args:
            hierarchy (list): List containing hierarchy elements
            
        Returns:
            str: Formatted hierarchy path
        """
        if not hierarchy:
            return ""
            
        formatted_parts = []
        
        # Format class
        if len(hierarchy) >= 1:
            formatted_parts.append(f"{self.emojis['book']} Class {hierarchy[0]}")
        
        # Format subject
        if len(hierarchy) >= 2:
            subject = hierarchy[1]
            formatted_parts.append(f"{self._get_subject_emoji(subject)} {subject}")
        
        # Format subsubject or chapter
        if len(hierarchy) >= 3:
            # Check if third element is subsubject or chapter
            if len(hierarchy) >= 4:  # If we have 4+ elements, 3rd is likely subsubject
                subsubject = hierarchy[2]
                formatted_parts.append(f"{self._get_subject_emoji(subsubject)} {subsubject}")
                
                # Format chapter if available
                if len(hierarchy) >= 4:
                    chapter = hierarchy[3]
                    formatted_parts.append(f"📖 {chapter}")
            else:
                # Third element is chapter
                chapter = hierarchy[2]
                formatted_parts.append(f"📖 {chapter}")
        
        return " > ".join(formatted_parts)
    
    def _get_subject_emoji(self, subject):
        """
        Get appropriate emoji for a subject
        
        Args:
            subject (str): Subject name
            
        Returns:
            str: Emoji for the subject
        """
        subject_lower = subject.lower() if subject else ""
        
        if "math" in subject_lower:
            return self.emojis["math"]
        elif "physics" in subject_lower:
            return self.emojis["physics"]
        elif "chemistry" in subject_lower:
            return self.emojis["chemistry"]
        elif "biology" in subject_lower:
            return self.emojis["biology"]
        elif "science" in subject_lower:
            return self.emojis["science"]
        elif "social" in subject_lower:
            return self.emojis["social_science"]
        elif "history" in subject_lower:
            return self.emojis["history"]
        elif "geography" in subject_lower:
            return self.emojis["geography"]
        elif "political" in subject_lower:
            return self.emojis["political_science"]
        elif "economics" in subject_lower:
            return self.emojis["economics"]
        elif "english" in subject_lower:
            return self.emojis["english"]
        elif "hindi" in subject_lower:
            return self.emojis["hindi"]
        elif "computer" in subject_lower or "information" in subject_lower:
            return self.emojis["computer_science"]
        else:
            return self.emojis["book"]
    
    def _get_resource_emoji(self, resource_type):
        """
        Get appropriate emoji for a resource type
        
        Args:
            resource_type (str): Resource type
            
        Returns:
            str: Emoji for the resource type
        """
        resource_lower = resource_type.lower() if resource_type else ""
        
        if "question" in resource_lower and "previous" not in resource_lower:
            return self.emojis["questions"]
        elif "previous" in resource_lower:
            return self.emojis["previous_year"]
        elif "sample" in resource_lower or "paper" in resource_lower:
            return self.emojis["sample_paper"]
        elif "summary" in resource_lower:
            return self.emojis["summary"]
        elif "notes" in resource_lower and "revision" not in resource_lower:
            return self.emojis["notes"]
        elif "formula" in resource_lower:
            return self.emojis["formula"]
        elif "diagram" in resource_lower:
            return self.emojis["diagram"]
        elif "mind" in resource_lower or "map" in resource_lower:
            return self.emojis["mind_map"]
        elif "revision" in resource_lower:
            return self.emojis["revision"]
        else:
            return self.emojis["book"]
