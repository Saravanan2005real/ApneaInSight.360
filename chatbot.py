import random
import re
from datetime import datetime

# Enhanced knowledge base for sleep apnea
sleep_apnea_knowledge = {
    "general": [
        "Sleep apnea is a serious sleep disorder where breathing repeatedly stops and starts during sleep. There are three main types: obstructive, central, and complex sleep apnea syndrome. It affects approximately 1 in 5 adults, with many cases going undiagnosed.",
        "Sleep apnea is more than just snoring. It's a medical condition that requires attention. The most common type is obstructive sleep apnea (OSA), where the airway becomes blocked during sleep. Untreated sleep apnea can lead to serious health complications including heart disease, high blood pressure, and diabetes.",
        "Sleep apnea affects millions of people worldwide. It's characterized by repeated interruptions in breathing during sleep, which can lead to poor sleep quality and various health issues. Early detection and treatment are crucial for preventing long-term complications."
    ],
    "symptoms": [
        "Common symptoms include loud snoring, episodes of stopped breathing during sleep, abrupt awakenings with gasping or choking, morning headache, and excessive daytime sleepiness. You might also experience difficulty concentrating, mood changes, high blood pressure, and decreased libido.",
        "Many people with sleep apnea don't realize they have it. Key symptoms to watch for include: waking up with a dry mouth, morning headaches, difficulty staying asleep, and feeling tired even after a full night's sleep. Partners often notice the symptoms first.",
        "Sleep apnea symptoms can vary between adults and children. Adults often experience daytime sleepiness and snoring, while children might show hyperactivity, poor school performance, or bedwetting. Other symptoms include night sweats, frequent urination at night, and teeth grinding."
    ],
    "causes": [
        "The main causes include excess weight, which can lead to fat deposits around the upper airway; anatomical factors like a thick neck or narrow airway; and lifestyle factors such as alcohol use and smoking. Age and family history also play a significant role.",
        "Sleep apnea occurs when the muscles in the back of your throat relax too much to allow normal breathing. This can be due to various factors including obesity, large tonsils, or structural issues in the airway. Hormonal changes and certain medical conditions can also contribute.",
        "Risk factors for sleep apnea include being overweight, having a large neck circumference, being male, being older, having a family history, and certain medical conditions like high blood pressure. Nasal congestion and smoking can also increase the risk."
    ],
    "treatment": [
        "Treatment options include CPAP therapy, which is the most common and effective treatment; oral appliances that help keep the airway open; surgery in some cases; and lifestyle changes like weight loss and exercise. The best treatment depends on the severity and type of sleep apnea.",
        "CPAP (Continuous Positive Airway Pressure) therapy is often the first-line treatment. It involves wearing a mask that delivers air pressure to keep your airway open. Other options include oral appliances, surgery, and lifestyle modifications. Treatment plans are personalized based on individual needs.",
        "Treatment plans are personalized based on your specific condition. They may include a combination of CPAP therapy, lifestyle changes, and in some cases, surgery. Regular follow-ups with your healthcare provider are important to ensure the treatment remains effective."
    ],
    "diagnosis": [
        "Sleep apnea is typically diagnosed through a sleep study (polysomnography) or home sleep apnea test. Your doctor may also use the Epworth Sleepiness Scale to assess your daytime sleepiness. The AHI (Apnea-Hypopnea Index) is used to measure severity.",
        "Diagnosis usually involves an overnight sleep study that monitors your breathing, oxygen levels, heart rate, and other factors. Home sleep tests are also available and can be more convenient for some patients. The results help determine the severity of your condition.",
        "To diagnose sleep apnea, doctors look at your medical history, symptoms, and results from sleep studies. The AHI score helps determine the severity of your condition and guides treatment decisions. Multiple tests might be needed for an accurate diagnosis."
    ],
    "complications": [
        "Untreated sleep apnea can lead to serious health problems including high blood pressure, heart disease, stroke, diabetes, and depression. It can also increase the risk of workplace or motor vehicle accidents due to daytime sleepiness.",
        "Long-term complications include cardiovascular problems, metabolic disorders, and cognitive issues. It can also affect your quality of life and relationships due to sleep disturbances. Children with untreated sleep apnea may develop behavioral problems.",
        "Sleep apnea can contribute to various health issues over time, including heart problems, type 2 diabetes, and liver problems. It's important to seek treatment to prevent these complications. The condition can also worsen existing health problems."
    ],
    "prevention": [
        "While you can't always prevent sleep apnea, you can reduce your risk by maintaining a healthy weight, exercising regularly, avoiding alcohol and sedatives, sleeping on your side, and treating nasal congestion.",
        "Preventive measures include maintaining a healthy lifestyle, avoiding smoking, managing your weight, and practicing good sleep hygiene. Regular exercise and a balanced diet can also help reduce the risk of developing sleep apnea.",
        "To prevent sleep apnea or reduce its severity, focus on maintaining a healthy weight, avoiding alcohol before bedtime, sleeping on your side, and keeping your nasal passages clear. Early detection and treatment of symptoms are crucial."
    ],
    "lifestyle": [
        "Lifestyle changes can significantly improve sleep apnea symptoms. These include weight management, regular exercise, avoiding alcohol and sedatives, establishing a regular sleep schedule, and creating a comfortable sleep environment.",
        "Making healthy lifestyle choices can help manage sleep apnea. This includes maintaining a healthy weight, exercising regularly, avoiding alcohol and smoking, and practicing good sleep hygiene. Small changes can make a big difference.",
        "Simple lifestyle changes can make a big difference. Try to maintain a regular sleep schedule, create a comfortable sleep environment, avoid alcohol before bedtime, and stay active during the day. These changes can improve sleep quality."
    ],
    "children": [
        "Sleep apnea in children is often caused by enlarged tonsils or adenoids. Symptoms may include snoring, restless sleep, bedwetting, and behavioral problems. Treatment often involves removing the tonsils and adenoids.",
        "Children with sleep apnea may show different symptoms than adults, such as poor school performance, hyperactivity, or bedwetting. It's important to consult a pediatrician if you suspect your child has sleep apnea.",
        "Pediatric sleep apnea requires special attention. Treatment options may include surgery to remove tonsils and adenoids, or in some cases, CPAP therapy. Early intervention is crucial for a child's development and learning."
    ],
    "cpap": [
        "CPAP therapy involves wearing a mask that delivers continuous air pressure to keep your airway open during sleep. It's the most common treatment for moderate to severe sleep apnea and requires regular cleaning and maintenance.",
        "CPAP machines can take some getting used to, but most people adapt within a few weeks. Regular cleaning of the equipment is important for effectiveness and hygiene. Your healthcare provider can help you find the right mask and settings.",
        "CPAP therapy is highly effective when used consistently. It's important to work with your healthcare provider to find the right mask and pressure settings. Regular follow-ups ensure the treatment remains effective."
    ],
    "diet": [
        "A healthy diet can help manage sleep apnea symptoms. Focus on whole foods, lean proteins, and plenty of fruits and vegetables. Avoid heavy meals before bedtime and limit alcohol and caffeine intake.",
        "Certain foods can help reduce sleep apnea symptoms. Include foods rich in magnesium, omega-3 fatty acids, and tryptophan. Avoid processed foods, sugary snacks, and heavy meals close to bedtime.",
        "Maintaining a healthy weight through proper nutrition is crucial for managing sleep apnea. Consider a Mediterranean-style diet rich in fruits, vegetables, whole grains, and healthy fats. Stay hydrated throughout the day."
    ],
    "exercise": [
        "Regular exercise can help reduce sleep apnea symptoms by improving overall health and promoting weight loss. Focus on aerobic activities, strength training, and yoga. Even moderate exercise can make a difference.",
        "Exercise helps strengthen the muscles in your airway and can improve sleep quality. Start with low-impact activities and gradually increase intensity. Consistency is more important than intensity.",
        "Physical activity can significantly improve sleep apnea symptoms. Aim for at least 30 minutes of moderate exercise most days of the week. Include both cardio and strength training exercises."
    ],
    "sleep_position": [
        "Sleeping on your side instead of your back can help reduce sleep apnea symptoms. Use pillows to maintain this position throughout the night. Special pillows and devices are available to help maintain side sleeping.",
        "Elevating your head while sleeping can help keep your airway open. Use a wedge pillow or adjust your bed's head position. Avoid sleeping flat on your back as it can worsen symptoms.",
        "Finding the right sleep position is crucial for managing sleep apnea. Side sleeping is generally recommended, and there are various devices available to help maintain this position throughout the night."
    ],
    "alternative_treatments": [
        "Alternative treatments for sleep apnea include oral appliances, positional therapy, and certain breathing exercises. These can be effective for mild to moderate cases or as complementary treatments.",
        "Some people find relief through alternative therapies like acupuncture, yoga, and certain breathing techniques. These should be used in conjunction with, not instead of, medical treatments.",
        "While CPAP is the gold standard, alternative treatments like oral appliances and positional therapy can be effective for some people. Consult your doctor before trying alternative treatments."
    ],
    "pregnancy": [
        "Sleep apnea can develop or worsen during pregnancy due to hormonal changes and weight gain. It's important to monitor symptoms and discuss them with your healthcare provider.",
        "Pregnant women with sleep apnea should work closely with their healthcare team. Treatment options may need to be adjusted during pregnancy to ensure safety for both mother and baby.",
        "Sleep apnea during pregnancy requires special attention. Treatment should be carefully managed to ensure the safety of both mother and baby. Regular monitoring is essential."
    ],
    "elderly": [
        "Sleep apnea is common in older adults and may present differently than in younger people. Treatment should be tailored to individual needs and may require special considerations.",
        "Elderly patients with sleep apnea may have additional health concerns that need to be considered in treatment planning. Regular monitoring and adjustments to treatment may be necessary.",
        "Managing sleep apnea in older adults requires a comprehensive approach that considers other health conditions and medications. Treatment should be carefully monitored and adjusted as needed."
    ]
}

