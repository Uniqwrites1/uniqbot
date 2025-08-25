import requests
import json
import logging
from django.conf import settings
from .models import UserSession

logger = logging.getLogger(__name__)

class WhatsAppBot:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        
        # Form links - Updated with actual URLs
        self.form_links = {
            'teacher': 'https://forms.gle/qNpJqTf5f8aiEZa57',
            'parent': 'https://forms.gle/eTkf1N9qrKZyNJr4A',
            'student': 'https://forms.gle/dGQ6G6KZzoycS1n67',
            'volunteer': 'https://docs.google.com/forms/d/e/1FAIpQLSeOp7MqoaTPE4Rvi_22VwLX_v4dbR62EIJcP8N3FtZWMk0leQ/viewform',
            'sponsor': 'https://docs.google.com/forms/d/e/1FAIpQLSeX_9GAHJB22l_1-OAN08avlW_fxRR1HIlAO_SxvNH9HF4fWg/viewform',
            'admin': 'https://docs.google.com/forms/d/e/1FAIpQLSesPzdDEMUc_V5BXdZUjupEhSpgMaLMVQMz61TlD3CxyOFi6w/viewform'
        }

    def process_message(self, phone_number, message):
        """Main message processing logic"""
        # Get or create user session
        session, created = UserSession.objects.get_or_create(
            phone_number=phone_number,
            defaults={'current_state': 'greeting'}
        )
        
        message_lower = message.lower()
        
        # Handle menu commands
        if message_lower in ['help', 'menu', '7']:
            return self.get_help_menu()
            
        # Handle help menu options
        if message_lower in ['1', 'mission', 'vision', 'values']:
            return self.get_mission_vision_values()
        elif message_lower in ['2', 'initiatives']:
            return self.get_initiatives()
        elif message_lower in ['3', 'services']:
            return self.get_services()
        elif message_lower in ['4', 'speak', 'human', 'agent']:
            return self.escalate_to_human()
        
        # Handle role selection
        if session.current_state == 'greeting' or created:
            if message_lower in ['1', 'teacher']:
                return self.handle_role_selection(session, 'teacher')
            elif message_lower in ['2', 'parent', 'guardian']:
                return self.handle_role_selection(session, 'parent')
            elif message_lower in ['3', 'student']:
                return self.handle_role_selection(session, 'student')
            elif message_lower in ['4', 'volunteer']:
                return self.handle_role_selection(session, 'volunteer')
            elif message_lower in ['5', 'sponsor']:
                return self.handle_role_selection(session, 'sponsor')
            elif message_lower in ['6', 'admin', 'school admin']:
                return self.handle_role_selection(session, 'admin')
            else:
                return self.get_greeting()
        
        # Default response
        return self.get_default_response()

    def get_greeting(self):
        """Return greeting message"""
        return ("👋 Welcome to Uniqwrites Educational Platform!\n"
                "We're redefining education through tutoring, teacher empowerment, and transformation programs.\n\n"
                "Before we continue, please tell us who you are:\n"
                "1️⃣ Teacher\n"
                "2️⃣ Parent/Guardian\n"
                "3️⃣ Student\n"
                "4️⃣ Volunteer\n"
                "5️⃣ Sponsor\n"
                "6️⃣ School Admin\n"
                "7️⃣ Help")

    def handle_role_selection(self, session, role):
        """Handle user role selection"""
        session.user_role = role
        session.current_state = 'role_selected'
        session.save()
        
        responses = {
            'teacher': (
                "🎉 Great! Welcome, Teacher 👩‍🏫. Please complete this form to get started:\n"
                f"👉 {self.form_links['teacher']}"
            ),
            'parent': (
                "🌟 Wonderful! We're excited to support your child's learning journey. Please complete this quick form to begin:\n"
                f"👉 {self.form_links['parent']}"
            ),
            'student': (
                "💡 Amazing! Welcome, future scholar. Please fill in this form so we can tailor your learning experience:\n"
                f"👉 {self.form_links['student']}"
            ),
            'volunteer': (
                "🤝 Thank you for your heart of service. Please share your details here so we can connect you with the right initiative:\n"
                f"👉 {self.form_links['volunteer']}"
            ),
            'sponsor': (
                "💎 Thank you for your generosity! Please fill in this sponsorship form to partner with us:\n"
                f"👉 {self.form_links['sponsor']}"
            ),
            'admin': (
                "🏫 Wonderful! Let's help you transform your school. Please complete this form to get started:\n"
                f"👉 {self.form_links['admin']}"
            )
        }
        
        return responses.get(role, self.get_default_response())

    def get_help_menu(self):
        """Return help menu"""
        return ("📚 Here's what I can help you with:\n\n"
                "1️⃣ Learn about our Mission, Vision & Values\n"
                "2️⃣ Explore our Initiatives\n"
                "3️⃣ Our Services\n"
                "4️⃣ Speak to a Human Agent")

    def get_mission_vision_values(self):
        """Return mission, vision, and values"""
        return ("Our Mission\n"
                "Empowering learners, uplifting educators. We make education personalized, inclusive, and accessible through innovative digital solutions, ensuring every learner excels and every educator thrives.\n\n"
                "Our Vision\n"
                "To make learning accessible to all by empowering students and educators through technology, personalization, and strong relationships. Uniqwrites—Education with You in Mind.\n\n"
                "Our Values\n"
                "Redefining Perspectives\n"
                "Impossibility is a perspective so we redefine it. We challenge the status quo and create new possibilities for learning and growth.\n\n"
                "Activating Potential\n"
                "Possibilities are rooted in potential. So we activate it. We believe in the power of every individual to learn, grow, and succeed.\n\n"
                "Facilitating Growth\n"
                "Growth is the process, so we embrace it. We foster a culture of continuous learning, improvement, and innovation for all.\n\n"
                "Creating Lasting Impact\n"
                "Our work fosters joy, success, and a fulfilled life through meaningful impacts.\n\n"
                "Our Team\n"
                "We are real people from diverse backgrounds, sharing experiences that mirror yours. Each of us is driven by a deep passion for transforming learning into a personalized and impactful experience. We believe that education should be an opportunity for everyone—one that nurtures the whole person and empowers individuals to unlock their full potential.")

    def get_initiatives(self):
        """Return initiatives"""
        return (f"Literacy Immersion Outreach Summary:\n"
                "This initiative tackles literacy barriers in public secondary schools through immersive educational programs, workshops, and resource provision. "
                "Born from the founder's personal transformation—going from struggling reader to top student thanks to a specialist's unique teaching methods—the mission carries deep emotional weight. "
                "The program recognizes that illiteracy blocks dreams, confidence, and future opportunities, denying students access to education, personal growth, and economic participation. "
                "Operating as more than just an initiative but as a 'lifeline,' it aims to break the cycle of illiteracy by stepping into schools where students still struggle with reading, spelling, and speaking. "
                "The vision is powerful: ensuring no child's potential is limited by their ability to read, and no student is left 'in the shadows of their own potential.'\n\n"
                "Back-to-School Initiative Summary:\n"
                "This program addresses educational abandonment by reaching out-of-school children and youth who've been pushed out by poverty, family struggles, discouragement, or learning difficulties. "
                "Moving beyond traditional supply distribution, it operates as a 'rescue mission for lost dreams,' actively seeking students on the streets and in forgotten places who've fallen through educational cracks. "
                "The initiative provides comprehensive support—financial aid, mentorship, tutoring, and confidence rebuilding—to remove barriers and bring children back to learning spaces. "
                "Driven by the powerful image of brilliant minds forced to 'trade school for survival,' the mission emphasizes that education shouldn't be a lost dream but an accessible right. "
                "The emotional core centers on giving 'just one more chance' to children whose potential remains untapped, transforming streets back into pathways toward classrooms 'where dreams are built and destinies are shaped.' "
                "It's positioned as a comeback opportunity for every deserving child.\n\n"
                f"Join as a volunteer: {self.form_links['volunteer']}\n"
                f"Sponsor: {self.form_links['sponsor']}")

    def get_services(self):
        """Return services"""
        return ("For Parents/Guardians\n"
                "Home Tutoring\n"
                "One-on-One & Group Tutoring: Personalized learning tailored to individual needs or collaborative sessions that encourage peer engagement and shared knowledge. Virtual & Physical Lessons: Flexible learning options—join classes from anywhere online or experience face-to-face instruction for hands-on guidance.\n\n"
                "Homework Help\n"
                "Expert support to simplify complex assignments, reinforce understanding, and boost academic confidence.\n\n"
                "Homeschooling\n"
                "A structured, student-centered approach to education at home, ensuring personalized learning at the right pace.\n\n"
                "Examination Prep\n"
                "Comprehensive coaching with proven strategies to help students excel in standardized tests and secure top scores (SAT, IGCSE, WAEC, NECO, JAMB, & more).\n\n"
                f"Request a Tutor: {self.form_links['parent']}\n\n"
                "For Schools\n"
                "Request for Teachers\n"
                "Hire trained professionals easily.\n\n"
                "Digital Transformation\n"
                "Modernize your school with edtech tools.\n\n"
                "School Management System\n"
                "Automate admin tasks and communication.\n\n"
                "EdTech Tools Consultation\n"
                "Explore the best digital teaching tools.\n\n"
                f"Request School Services: {self.form_links['admin']}\n\n"
                "For Teachers\n"
                "Access Free Resources\n"
                "Upgrade skills with top-notch teaching materials and strategies.\n\n"
                "Become Indispensable\n"
                "Gain training and insights to stand out as an exceptional educator.\n\n"
                "Secure Dignified Job Opportunities\n"
                "Connect with schools and families that respect and value educators.\n\n"
                "Join a Purpose-Driven Community\n"
                "Be part of a network that protects teachers' interests and advocates against any form of disrespect or exploitation from students, parents, or administrators.\n\n"
                f"Become a Tutor: {self.form_links['teacher']}")

    def escalate_to_human(self):
        """Escalate to human agent"""
        return "👨‍💼 A human agent will connect with you shortly. Please hold on…"

    def get_default_response(self):
        """Return default response"""
        return ("I'm here to help! Type 'help' or 'menu' to see what I can assist you with.\n\n"
                "You can also choose your role:\n"
                "1️⃣ Teacher\n"
                "2️⃣ Parent/Guardian\n"
                "3️⃣ Student\n"
                "4️⃣ Volunteer\n"
                "5️⃣ Sponsor\n"
                "6️⃣ School Admin")

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
