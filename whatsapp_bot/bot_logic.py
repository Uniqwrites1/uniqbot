import requests
import json
import logging
import re
from django.conf import settings
from .models import UserSession

logger = logging.getLogger(__name__)

class SmartIntentRecognizer:
    """Intelligent intent recognition for Uniqwrites educational services"""
    
    def __init__(self):
        # Define intent patterns with keywords and phrases
        self.intent_patterns = {
            # Service-related intents
            'tutoring_inquiry': [
                'tutor', 'tutoring', 'home tutoring', 'one on one', 'group tutoring',
                'homework help', 'assignment', 'study help', 'private teacher',
                'math tutor', 'english tutor', 'science tutor', 'subject help'
            ],
            
            'exam_prep': [
                'exam', 'examination', 'test prep', 'sat', 'igcse', 'waec', 'neco', 'jamb',
                'exam preparation', 'test preparation', 'standardized test', 'exam coaching'
            ],
            
            'homeschooling': [
                'homeschool', 'home school', 'home education', 'home learning',
                'structured learning', 'personalized education', 'home curriculum'
            ],
            
            'teacher_recruitment': [
                'hire teacher', 'recruit teacher', 'need teacher', 'find teacher',
                'school staffing', 'teacher vacancy', 'qualified teacher', 'professional teacher'
            ],
            
            'school_services': [
                'digital transformation', 'school management system', 'edtech', 'school software',
                'admin automation', 'school technology', 'management system'
            ],
            
            'teacher_resources': [
                'teacher training', 'teaching resources', 'free resources', 'teacher development',
                'teaching materials', 'educator training', 'teaching skills'
            ],
            
            # Program-related intents
            'pap_interest': [
                'purpose action point', 'pap program', 'pap', 'career guidance', 'life coaching',
                'purpose discovery', 'mentorship program', '9 month program', 'life skills'
            ],
            
            'literacy_initiative': [
                'literacy', 'reading program', 'literacy outreach', 'reading workshop',
                'literacy immersion', 'reading skills', 'literacy support', 'literacy programs',
                'reading help', 'struggling reader', 'children reading', 'reading assistance'
            ],
            
            'back_to_school': [
                'back to school', 'school supplies', 'out of school', 'dropout', 'return to school',
                'school support', 'educational support', 'back to learning'
            ],
            
            'volunteer_interest': [
                'volunteer', 'volunteering', 'help out', 'contribute', 'give back',
                'community service', 'support initiative', 'get involved'
            ],
            
            'sponsor_interest': [
                'sponsor', 'donate', 'funding', 'financial support', 'sponsorship',
                'support financially', 'contribute money', 'fund initiative'
            ],
            
            # Support and information intents
            'pricing_inquiry': [
                'price', 'cost', 'fee', 'payment', 'charges', 'how much', 'pricing',
                'rates', 'tuition', 'affordable', 'budget'
            ],
            
            'schedule_inquiry': [
                'schedule', 'time', 'when', 'available', 'timing', 'hours',
                'appointment', 'session time', 'class time'
            ],
            
            'location_inquiry': [
                'location', 'where', 'address', 'area', 'region', 'city', 'place',
                'physical location', 'office', 'center'
            ],
            
            'general_info': [
                'about', 'information', 'what is', 'tell me about', 'explain',
                'details', 'more info', 'description'
            ],
            
            'complaint_concern': [
                'problem', 'issue', 'complaint', 'not working', 'dissatisfied',
                'trouble', 'difficulty', 'concern', 'frustration'
            ],
            
            'greeting': [
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
                'greetings', 'howdy', 'what\'s up', 'how are you'
            ]
        }
        
        # Intent priorities (higher number = higher priority)
        self.intent_priorities = {
            'exam_prep': 9,
            'tutoring_inquiry': 8,
            'teacher_recruitment': 8,
            'pap_interest': 7,
            'homeschooling': 7,
            'volunteer_interest': 6,
            'sponsor_interest': 6,
            'school_services': 6,
            'teacher_resources': 5,
            'literacy_initiative': 5,
            'back_to_school': 5,
            'pricing_inquiry': 4,
            'schedule_inquiry': 3,
            'location_inquiry': 3,
            'complaint_concern': 8,  # High priority for issues
            'general_info': 2,
            'greeting': 1
        }

    def detect_intent(self, message):
        """Detect user intent from message with confidence scoring"""
        message_lower = message.lower().strip()
        
        # Remove punctuation and extra spaces
        cleaned_message = re.sub(r'[^\w\s]', ' ', message_lower)
        cleaned_message = re.sub(r'\s+', ' ', cleaned_message).strip()
        
        intent_scores = {}
        
        # Score each intent based on keyword matches
        for intent, keywords in self.intent_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in cleaned_message:
                    # Exact phrase match gets higher score
                    if len(keyword.split()) > 1:
                        score += 3
                    else:
                        score += 1
                        
                    # Bonus for multiple keyword matches
                    if score > 1:
                        score += 0.5
            
            if score > 0:
                # Apply intent priority weighting
                priority_weight = self.intent_priorities.get(intent, 1)
                intent_scores[intent] = score * (priority_weight * 0.1 + 1)
        
        # Return the highest scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 5.0, 1.0)  # Normalize to 0-1
            
            logger.info(f"Intent detected: {best_intent} (confidence: {confidence:.2f})")
            return best_intent, confidence
        
        return 'unknown', 0.0

    def get_contextual_response(self, intent, confidence, user_role=None):
        """Generate contextual response based on detected intent"""
        
        if confidence < 0.3:
            return None  # Low confidence, use default flow
        
        responses = {
            'tutoring_inquiry': {
                '2': """🎓 Perfect! We offer comprehensive tutoring services:
                
✨ One-on-One & Group Tutoring
✨ Virtual & Physical Lessons  
✨ Homework Help
✨ All subjects covered

Ready to find the perfect tutor for your child?
👉 Fill this form: https://forms.gle/eTkf1N9qrKZyNJr4A

Or type 'menu' to see all our services.""",

                'default': """🎓 Great! We provide excellent tutoring services:

📚 Home Tutoring (One-on-One & Group)
💻 Virtual & Physical Lessons
📝 Homework Help  
📊 All subjects available

Are you a parent looking for a tutor? Type '2'
Are you a student needing help? Type '3'

Or visit: https://forms.gle/eTkf1N9qrKZyNJr4A"""
            },
            
            'exam_prep': {
                'default': """🎯 Excellent! We specialize in exam preparation:

📋 Supported Exams:
• SAT, IGCSE, WAEC, NECO, JAMB
• Comprehensive coaching with proven strategies
• Personalized study plans
• Top scores guaranteed approach

Ready to excel in your exams?
👉 Request exam prep: https://forms.gle/eTkf1N9qrKZyNJr4A

Type 'menu' for more options."""
            },
            
            'teacher_recruitment': {
                '6': """🏫 Perfect! We help schools find qualified teachers:

✅ Trained professionals
✅ Easy hiring process  
✅ Quality assurance
✅ Quick turnaround

Ready to hire excellent teachers?
👉 Request teachers: https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487

We also offer:
• Digital transformation
• School management systems
• EdTech consultation""",

                'default': """🏫 We help schools find qualified teachers!

Are you a school administrator? Type '6' 
Are you a teacher looking for opportunities? Type '1'

Or directly request teachers:
👉 https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487"""
            },
            
            'pap_interest': {
                'default': """🌟 Amazing! Purpose Action Point (PAP) is transformative:

🎯 9-month life-shaping program for high school graduates

What you'll gain:
✨ Align Passion with Purpose  
🔍 Discover Your Unique Identity
💪 Develop Essential Life Skills
📚 Fill Learning Gaps
🚀 Prepare for Real-Life Challenges

🌟 Status: Coming Soon!

Stay tuned for this life-changing opportunity.
Type 'menu' to explore other services."""
            },
            
            'volunteer_interest': {
                'default': """🤝 Thank you for your heart of service!

Join our impactful initiatives:
📚 Literacy Immersion Outreach  
🎒 Back-to-School Initiative

Make a difference in young lives today:
👉 Volunteer here: https://docs.google.com/forms/d/e/1FAIpQLSeOp7MqoaTPE4Rvi_22VwLX_v4dbR62EIJcP8N3FtZWMk0leQ/viewform?usp=sharing&ouid=116162016347061818487

Every child deserves a chance to learn! 💖"""
            },
            
            'sponsor_interest': {
                'default': """💎 Thank you for your generosity!

Support our life-changing initiatives:
📖 Literacy programs for struggling readers
🎒 Back-to-school support for disadvantaged children
🌟 Educational transformation across communities

Your sponsorship creates lasting impact:
👉 Sponsor here: https://docs.google.com/forms/d/e/1FAIpQLSeX_9GAHJB22l_1-OAN08avlW_fxRR1HIlAO_SxvNH9HF4fWg/viewform?usp=sharing&ouid=116162016347061818487

Together, we're changing lives! ✨"""
            },
            
            'pricing_inquiry': {
                'default': """💰 Great question! Our pricing is competitive and value-focused.

For specific pricing information:
🎓 Tutoring rates vary by subject and format
🏫 School services are customized per needs  
📚 Many teacher resources are FREE

Get personalized pricing:
👉 Parents: https://forms.gle/eTkf1N9qrKZyNJr4A
👉 Schools: https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487

Or speak to a human agent - type '14'"""
            },
            
            'complaint_concern': {
                'default': """😔 I'm sorry to hear about your concern.

Your feedback is important to us. Let me connect you with a human agent who can address this properly.

👨‍💼 A human agent will connect with you shortly. Please hold on...

In the meantime, you can also:
• Type 'menu' to explore our services
• Share more details about your concern"""
            }
        }
        
        # Get role-specific response or default
        intent_responses = responses.get(intent, {})
        response = intent_responses.get(user_role, intent_responses.get('default'))
        
        return response