# Enhanced keywords for topic detection
topic_keywords = {
    "general": ["what is", "define", "explain", "tell me about", "overview", "sleep apnea", "apnea", "disorder"],
    "symptoms": ["symptoms", "signs", "how do i know", "indicators", "warning signs", "feel", "experience", "show"],
    "causes": ["causes", "why", "reason", "risk factors", "what causes", "trigger", "lead to", "result"],
    "treatment": ["treatment", "cure", "therapy", "how to treat", "management", "help", "fix", "solution"],
    "diagnosis": ["diagnose", "test", "how to know", "detection", "screening", "check", "find out", "identify"],
    "complications": ["complications", "risks", "dangers", "problems", "effects", "consequences", "impact", "result"],
    "prevention": ["prevent", "avoid", "stop", "reduce risk", "protection", "lower chance", "ward off"],
    "lifestyle": ["lifestyle", "diet", "exercise", "habits", "daily routine", "living", "changes", "routine"],
    "children": ["children", "kids", "pediatric", "child", "young", "baby", "teen", "adolescent"],
    "cpap": ["cpap", "machine", "device", "mask", "therapy", "treatment", "equipment", "appliance"],
    "diet": ["diet", "food", "nutrition", "eating", "meal", "dietary", "nutritional", "foods"],
    "exercise": ["exercise", "workout", "physical activity", "fitness", "training", "movement", "activity"],
    "sleep_position": ["position", "sleeping position", "posture", "side sleeping", "back sleeping", "elevation"],
    "alternative_treatments": ["alternative", "natural", "holistic", "complementary", "other treatments", "options"],
    "pregnancy": ["pregnancy", "pregnant", "expecting", "mother", "maternal", "gestation", "prenatal"],
    "elderly": ["elderly", "older", "senior", "aging", "aged", "geriatric", "mature", "old age"]
}

