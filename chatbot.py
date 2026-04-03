"""
CRIMERADAR AI — Police Chatbot Assistant
A rule-based + keyword AI chatbot for public safety queries.
Can be integrated into Flask via /chatbot endpoint.
"""

import re

KNOWLEDGE_BASE = {
    "robbery": {
        "keywords": ["robbery", "robber", "mugging", "steal", "snatching"],
        "response": "🚨 Robbery Alert Protocol:\n1. Do not resist — your safety comes first.\n2. Call 100 (Police) immediately after.\n3. Note the suspect's description, direction fled.\n4. Preserve the crime scene for forensics.\n⚡ High-risk zones currently: T Nagar, Tambaram, Sholinganallur."
    },
    "women_safety": {
        "keywords": ["women", "woman", "girl", "sos", "harassment", "unsafe", "safe route"],
        "response": "🔴 Women Safety Resources:\n📞 Emergency: 181 (Women Helpline)\n📞 Police: 100\n📱 Share live location with trusted contacts.\n⚠️ High-risk night zones: Guindy, T Nagar, Chromepet.\n✅ Safer alternatives: Use well-lit main roads after 8 PM."
    },
    "accident": {
        "keywords": ["accident", "crash", "collision", "road", "blackspot", "injured"],
        "response": "🚑 Accident Response:\n1. Call 108 (Ambulance) immediately.\n2. Call 100 (Police) for FIR.\n3. Do not move injured persons unless life-threatening.\n⚠️ Known accident blackspots: Velachery, Guindy flyover, Sholinganallur junction."
    },
    "patrol": {
        "keywords": ["patrol", "route", "officer", "police beat", "coverage"],
        "response": "🚔 Smart Patrol Routing:\nOur AI optimizes patrol routes daily based on:\n• Real-time FIR data\n• Historical crime heatmaps\n• Accident blackspot density\n• Women safety zones\nCurrent high-priority patrol: T Nagar → Guindy → Velachery → Tambaram loop."
    },
    "theft": {
        "keywords": ["theft", "stolen", "pickpocket", "missing", "burglar"],
        "response": "🔍 Theft Incident Protocol:\n1. File FIR at nearest station or online at tncrime.tn.gov.in.\n2. Provide time, location, description of stolen items.\n3. Check nearby CCTV footage (we can help request).\n📍 High theft zones: Anna Nagar markets, T Nagar shopping areas."
    },
    "heatmap": {
        "keywords": ["heatmap", "hotspot", "crime map", "danger zone", "high crime"],
        "response": "🗺️ Current Crime Heatmap Status:\n🔴 CRITICAL: Velachery, Sholinganallur (risk 90+)\n🟠 HIGH: T Nagar, Guindy, Tambaram (risk 85-90)\n🟡 MEDIUM: Adyar, Kodambakkam (risk 70-85)\n🟢 LOW: Porur, Perambur (risk < 70)\nData updated in real-time from FIR database."
    },
    "risk": {
        "keywords": ["risk", "dangerous", "safe", "prediction", "ai predict"],
        "response": "🤖 AI Risk Prediction Engine:\nOur Random Forest model analyzes:\n• Historical crime density\n• Time of day patterns\n• Location proximity to hotspots\n• Seasonal crime trends\nRisk scores: 0-60 (Low) | 61-80 (Medium) | 81-100 (High/Critical)"
    },
    "emergency": {
        "keywords": ["emergency", "help", "urgent", "immediate", "danger"],
        "response": "🆘 EMERGENCY CONTACTS:\n🚔 Police: 100\n🚑 Ambulance: 108\n🔥 Fire: 101\n👩 Women Helpline: 181\n🧒 Child Helpline: 1098\n🌐 Cyber Crime: 1930\n⚡ ALL ARE FREE TO CALL — Available 24/7"
    }
}

DEFAULT_RESPONSES = [
    "I'm the CRIMERADAR AI assistant. I can help with crime reporting, safety tips, patrol routes, and emergency contacts. What do you need?",
    "Please describe your situation. I can assist with: crime reports, safe routes, women safety, accident zones, and emergency help.",
    "Try asking about: 'safe route', 'robbery', 'accident zone', 'women safety', or 'emergency numbers'."
]

_default_idx = 0


def get_response(user_input: str) -> str:
    """Process user input and return appropriate response."""
    global _default_idx

    user_lower = user_input.lower().strip()

    # Greeting
    if any(g in user_lower for g in ["hello", "hi", "hey", "namaste", "vanakkam"]):
        return "👋 Welcome to CRIMERADAR AI! I'm here to help with public safety. How can I assist you today?"

    # Check knowledge base
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_lower:
                return data["response"]

    # Fallback
    response = DEFAULT_RESPONSES[_default_idx % len(DEFAULT_RESPONSES)]
    _default_idx += 1
    return response


def chat_loop():
    """Interactive terminal chat loop."""
    print("=" * 60)
    print("🤖 CRIMERADAR AI Chatbot — Public Safety Assistant")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the session.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Stay safe! Goodbye. 🚔")
            break

        response = get_response(user_input)
        print(f"\nBot: {response}\n")
        print("-" * 40)


if __name__ == "__main__":
    chat_loop()
