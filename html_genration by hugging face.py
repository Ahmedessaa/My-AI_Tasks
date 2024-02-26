from transformers import pipeline

def analyze_sentiment_and_generate_html(text):

    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)
    sentiment_score = result[0]['score']

  
    sentiment_label = "Positive" if sentiment_score >= 0.5 else "Negative"

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{text}</title>
    </head>
    <body>
        <h1>{text}</h1>
        <p>{text}</p>

    </body>
    </html>
    """

    with open('sentiment_analysis_result.html', 'w') as file:
        file.write(html_content)

    print("HTML file 'sentiment_analysis_result.html' created successfully.")

if __name__ == "__main__":
    user_input = input("Enter the text : ")

    # Analyze sentiment and generate HTML file
    analyze_sentiment_and_generate_html(user_input)
