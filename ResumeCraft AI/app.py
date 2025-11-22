from flask import Flask, render_template, request, send_file
import openai
import pdfkit

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    # Get user input
    name = request.form.get('name')
    email = request.form.get('email')
    education = request.form.get('education')
    experience = request.form.get('experience')
    skills = request.form.get('skills')

    # Optional AI-generated summary
    prompt = f"Write a professional summary for {name}, skills: {skills}, experience: {experience}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    summary = response.choices[0].text.strip()

    # Render resume HTML
    rendered = render_template('resume_template.html', name=name, email=email,
                               education=education, experience=experience,
                               skills=skills, summary=summary)

    # Convert HTML to PDF
    pdfkit.from_string(rendered, 'static/resume.pdf')

    return send_file('static/resume.pdf')

if __name__ == '__main__':
    app.run(debug=True)
