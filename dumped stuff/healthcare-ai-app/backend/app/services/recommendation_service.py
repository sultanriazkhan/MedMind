import openai
import json
import os

class RecommendationService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_diet_plan(self, profile_data, report_data=None):
        prompt = f"""
        Generate a 7-day personalized meal plan based on:
        Age: {profile_data.get('age')}
        Sex: {profile_data.get('sex')}
        Weight: {profile_data.get('weight')}kg
        Height: {profile_data.get('height')}cm
        Activity Level: {profile_data.get('activity_level')}
        Conditions: {', '.join(profile_data.get('conditions', []))}
        Dietary Restrictions: {', '.join(profile_data.get('dietary_restrictions', []))}
        Goals: {', '.join(profile_data.get('goals', []))}
        Report Insights: {json.dumps(report_data) if report_data else 'None'}
        
        Return as JSON with structure: 
        {{
            "weekly_plan": [
                {{
                    "day": "Monday",
                    "meals": {{
                        "breakfast": "string",
                        "lunch": "string",
                        "dinner": "string",
                        "snacks": "string"
                    }}
                }}
            ],
            "foods_to_eat": ["list"],
            "foods_to_avoid": ["list"],
            "nutritional_rationale": "string"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_exercise_plan(self, profile_data):
        prompt = f"""
        Create a weekly exercise plan for someone with:
        Age: {profile_data.get('age')}
        Activity Level: {profile_data.get('activity_level')}
        Conditions: {', '.join(profile_data.get('conditions', []))}
        Goals: {', '.join(profile_data.get('goals', []))}
        
        Return JSON: {{
            "weekly_schedule": [
                {{
                    "day": "Monday",
                    "activities": [
                        {{
                            "type": "string",
                            "duration": "minutes",
                            "intensity": "low/medium/high",
                            "frequency": "string"
                        }}
                    ]
                }}
            ],
            "safety_warnings": ["list"],
            "exercise_library": [
                {{
                    "name": "string",
                    "type": "string",
                    "benefits": "string",
                    "instructions": "string"
                }}
            ]
        }}
        """
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_lifestyle_recommendations(self, profile_data, report_data=None):
        prompt = f"""
        Generate lifestyle recommendations based on:
        Profile: {json.dumps(profile_data)}
        Health Report: {json.dumps(report_data) if report_data else 'None'}
        
        Return JSON array of recommendations with:
        - title, description, priority (high/medium/low), category (diet/exercise/lifestyle)
        """
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7
        )
        
        return json.loads(response.choices[0].message.content)