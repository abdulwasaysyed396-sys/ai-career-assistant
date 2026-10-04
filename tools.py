def calculator(expression):
    """
    Safely calculate a basic mathematical expression.
    """

    allowed_characters = "0123456789+-*/(). "

    # Check that the expression contains only allowed characters
    if not all(
        character in allowed_characters
        for character in expression
    ):
        return "Invalid mathematical expression."

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "Could not calculate the expression."


def generate_interview_topics(topic):
    """
    Generate interview topics based on the selected topic.
    """

    topics = {
        "python": [
            "Variables and data types",
            "Lists, tuples and dictionaries",
            "Functions",
            "Object-oriented programming",
            "Exception handling"
        ],

        "sql": [
            "SELECT queries",
            "WHERE clause",
            "JOINs",
            "GROUP BY",
            "Subqueries"
        ],

        "machine learning": [
            "Supervised learning",
            "Unsupervised learning",
            "Train-test split",
            "Overfitting",
            "Model evaluation"
        ]
    }

    # Convert the user's topic to lowercase
    topic = topic.lower()

    # Return matching topics
    if topic in topics:
        return topics[topic]

    # Default topics if the topic isn't in our list
    return [
        "Programming fundamentals",
        "Data structures",
        "Algorithms",
        "Problem solving",
        "Basic system concepts"
    ]