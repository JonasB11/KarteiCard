import os
import random
from datetime import datetime, timezone

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


db = SQLAlchemy()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(120), nullable=False, default="Allgemein")
    times_seen = db.Column(db.Integer, nullable=False, default=0)
    times_correct = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def success_rate(self):
        if self.times_seen == 0:
            return 0
        return round((self.times_correct / self.times_seen) * 100)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://karteicard:karteicard@db:3306/karteicard",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        category = request.args.get("category", "").strip()
        query = Card.query
        if category:
            query = query.filter(Card.category == category)

        cards = query.order_by(Card.created_at.desc()).all()
        categories = [
            row[0]
            for row in db.session.query(Card.category)
            .filter(Card.category != "")
            .distinct()
            .order_by(Card.category.asc())
            .all()
        ]
        stats = {
            "total": Card.query.count(),
            "categories": len(categories),
            "learned": db.session.query(func.coalesce(func.sum(Card.times_seen), 0)).scalar(),
            "correct": db.session.query(func.coalesce(func.sum(Card.times_correct), 0)).scalar(),
        }
        return render_template("index.html", cards=cards, categories=categories, active_category=category, stats=stats)

    @app.route("/cards", methods=["POST"])
    def create_card():
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        category = request.form.get("category", "").strip() or "Allgemein"

        if not question or not answer:
            flash("Bitte fülle Frage und Antwort aus.", "error")
            return redirect(url_for("index"))

        db.session.add(Card(question=question, answer=answer, category=category))
        db.session.commit()
        flash("Karte gespeichert.", "success")
        return redirect(url_for("index"))

    @app.route("/cards/<int:card_id>/delete", methods=["POST"])
    def delete_card(card_id):
        card = db.get_or_404(Card, card_id)
        db.session.delete(card)
        db.session.commit()
        flash("Karte gelöscht.", "success")
        return redirect(url_for("index"))

    @app.route("/cards/<int:card_id>/result", methods=["POST"])
    def record_result(card_id):
        card = db.get_or_404(Card, card_id)
        result = request.form.get("result")
        card.times_seen += 1
        if result == "correct":
            card.times_correct += 1
        db.session.commit()
        return redirect(request.form.get("next") or url_for("learn"))

    @app.route("/learn")
    def learn():
        category = request.args.get("category", "").strip()
        query = Card.query
        if category:
            query = query.filter(Card.category == category)

        cards = query.order_by(Card.times_seen.asc(), Card.updated_at.asc()).all()
        card = cards[0] if cards else None
        categories = [row[0] for row in db.session.query(Card.category).distinct().order_by(Card.category.asc()).all()]
        return render_template("learn.html", card=card, categories=categories, active_category=category)

    @app.route("/quiz")
    def quiz():
        cards = Card.query.all()
        if len(cards) < 2:
            return render_template("quiz.html", question_card=None, options=[], needs_more=True)

        question_card = random.choice(cards)
        wrong_options = [card.answer for card in cards if card.id != question_card.id]
        options = random.sample(wrong_options, k=min(3, len(wrong_options)))
        options.append(question_card.answer)
        random.shuffle(options)
        return render_template("quiz.html", question_card=question_card, options=options, needs_more=False)

    @app.route("/quiz/<int:card_id>/answer", methods=["POST"])
    def answer_quiz(card_id):
        card = db.get_or_404(Card, card_id)
        selected = request.form.get("answer", "")
        card.times_seen += 1
        if selected == card.answer:
            card.times_correct += 1
            flash("Richtig beantwortet.", "success")
        else:
            flash(f"Nicht ganz. Die richtige Antwort war: {card.answer}", "error")
        db.session.commit()
        return redirect(url_for("quiz"))

    return app


app = create_app()