# Bot responses dictionary
BOT_RESPONSES = {
    "greeting": """👋 Welcome to Uniqwrites Educational Platform!
We're redefining education through tutoring, teacher empowerment, and transformation programs.

Before we continue, please tell us who you are:
1️⃣ Teacher
2️⃣ Parent/Guardian
3️⃣ Student
4️⃣ Volunteer
5️⃣ Sponsor
6️⃣ School Admin
7️⃣ Help
""",

    # --- ROLE SELECTION ---
    "1": """🎉 Great! Welcome, Teacher 👩‍🏫.
Please complete this form to get started:
👉 https://forms.gle/qNpJqTf5f8aiEZa57
""",

    "2": """🌟 Wonderful! We're excited to support your child's learning journey.
Please complete this quick form to begin:
👉 https://forms.gle/eTkf1N9qrKZyNJr4A
""",

    "3": """💡 Amazing! Welcome, future scholar.
Please fill in this form so we can tailor your learning experience:
👉 https://forms.gle/dGQ6G6KZzoycS1n67
""",

    "4": """🤝 Thank you for your heart of service.
Please share your details here so we can connect you with the right initiative:
👉 https://docs.google.com/forms/d/e/1FAIpQLSeOp7MqoaTPE4Rvi_22VwLX_v4dbR62EIJcP8N3FtZWMk0leQ/viewform?usp=sharing&ouid=116162016347061818487
""",

    "5": """💎 Thank you for your generosity!
Please fill in this sponsorship form to partner with us:
👉 https://docs.google.com/forms/d/e/1FAIpQLSeX_9GAHJB22l_1-OAN08avlW_fxRR1HIlAO_SxvNH9HF4fWg/viewform?usp=sharing&ouid=116162016347061818487
""",

    "6": """🏫 Wonderful! Let's help you transform your school.
Please complete this form to get started:
👉 https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487
""",

    # --- HELP MENU ---
    "7": """📚 Here's what I can help you with:

11 Learn about our Mission, Vision & Values
12 Explore our Initiatives
13 Our Services
14 Speak to a Human Agent

Type 'back' to return to main menu
""",

    # --- HELP SUBMENU ---
    "11": """🌟 Our Mission
Empowering learners, uplifting educators. We make education personalized, inclusive, and accessible through innovative digital solutions, ensuring every learner excels and every educator thrives.

👁️ Our Vision
To make learning accessible to all by empowering students and educators through technology, personalization, and strong relationships. Uniqwrites—Education with You in Mind.

💎 Our Values
- Redefining Perspectives: Impossibility is a perspective so we redefine it.
- Activating Potential: Possibilities are rooted in potential. So we activate it.
- Facilitating Growth: Growth is the process, so we embrace it.
- Creating Lasting Impact: We foster joy, success, and fulfillment through education.

👥 Our Team
We are real people from diverse backgrounds, united by passion for transforming learning into a personalized and impactful experience.

Type 'back' to return to help menu or 'menu' for main menu
""",

    "12": """📌 Our Initiatives

✨ Literacy Immersion Outreach
We tackle literacy barriers in public secondary schools through immersive programs, workshops, and resources. Inspired by our founder's journey from struggling reader to top student, we aim to ensure no child's potential is limited by literacy challenges.

✨ Back-to-School Initiative
A rescue mission for lost dreams—helping out-of-school children return to classrooms. We provide mentorship, tutoring, and financial aid to turn streets back into pathways of education.

👉 Volunteer: https://docs.google.com/forms/d/e/1FAIpQLSeOp7MqoaTPE4Rvi_22VwLX_v4dbR62EIJcP8N3FtZWMk0leQ/viewform?usp=sharing&ouid=116162016347061818487
👉 Sponsor: https://docs.google.com/forms/d/e/1FAIpQLSeX_9GAHJB22l_1-OAN08avlW_fxRR1HIlAO_SxvNH9HF4fWg/viewform?usp=sharing&ouid=116162016347061818487

Type 'back' to return to help menu or 'menu' for main menu
""",

    "13": """🛠 Our Services

👨‍👩‍👧 For Parents/Guardians
- Home Tutoring (1-on-1 & group, online & physical)
- Homework Help
- Homeschooling
- Exam Prep (SAT, IGCSE, WAEC, NECO, JAMB & more)
👉 Request a Tutor: https://forms.gle/eTkf1N9qrKZyNJr4A

🏫 For Schools
- Request Teachers
- Digital Transformation
- School Management System
- EdTech Tools Consultation
👉 Request Services: https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487

👩‍🏫 For Teachers
- Access Free Resources
- Professional Training
- Secure Dignified Job Opportunities
- Join a Purpose-Driven Community
👉 Become a Tutor: https://forms.gle/qNpJqTf5f8aiEZa57

Type 'back' to return to help menu or 'menu' for main menu
""",

    "14": """👨‍💼 A human agent will connect with you shortly. Please hold on…"""
}

