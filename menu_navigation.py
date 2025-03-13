"""
Study Sphere AI - Menu Navigation Module
This module handles the hierarchical menu navigation system for the Study Sphere AI bot
"""

import json
from course_data import COURSE_DATA, RESOURCE_TYPES, DIFFICULTY_LEVELS

class MenuNavigation:
    """
    Class to handle hierarchical menu navigation for the Study Sphere AI bot
    """
    
    def __init__(self):
        """
        Initialize the MenuNavigation class
        """
        self.course_data = COURSE_DATA
        self.resource_types = RESOURCE_TYPES
        self.difficulty_levels = DIFFICULTY_LEVELS
    
    def build_class_keyboard(self):
        """
        Build keyboard for class selection
        
        Returns:
            dict: Inline keyboard markup for class selection
        """
        buttons = []
        row = []
        
        # Create a 2x2 grid for class buttons
        for i, class_num in enumerate(self.course_data.keys()):
            row.append({
                "text": f"📚 Class {class_num}",
                "callback_data": f"c:{class_num}"  # Shortened callback data
            })
            
            # Add 2 buttons per row
            if (i + 1) % 2 == 0 or i == len(self.course_data) - 1:
                buttons.append(row)
                row = []
        
        # Add Start Over button (not needed at the initial screen, but added for consistency)
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_subject_keyboard(self, class_num):
        """
        Build keyboard for subject selection
        
        Args:
            class_num (str): Selected class number
            
        Returns:
            dict: Inline keyboard markup for subject selection
        """
        buttons = []
        
        # Get subjects for the selected class
        subjects = list(self.course_data.get(class_num, {}).keys())
        
        # Add subject buttons (one per row)
        for subject in subjects:
            # Add appropriate emoji based on subject
            emoji = self._get_subject_emoji(subject)
            # Truncate subject name if needed to keep callback data short
            short_subject = subject[:20]  # Limit to 20 chars
            buttons.append([{
                "text": f"{emoji} {subject}",
                "callback_data": f"s:{class_num}:{short_subject}"
            }])
        
        # Add back button
        buttons.append([{
            "text": "🔙 Go Back",
            "callback_data": "b:c"  # Back to class
        }])
        
        # Add Start Over button
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_subsubject_keyboard(self, class_num, subject):
        """
        Build keyboard for sub-subject selection
        
        Args:
            class_num (str): Selected class number
            subject (str): Selected subject
            
        Returns:
            dict: Inline keyboard markup for sub-subject selection
        """
        buttons = []
        
        # Get sub-subjects for the selected subject
        subsubjects = list(self.course_data.get(class_num, {}).get(subject, {}).get("Subsubjects", {}).keys())
        
        # Add sub-subject buttons (one per row)
        for subsubject in subsubjects:
            # Add appropriate emoji based on sub-subject
            emoji = self._get_subject_emoji(subsubject)
            # Truncate subsubject name if needed
            short_subsubject = subsubject[:20]  # Limit to 20 chars
            buttons.append([{
                "text": f"{emoji} {subsubject}",
                "callback_data": f"ss:{class_num}:{short_subsubject}"
            }])
        
        # Add back button
        buttons.append([{
            "text": "🔙 Go Back",
            "callback_data": f"b:s:{class_num}"  # Back to subject
        }])
        
        # Add Start Over button
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_chapter_keyboard(self, hierarchy):
        """
        Build keyboard for chapter selection
        
        Args:
            hierarchy (list): List containing [class_num, subject, (optional) subsubject]
            
        Returns:
            dict: Inline keyboard markup for chapter selection
        """
        buttons = []
        
        # Extract hierarchy components
        class_num = hierarchy[0]
        subject = hierarchy[1]
        
        # Determine if we have a sub-subject
        if len(hierarchy) == 3:
            subsubject = hierarchy[2]
            chapters = self.course_data.get(class_num, {}).get(subject, {}).get("Subsubjects", {}).get(subsubject, {}).get("Chapters", [])
            back_callback = f"b:ss:{class_num}"  # Back to subsubject
        else:
            chapters = self.course_data.get(class_num, {}).get(subject, {}).get("Chapters", [])
            back_callback = f"b:s:{class_num}"  # Back to subject
        
        # Add chapter buttons (one per row)
        for chapter in chapters:
            # Truncate chapter name if needed
            short_chapter = chapter[:20]  # Limit to 20 chars
            buttons.append([{
                "text": f"📖 {chapter}",
                "callback_data": f"ch:{class_num}:{short_chapter}"
            }])
        
        # Add back button
        buttons.append([{
            "text": "🔙 Go Back",
            "callback_data": back_callback
        }])
        
        # Add Start Over button
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_resource_type_keyboard(self, hierarchy):
        """
        Build keyboard for resource type selection
        
        Args:
            hierarchy (list): List containing [class_num, subject, (optional) subsubject, chapter]
            
        Returns:
            dict: Inline keyboard markup for resource type selection
        """
        buttons = []
        
        # Extract class_num for back button
        class_num = hierarchy[0]
        subject = hierarchy[1]
        chapter = hierarchy[-1]  # Last item is chapter
        
        # Determine back callback based on hierarchy
        back_callback = f"b:ch:{class_num}"  # Back to chapter
        
        # Get appropriate resource types based on subject
        resource_types = self._get_subject_specific_resources(subject)
        
        # Add resource type buttons (one per row)
        for resource_type in resource_types:
            # Add appropriate emoji based on resource type
            emoji = self._get_resource_emoji(resource_type)
            # Truncate resource type if needed
            short_resource = resource_type[:20]  # Limit to 20 chars
            buttons.append([{
                "text": f"{emoji} {resource_type}",
                "callback_data": f"r:{class_num}:{short_resource}"
            }])
        
        # Add back button
        buttons.append([{
            "text": "🔙 Go Back",
            "callback_data": back_callback
        }])
        
        # Add Start Over button
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_difficulty_keyboard(self, hierarchy):
        """
        Build keyboard for difficulty selection
        
        Args:
            hierarchy (list): List containing [class_num, subject, (optional) subsubject, chapter, resource_type]
            
        Returns:
            dict: Inline keyboard markup for difficulty selection
        """
        buttons = []
        
        # Extract class_num for back button
        class_num = hierarchy[0]
        resource_type = hierarchy[-1]  # Last item is resource type
        
        # Determine back callback based on hierarchy
        back_callback = f"b:r:{class_num}"  # Back to resource
        
        # Add difficulty buttons (one per row)
        for difficulty in self.difficulty_levels:
            buttons.append([{
                "text": difficulty["name"],
                "callback_data": f"d:{class_num}:{difficulty['value']}"
            }])
        
        # Add back button
        buttons.append([{
            "text": "🔙 Go Back",
            "callback_data": back_callback
        }])
        
        # Add Start Over button
        buttons.append([{
            "text": "🔄 Start Over",
            "callback_data": "p:start"
        }])
        
        return {"inline_keyboard": buttons}
    
    def build_post_response_keyboard(self):
        """
        Build keyboard for post-response options
        
        Returns:
            dict: Inline keyboard markup for post-response options
        """
        buttons = [
            [{"text": "📚 Choose Another Chapter", "callback_data": "p:ch"}],
            [{"text": "📘 Reselect Subject", "callback_data": "p:s"}],
            [{"text": "🏫 Reselect Class", "callback_data": "p:c"}],
            [{"text": "🔄 Start Over", "callback_data": "p:start"}]
        ]
        
        return {"inline_keyboard": buttons}
    
    def _get_subject_emoji(self, subject):
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
    
    def _get_resource_emoji(self, resource_type):
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
    
    def _get_subject_specific_resources(self, subject):
        """
        Get subject-specific resource types
        
        Args:
            subject (str): Subject name
            
        Returns:
            list: List of appropriate resource types for the subject
        """
        # Common resources for all subjects
        common_resources = [
            "Important Questions",
            "Previous Year Questions",
            "Sample Paper",
            "Chapter Summary",
            "Study Notes",
            "Quick Revision Notes"
        ]
        
        # Subject-specific resources
        subject_specific = {
            "Mathematics": ["Formula Sheet", "Mind Map"],
            "Math": ["Formula Sheet", "Mind Map"],
            "Physics": ["Formula Sheet", "Diagram Sheet", "Mind Map"],
            "Chemistry": ["Formula Sheet", "Diagram Sheet", "Mind Map"],
            "Biology": ["Diagram Sheet", "Mind Map"],
            "Science": ["Formula Sheet", "Diagram Sheet", "Mind Map"],
            "Computer Science": ["Diagram Sheet", "Mind Map"],
            "Information Technology": ["Diagram Sheet", "Mind Map"]
        }
        
        # Combine common resources with subject-specific ones
        result = common_resources.copy()
        result.extend(subject_specific.get(subject, []))
        
        return result
    
    def parse_callback_data(self, callback_data):
        """
        Parse callback data to determine action and parameters
        
        Args:
            callback_data (str): Callback data from button press
            
        Returns:
            tuple: (action, parameters)
        """
        parts = callback_data.split(":")
        action_code = parts[0]
        parameters = parts[1:] if len(parts) > 1 else []
        
        # Map short action codes to full action names
        action_map = {
            "c": "class",
            "s": "subject",
            "ss": "subsubject",
            "ch": "chapter",
            "r": "resource",
            "d": "difficulty",
            "b": "back",
            "p": "post"
        }
        
        action = action_map.get(action_code, action_code)
        
        return action, parameters
    
    def get_hierarchy_description(self, hierarchy):
        """
        Get a human-readable description of the current hierarchy
        
        Args:
            hierarchy (list): List containing hierarchy elements
            
        Returns:
            str: Human-readable description
        """
        if len(hierarchy) == 0:
            return ""
            
        class_num = hierarchy[0]
        result = f"Class {class_num}"
        
        if len(hierarchy) > 1:
            subject = hierarchy[1]
            result += f" > {subject}"
            
        if len(hierarchy) > 2:
            # Check if third element is subsubject or chapter
            if len(hierarchy) > 3 and self._is_subsubject(class_num, subject, hierarchy[2]):
                subsubject = hierarchy[2]
                result += f" > {subsubject}"
                
                if len(hierarchy) > 3:
                    chapter = hierarchy[3]
                    result += f" > {chapter}"
            else:
                chapter = hierarchy[2]
                result += f" > {chapter}"
                
        return result
    
    def _is_subsubject(self, class_num, subject, name):
        """
        Check if a name is a subsubject
        
        Args:
            class_num (str): Class number
            subject (str): Subject name
            name (str): Name to check
            
        Returns:
            bool: True if name is a subsubject, False otherwise
        """
        subsubjects = self.course_data.get(class_num, {}).get(subject, {}).get("Subsubjects", {})
        return name in subsubjects
