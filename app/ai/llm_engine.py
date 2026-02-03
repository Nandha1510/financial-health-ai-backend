import google.generativeai as genai
from app.core.config import OPENAI_API_KEY
import json
import os

# Use OPENAI_API_KEY env var as GEMINI_API_KEY for backward compatibility
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

def generate_ai_insights(financial_summary: dict, language="en"):
    """Generate AI insights using Google Gemini API"""
    try:
        prompt = f"""You are a financial analyst expert for SMEs. Analyze this financial data and provide insights in {language.upper()}:

Financial Data:
{json.dumps(financial_summary, indent=2)}

Please provide:
1. Financial Health Assessment (score 0-100)
2. Creditworthiness Analysis
3. Key Financial Risks
4. Cost Optimization Opportunities (top 3)
5. Actionable Next Steps

Be concise and practical for a small business owner."""

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback if API fails
        return generate_fallback_insights(financial_summary, language)

def generate_fallback_insights(financial_summary: dict, language="en"):
    """Fallback insights when API unavailable"""
    health_score = financial_summary.get('health_score', 50)
    risks = financial_summary.get('risks', [])
    
    if language == "hi":
        return f"""वित्तीय स्वास्थ्य विश्लेषण (स्कोर: {health_score}/100):
        
आपकी वर्तमान स्थिति: {'मजबूत' if health_score > 70 else 'औसत' if health_score > 50 else 'कमजोर'}
        
पहचाने गए जोखिम: {', '.join(risks) if risks else 'कोई नहीं'}
        
अनुशंसाएं:
        1. नियमित रूप से वित्तीय मेट्रिक्स ट्रैक करें
        2. प्राप्य खातों को बेहतर करें
        3. लागत अनुकूलन पर ध्यान दें
        """
    else:
        return f"""Financial Health Analysis (Score: {health_score}/100):
        
Current Status: {'Strong' if health_score > 70 else 'Average' if health_score > 50 else 'Weak'}
        
Identified Risks: {', '.join(risks) if risks else 'None'}
        
Recommendations:
        1. Track financial metrics regularly
        2. Improve receivables collection
        3. Focus on cost optimization
        """
