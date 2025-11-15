
import torch
import numpy as np
import joblib
import json
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class GenrePredictor:

    def __init__(self, model_path):
  
        self.model_path = model_path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        print(f"Loading model on {self.device.upper()}...")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        # Load MultiLabelBinarizer
        mlb_path = os.path.join(os.path.dirname(model_path), 'mlb_encoder.pkl')
        self.mlb = joblib.load(mlb_path)
        
        # Load genre info
        info_path = os.path.join(os.path.dirname(model_path), 'genre_info.json')
        with open(info_path, 'r') as f:
            self.genre_info = json.load(f)
        
        self.max_length = self.genre_info.get('max_sequence_length', 2000)
        
        print(f" Model loaded successfully!")
        print(f"   - {len(self.mlb.classes_)} genres")
        print(f"   - Max sequence length: {self.max_length} chars")
    
    def predict(self, plot_text, threshold=0.5, top_k=5):

        # Truncate text if too long
        plot_text = plot_text[:self.max_length]
        
        # Tokenize
        inputs = self.tokenizer(
            plot_text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors='pt'
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits).cpu().numpy()[0]
        
        # Get genres above threshold
        predicted_indices = np.where(probabilities >= threshold)[0]
        predicted_genres = [self.mlb.classes_[i] for i in predicted_indices]
        predicted_probs = [float(probabilities[i]) for i in predicted_indices]
        
        # Get top K genres by probability
        top_indices = np.argsort(probabilities)[-top_k:][::-1]
        top_genres = [
            {
                'genre': self.mlb.classes_[i],
                'probability': float(probabilities[i]),
                'confidence': self._get_confidence_level(probabilities[i])
            }
            for i in top_indices
        ]
        
        return {
            'genres': predicted_genres,
            'probabilities': predicted_probs,
            'top_genres': top_genres,
            'all_probabilities': {
                genre: float(prob) 
                for genre, prob in zip(self.mlb.classes_, probabilities)
            }
        }
    
    
    def _get_confidence_level(self, probability):
        """Get human-readable confidence level"""
        if probability >= 0.8:
            return "Very High"
        elif probability >= 0.6:
            return "High"
        elif probability >= 0.4:
            return "Medium"
        elif probability >= 0.2:
            return "Low"
        else:
            return "Very Low"
    
