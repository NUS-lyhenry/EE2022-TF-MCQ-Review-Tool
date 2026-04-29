#!/usr/bin/env python3
"""
EE2022 Concept Quiz - Streamlit UI version

Run:
    pip install streamlit
    streamlit run ee2022_concept_quiz_ui.py

Put this file in the same folder as ee2022_concept_quiz.py.
It imports the question bank from the command-line version.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import List

import streamlit as st

# Make local imports work when launched from another directory.
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

try:
    from ee2022_concept_quiz import QUESTIONS, MCQ_CHOICE_EXPLANATIONS, Question
except Exception as exc:  # pragma: no cover
    st.error(
        "Could not import ee2022_concept_quiz.py. Put this UI file in the same "
        "folder as ee2022_concept_quiz.py.\n\n"
        f"Import error: {exc}"
    )
    st.stop()


st.set_page_config(
    page_title="EE2022 Concept Quiz",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.block-container { padding-top: 1.5rem; max-width: 1200px; }
.quiz-card {
    border: 1px solid rgba(127,127,127,0.25);
    border-radius: 18px;
    padding: 1.25rem 1.35rem;
    background: rgba(127,127,127,0.06);
    margin-bottom: 1rem;
}
.topic-pill {
    display: inline-block;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    background: rgba(255, 193, 7, 0.18);
    border: 1px solid rgba(255, 193, 7, 0.35);
    font-size: 0.85rem;
    margin-bottom: 0.55rem;
}
.question-text { font-size: 1.28rem; line-height: 1.55; font-weight: 650; }
.small-muted { color: #777; font-size: 0.92rem; }
.result-box {
    border-radius: 14px;
    padding: 0.95rem 1rem;
    margin: 0.75rem 0;
}
.correct-box { background: rgba(46, 160, 67, 0.13); border: 1px solid rgba(46, 160, 67, 0.35); }
.wrong-box { background: rgba(248, 81, 73, 0.12); border: 1px solid rgba(248, 81, 73, 0.35); }
.explain-box { background: rgba(56, 139, 253, 0.10); border: 1px solid rgba(56, 139, 253, 0.28); }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state() -> None:
    defaults = {
        "quiz_started": False,
        "quiz_questions": [],
        "current_index": 0,
        "submitted": False,
        "selected_answer": None,
        "answers": [],  # list of dicts: question, selected, correct
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def question_type_label(kind: str) -> str:
    return "True / False" if kind == "tf" else "Multiple Choice"


def valid_options(q: Question) -> List[tuple[str, str]]:
    if q.kind == "tf":
        return [("T", "True"), ("F", "False")]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return [(letters[i], choice) for i, choice in enumerate(q.choices or [])]


def build_pool(selected_topics: List[str], qtype: str) -> List[Question]:
    pool = [q for q in QUESTIONS if q.topic in selected_topics]
    if qtype == "True/False only":
        pool = [q for q in pool if q.kind == "tf"]
    elif qtype == "MCQ only":
        pool = [q for q in pool if q.kind == "mcq"]
    return pool


def start_quiz(pool: List[Question], n: int, seed: int | None) -> None:
    rng = random.Random(seed)
    questions = pool[:]
    rng.shuffle(questions)
    st.session_state.quiz_questions = questions[:n]
    st.session_state.current_index = 0
    st.session_state.submitted = False
    st.session_state.selected_answer = None
    st.session_state.answers = []
    st.session_state.quiz_started = True


def reset_quiz() -> None:
    st.session_state.quiz_started = False
    st.session_state.quiz_questions = []
    st.session_state.current_index = 0
    st.session_state.submitted = False
    st.session_state.selected_answer = None
    st.session_state.answers = []


def submit_current_answer(q: Question) -> None:
    selected = st.session_state.get("selected_answer")
    if not selected:
        st.warning("Choose an answer first.")
        return
    correct = selected == q.answer
    st.session_state.submitted = True

    # Avoid duplicate recording if user presses Submit repeatedly.
    if len(st.session_state.answers) == st.session_state.current_index:
        st.session_state.answers.append(
            {"question": q, "selected": selected, "correct": correct}
        )


def next_question() -> None:
    st.session_state.current_index += 1
    st.session_state.submitted = False
    st.session_state.selected_answer = None


def answer_text(q: Question, letter: str) -> str:
    if q.kind == "tf":
        return "True" if letter == "T" else "False"
    choices = q.choices or []
    idx = ord(letter) - ord("A")
    return choices[idx] if 0 <= idx < len(choices) else letter


def render_question(q: Question, idx: int, total: int) -> None:
    st.progress((idx) / total)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.metric("Question", f"{idx + 1}/{total}")
    with c2:
        score = sum(1 for a in st.session_state.answers if a["correct"])
        st.metric("Score so far", f"{score}/{len(st.session_state.answers)}")
    with c3:
        st.metric("Type", question_type_label(q.kind))

    st.markdown(
        f"""
        <div class="quiz-card">
            <div class="topic-pill">{q.topic}</div>
            <div class="question-text">{q.prompt}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = valid_options(q)
    radio_options = [f"{letter}. {text}" for letter, text in options]
    letter_from_label = {f"{letter}. {text}": letter for letter, text in options}

    disabled = st.session_state.submitted
    chosen_label = st.radio(
        "Choose your answer",
        radio_options,
        index=None,
        key=f"radio_{idx}",
        disabled=disabled,
    )
    if chosen_label is not None and not disabled:
        st.session_state.selected_answer = letter_from_label[chosen_label]

    left, right = st.columns([1, 4])
    with left:
        st.button(
            "Submit",
            type="primary",
            disabled=st.session_state.submitted,
            on_click=submit_current_answer,
            args=(q,),
            use_container_width=True,
        )
    with right:
        if st.session_state.submitted:
            is_last = idx == total - 1
            label = "Finish quiz" if is_last else "Next question"
            if st.button(label, use_container_width=False):
                if is_last:
                    st.session_state.current_index = total
                else:
                    next_question()
                st.rerun()

    if st.session_state.submitted:
        selected = st.session_state.answers[idx]["selected"]
        correct = selected == q.answer
        if correct:
            st.markdown(
                "<div class='result-box correct-box'>✅ <b>Correct.</b></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='result-box wrong-box'>❌ <b>Wrong.</b></div>",
                unsafe_allow_html=True,
            )
            st.write(f"**Your answer:** {selected}. {answer_text(q, selected)}")
            st.write(f"**Correct answer:** {q.answer}. {answer_text(q, q.answer)}")

            if q.kind == "mcq":
                wrong_reason = MCQ_CHOICE_EXPLANATIONS.get(q.prompt, {}).get(selected)
                if wrong_reason:
                    st.markdown(
                        f"<div class='result-box wrong-box'><b>Why your option is wrong:</b><br>{wrong_reason}</div>",
                        unsafe_allow_html=True,
                    )

        st.markdown(
            f"<div class='result-box explain-box'><b>Explanation:</b><br>{q.explanation}</div>",
            unsafe_allow_html=True,
        )


