"""
Chat interface for CLI Pilot - simulates GitHub Copilot Chat.
"""

import json
import time
from typing import Dict, List, Any, Optional
from .config import CLIConfig


class ChatInterface:
    """Interface for chat functionality, simulating GitHub Copilot Chat."""
    
    def __init__(self, config: CLIConfig, verbose: bool = False):
        """Initialize chat interface.
        
        Args:
            config: Configuration object
            verbose: Enable verbose logging
        """
        self.config = config
        self.verbose = verbose
        self.session_history = []
        
    def send_message(self, message: str, context: Dict[str, Any] = None, 
                    agent: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to the chat system.
        
        Args:
            message: The chat message
            context: Context information
            agent: Specific agent to use
            
        Returns:
            Response dictionary
        """
        if not self.config.is_configured():
            return {
                "error": "CLI Pilot is not configured. Please run 'python main.py setup' first."
            }
        
        try:
            # Prepare the request
            chat_request = self._prepare_request(message, context, agent)
            
            if self.verbose:
                print(f"Sending chat request with {len(chat_request.get('context', {}).get('files', []))} files...")
            
            # For demo purposes, we'll simulate a response
            # In a real implementation, this would connect to GitHub Copilot's API
            response = self._simulate_copilot_response(chat_request)
            
            # Add to session history
            self.session_history.append({
                "type": "request",
                "message": message,
                "context": context,
                "timestamp": time.time()
            })
            
            self.session_history.append({
                "type": "response",
                "content": response.get("content", ""),
                "timestamp": time.time()
            })
            
            return response
            
        except Exception as e:
            return {
                "error": f"Failed to send message: {str(e)}"
            }
    
    def _prepare_request(self, message: str, context: Dict[str, Any] = None, 
                        agent: Optional[str] = None) -> Dict[str, Any]:
        """Prepare the chat request.
        
        Args:
            message: The chat message
            context: Context information
            agent: Specific agent to use
            
        Returns:
            Prepared request dictionary
        """
        chat_config = self.config.get_chat_config()
        
        request = {
            "message": message,
            "agent": agent or chat_config.get("default_agent", "workspace"),
            "context": context or {},
            "session_id": "cli_session",
            "timestamp": time.time(),
            "config": {
                "temperature": chat_config.get("temperature", 0.1),
                "max_tokens": chat_config.get("max_context_size", 4096)
            }
        }
        
        return request
    
    def _simulate_copilot_response(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a GitHub Copilot response.
        
        Note: This is a simulation for demo purposes. In a real implementation,
        this would connect to GitHub Copilot's actual API.
        
        Args:
            request: The chat request
            
        Returns:
            Simulated response
        """
        message = request["message"].lower()
        context = request.get("context", {})
        files = context.get("files", [])
        workspace_info = context.get("workspace_info", {})
        
        # Simulate different types of responses based on the message
        if any(word in message for word in ["explain", "what does", "how does"]):
            return self._generate_explanation_response(files, message)
        
        elif any(word in message for word in ["hello", "hi", "hey"]):
            return self._generate_greeting_response(context)
        
        elif any(word in message for word in ["create", "generate", "make", "build"]):
            return self._generate_creation_response(message, workspace_info)
        
        elif any(word in message for word in ["fix", "debug", "error", "bug"]):
            return self._generate_fix_response(files, message)
        
        elif any(word in message for word in ["test", "testing", "unittest"]):
            return self._generate_test_response(files, workspace_info)
        
        elif any(word in message for word in ["refactor", "improve", "optimize"]):
            return self._generate_refactor_response(files, message)
        
        else:
            return self._generate_general_response(message, context)
    
    def _generate_greeting_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a greeting response."""
        workspace_path = context.get("workspace", "current directory")
        project_type = context.get("workspace_info", {}).get("project_info", {}).get("type", "unknown")
        
        content = f"""Hello! I'm CLI Pilot, your command-line GitHub Copilot assistant.

I can see you're working in: {workspace_path}"""
        
        if project_type != "unknown":
            content += f"\nProject type detected: {project_type}"
        
        content += """

I can help you with:
• Code explanation and documentation
• Creating new functions and classes
• Debugging and fixing issues
• Writing tests
• Code refactoring and optimization
• General programming questions

What would you like to work on today?"""
        
        return {
            "content": content,
            "references": []
        }
    
    def _generate_explanation_response(self, files: List[Dict[str, Any]], message: str) -> Dict[str, Any]:
        """Generate an explanation response."""
        if not files:
            content = """I'd be happy to explain code for you! However, I don't see any files in the context. 

To get a detailed explanation, you can:
1. Include specific files: `python main.py chat "Explain this code" --file yourfile.py`
2. Include workspace context: `python main.py chat "Explain this code" --context`

What specific code would you like me to explain?"""
        else:
            file = files[0]  # Focus on the first file
            language = file.get("language", "unknown")
            lines = len(file.get("content", "").split('\n'))
            
            content = f"""I'll explain the code in `{file['path']}`:

**File Overview:**
- Language: {language.title() if language else 'Unknown'}
- Size: {file.get('size', 0)} bytes
- Lines: {lines}

**Code Analysis:**
This appears to be a {language} file. """
            
            # Add specific analysis based on file content
            if language == "python":
                content += """Here's what I can see:

• The file contains Python code
• I can help explain functions, classes, imports, and logic
• I can suggest improvements or identify potential issues

Would you like me to focus on a specific part of the code?"""
            elif language == "javascript":
                content += """Here's what I can see:

• The file contains JavaScript code
• I can explain functions, objects, async patterns, and DOM manipulation
• I can help with modern JS features and best practices

What specific part would you like me to explain in detail?"""
            else:
                content += f"""I can analyze the structure and provide insights about this {language} code.

What specific aspects would you like me to explain?"""
        
        return {
            "content": content,
            "references": [f.get("path") for f in files]
        }
    
    def _generate_creation_response(self, message: str, workspace_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a code creation response."""
        project_type = workspace_info.get("project_info", {}).get("type", "unknown")
        
        if "function" in message:
            if project_type == "python":
                content = """I'll help you create a Python function! Here's a template:

```python
def your_function_name(parameter1, parameter2):
    \"\"\"
    Brief description of what the function does.
    
    Args:
        parameter1: Description of parameter1
        parameter2: Description of parameter2
        
    Returns:
        Description of return value
    \"\"\"
    # Your implementation here
    result = parameter1 + parameter2  # Example logic
    return result

# Example usage:
# result = your_function_name(5, 10)
# print(result)  # Output: 15
```

Please provide more details about:
1. What should the function do?
2. What parameters does it need?
3. What should it return?"""
            else:
                content = """I'll help you create a function! To provide the best assistance, please tell me:

1. What programming language?
2. What should the function do?
3. What parameters does it need?
4. What should it return?

For example: "Create a JavaScript function that validates email addresses" """
        
        elif "class" in message:
            content = """I'll help you create a class! Here's what I need to know:

1. What programming language?
2. What should the class represent?
3. What properties should it have?
4. What methods does it need?

For example: "Create a Python class for a User with name, email, and login methods" """
        
        else:
            content = f"""I'd be happy to help you create code! 

Based on your workspace, I can see this is a {project_type} project. I can help create:
• Functions and classes
• Configuration files
• Test files
• Documentation
• Scripts and utilities

Please be more specific about what you'd like to create. For example:
"Create a Python function that reads a CSV file"
"Create a React component for a login form" """
        
        return {
            "content": content,
            "references": []
        }
    
    def _generate_fix_response(self, files: List[Dict[str, Any]], message: str) -> Dict[str, Any]:
        """Generate a debugging/fix response."""
        if not files:
            content = """I'd love to help you fix bugs and debug issues! 

To provide the best assistance, please:
1. Include the problematic file: `--file yourfile.py`
2. Describe the specific error or issue
3. Include any error messages you're seeing

Common debugging approaches I can help with:
• Syntax errors and exceptions
• Logic errors and unexpected behavior
• Performance issues
• Code smells and anti-patterns

What specific issue are you encountering?"""
        else:
            file = files[0]
            language = file.get("language", "unknown")
            
            content = f"""I'll help you debug the code in `{file['path']}`!

**Debugging Analysis:**
• File: {file['path']}
• Language: {language.title() if language else 'Unknown'}
• Size: {file.get('size', 0)} bytes

**Common Issues to Check:**
"""
            
            if language == "python":
                content += """• Indentation errors (Python is whitespace-sensitive)
• Missing imports or incorrect module names
• Variable scope issues
• Type-related errors
• Logic errors in conditionals or loops

**Next Steps:**
1. What error message are you seeing?
2. What's the expected vs actual behavior?
3. Can you point to the specific problematic code section?"""
            
            elif language == "javascript":
                content += """• Undefined variables or functions
• Async/await or Promise handling issues
• DOM element not found errors
• Scope and closure problems
• Type coercion issues

**Next Steps:**
1. Check the browser console for error messages
2. What's the expected vs actual behavior?
3. Are there any network or timing issues?"""
            
            else:
                content += f"""• Syntax errors specific to {language}
• Runtime errors and exceptions
• Logic errors in algorithms
• Memory or resource issues

**Next Steps:**
1. What error messages are you seeing?
2. What's the expected behavior?
3. When does the issue occur?"""
        
        return {
            "content": content,
            "references": [f.get("path") for f in files]
        }
    
    def _generate_test_response(self, files: List[Dict[str, Any]], workspace_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a testing response."""
        project_type = workspace_info.get("project_info", {}).get("type", "unknown")
        
        content = f"""I'll help you write tests! 

**Project Type:** {project_type.title() if project_type != 'unknown' else 'Unknown'}
"""
        
        if project_type == "python":
            content += """
**Python Testing Options:**
• `unittest` (built-in)
• `pytest` (popular third-party)
• `doctest` (for documentation examples)

**Example Test Structure:**
```python
import unittest
from your_module import your_function

class TestYourFunction(unittest.TestCase):
    def test_basic_functionality(self):
        result = your_function(input_value)
        self.assertEqual(result, expected_value)
    
    def test_edge_cases(self):
        # Test edge cases here
        pass

if __name__ == '__main__':
    unittest.main()
```"""
        
        elif project_type == "nodejs":
            content += """
**JavaScript Testing Options:**
• Jest (popular choice)
• Mocha + Chai
• Jasmine

**Example Jest Test:**
```javascript
const yourFunction = require('./your-module');

describe('Your Function', () => {
    test('should return expected value', () => {
        const result = yourFunction(inputValue);
        expect(result).toBe(expectedValue);
    });
    
    test('should handle edge cases', () => {
        // Test edge cases here
    });
});
```"""
        
        else:
            content += """
I can help you write tests for various frameworks and languages!

Please tell me:
1. What code do you want to test?
2. What testing framework are you using?
3. What specific scenarios should the tests cover?"""
        
        if files:
            content += f"\n\n**Files to Test:**\n"
            for file in files[:3]:  # Limit to first 3 files
                content += f"• {file['path']} ({file.get('language', 'unknown')})\n"
        
        return {
            "content": content,
            "references": [f.get("path") for f in files]
        }
    
    def _generate_refactor_response(self, files: List[Dict[str, Any]], message: str) -> Dict[str, Any]:
        """Generate a refactoring response."""
        if not files:
            content = """I'd be happy to help you refactor and improve your code!

**Refactoring Areas I Can Help With:**
• Code organization and structure
• Performance optimization
• Readability improvements
• Design pattern implementation
• Code smell elimination
• Function/class extraction

Please include the file you want to refactor:
`python main.py chat "Refactor this code" --file yourfile.py`

What specific improvements are you looking for?"""
        else:
            file = files[0]
            language = file.get("language", "unknown")
            
            content = f"""I'll help you refactor `{file['path']}`!

**Refactoring Analysis:**
• File: {file['path']}
• Language: {language.title() if language else 'Unknown'}
• Size: {file.get('size', 0)} bytes

**Common Refactoring Opportunities:**
"""
            
            if language == "python":
                content += """• Extract long functions into smaller ones
• Use list/dict comprehensions where appropriate
• Apply PEP 8 style guidelines
• Remove code duplication
• Improve variable and function names
• Add type hints for better clarity
• Optimize imports and dependencies"""
            
            elif language == "javascript":
                content += """• Convert to modern ES6+ syntax
• Extract reusable components/functions
• Improve async/await usage
• Optimize DOM manipulations
• Remove unused variables and functions
• Improve error handling
• Apply consistent naming conventions"""
            
            else:
                content += f"""• Extract common functionality
• Improve naming conventions
• Optimize performance bottlenecks
• Enhance error handling
• Improve code organization
• Add documentation and comments"""
            
            content += """

**What would you like to focus on?**
• Performance optimization
• Code readability
• Better structure/organization
• Specific code smells you've noticed"""
        
        return {
            "content": content,
            "references": [f.get("path") for f in files]
        }
    
    def _generate_general_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a general response."""
        workspace_path = context.get("workspace", "current directory")
        
        content = f"""I'm here to help with your development tasks in {workspace_path}!

**Your Message:** {message}

I can assist you with:
• **Code Analysis**: Explain existing code, identify patterns, suggest improvements
• **Code Generation**: Create functions, classes, scripts, and configurations
• **Debugging**: Help find and fix bugs, analyze error messages
• **Testing**: Write unit tests, integration tests, and test strategies
• **Refactoring**: Improve code structure, performance, and readability
• **Documentation**: Generate comments, docstrings, and README files

**To get more specific help, try:**
• Include files: `--file yourfile.py`
• Add workspace context: `--context`
• Be specific about what you want to achieve

**Example commands:**
• `python main.py chat "Explain this function" --file utils.py`
• `python main.py chat "Create a user authentication system" --context`
• `python main.py chat "Fix the bug in login.js" --file login.js`

How can I help you with your code today?"""
        
        return {
            "content": content,
            "references": []
        }
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the current session history.
        
        Returns:
            List of session messages
        """
        return self.session_history.copy()
    
    def clear_session_history(self):
        """Clear the session history."""
        self.session_history.clear()