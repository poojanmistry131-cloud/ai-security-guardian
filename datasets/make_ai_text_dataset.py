"""
Generates a labeled dataset for AI-Generated vs Human-Written Text Detection.
label = 1 -> AI-generated style
label = 0 -> Human-written style
Fully offline - style-based synthetic generation (formal/structured vs casual/personal).
"""
import csv
import random

random.seed(7)

topics = [
    "climate change", "remote work", "artificial intelligence", "healthy eating",
    "electric vehicles", "online education", "social media", "space exploration",
    "cryptocurrency", "mental health", "renewable energy", "urban farming",
    "video games", "book reading habits", "travel after the pandemic",
    "the future of jobs", "cybersecurity", "fitness trends", "sleep quality",
    "sustainable fashion", "artificial general intelligence", "smart cities",
    "digital privacy", "the gig economy", "plant-based diets",
]

# ---------- AI-STYLE TEMPLATES (structured, hedging, formal connectors) ----------
ai_templates = [
    "{topic} is a multifaceted issue that has garnered significant attention in recent years. "
    "On one hand, it offers numerous benefits; on the other hand, it also presents certain challenges. "
    "In conclusion, a balanced approach is essential to fully realize its potential.",

    "When considering {topic}, it is important to note several key factors. Firstly, the impact on society "
    "cannot be overstated. Secondly, economic considerations play a crucial role. Finally, further research "
    "is needed to fully understand the long-term implications.",

    "{topic} has become increasingly relevant in today's rapidly evolving landscape. As an AI language model, "
    "I can provide an overview of the main considerations. Overall, it is a complex topic with both advantages "
    "and disadvantages that merit careful examination.",

    "In summary, {topic} represents both an opportunity and a challenge. It is essential to weigh the pros and "
    "cons carefully. Moreover, stakeholders must collaborate to address the underlying issues effectively.",

    "There are several important aspects to consider regarding {topic}. To begin with, it affects various "
    "sectors differently. Additionally, it is worth noting that ongoing developments continue to shape the "
    "discourse. Ultimately, a comprehensive strategy is required.",

    "{topic} plays a pivotal role in shaping modern society. Furthermore, its implications extend beyond the "
    "immediate context, influencing broader systemic outcomes. It is imperative that we approach this subject "
    "with a nuanced perspective.",

    "1. Understanding {topic} requires examining multiple perspectives. 2. Experts generally agree on its "
    "significance. 3. However, opinions diverge on the best path forward. In conclusion, continued dialogue "
    "is necessary.",

    "The topic of {topic} can be broken down into several key components. First, we must consider the "
    "historical context. Second, the current state of affairs warrants attention. Third, future trends "
    "suggest continued evolution in this space.",
]

# ---------- HUMAN-STYLE TEMPLATES (casual, personal, contractions, typos) ----------
human_templates = [
    "honestly idk much about {topic} but my friend keeps talking about it lol, seems kinda interesting tho",
    "so i was reading about {topic} last night and man it's wild how much things have changed just in the past few years",
    "not gonna lie, {topic} stresses me out sometimes. like theres just so much info out there and its hard to keep up",
    "my uncle won't stop ranting about {topic} at every family dinner lmao, he thinks he knows everything about it",
    "ok so {topic}... where do i even start. i guess it depends on who you ask tbh",
    "i took a class on {topic} last semester and honestly it was way more interesting than i expected!!",
    "just watched a documentary about {topic}, kinda blew my mind ngl. def gonna look into it more this weekend",
    "ugh {topic} again in the news today. feel like i see this everywhere lately, not sure what to think honestly",
    "my coworker asked me about {topic} today and i had zero idea what to say lol, felt kinda embarrassed",
    "been thinking about {topic} a lot recently bc of that podcast i listen to on my commute",
    "so my sister's really into {topic}, she keeps sending me articles about it every other day haha",
    "tbh i dont fully get {topic} but i tried explaining it to my mom and she was even more confused than me",
    "reading up on {topic} rn for a project, gonna be up all night probably lol",
    "someone in my group chat brought up {topic} and now everyone's arguing about it, classic",
    "i remember when {topic} wasn't even a thing people talked about, crazy how fast it blew up",
]

def build_dataset():
    rows = []
    for topic in topics:
        for t in ai_templates:
            rows.append((t.format(topic=topic), 1))
        for t in human_templates:
            rows.append((t.format(topic=topic), 0))
    random.shuffle(rows)
    return rows

if __name__ == "__main__":
    rows = build_dataset()
    with open("ai_text_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    n_ai = sum(1 for r in rows if r[1] == 1)
    n_hum = sum(1 for r in rows if r[1] == 0)
    print(f"Total rows: {len(rows)} | AI-generated: {n_ai} | human: {n_hum}")
