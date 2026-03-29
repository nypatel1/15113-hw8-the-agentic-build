import json
import os

FEEDBACK_FILE = 'data/feedback.json'

class FeedbackSystem:
    def __init__(self, username):
        self.username = username
        self.feedback = self.load_feedback()
    
    def load_feedback(self):
        if not os.path.exists(FEEDBACK_FILE):
            return {}
        try:
            with open(FEEDBACK_FILE, 'r') as f:
                all_feedback = json.load(f)
                return all_feedback.get(self.username, {})
        except (json.JSONDecodeError, IOError):
            return {}
    
    def save_feedback(self):
        all_feedback = {}
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, 'r') as f:
                    all_feedback = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        all_feedback[self.username] = self.feedback
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(all_feedback, f, indent=2)
    
    def get_rating(self, question_id):
        return self.feedback.get(question_id, 'neutral')
    
    def submit_feedback(self, question_id, rating):
        if rating in ['like', 'dislike', 'skip']:
            self.feedback[question_id] = rating
            self.save_feedback()