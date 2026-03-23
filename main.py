import os
import argparse
from datetime import datetime
from crew import InstagramContentFactory


def save_output(topic: str, outputs: dict):
    slug = topic.lower().replace(" ", "_").replace("/", "_")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = os.path.join("outputs", f"{ts}_{slug}")
    os.makedirs(outdir, exist_ok=True)

    for name, content in outputs.items():
        path = os.path.join(outdir, f"{name}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return outdir


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Instagram AI/ML content for a technical audience."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic to generate content for",
    )
    parser.add_argument(
        "--audience",
        default="AI engineers, ML engineers, data scientists, and technical founders",
        help="Target audience",
    )
    parser.add_argument(
        "--goal",
        default="educate a technical audience and attract followers interested in AI/ML systems",
        help="Content goal",
    )
    parser.add_argument(
        "--tone",
        default="technical, sharp, concise, slightly bold",
        help="Content tone",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    factory = InstagramContentFactory()
    outputs = factory.run(
        topic=args.topic,
        audience=args.audience,
        goal=args.goal,
        tone=args.tone,
    )

    output_dir = save_output(args.topic, outputs)

    print("\n=== STRATEGY ===\n")
    print(outputs["strategy"])
    print("\n=== CAROUSEL ===\n")
    print(outputs["carousel"])
    print("\n=== REEL ===\n")
    print(outputs["reel"])
    print("\n=== FINAL ===\n")
    print(outputs["final"])
    print(f"\nSaved outputs to: {output_dir}")
