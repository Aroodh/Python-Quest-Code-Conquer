# app.py
import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
from styles import get_styles  # Import CSS from styles.py

# Set page configuration
st.set_page_config(
    page_title="Python Quiz Master",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_styles(), unsafe_allow_html=True)

class Question:
    def __init__(self, prompt, options, correct_answer, explanation, category, difficulty):
        self.prompt = prompt
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.category = category
        self.difficulty = difficulty

class QuizGame:
    def __init__(self, questions):
        self.questions = questions
        self.total_questions = len(questions)
        
        # Initialize session state variables if they don't exist
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'answered' not in st.session_state:
            st.session_state.answered = False
        if 'selected_option' not in st.session_state:
            st.session_state.selected_option = None
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        if 'quiz_completed' not in st.session_state:
            st.session_state.quiz_completed = False
        if 'correct_answers' not in st.session_state:
            st.session_state.correct_answers = []
        if 'time_taken' not in st.session_state:
            st.session_state.time_taken = []
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
        if 'selected_category' not in st.session_state:
            st.session_state.selected_category = "All"
        if 'selected_difficulty' not in st.session_state:
            st.session_state.selected_difficulty = "All"
        if 'username' not in st.session_state:
            st.session_state.username = ""
        if 'filtered_questions' not in st.session_state:
            st.session_state.filtered_questions = questions
            
    def display_welcome(self):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h1 style='color: #2C3E50;'>Python Quiz Master 🧠</h1>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 18px;'>Test your Python knowledge with our interactive quiz!</p>", unsafe_allow_html=True)
            
            # Get username
            username = st.text_input("Enter your name:", value=st.session_state.username)
            if username:
                st.session_state.username = username
            
            # Get all available categories and difficulties
            categories = ["All"] + list(set(q.category for q in self.questions))
            difficulties = ["All"] + list(set(q.difficulty for q in self.questions))
            
            col_cat, col_diff = st.columns(2)
            with col_cat:
                category = st.selectbox("Select Category:", categories, index=categories.index(st.session_state.selected_category))
                st.session_state.selected_category = category
            
            with col_diff:
                difficulty = st.selectbox("Select Difficulty:", difficulties, index=difficulties.index(st.session_state.selected_difficulty))
                st.session_state.selected_difficulty = difficulty
            
            # Filter questions based on selection
            filtered_questions = self.questions
            if category != "All":
                filtered_questions = [q for q in filtered_questions if q.category == category]
            if difficulty != "All":
                filtered_questions = [q for q in filtered_questions if q.difficulty == difficulty]
            
            # Ensure we have questions left after filtering
            if not filtered_questions:
                st.warning("No questions match your selected filters. Please try a different combination.")
                return
            
            st.session_state.filtered_questions = filtered_questions
                
            # Start button
            if not st.session_state.quiz_started:
                if st.button("Start Quiz", use_container_width=True):
                    self.reset_quiz()
                    st.session_state.quiz_started = True
                    st.session_state.start_time = time.time()
            
        with col2:
            st.markdown("""
            <div class="stats-card">
                <h3 style="text-align: center; color: #2C3E50;">Quiz Stats</h3>
                <ul>
                    <li>Questions: {}</li>
                    <li>Categories: {}</li>
                    <li>Difficulty levels: {}</li>
                </ul>
            </div>
            """.format(
                len(st.session_state.filtered_questions),
                len(set(q.category for q in self.questions))-1,
                len(set(q.difficulty for q in self.questions))
            ), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stats-card">
                <h3 style="text-align: center; color: #2C3E50;">How to Play</h3>
                <ol>
                    <li>Enter your name</li>
                    <li>Select category and difficulty</li>
                    <li>Click Start Quiz</li>
                    <li>Answer each question</li>
                    <li>See your results at the end</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    def reset_quiz(self):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.session_state.quiz_completed = False
        st.session_state.correct_answers = []
        st.session_state.time_taken = []
        random.shuffle(st.session_state.filtered_questions)
    
    def display_question(self):
        if st.session_state.current_question < len(st.session_state.filtered_questions):
            question = st.session_state.filtered_questions[st.session_state.current_question]
            
            # Display question number and progress
            progress = (st.session_state.current_question) / len(st.session_state.filtered_questions)
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span class="badge" style="background-color: #6c757d;">Question {st.session_state.current_question + 1}/{len(st.session_state.filtered_questions)}</span>
                <span class="badge" style="background-color: {self.get_difficulty_color(question.difficulty)};">{question.difficulty}</span>
                <span class="badge">{question.category}</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {progress * 100}%;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display question
            st.markdown(f"""
            <div class="question-card">
                <h2 style="color: #2C3E50; margin-bottom: 20px;">{question.prompt}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # If not answered yet, display option buttons
            if not st.session_state.answered:
                question_start_time = time.time()
                
                # Display options as buttons
                for i, option in enumerate(question.options, 1):
                    if st.button(f"{i}. {option}", key=f"option_{i}", use_container_width=True):
                        st.session_state.selected_option = i
                        st.session_state.answered = True
                        
                        # Calculate time taken
                        time_taken = time.time() - question_start_time
                        st.session_state.time_taken.append(time_taken)
                        
                        # Check if answer is correct
                        is_correct = (i == question.correct_answer)
                        st.session_state.correct_answers.append(is_correct)
                        
                        if is_correct:
                            st.session_state.score += 1
                        
                        # Force a rerun to show feedback
                        st.rerun()
            
            # If answered, display feedback
            else:
                selected_option = st.session_state.selected_option
                is_correct = (selected_option == question.correct_answer)
                
                # Display selected option with styling
                for i, option in enumerate(question.options, 1):
                    button_style = ""
                    if i == selected_option:
                        if is_correct:
                            button_style = "background-color: #d4edda; border-color: #c3e6cb;"
                        else:
                            button_style = "background-color: #f8d7da; border-color: #f5c6cb;"
                    elif i == question.correct_answer and not is_correct:
                        button_style = "background-color: #d4edda; border-color: #c3e6cb;"
                    
                    st.markdown(f"""
                    <div class="option-button" style="{button_style}">
                        {i}. {option}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display feedback message
                if is_correct:
                    st.markdown(f"""
                    <div class="feedback-correct">
                        <strong>✓ Correct!</strong> Well done!
                        <p>{question.explanation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="feedback-incorrect">
                        <strong>✗ Incorrect.</strong> The correct answer was: {question.correct_answer}. {question.options[question.correct_answer-1]}
                        <p>{question.explanation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Next question button
                if st.button("Next Question", use_container_width=True):
                    st.session_state.current_question += 1
                    st.session_state.answered = False
                    st.session_state.selected_option = None
                    
                    # Check if the quiz is complete
                    if st.session_state.current_question >= len(st.session_state.filtered_questions):
                        st.session_state.quiz_completed = True
                    
                    # Force a rerun to display next question
                    st.rerun()
    
    def get_difficulty_color(self, difficulty):
        colors = {
            "Easy": "#28a745",
            "Medium": "#ffc107",
            "Hard": "#dc3545"
        }
        return colors.get(difficulty, "#6c757d")
    
    def display_final_result(self):
        # Calculate total time
        total_time = time.time() - st.session_state.start_time
        average_time = sum(st.session_state.time_taken) / len(st.session_state.time_taken) if st.session_state.time_taken else 0
        
        # Calculate score
        score = st.session_state.score
        total = len(st.session_state.filtered_questions)
        percentage = (score / total) * 100
        
        # Display result header
        st.markdown(f"""
        <div class="result-card">
            <h1 style="color: #2C3E50;">Quiz Complete! 🎉</h1>
            <h2>{st.session_state.username or "Player"}'s Results</h2>
            
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {percentage}%;"></div>
            </div>
            
            <h3 style="font-size: 36px; color: #2C3E50;">{score}/{total} ({percentage:.1f}%)</h3>
        """, unsafe_allow_html=True)
        
        # Add feedback based on score
        if percentage >= 80:
            st.markdown("""
            <div style="margin: 20px 0;">
                <h3 style="color: #28a745;">Excellent job! 🏆</h3>
                <p>You're a Python master! Your knowledge is impressive.</p>
            </div>
            """, unsafe_allow_html=True)
        elif percentage >= 60:
            st.markdown("""
            <div style="margin: 20px 0;">
                <h3 style="color: #ffc107;">Good work! 👍</h3>
                <p>You have a solid understanding of Python.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin: 20px 0;">
                <h3 style="color: #dc3545;">Keep practicing! 💪</h3>
                <p>With more study, you'll improve your Python knowledge.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display time statistics
        st.markdown(f"""
            <div style="margin: 20px 0; display: flex; justify-content: center; gap: 20px;">
                <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; min-width: 150px;">
                    <h4>Total Time</h4>
                    <p>{int(total_time // 60)} min {int(total_time % 60)} sec</p>
                </div>
                <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; min-width: 150px;">
                    <h4>Avg. Time per Question</h4>
                    <p>{average_time:.1f} sec</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for statistics charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create performance by category
            if len(set(q.category for q in st.session_state.filtered_questions)) > 1:
                st.markdown("""
                <div class="stats-card">
                    <h3 style="text-align: center; color: #2C3E50;">Performance by Category</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Create dataframe for category performance
                categories = {}
                for i, q in enumerate(st.session_state.filtered_questions):
                    if q.category not in categories:
                        categories[q.category] = {"correct": 0, "total": 0}
                    categories[q.category]["total"] += 1
                    if st.session_state.correct_answers[i]:
                        categories[q.category]["correct"] += 1
                
                # Calculate percentages and create dataframe
                category_data = {
                    "Category": [],
                    "Percentage": []
                }
                for cat, data in categories.items():
                    category_data["Category"].append(cat)
                    category_data["Percentage"].append((data["correct"] / data["total"]) * 100)
                
                df = pd.DataFrame(category_data)
                st.bar_chart(df.set_index("Category"))
        
        with col2:
            # Create performance by difficulty
            if len(set(q.difficulty for q in st.session_state.filtered_questions)) > 1:
                st.markdown("""
                <div class="stats-card">
                    <h3 style="text-align: center; color: #2C3E50;">Performance by Difficulty</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Create dataframe for difficulty performance
                difficulties = {}
                for i, q in enumerate(st.session_state.filtered_questions):
                    if q.difficulty not in difficulties:
                        difficulties[q.difficulty] = {"correct": 0, "total": 0}
                    difficulties[q.difficulty]["total"] += 1
                    if st.session_state.correct_answers[i]:
                        difficulties[q.difficulty]["correct"] += 1
                
                # Calculate percentages and create dataframe
                difficulty_data = {
                    "Difficulty": [],
                    "Percentage": []
                }
                for diff, data in difficulties.items():
                    difficulty_data["Difficulty"].append(diff)
                    difficulty_data["Percentage"].append((data["correct"] / data["total"]) * 100)
                
                df = pd.DataFrame(difficulty_data)
                st.bar_chart(df.set_index("Difficulty"))
        
        # Play again button
        if st.button("Play Again", use_container_width=True):
            self.reset_quiz()
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.rerun()
    
    def run(self):
        if not st.session_state.quiz_started:
            self.display_welcome()
        elif st.session_state.quiz_completed:
            self.display_final_result()
        else:
            self.display_question()

# Create expanded questions with categories and difficulty levels
questions = [
    Question(
        "What is the correct way to create a function in Python?",
        ["function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"],
        2,
        "In Python, functions are defined using the 'def' keyword followed by the function name and parentheses.",
        "Basics",
        "Easy"
    ),
    Question(
        "Which of the following is NOT a valid variable name in Python?",
        ["my_var", "myVar", "2myVar", "_myVar"],
        3,
        "Variable names cannot start with a number in Python.",
        "Basics",
        "Easy"
    ),
    Question(
        "What does the 'len()' function do in Python?",
        ["Calculates the length of a string", "Returns the largest item in a list", "Counts the number of items in a list, tuple, or string", "None of the above"],
        3,
        "The len() function returns the number of items in an object like strings, lists, tuples, etc.",
        "Basics",
        "Easy"
    ),
    Question(
        "What is the output of: print(2 ** 3)?",
        ["6", "8", "5", "Error"],
        2,
        "The ** operator in Python represents exponentiation. 2 raised to the power of 3 equals 8.",
        "Operators",
        "Easy"
    ),
    Question(
        "Which data type is mutable in Python?",
        ["String", "Tuple", "List", "Integer"],
        3,
        "Lists are mutable, meaning they can be changed after creation. Strings, tuples, and integers are immutable.",
        "Data Types",
        "Medium"
    ),
    Question(
        "What is the correct way to import a module named 'mymodule' in Python?",
        ["import mymodule", "include mymodule", "using mymodule", "#include <mymodule>"],
        1,
        "In Python, modules are imported using the 'import' keyword followed by the module name.",
        "Modules",
        "Easy"
    ),
    Question(
        "Which of the following is a correct way to create a list comprehension in Python?",
        ["[x * 2 for x in range(10)]", "list(x * 2 for x in range(10))", "array[x * 2 for x in range(10)]", "All of the above"],
        1,
        "List comprehensions use square brackets and follow the pattern [expression for item in iterable].",
        "Data Structures",
        "Medium"
    ),
    Question(
        "What is the purpose of the '__init__' method in Python classes?",
        ["To initialize class attributes", "To create new instances", "To define class methods", "To delete objects"],
        1,
        "The '__init__' method is called when an object is created and is used to initialize attributes of the class.",
        "OOP",
        "Medium"
    ),
    Question(
        "What is the correct way to catch all exceptions in Python?",
        ["catch(Exception e) { }", "except Exception as e:", "try(Exception e) { }", "catch Exception as e:"],
        2,
        "In Python, 'except Exception as e:' is used to catch all exceptions and store the exception object in variable e.",
        "Error Handling",
        "Medium"
    ),
    Question(
        "What is a decorator in Python?",
        ["A function that takes a function and returns a function", "A class inheritance mechanism", "A type of loop", "A way to format output"],
        1,
        "A decorator is a function that takes another function as an argument, extends its behavior, and returns it.",
        "Advanced",
        "Hard"
    ),
    Question(
        "What is the purpose of 'self' in Python class methods?",
        ["To reference the class itself", "To reference the current instance of the class", "To make the method private", "To reference the parent class"],
        2,
        "In Python class methods, 'self' is a reference to the instance of the class. It's used to access variables and methods belonging to the instance.",
        "OOP",
        "Medium"
    ),
    Question(
        "What is the difference between '==' and 'is' in Python?",
        ["'==' checks for equality of value, 'is' checks for identity", "They are identical in functionality", "'==' is for numbers, 'is' is for strings", "'is' checks for equality of value, '==' checks for identity"],
        1,
        "'==' checks if two objects have the same value, while 'is' checks if two references refer to the same object in memory.",
        "Operators",
        "Medium"
    ),
    Question(
        "What is a generator in Python?",
        ["A function that returns a list", "A function that yields values one at a time", "A class that generates random numbers", "A tool for generating Python code"],
        2,
        "A generator is a function that returns an iterator that yields items one at a time, rather than returning them all at once.",
        "Advanced",
        "Hard"
    ),
    Question(
        "Which of the following is a valid way to create a set in Python?",
        ["{1, 2, 3}", "set([1, 2, 3])", "Both A and B", "Neither A nor B"],
        3,
        "In Python, sets can be created using curly braces {1, 2, 3} or the set() constructor with an iterable.",
        "Data Structures",
        "Medium"
    ),
    Question(
        "What does the 'yield' keyword do in Python?",
        ["Returns a value from a function", "Pauses a function and returns a value", "Ends a function execution", "Creates a new object"],
        2,
        "The 'yield' keyword pauses a function's execution and returns a value, allowing the function to resume from where it left off when called again.",
        "Advanced",
        "Hard"
    )
]

def main():
    game = QuizGame(questions)
    game.run()

if __name__ == "__main__":
    main()