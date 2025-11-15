from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from io import BytesIO
import tempfile

from src.agent.chat_manager import run_chat_agent
from src.agent.speech_module import tts_generate, transcribe_local_file
from src.utils.agent_utils import serialize_message, allowed_file
from src.utils.tracing_setup import setup_tracing
from src.models.genre_predictor import GenrePredictor
from src.models.plot_summarizer import PlotSummarizer


app = Flask(__name__, template_folder='templates', static_folder='static')
sessions = {}  # In-memory session storage

# Initialize models
print("Loading ML models...")
genre_predictor = GenrePredictor(model_path='models/distilbert_genre_classifier')
plot_summarizer = PlotSummarizer()
print(" Models loaded successfully!")

# Setup databases if not present
def setup_databases():
    vector_db_exists = os.path.exists("data/vector_store/faiss_index")
    if not vector_db_exists:
        print("[WARN] Vector DB not found. Building vector database...")
        try:
            from src.builders.build_vectorstore import build as build_vector_db
            build_vector_db()
            print("[SUCCESS] Vector database built successfully!")
        except Exception as e:
            print(f"[ERROR] Error building vector database: {e}")


# MAIN PAGE - Landing page with navigation

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/chatbot')
def chat_page():
    return render_template('chat.html')



@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json or {}
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        debug_mode = data.get('debug', False)

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Manage session and thread IDs
        thread_id = sessions.setdefault(session_id, str(uuid.uuid4()))

        if debug_mode:
            response_data = run_chat_agent(user_message, thread_id, return_full_response=True)
            full_resp = [serialize_message(msg) for msg in response_data['full_response'].get("messages", [])]
            return jsonify({
                'response': response_data['display_response'],
                'full_response': {'messages': full_resp},
                'session_id': session_id
            })

        response, _ = run_chat_agent(user_message, thread_id)
        return jsonify({'response': response, 'session_id': session_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/chat/voice', methods=['POST'])
def chat_voice():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        if not allowed_file(audio_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        session_id = request.form.get('session_id', str(uuid.uuid4()))
        debug_mode = request.form.get('debug', 'false').lower() == 'true'

        # Save audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{secure_filename(audio_file.filename)}") as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        try:
            user_message = transcribe_local_file(tmp_path)
            thread_id = sessions.setdefault(session_id, str(uuid.uuid4()))

            if debug_mode:
                response_data = run_chat_agent(user_message, thread_id, return_full_response=True)
                full_resp = [serialize_message(msg) for msg in response_data['full_response'].get("messages", [])]
                response_text = response_data['display_response']
            else:
                response_text, _ = run_chat_agent(user_message, thread_id)
                full_resp = []

            tts_generate(response_text)

            return jsonify({
                'transcription': user_message,
                'response': response_text,
                'session_id': session_id,
                'full_response': {'messages': full_resp} if debug_mode else None,
                'has_audio': True
            })

        finally:
            os.remove(tmp_path)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        text = (request.json or {}).get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        audio_bytes = tts_generate(text)
        return send_file(BytesIO(audio_bytes), mimetype='audio/mpeg', as_attachment=False)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/new-session', methods=['POST'])
def new_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = str(uuid.uuid4())
    return jsonify({'session_id': session_id})


# GENRE PREDICTION ROUTES
@app.route('/genre-prediction')
def genre_prediction_page():
    return render_template('genre_prediction.html')


@app.route('/api/predict-genre', methods=['POST'])
def predict_genre():
    try:
        data = request.json or {}
        plot = data.get('plot', '').strip()
        
        if not plot:
            return jsonify({'error': 'No plot provided'}), 400
        
        if len(plot) < 20:
            return jsonify({'error': 'Plot too short. Please provide at least 20 characters.'}), 400
        
        result = genre_predictor.predict(plot)
        
        return jsonify({
            'success': True,
            'genres': result['genres'],
            'probabilities': result['probabilities'],
            'top_genres': result['top_genres'],
            'plot_length': len(plot)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/genre-info', methods=['GET'])
def genre_info():
    try:
        info = genre_predictor.get_genre_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# PLOT SUMMARIZATION ROUTES

@app.route('/plot-summarizer')
def plot_summarizer_page():
    return render_template('plot_summarizer.html')


@app.route('/api/summarize-plot', methods=['POST'])
def summarize_plot():
    try:
        data = request.json or {}
        plot = data.get('plot', '').strip()
        
        if not plot:
            return jsonify({'error': 'No plot provided'}), 400
        
        if len(plot) < 50:
            return jsonify({'error': 'Plot too short. Please provide at least 50 characters.'}), 400
        
        summary = plot_summarizer.summarize(plot)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'original_length': len(plot),
            'summary_length': len(summary)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500






if __name__ == '__main__':
    setup_tracing()
    setup_databases()
    app.run(debug=False, host='0.0.0.0', port=8001)