# Greeting patterns
greetings = [
    "Hello! I'm your Sleep Apnea Assistant. How can I help you today?",
    "Hi there! I'm here to answer your questions about sleep apnea. What would you like to know?",
    "Welcome! I'm your sleep apnea expert. Feel free to ask me anything about sleep apnea.",
    "Greetings! I'm here to provide information about sleep apnea. What would you like to learn about?",
    "Hello! I'm your sleep health assistant. How can I help you with sleep apnea today?"
]

# Farewell patterns
farewells = [
    "Take care and remember to prioritize your sleep health!",
    "Wishing you restful sleep and good health!",
    "Feel free to come back if you have more questions about sleep apnea!",
    "Best wishes for better sleep and improved health!",
    "Take care and don't hesitate to return with more questions!"
]

def get_chatbot_response(user_input):
    # Convert input to lowercase for matching
    user_input = user_input.lower().strip()
    
    # Check for greetings
    if any(greeting in user_input for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
        return random.choice(greetings)
    
    # Check for farewells
    if any(farewell in user_input for farewell in ["bye", "goodbye", "thanks", "thank you", "see you"]):
        return random.choice(farewells)
    
    # Check for topic keywords with improved matching
    matched_topic = None
    best_match_score = 0
    
    for topic, keywords in topic_keywords.items():
        match_score = sum(1 for keyword in keywords if keyword in user_input)
        if match_score > best_match_score:
            best_match_score = match_score
            matched_topic = topic
    
    if matched_topic and matched_topic in sleep_apnea_knowledge:
        # Get a random response from the matched topic
        response = random.choice(sleep_apnea_knowledge[matched_topic])
        
        # Add follow-up question
        follow_ups = {
            "general": "Would you like to know more about specific symptoms or treatments?",
            "symptoms": "Would you like to know about causes or treatment options?",
            "causes": "Would you like to learn about prevention or treatment options?",
            "treatment": "Would you like to know more about CPAP therapy or lifestyle changes?",
            "diagnosis": "Would you like to know about treatment options or lifestyle changes?",
            "complications": "Would you like to know how to prevent these complications?",
            "prevention": "Would you like to know more about lifestyle changes or treatment options?",
            "lifestyle": "Would you like to know more about specific treatment options?",
            "children": "Would you like to know more about diagnosis or treatment for children?",
            "cpap": "Would you like to know more about other treatment options?",
            "diet": "Would you like to know about exercise recommendations or sleep positions?",
            "exercise": "Would you like to know about dietary recommendations or sleep positions?",
            "sleep_position": "Would you like to know about other lifestyle changes or treatments?",
            "alternative_treatments": "Would you like to know about traditional treatments or lifestyle changes?",
            "pregnancy": "Would you like to know about treatment options or lifestyle changes during pregnancy?",
            "elderly": "Would you like to know about treatment options or lifestyle changes for older adults?"
        }
        
        return f"{response} {follow_ups.get(matched_topic, 'Is there anything else you would like to know?')}"
    
    # If no specific topic is matched, provide a contextual response
    contextual_responses = [
        "I'm here to help with sleep apnea information. Could you tell me more about what you'd like to know?",
        "I specialize in sleep apnea information. Could you be more specific about your question?",
        "I'd be happy to help with your sleep apnea questions. What specific aspect would you like to know more about?",
        "I understand you have questions about sleep apnea. Would you like to know about symptoms, causes, treatment, or something else?",
        "I can help you with information about sleep apnea. What specific topic would you like to learn about?"
    ]
    
    return random.choice(contextual_responses) 