class WhatsAppBot:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.intent_recognizer = SmartIntentRecognizer()

    def process_message(self, phone_number, message):
        """Enhanced message processing with smart intent recognition"""
        try:
            session, created = UserSession.objects.get_or_create(
                phone_number=phone_number,
                defaults={'current_state': 'greeting'}
            )
        except Exception as db_error:
            logger.error(f"Database error, using stateless mode: {str(db_error)}")
            return self._process_message_stateless(phone_number, message)
        
        message_lower = message.lower().strip()
        
        # First, check for smart intent recognition (unless it's a menu navigation)
        if not message_lower.isdigit() and message_lower not in ['back', 'menu', 'start', 'main', 'help']:
            intent, confidence = self.intent_recognizer.detect_intent(message)
            
            if confidence > 0.4:  # High confidence threshold
                logger.info(f"Smart intent detected: {intent} (confidence: {confidence:.2f})")
                
                # Get contextual response
                smart_response = self.intent_recognizer.get_contextual_response(
                    intent, confidence, session.user_role
                )
                
                if smart_response:
                    # Update session with detected intent
                    session.last_intent = intent
                    session.intent_confidence = confidence
                    session.save()
                    return smart_response
        
        # Handle back navigation
        if message_lower == 'back':
            if session.current_state == 'help_submenu':
                session.current_state = 'help_menu'
                session.save()
                return BOT_RESPONSES["7"]
            else:
                session.current_state = 'greeting'
                session.save()
                return BOT_RESPONSES["greeting"]
        
        # Handle menu navigation
        if message_lower in ['menu', 'start', 'main']:
            session.current_state = 'greeting'
            session.save()
            return BOT_RESPONSES["greeting"]
        
        # Handle help commands
        if message_lower in ['help', '7']:
            session.current_state = 'help_menu'
            session.save()
            return BOT_RESPONSES["7"]
        
        # Handle main menu options (1-6)
        if message_lower in ['1', '2', '3', '4', '5', '6']:
            session.current_state = 'role_selected'
            session.user_role = message_lower
            session.save()
            return BOT_RESPONSES[message_lower]
        
        # Handle help submenu options (11-14)
        if message_lower in ['11', '12', '13', '14']:
            session.current_state = 'help_submenu'
            session.save()
            return BOT_RESPONSES[message_lower]
        
        # Handle text alternatives
        text_mappings = {
            'teacher': '1',
            'parent': '2', 'guardian': '2',
            'student': '3',
            'volunteer': '4',
            'sponsor': '5',
            'admin': '6', 'school admin': '6',
            'mission': '11', 'vision': '11', 'values': '11',
            'initiatives': '12',
            'services': '13',
            'human': '14', 'agent': '14'
        }
        
        if message_lower in text_mappings:
            mapped_option = text_mappings[message_lower]
            if mapped_option in ['1', '2', '3', '4', '5', '6']:
                session.current_state = 'role_selected'
                session.user_role = mapped_option
                session.save()
                return BOT_RESPONSES[mapped_option]
            else:
                session.current_state = 'help_submenu'
                session.save()
                return BOT_RESPONSES[mapped_option]
        
        # If no specific intent detected, show contextual response based on user role
        if session.user_role:
            return self._get_role_specific_help(session.user_role)
        
        # Default: show greeting
        session.current_state = 'greeting'
        session.save()
        return BOT_RESPONSES["greeting"]
    
    def _get_role_specific_help(self, user_role):
        """Provide contextual help based on user role"""
        role_help = {
            '1': """🎓 As a teacher, you can:
            
• Access free teaching resources
• Get professional training
• Find dignified job opportunities  
• Join our supportive community

What interests you most?
👉 Complete your profile: https://forms.gle/qNpJqTf5f8aiEZa57

Or type 'menu' to see all options.""",

            '2': """👨‍👩‍👧 As a parent, I can help you with:
            
• Finding the perfect tutor for your child
• Homework help and exam preparation  
• Homeschooling guidance
• Educational support

What do you need help with today?
👉 Find a tutor: https://forms.gle/eTkf1N9qrKZyNJr4A

Or type 'menu' to explore all services.""",

            '3': """📚 As a student, you can get:
            
• Personalized tutoring in any subject
• Homework help and study support
• Exam preparation coaching
• Purpose discovery through PAP (coming soon!)

Ready to excel in your studies?
👉 Get academic support: https://forms.gle/dGQ6G6KZzoycS1n67

Or type 'menu' for more options.""",

            '4': """🤝 Thank you for volunteering! You can help with:
            
• Literacy programs for struggling readers
• Back-to-school support for disadvantaged children
• Community educational initiatives

Ready to make an impact?
👉 Join as volunteer: https://docs.google.com/forms/d/e/1FAIpQLSeOp7MqoaTPE4Rvi_22VwLX_v4dbR62EIJcP8N3FtZWMk0leQ/viewform?usp=sharing&ouid=116162016347061818487""",

            '5': """💎 Thank you for your generosity! Your sponsorship supports:
            
• Educational programs for underserved communities
• Literacy initiatives and reading programs
• Back-to-school supplies for children in need

Make a lasting impact today:
👉 Become a sponsor: https://docs.google.com/forms/d/e/1FAIpQLSeX_9GAHJB22l_1-OAN08avlW_fxRR1HIlAO_SxvNH9HF4fWg/viewform?usp=sharing&ouid=116162016347061818487""",

            '6': """🏫 As a school administrator, we can help with:
            
• Teacher recruitment and training
• Digital transformation solutions
• School management systems
• EdTech consultation

Ready to transform your school?
👉 Request services: https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform?usp=sharing&ouid=116162016347061818487"""
        }
        
        return role_help.get(user_role, BOT_RESPONSES["greeting"])
    
    def _process_message_stateless(self, phone_number, message):
        """Stateless fallback processing when database is unavailable"""
        message_lower = message.lower().strip()
        
        # Handle help commands
        if message_lower in ['help', '7']:
            return BOT_RESPONSES["7"]
        
        # Handle main menu options (1-6)
        if message_lower in ['1', '2', '3', '4', '5', '6']:
            return BOT_RESPONSES[message_lower]
        
        # Handle help submenu options (11-14)
        if message_lower in ['11', '12', '13', '14']:
            return BOT_RESPONSES[message_lower]
        
        # Handle back navigation - return to help menu
        if message_lower == 'back':
            return BOT_RESPONSES["7"]
        
        # Handle menu navigation
        if message_lower in ['menu', 'start', 'main']:
            return BOT_RESPONSES["greeting"]
        
        # Handle text alternatives
        text_mappings = {
            'teacher': '1',
            'parent': '2', 'guardian': '2',
            'student': '3',
            'volunteer': '4',
            'sponsor': '5',
            'admin': '6', 'school admin': '6',
            'mission': '11', 'vision': '11', 'values': '11',
            'initiatives': '12',
            'services': '13',
            'human': '14', 'agent': '14'
        }
        
        if message_lower in text_mappings:
            mapped_option = text_mappings[message_lower]
            return BOT_RESPONSES[mapped_option]
        
        # Default: show greeting for any unrecognized input
        return BOT_RESPONSES["greeting"]

    def send_message(self, phone_number, message):
        """Send message via WhatsApp API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'text',
            'text': {'body': message}
        }
        
        try:
            logger.info(f"Sending message to {phone_number}")
            logger.info(f"Request URL: {self.api_url}")
            logger.info(f"Request data: {json.dumps(data, indent=2)}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(data)
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}", exc_info=True)
            return False
