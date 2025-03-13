"""
Study Sphere AI - Navigation Handler Module
This module handles navigation between different menu levels for the Study Sphere AI bot
"""

class NavigationHandler:
    """
    Class to handle navigation between different menu levels
    """
    def __init__(self, menu_navigation, user_experience):
        """
        Initialize the NavigationHandler with required components
        
        Args:
            menu_navigation: Instance of MenuNavigation class
            user_experience: Instance of UserExperience class
        """
        self.menu_navigation = menu_navigation
        self.ux = user_experience
        
        # Store user navigation state
        self.user_states = {}
    
    def handle_start(self, chat_id, telegram_api):
        """
        Handle /start command
        
        Args:
            chat_id (int): Chat ID
            telegram_api: Instance of TelegramAPI class
            
        Returns:
            bool: True if handled successfully
        """
        # Reset user state
        self.user_states[chat_id] = {
            "current_level": "start",
            "hierarchy": [],
            "last_message_id": None
        }
        
        # Send welcome message with class selection keyboard
        welcome_message = self.ux.get_welcome_message()
        class_keyboard = self.menu_navigation.build_class_keyboard()
        
        result = telegram_api.send_message(chat_id, welcome_message, class_keyboard)
        
        if result.get("ok", False) and "result" in result:
            self.user_states[chat_id]["last_message_id"] = result["result"]["message_id"]
            return True
        
        return False
    
    def handle_callback(self, chat_id, callback_data, telegram_api, content_generator, error_handler):
        """
        Handle callback queries from inline keyboards
        
        Args:
            chat_id (int): Chat ID
            callback_data (str): Callback data from button press
            telegram_api: Instance of TelegramAPI class
            content_generator: Instance of ContentGenerator class
            error_handler: Instance of ErrorHandler class
            
        Returns:
            bool: True if handled successfully
        """
        # Parse callback data
        action, parameters = self.menu_navigation.parse_callback_data(callback_data)
        
        # Get current user state
        user_state = self.user_states.get(chat_id, {
            "current_level": "start",
            "hierarchy": [],
            "last_message_id": None
        })
        
        # Store user state if not exists
        if chat_id not in self.user_states:
            self.user_states[chat_id] = user_state
        
        # Handle different actions
        if action == "class":
            return self._handle_class_selection(chat_id, parameters, telegram_api, user_state)
            
        elif action == "subject":
            return self._handle_subject_selection(chat_id, parameters, telegram_api, user_state)
            
        elif action == "subsubject":
            return self._handle_subsubject_selection(chat_id, parameters, telegram_api, user_state)
            
        elif action == "chapter":
            return self._handle_chapter_selection(chat_id, parameters, telegram_api, user_state)
            
        elif action == "resource":
            return self._handle_resource_selection(chat_id, parameters, telegram_api, content_generator, error_handler, user_state)
            
        elif action == "difficulty":
            return self._handle_difficulty_selection(chat_id, parameters, telegram_api, content_generator, error_handler, user_state)
            
        elif action == "back":
            return self._handle_back_navigation(chat_id, parameters, telegram_api, user_state)
            
        elif action == "post":
            return self._handle_post_response(chat_id, parameters, telegram_api, user_state)
            
        elif action == "retry":
            # Retry last action
            if user_state["current_level"] == "generating":
                # Get stored parameters for retry
                hierarchy = user_state.get("hierarchy", [])
                resource_type = user_state.get("resource_type")
                difficulty = user_state.get("difficulty")
                
                if hierarchy and resource_type and difficulty:
                    return self._handle_difficulty_selection(
                        chat_id, 
                        hierarchy + [resource_type, difficulty], 
                        telegram_api, 
                        content_generator,
                        error_handler,
                        user_state
                    )
            
            # If retry not possible, go back to start
            return self.handle_start(chat_id, telegram_api)
        
        # Unknown action
        return False
    
    def _handle_class_selection(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle class selection
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if not parameters:
            return False
            
        class_num = parameters[0]
        
        # Update user state
        user_state["current_level"] = "class"
        user_state["hierarchy"] = [class_num]
        
        # Send subject selection message
        message = self.ux.get_subject_selection_message(class_num)
        keyboard = self.menu_navigation.build_subject_keyboard(class_num)
        
        result = telegram_api.send_message(chat_id, message, keyboard)
        
        if result.get("ok", False) and "result" in result:
            user_state["last_message_id"] = result["result"]["message_id"]
            return True
        
        return False
    
    def _handle_subject_selection(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle subject selection
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if len(parameters) < 2:
            return False
            
        class_num = parameters[0]
        subject_short = parameters[1]
        
        # Get the full subject name from the shortened version
        subject = self._get_full_subject_name(class_num, subject_short)
        
        if not subject:
            # If we can't find the subject, try to use the short name directly
            subject = subject_short
        
        # Update user state
        user_state["current_level"] = "subject"
        user_state["hierarchy"] = [class_num, subject]
        
        # Check if subject has subsubjects
        subject_info = self.menu_navigation.course_data.get(class_num, {}).get(subject, {})
        
        if "Subsubjects" in subject_info:
            # Send subsubject selection message
            message = self.ux.get_subsubject_selection_message(class_num, subject)
            keyboard = self.menu_navigation.build_subsubject_keyboard(class_num, subject)
        else:
            # Send chapter selection message
            message = self.ux.get_chapter_selection_message(class_num, subject)
            keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject])
        
        result = telegram_api.send_message(chat_id, message, keyboard)
        
        if result.get("ok", False) and "result" in result:
            user_state["last_message_id"] = result["result"]["message_id"]
            return True
        
        return False
    
    def _handle_subsubject_selection(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle subsubject selection
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if len(parameters) < 2:
            return False
            
        class_num = parameters[0]
        subsubject_short = parameters[1]
        
        # Get current hierarchy from user state
        hierarchy = user_state.get("hierarchy", [])
        if len(hierarchy) < 2:
            return False
            
        subject = hierarchy[1]
        
        # Get the full subsubject name from the shortened version
        subsubject = self._get_full_subsubject_name(class_num, subject, subsubject_short)
        
        if not subsubject:
            # If we can't find the subsubject, try to use the short name directly
            subsubject = subsubject_short
        
        # Update user state
        user_state["current_level"] = "subsubject"
        user_state["hierarchy"] = [class_num, subject, subsubject]
        
        # Send chapter selection message
        message = self.ux.get_chapter_selection_message(class_num, subject, subsubject)
        keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject, subsubject])
        
        result = telegram_api.send_message(chat_id, message, keyboard)
        
        if result.get("ok", False) and "result" in result:
            user_state["last_message_id"] = result["result"]["message_id"]
            return True
        
        return False
    
    def _handle_chapter_selection(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle chapter selection
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if len(parameters) < 2:
            return False
            
        class_num = parameters[0]
        chapter_short = parameters[1]
        
        # Get current hierarchy from user state
        hierarchy = user_state.get("hierarchy", [])
        if len(hierarchy) < 2:
            return False
            
        subject = hierarchy[1]
        
        # Check if we have a subsubject
        if len(hierarchy) >= 3:
            subsubject = hierarchy[2]
            # Get the full chapter name from the shortened version
            chapter = self._get_full_chapter_name(class_num, subject, chapter_short, subsubject)
            if chapter:
                hierarchy = [class_num, subject, subsubject, chapter]
            else:
                # If we can't find the chapter, try to use the short name directly
                chapter = chapter_short
                hierarchy = [class_num, subject, subsubject, chapter]
        else:
            # Get the full chapter name from the shortened version
            chapter = self._get_full_chapter_name(class_num, subject, chapter_short)
            if chapter:
                hierarchy = [class_num, subject, chapter]
            else:
                # If we can't find the chapter, try to use the short name directly
                chapter = chapter_short
                hierarchy = [class_num, subject, chapter]
        
        # Update user state
        user_state["current_level"] = "chapter"
        user_state["hierarchy"] = hierarchy
        
        # Get hierarchy description
        hierarchy_desc = self.menu_navigation.get_hierarchy_description(hierarchy)
        
        # Send resource type selection message
        message = self.ux.get_resource_type_selection_message(hierarchy_desc, chapter)
        keyboard = self.menu_navigation.build_resource_type_keyboard(hierarchy)
        
        result = telegram_api.send_message(chat_id, message, keyboard)
        
        if result.get("ok", False) and "result" in result:
            user_state["last_message_id"] = result["result"]["message_id"]
            return True
        
        return False
    
    def _handle_resource_selection(self, chat_id, parameters, telegram_api, content_generator, error_handler, user_state):
        """
        Handle resource type selection
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            content_generator: Instance of ContentGenerator class
            error_handler: Instance of ErrorHandler class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if len(parameters) < 2:
            return False
            
        class_num = parameters[0]
        resource_short = parameters[1]
        
        # Get the full resource type from the shortened version
        resource_type = self._get_full_resource_type(resource_short)
        
        if not resource_type:
            # If we can't find the resource type, try to use the short name directly
            resource_type = resource_short
        
        # Get current hierarchy from user state
        hierarchy = user_state.get("hierarchy", [])
        
        # Update user state
        user_state["current_level"] = "resource"
        user_state["resource_type"] = resource_type
        
        # Check if resource type needs difficulty selection
        if resource_type in ["Important Questions", "Previous Year Questions", "Sample Paper"]:
            # Send difficulty selection message
            message = self.ux.get_difficulty_selection_message(resource_type)
            keyboard = self.menu_navigation.build_difficulty_keyboard(hierarchy + [resource_type])
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
        else:
            # For other resource types, generate content directly with "mixed" difficulty
            return self._handle_difficulty_selection(
                chat_id, 
                [class_num, "mixed"], 
                telegram_api, 
                content_generator,  # Pass the content_generator object
                error_handler,      # Pass the error_handler object
                user_state
            )
        
        return False
    
    def _handle_difficulty_selection(self, chat_id, parameters, telegram_api, content_generator, error_handler, user_state):
        """
        Handle difficulty selection and content generation
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            content_generator: Instance of ContentGenerator class
            error_handler: Instance of ErrorHandler class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if len(parameters) < 2:
            return False
            
        class_num = parameters[0]
        difficulty = parameters[1]
        
        # Get current hierarchy and resource type from user state
        hierarchy = user_state.get("hierarchy", [])
        resource_type = user_state.get("resource_type")
        
        if not hierarchy or not resource_type:
            return False
        
        # Update user state
        user_state["current_level"] = "generating"
        user_state["difficulty"] = difficulty
        
        # Get chapter (last element in hierarchy)
        chapter = hierarchy[-1]
        
        # Send generating message
        generating_message = self.ux.get_generating_message(resource_type, chapter)
        telegram_api.send_message(chat_id, generating_message)
        
        # Show typing indicator
        telegram_api.send_chat_action(chat_id, "typing")
        
        try:
            # Check if content_generator is provided
            if content_generator is None:
                error_msg = "Content generator is not available. Please try again later."
                telegram_api.send_message(chat_id, f"❌ {error_msg}")
                return False
                
            # Generate content
            content = content_generator.generate_content(hierarchy, resource_type)
            
            # Format content with emojis
            formatted_content = content  # Fixed typo: was content_generator
            
            # Build post-response keyboard
            post_keyboard = self.menu_navigation.build_post_response_keyboard()
            
            # Check if error_handler is provided
            if error_handler is None:
                # Fallback if error_handler is not available
                # Split content manually if needed
                if len(formatted_content) > 4096:
                    chunks = [formatted_content[i:i+4096] for i in range(0, len(formatted_content), 4096)]
                    for chunk in chunks:
                        telegram_api.send_message(chat_id, chunk)
                    telegram_api.send_message(chat_id, "Select an option:", post_keyboard)
                else:
                    telegram_api.send_message(chat_id, formatted_content, post_keyboard)
            else:
                # Use error handler to handle API response
                error_handler.handle_api_response(chat_id, formatted_content, post_keyboard)
            
            # Update user state
            user_state["current_level"] = "completed"
            
            # Send post-response message
            post_message = self.ux.get_post_response_message()
            telegram_api.send_message(chat_id, post_message)
            
            return True
            
        except Exception as e:
            # Handle error
            error_msg = f"Error generating content: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Check if error_handler is provided
            if error_handler is None:
                # Fallback if error_handler is not available
                telegram_api.send_message(chat_id, f"❌ {error_msg}")
            else:
                error_handler.handle_error(chat_id, e, "Content Generation Error")
                
            return False
    
    def _handle_back_navigation(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle back navigation
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if not parameters:
            return False
            
        target_level = parameters[0]
        
        if target_level == "c":
            # Go back to class selection
            return self.handle_start(chat_id, telegram_api)
            
        elif target_level == "s":
            # Go back to subject selection
            if len(parameters) < 2:
                return False
                
            class_num = parameters[1]
            
            # Update user state
            user_state["current_level"] = "class"
            user_state["hierarchy"] = [class_num]
            
            # Send subject selection message
            message = self.ux.get_subject_selection_message(class_num)
            keyboard = self.menu_navigation.build_subject_keyboard(class_num)
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
                
        elif target_level == "ss":
            # Go back to subsubject selection
            if len(parameters) < 2:
                return False
                
            class_num = parameters[1]
            
            # Get current hierarchy from user state
            hierarchy = user_state.get("hierarchy", [])
            if len(hierarchy) < 2:
                return False
                
            subject = hierarchy[1]
            
            # Update user state
            user_state["current_level"] = "subject"
            user_state["hierarchy"] = [class_num, subject]
            
            # Send subsubject selection message
            message = self.ux.get_subsubject_selection_message(class_num, subject)
            keyboard = self.menu_navigation.build_subsubject_keyboard(class_num, subject)
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
                
        elif target_level == "ch":
            # Go back to chapter selection
            if len(parameters) < 2:
                return False
                
            class_num = parameters[1]
            
            # Get current hierarchy from user state
            hierarchy = user_state.get("hierarchy", [])
            if len(hierarchy) < 2:
                return False
                
            subject = hierarchy[1]
            
            # Determine if we have a sub-subject
            if len(hierarchy) >= 3 and self.menu_navigation._is_subsubject(class_num, subject, hierarchy[2]):
                # class, subject, subsubject
                subsubject = hierarchy[2]
                
                # Update user state
                user_state["current_level"] = "subsubject"
                user_state["hierarchy"] = [class_num, subject, subsubject]
                
                # Send chapter selection message
                message = self.ux.get_chapter_selection_message(class_num, subject, subsubject)
                keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject, subsubject])
            else:
                # class, subject
                # Update user state
                user_state["current_level"] = "subject"
                user_state["hierarchy"] = [class_num, subject]
                
                # Send chapter selection message
                message = self.ux.get_chapter_selection_message(class_num, subject)
                keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject])
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
                
        elif target_level == "r":
            # Go back to resource selection
            if len(parameters) < 2:
                return False
                
            class_num = parameters[1]
            
            # Get current hierarchy from user state
            hierarchy = user_state.get("hierarchy", [])
            
            # Update user state
            user_state["current_level"] = "chapter"
            
            # Get chapter (last element in hierarchy)
            chapter = hierarchy[-1]
            
            # Get hierarchy description
            hierarchy_desc = self.menu_navigation.get_hierarchy_description(hierarchy)
            
            # Send resource type selection message
            message = self.ux.get_resource_type_selection_message(hierarchy_desc, chapter)
            keyboard = self.menu_navigation.build_resource_type_keyboard(hierarchy)
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
        
        return False
    
    def _handle_post_response(self, chat_id, parameters, telegram_api, user_state):
        """
        Handle post-response options
        
        Args:
            chat_id (int): Chat ID
            parameters (list): Parameters from callback data
            telegram_api: Instance of TelegramAPI class
            user_state (dict): Current user state
            
        Returns:
            bool: True if handled successfully
        """
        if not parameters:
            return False
            
        option = parameters[0]
        
        if option == "ch":
            # Go back to chapter selection
            hierarchy = user_state.get("hierarchy", [])
            
            if len(hierarchy) < 2:
                return self.handle_start(chat_id, telegram_api)
                
            # Determine if we have a subsubject
            class_num = hierarchy[0]
            subject = hierarchy[1]
            
            if len(hierarchy) >= 3 and self.menu_navigation._is_subsubject(class_num, subject, hierarchy[2]):
                # class, subject, subsubject
                subsubject = hierarchy[2]
                
                # Update user state
                user_state["current_level"] = "subsubject"
                user_state["hierarchy"] = [class_num, subject, subsubject]
                
                # Send chapter selection message
                message = self.ux.get_chapter_selection_message(class_num, subject, subsubject)
                keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject, subsubject])
            else:
                # class, subject
                # Update user state
                user_state["current_level"] = "subject"
                user_state["hierarchy"] = [class_num, subject]
                
                # Send chapter selection message
                message = self.ux.get_chapter_selection_message(class_num, subject)
                keyboard = self.menu_navigation.build_chapter_keyboard([class_num, subject])
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
                
        elif option == "s":
            # Go back to subject selection
            hierarchy = user_state.get("hierarchy", [])
            
            if len(hierarchy) < 1:
                return self.handle_start(chat_id, telegram_api)
                
            class_num = hierarchy[0]
            
            # Update user state
            user_state["current_level"] = "class"
            user_state["hierarchy"] = [class_num]
            
            # Send subject selection message
            message = self.ux.get_subject_selection_message(class_num)
            keyboard = self.menu_navigation.build_subject_keyboard(class_num)
            
            result = telegram_api.send_message(chat_id, message, keyboard)
            
            if result.get("ok", False) and "result" in result:
                user_state["last_message_id"] = result["result"]["message_id"]
                return True
                
        elif option == "c" or option == "start":
            # Go back to class selection
            return self.handle_start(chat_id, telegram_api)
        
        return False
    
    # Helper methods to get full names from shortened versions
    def _get_full_subject_name(self, class_num, subject_short):
        """
        Get full subject name from shortened version
        
        Args:
            class_num (str): Class number
            subject_short (str): Shortened subject name
            
        Returns:
            str: Full subject name or None if not found
        """
        subjects = list(self.menu_navigation.course_data.get(class_num, {}).keys())
        
        # First try direct match
        if subject_short in subjects:
            return subject_short
        
        # Try to find a subject that starts with the shortened version
        for subject in subjects:
            if subject.lower().startswith(subject_short.lower()):
                return subject
                
        # Try to find a subject that contains the shortened version
        for subject in subjects:
            if subject_short.lower() in subject.lower():
                return subject
        
        return None
    
    def _get_full_subsubject_name(self, class_num, subject, subsubject_short):
        """
        Get full subsubject name from shortened version
        
        Args:
            class_num (str): Class number
            subject (str): Subject name
            subsubject_short (str): Shortened subsubject name
            
        Returns:
            str: Full subsubject name or None if not found
        """
        subsubjects = list(self.menu_navigation.course_data.get(class_num, {}).get(subject, {}).get("Subsubjects", {}).keys())
        
        # First try direct match
        if subsubject_short in subsubjects:
            return subsubject_short
        
        # Try to find a subsubject that starts with the shortened version
        for subsubject in subsubjects:
            if subsubject.lower().startswith(subsubject_short.lower()):
                return subsubject
                
        # Try to find a subsubject that contains the shortened version
        for subsubject in subsubjects:
            if subsubject_short.lower() in subsubject.lower():
                return subsubject
        
        return None
    
    def _get_full_chapter_name(self, class_num, subject, chapter_short, subsubject=None):
        """
        Get full chapter name from shortened version
        
        Args:
            class_num (str): Class number
            subject (str): Subject name
            chapter_short (str): Shortened chapter name
            subsubject (str, optional): Subsubject name
            
        Returns:
            str: Full chapter name or None if not found
        """
        if subsubject:
            chapters = self.menu_navigation.course_data.get(class_num, {}).get(subject, {}).get("Subsubjects", {}).get(subsubject, {}).get("Chapters", [])
        else:
            chapters = self.menu_navigation.course_data.get(class_num, {}).get(subject, {}).get("Chapters", [])
        
        # First try direct match
        if chapter_short in chapters:
            return chapter_short
        
        # Try to find a chapter that starts with the shortened version
        for chapter in chapters:
            if chapter.lower().startswith(chapter_short.lower()):
                return chapter
                
        # Try to find a chapter that contains the shortened version
        for chapter in chapters:
            if chapter_short.lower() in chapter.lower():
                return chapter
        
        return None
    
    def _get_full_resource_type(self, resource_short):
        """
        Get full resource type from shortened version
        
        Args:
            resource_short (str): Shortened resource type
            
        Returns:
            str: Full resource type or None if not found
        """
        resource_types = self.menu_navigation.resource_types
        
        # First try direct match
        if resource_short in resource_types:
            return resource_short
        
        # Try to find a resource type that starts with the shortened version
        for resource_type in resource_types:
            if resource_type.lower().startswith(resource_short.lower()):
                return resource_type
                
        # Try to find a resource type that contains the shortened version
        for resource_type in resource_types:
            if resource_short.lower() in resource_type.lower():
                return resource_type
        
        return None