def render_summary() -> None:
    answers = st.session_state.answers
    total = len(st.session_state.quiz_questions)
    score = sum(1 for a in answers if a["correct"])
    pct = 100 * score / total if total else 0

    st.title("Quiz summary")
    st.metric("Final score", f"{score}/{total}", f"{pct:.1f}%")
    st.progress(score / total if total else 0)

    wrong = [a for a in answers if not a["correct"]]
    if not wrong:
        st.success("Perfect score. Nice work.")
    else:
        st.subheader("Review wrong answers")
        for i, item in enumerate(wrong, 1):
            q = item["question"]
            selected = item["selected"]
            with st.expander(f"{i}. [{q.topic}] {q.prompt}", expanded=True):
                st.write(f"**Your answer:** {selected}. {answer_text(q, selected)}")
                st.write(f"**Correct answer:** {q.answer}. {answer_text(q, q.answer)}")
                if q.kind == "mcq":
                    wrong_reason = MCQ_CHOICE_EXPLANATIONS.get(q.prompt, {}).get(selected)
                    if wrong_reason:
                        st.warning(f"Why your option is wrong: {wrong_reason}")
                st.info(q.explanation)

    if st.button("Start a new quiz", type="primary"):
        reset_quiz()
        st.rerun()


init_state()

st.title("⚡ EE2022 Concept Quiz")
st.caption("Exam-style conceptual True/False and MCQ practice. No long calculations.")

all_topics = sorted(set(q.topic for q in QUESTIONS))

with st.sidebar:
    st.header("Quiz setup")
    selected_topics = st.multiselect(
        "Topics",
        all_topics,
        default=all_topics,
        help="Choose one or more topics to include.",
    )
    qtype = st.radio(
        "Question type",
        ["All", "True/False only", "MCQ only"],
        horizontal=False,
    )
    pool = build_pool(selected_topics or all_topics, qtype)
    max_n = max(1, len(pool))
    n = st.slider("Number of questions", 1, max_n, min(20, max_n))
    use_seed = st.toggle("Use fixed shuffle seed", value=False)
    seed = st.number_input("Seed", value=2022, step=1, disabled=not use_seed)

    st.write(f"Available questions: **{len(pool)}**")
    start_disabled = len(pool) == 0
    if st.button("Start / restart quiz", type="primary", disabled=start_disabled, use_container_width=True):
        start_quiz(pool, n, int(seed) if use_seed else None)
        st.rerun()

    if st.button("Reset", use_container_width=True):
        reset_quiz()
        st.rerun()

    st.divider()
    st.markdown(
        "**Tip:** For MCQ, if you choose a wrong option, the app explains why that specific option is wrong."
    )

if not st.session_state.quiz_started:
    st.info("Choose your topics and click **Start / restart quiz** in the sidebar.")

    cols = st.columns(3)
    with cols[0]:
        st.metric("Total questions", len(QUESTIONS))
    with cols[1]:
        st.metric("Topics", len(all_topics))
    with cols[2]:
        st.metric("Question styles", "TF + MCQ")

    st.subheader("Included topics")
    st.write(", ".join(all_topics))
else:
    questions = st.session_state.quiz_questions
    idx = st.session_state.current_index
    if idx >= len(questions):
        render_summary()
    else:
        render_question(questions[idx], idx, len(questions))
