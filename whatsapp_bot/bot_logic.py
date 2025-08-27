import requests
import json
import logging
from django.conf import settings
from .models import UserSession

logger = logging.getLogger(__name__)

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

    def process_message(self, phone_number, message):
        """Main message processing logic"""
        # Get or create user session
        session, created = UserSession.objects.get_or_create(
            phone_number=phone_number,
            defaults={'current_state': 'greeting'}
        )
        
        message_lower = message.lower().strip()
        
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
        
        # Default: show greeting
        session.current_state = 'greeting'
        session.save()
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
