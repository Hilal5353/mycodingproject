from celery import shared_task


from .models import Ai_todo_steps, Todo
import ollama
from django.contrib.auth.models import User

@shared_task
def generate_todo_steps(task, user_id):
    ai_todosteps = Ai_todo_steps(steps=[])
    prompth = f"""
    You are a friendly and helpful assistant inside a to-do app.

    Your job:
    - Break the user’s task into 3 to 7 simple, actionable steps.
    - Use plain, clear, and positive language anyone can understand.
    - If the task is complicated, gently encourage and motivate the user.
    - Offer helpful tips or reminders when appropriate (e.g., suggest to take breaks or prioritize).
    - Avoid unnecessary explanations or extra text.
    - Return ONLY valid JSON — no code blocks, markdown, or extra words.
    - If the task seems unclear or too vague, provide clear steps based on the most likely meaning.
    - Keep the tone supportive and patient, as if guiding a beginner.
    - Do not assume prior knowledge; keep it accessible to everyone.
    - Use consistent formatting and punctuation for readability.

    Format:
    {ai_todosteps.model_dump_json(indent=4)}

    Task: "{task}"
    """

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompth}]
    )
    content = response["message"]["content"]
    ai_todo_steps = Ai_todo_steps.model_validate_json(content)
    user = User.objects.get(id=user_id)
    new_todo = Todo(user=user, todo_name=task, steps=ai_todo_steps.steps)
    new_todo.save()
