from flask import Flask, request, jsonify
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os

app = Flask(__name__)

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    task_input = data.get('task', '')

    analyst = Agent(
        role='محلل المنتج',
        goal='تحليل المنتج وتحديد فرص النجاح',
        backstory='خبير في تحليل منتجات CPA والتجارة الإلكترونية',
        llm=llm,
        verbose=True
    )

    critic = Agent(
        role='الناقد',
        goal='اكتشاف الأخطاء والمشاكل المحتملة',
        backstory='خبير في تحديد مخاطر حملات CPA',
        llm=llm,
        verbose=True
    )

    strategist = Agent(
        role='الاستراتيجي',
        goal='بناء استراتيجية إعلانية كاملة',
        backstory='خبير في إعلانات Meta وCPA',
        llm=llm,
        verbose=True
    )

    task1 = Task(
        description=f'حلل هذا المنتج: {task_input}',
        agent=analyst,
        expected_output='تحليل شامل للمنتج'
    )

    task2 = Task(
        description='انتقد التحليل واكتشف الأخطاء',
        agent=critic,
        expected_output='قائمة بالمشاكل والمخاطر'
    )

    task3 = Task(
        description='بناء استراتيجية إعلانية نهائية بناءً على التحليل والنقد',
        agent=strategist,
        expected_output='استراتيجية إعلانية كاملة جاهزة للتنفيذ'
    )

    crew = Crew(
        agents=[analyst, critic, strategist],
        tasks=[task1, task2, task3],
        verbose=True
    )

    result = crew.kickoff()
    return jsonify({'result': str(result)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get
