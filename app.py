from flask import Flask, render_template, request
import json
import os


app = Flask(__name__)

questions = [
        {
        'question': '12 x 15',
        'answer': '180'
    },
    {
        'question': '23 / 5',
        'answer': '4.6'
    },
    {
        'question': '356 + 179',
        'answer': '535'
    },
    {
        'question': 'Simplify √98',
        'answer': '7√2'
    },
    {
        'question': '16 + 54 x ... - 24 = 262',
        'answer': '5'
    },
    {
        'question': 'If 4x + 25 = 60, find x',
        'answer': '8.75'
    },
    {
        'question': 'Convert 54/8 to decimal form',
        'answer': '6.75'
    },
    {
        'question': 'What is the next number? 2, 6, 12, 20, 30, ....',
        'answer': '42'
    },
    {
        'question': 'Simplify (3² + 4²)½',
        'answer': '5'
    },
    {
        'question': '2(3x - 4) + 5 = 25',
        'answer': '4'
    }
]

# halaman utama
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        username = request.form['username']
        return render_template(
            'quiz.html',
            username=username,
            questions=questions
        )

    return render_template('index.html')

# GET = buka halaman
# POST = kirim data form

# request.method = usser sedang membuka / submit form?

# halaman result
@app.route('/result', methods=['POST'])
def result():

    username = request.form['username']
# request form = ambil dari HTML form

    score = 0

# Pembetulan
    wrong_answers = []

    # Hitung Score
    for index, item in enumerate(questions, start=1):
        user_answer = request.form[f'answer{index}']

        if user_answer.strip().lower() == item['answer'].lower():
            score += 1
        
        else:
            wrong_answers.append({
                'question': item['question'],
                'your_answer': user_answer,
                'correct_answer': item['answer']
            })
    
    # Data User
    data = {
        'username': username,
        'score': score
    }

    # Lokasi data.json
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'data.json')

    # Cek file JSON
    if os.path.exists(file_path):

        with open(file_path, 'r') as file:
            try:
                all_data = json.load(file)
            except:
                all_data = []
    else:
        all_data = []

    # Tambah data baru
    all_data.append(data)

    # Simpan Kembali
    with open(file_path, 'w') as file:
        json.dump(all_data, file, indent=4)

    # Ranking system
    def get_score(x):
        return x.get('score', 0)
    
    sorted_data = sorted(
        all_data,
        key=get_score,
        reverse=True
    )

    # Tampilkan Hasil
    return render_template(
        'result.html',

        username=username,
        score=score,
        ranking=sorted_data[:3],
        wrong_answers=wrong_answers
    )
    
if __name__ == '__main__':
    app.run(debug=True)

