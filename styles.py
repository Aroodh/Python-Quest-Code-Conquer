# styles.py

def get_styles():
    """Returns the CSS styles as a string."""
    return """
    <style>
        .main {
            background-color: #f5f7f9;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .question-card {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .option-button {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            background-color: #f0f2f6;
            border: 1px solid #dfe1e5;
            text-align: left;
            transition: all 0.3s;
        }
        .option-button:hover {
            background-color: #e2e5e9;
            transform: translateY(-2px);
        }
        .feedback-correct {
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .feedback-incorrect {
            background-color: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .result-card {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .progress-bar-bg {
            height: 10px;
            background-color: #e9ecef;
            border-radius: 5px;
            margin: 20px 0;
        }
        .progress-bar-fill {
            height: 10px;
            background-color: #4CAF50;
            border-radius: 5px;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            background-color: #17a2b8;
            color: white;
            margin: 5px;
        }
        .stats-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
    </style>
    """