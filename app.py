import random
import gradio as gr

# --- Poem generator templates ---
OPENERS = [
    "I read your claim and raise an eyebrow—",
    "You bring a headline; I bring the method—",
    "Broad claim, bright lights; let's dim them down—",
    "A careful voice replies: first, the caveats—",
]

SKEPTIC_LINES = [
    "Is the dataset broad or a narrow echo?",
    "Has bias crept in where we hoped for truth?",
    "Does the metric match the human cost?",
    "Was the model tested beyond its training dusk?",
]

LIMITATIONS = [
    "Overfitting glows under the validation light.",
    "Domain shifts arrive like uninvited guests.",
    "Labels decay; what once was gold may rust.",
    "Transparency hides behind complex weights.",
]

SUGGESTIONS = [
    "Run ablations; measure uncertainty; report all seeds.",
    "Benchmark on held-out regions, not just the same fields.",
    "Add human-in-loop checks and error-cost matrices.",
    "Open your data, document preprocessing and caveats.",
]

CLOSES = [
    "Skepticism is not cynicism—it's careful craft.",
    "I doubt, therefore I test; proceed with measured steps.",
    "Claim with evidence, and then we'll speak in trust.",
    "I question loud so your models whisper truth.",
]


def make_line(pool):
    return random.choice(pool)


def craft_poem(prompt: str, style_length: str = "short") -> str:
    seed = abs(hash(prompt)) % (2**32)
    random.seed(seed)

    poem_lines = []
    poem_lines.append(make_line(OPENERS))
    poem_lines.append(f"You asked: '{prompt.strip()}'")
    poem_lines.append(make_line(SKEPTIC_LINES))
    poem_lines.append(make_line(LIMITATIONS))

    if style_length == "short":
        poem_lines.append(make_line(SUGGESTIONS))
        poem_lines.append(make_line(CLOSES))
    elif style_length == "medium":
        poem_lines += [make_line(SUGGESTIONS) for _ in range(2)]
        poem_lines.append(make_line(CLOSES))
    else:
        poem_lines += [make_line(SUGGESTIONS) for _ in range(3)]
        poem_lines.append(make_line(CLOSES))

    return "\n".join(poem_lines)


def respond(user_input, length_choice):
    if not user_input.strip():
        return "Kelly remains silent; curiosity needs a prompt."
    return craft_poem(user_input, length_choice)


css = "footer {display:none}"

with gr.Blocks(css=css, title="Kelly — AI Scientist Poet") as demo:
    gr.Markdown(
        "# 🤖 Kelly — The AI Scientist Poet\n"
        "Ask any AI question below. Kelly replies in poetic skepticism."
    )

    with gr.Row():
        inp = gr.Textbox(label="Ask Kelly a question about AI", lines=3)
        length = gr.Radio(["short", "medium", "long"], value="short", label="Poem length")

    btn = gr.Button("Ask Kelly")
    out = gr.Textbox(label="Kelly replies (poem)", lines=10)

    btn.click(respond, inputs=[inp, length], outputs=out)

demo.launch()
