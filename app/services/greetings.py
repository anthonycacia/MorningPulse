import os
import random
from dotenv import load_dotenv
from app.core.config import MY_NAME

load_dotenv()



GREETINGS = [
    {
        "text": "Good morning",
        "fact": "I had an interesting dream!",
    },
    
    {
        "text" : "Buongiorno",
        "facts" : [
            "There\'s an Italian saying: Vedi Napoli e poi muori; which means that you have to see the beauty of Naples!",
            "In italy, you can find the oldest university in the world! The University of Bologna, founded in 1088."
        ],
    },
    
    {
        "text" : "Zǎoshànghǎo",
        "facts" : [
            "This is good morning in Mandarin Chinese. You can listen to pronunciation here: https://omniglot.com/soundfiles/mandarin/goodmorning2_mandarin.mp3",
            "Did you know that Chinese is the only surviving pictographic writing system?",
            "The Hong Kong-Zhuhai-Macau Bridge is the longest sea-crossing bridge in the world. The total length of the bridge is 55 kilometers or 34 miles!",
        ],
    },

    {
        "text" : "Namaste",
        "facts" : [
            'In Hindi, "namaste" is a common greeting; but literally translates to "bow to you", which has spiritual importance reflecting the belief: "the divine and self are the same within you and me."',
        ],
    },

    {
        "text" : "Buenos días",
        "facts": [
            "Did you know that, apart from Latin, Arabic is the largest contributor to Spanish? Arab armies conquered the Iberian Peninsula in the year 711. Spain expelled the Arabs in 1492.",
        ],
    },
    
    {
        "text" : "Bonjour",
        "facts": [
            "Did you know that the Louvre Museum in Paris is the largest art museum in the world! France is also the most visited country.",
        ],
    },

    {
        "text" : "Sabah al-kheir", 
        "facts" : [
            "Good morning in Arabic!",
        ],
    },

    {
        "text" : "Suprabhāta",
        "facts": [
            "This is one of the two main translations of Good Morning in Bengali; do you know the other?",
        ]
    }
]


def morning_greeting():
    greeting = random.choice(GREETINGS)

    # pick one fact randomly if we decide to include it
    fact = random.choice(greeting.get("facts", [""]))

    # 1 in 5 chance of including the fact
    if random.randint(1, 6) == 1:
        return f"{greeting['text']} {MY_NAME}!\n — {fact}"

    return f"{greeting["text"]} {MY_NAME}!"