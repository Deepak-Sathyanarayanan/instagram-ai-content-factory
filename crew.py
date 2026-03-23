import os
from dotenv import load_dotenv
from openai import OpenAI
import yaml

load_dotenv()


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


STYLE_GUIDE = """
STYLE GUIDE

Tone:
- Direct
- Slightly bold
- Concise
- Technical but readable
- No fluff

Avoid:
- Corporate tone
- Generic motivational advice
- Oversimplified beginner explanations
- Long sentences
- Vague claims
- Buzzword-heavy writing

Prefer:
- Punchy lines
- Strong opinions
- Clear technical framing
- Specific examples
- Practical takeaways
- Platform-native wording
"""

TECHNICAL_CONTENT_GUIDE = """
TECHNICAL CONTENT GUIDE

Topic Focus:
- Artificial Intelligence
- Machine Learning
- LLMs
- Agents
- RAG
- MLOps
- Prompting
- Fine-tuning
- Evaluation
- Inference
- Vector databases
- AI product engineering
- Deployment and production issues

Target Audience:
- AI engineers
- ML engineers
- Data scientists
- Technical founders
- Developers building AI systems

Audience Rules:
- Assume the audience is technical
- Do not write like a beginner course
- Do not over-explain basic concepts
- Focus on real technical pain points, tradeoffs, and implementation realities
- Prefer practical insights over inspiration
- Prefer depth over generic productivity advice

Content Rules:
- Use examples from real AI/ML workflows
- Mention failure modes, bottlenecks, tradeoffs, and lessons learned where relevant
- Make content feel credible to engineers
- Avoid shallow “AI will change everything” style content
- Prioritize technical usefulness, clarity, and specificity
"""

CAROUSEL_STYLE_RULES = """
SLIDE STYLE RULES (CRITICAL):

- Max 6–8 words per line
- Max 2 lines per slide
- Prefer 1 line if possible
- No explanations
- No long sentences
- No commas-heavy sentences

WRITING STYLE:
- Each slide = one punch
- Use contrast, tension, or surprise
- Break expectations
- Sound like a strong opinion

BAD:
"Implement drift detection and monitor distributions"

GOOD:
"You don’t have a model problem

You have a data problem"
"""


class OllamaLLM:
    def __init__(self):
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        api_key = os.getenv("OPENAI_API_KEY", "ollama")
        self.model = os.getenv("OLLAMA_MODEL", "gemma3")
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise Instagram content generation assistant "
                        "specialized in AI/ML content for technical audiences."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content or ""


class InstagramContentFactory:
    def __init__(self):
        self.agents = load_yaml("agents.yaml")
        self.tasks = load_yaml("tasks.yaml")
        self.llm = OllamaLLM()

    def run(self, topic: str, audience: str, goal: str, tone: str):
        strategy_prompt = f"""
{STYLE_GUIDE}
{TECHNICAL_CONTENT_GUIDE}
{CAROUSEL_STYLE_RULES}

Agent Role: {self.agents['strategist']['role']}
Goal: {self.agents['strategist']['goal']}
Backstory: {self.agents['strategist']['backstory']}

Task:
{self.tasks['strategy_task']['description']}

INPUT:
- Topic: {topic}
- Audience: {audience}
- Goal: {goal}
- Tone: {tone}

HOOK RULES:
- Must trigger curiosity, tension, or a bold claim
- Should challenge assumptions or expose a technical mistake
- Avoid generic advice
- Must make a technical reader stop scrolling
- Should sound credible to engineers

STRATEGY RULES:
- Focus on one sharp angle
- Make the pain point specific and technically real
- Keep takeaways practical and non-generic
- Write for Instagram, not a blog
- Make the output feel save-worthy and share-worthy
- Prioritize AI/ML implementation insights
- Prefer tradeoffs, lessons, and failure modes over broad claims

Return exactly:
Content Angle:
Target Pain Point:
Hook Ideas:
Key Takeaways:
"""
        strategy = self.llm.generate(strategy_prompt)

        carousel_prompt = f"""
{STYLE_GUIDE}

{TECHNICAL_CONTENT_GUIDE}

Agent Role: {self.agents['carousel_creator']['role']}
Goal: {self.agents['carousel_creator']['goal']}
Backstory: {self.agents['carousel_creator']['backstory']}

Task:
{self.tasks['carousel_task']['description']}

INPUT STRATEGY:
{strategy}

CAROUSEL RULES:
- Slide 1 must stop the scroll
- Slides 2 to 6 must be short, sharp, and easy to skim
- Make each slide feel like it can stand alone
- Use tension, contrast, clarity, or bold framing
- Avoid paragraphs
- Avoid sounding like a blog post
- Make it feel native to Instagram
- Caption must start strong in the first line
- CTA should feel clear and natural
- Keep examples relevant to AI/ML engineering
- Prefer specific technical truths over general creator advice

Return exactly:
Slide 1:
Slide 2:
Slide 3:
Slide 4:
Slide 5:
Slide 6:
Slide 7:
Design Notes:
Caption:
Hashtags:
"""
        carousel = self.llm.generate(carousel_prompt)

        reel_prompt = f"""
{STYLE_GUIDE}

{TECHNICAL_CONTENT_GUIDE}

Agent Role: {self.agents['reel_creator']['role']}
Goal: {self.agents['reel_creator']['goal']}
Backstory: {self.agents['reel_creator']['backstory']}

Task:
{self.tasks['reel_task']['description']}

INPUT STRATEGY:
{strategy}

REEL RULES:
- Hook must hit in the first 1 to 3 seconds
- Use short spoken lines
- Keep pacing fast
- Avoid robotic or essay-like phrasing
- Make it sound natural when spoken aloud
- Body should deliver fast value
- CTA should be simple and clear
- Keep the examples grounded in AI/ML topics
- Make the script sound credible to technical people

Return exactly:
Hook:
Body:
Closing CTA:
On-screen Text:
Shot Suggestions:
"""
        reel = self.llm.generate(reel_prompt)

        editor_prompt = f"""
{STYLE_GUIDE}

{TECHNICAL_CONTENT_GUIDE}

Agent Role: {self.agents['editor']['role']}
Goal: {self.agents['editor']['goal']}
Backstory: {self.agents['editor']['backstory']}

Task:
{self.tasks['editor_task']['description']}

EDITOR RULES:
- Tighten weak phrasing
- Remove fluff
- Make hooks stronger
- Make slides more skimmable
- Make reel lines more natural to speak
- Keep the original meaning
- Do not make it sound corporate
- Do not add unnecessary explanation
- Preserve technical credibility
- Remove generic creator-language if it appears
- Keep the content useful for AI/ML practitioners

Carousel Draft:
{carousel}

Reel Draft:
{reel}

Return exactly:
FINAL CAROUSEL:
FINAL REEL:
"""
        final_output = self.llm.generate(editor_prompt)

        return {
            "strategy": strategy,
            "carousel": carousel,
            "reel": reel,
            "final": final_output,
        }