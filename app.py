import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from database import (init_db, insert_customer, get_customer, get_all_customers,
                       get_stats, update_customer)

load_dotenv()

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        return "Name and Email are required.", 400

    company = request.form.get("company", "").strip()
    need = request.form.get("need", "").strip()
    budget = request.form.get("budget", "").strip()
    timeline = request.form.get("timeline", "").strip()
    notes = request.form.get("notes", "").strip()

    customer_id = insert_customer(name, email, company, need, budget,
                                  timeline, notes)

    try:
        from ai_service import analyze_customer
        result = analyze_customer(name, email, company, need, budget,
                                  timeline, notes)

        from database import update_customer
        update_customer(customer_id,
                        intent_level=result["intent_level"],
                        intent_reason=result["intent_reason"],
                        ai_analysis=result["ai_analysis"],
                        email_draft=result["email_draft"],
                        follow_up_date=result["follow_up_date"])
    except Exception as e:
        print(f"AI analysis error: {e}")

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/dashboard")
def dashboard():
    intent_filter = request.args.get("intent", "")
    if intent_filter not in ("High", "Medium", "Low"):
        intent_filter = ""
    customers = get_all_customers(intent_filter or None)
    stats = get_stats()
    return render_template("dashboard.html", customers=customers,
                           stats=stats, current_filter=intent_filter)


@app.route("/customer/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer(customer_id)
    if not customer:
        return "Customer not found.", 404
    return render_template("customer.html", customer=customer)


@app.route("/export")
def export_csv():
    import csv
    import io
    from flask import Response

    customers = get_all_customers()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Company", "Need", "Budget",
                     "Timeline", "Notes", "Intent Level", "AI Analysis",
                     "Email Draft", "Follow-up Date", "Created At"])
    for c in customers:
        writer.writerow([
            c["id"], c["name"], c["email"], c["company"], c["need"],
            c["budget"], c["timeline"], c["notes"], c["intent_level"],
            c["ai_analysis"], c["email_draft"], c["follow_up_date"],
            c["created_at"]
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=customers.csv"}
    )


@app.route("/generate-demo", methods=["POST"])
def generate_demo():
    import random
    from datetime import datetime, timedelta

    demos = [
        {
            "name": "Sarah Johnson",
            "email": "sarah@acmecorp.com",
            "company": "Acme Corp",
            "need": "Need AI-powered customer support automation for 200+ agents. Currently handling 5000+ tickets/day manually.",
            "budget": "$80K-$120K annually",
            "timeline": "Within 2 months",
            "notes": "Referred by partner. Already using Salesforce."
        },
        {
            "name": "Mike Chen",
            "email": "mike@techstart.io",
            "company": "TechStart Inc",
            "need": "Looking for AI chatbot solution for our SaaS platform. Need multi-language support.",
            "budget": "$20K-$30K",
            "timeline": "Q3 this year",
            "notes": ""
        },
        {
            "name": "Emma Williams",
            "email": "emma@globalretail.com",
            "company": "Global Retail Group",
            "need": "Interested in AI data analytics for supply chain optimization.",
            "budget": "Not defined yet",
            "timeline": "Exploring options, no rush",
            "notes": "Met at industry conference."
        },
        {
            "name": "David Park",
            "email": "david@fintechpro.com",
            "company": "FinTech Pro",
            "need": "Need AI compliance checking solution for financial transactions. Security is top priority.",
            "budget": "$150K+",
            "timeline": "ASAP - regulatory deadline in 3 months",
            "notes": "Urgent. Has board approval."
        },
        {
            "name": "Lisa Wang",
            "email": "lisa@healthfirst.com",
            "company": "HealthFirst Medical",
            "need": "Looking for AI appointment scheduling and patient triage system.",
            "budget": "$50K-$70K",
            "timeline": "Next quarter",
            "notes": ""
        },
        {
            "name": "Tom Baker",
            "email": "tom@localbiz.org",
            "company": "LocalBiz Solutions",
            "need": "Just browsing AI options for small business automation.",
            "budget": "Under $5K",
            "timeline": "No specific timeline",
            "notes": "Small team of 5."
        },
        {
            "name": "Anna Kowalski",
            "email": "anna@ecommercepro.eu",
            "company": "E-Commerce Pro EU",
            "need": "AI recommendation engine for 2M+ product catalog. Need integration with existing stack.",
            "budget": "€60K-€90K",
            "timeline": "Before holiday season",
            "notes": "European market focus. GDPR compliance required."
        },
        {
            "name": "James Liu",
            "email": "james@devstudio.cn",
            "company": "DevStudio",
            "need": "Want to embed AI code review into our CI/CD pipeline.",
            "budget": "$15K",
            "timeline": "1-2 months",
            "notes": ""
        },
    ]

    for demo in demos:
        customer_id = insert_customer(
            demo["name"], demo["email"], demo["company"],
            demo["need"], demo["budget"], demo["timeline"], demo["notes"]
        )

        try:
            from ai_service import analyze_customer
            result = analyze_customer(
                demo["name"], demo["email"], demo["company"],
                demo["need"], demo["budget"], demo["timeline"],
                demo["notes"]
            )
            update_customer(customer_id,
                          intent_level=result["intent_level"],
                          intent_reason=result["intent_reason"],
                          ai_analysis=result["ai_analysis"],
                          email_draft=result["email_draft"],
                          follow_up_date=result["follow_up_date"])
        except Exception as e:
            # If AI fails, assign random intent for demo purposes
            intent = random.choice(["High", "Medium", "Low"])
            update_customer(customer_id, intent_level=intent,
                          intent_reason="Demo data (no AI analysis)")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("Starting AI Consultation Assistant...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(debug=False, host="0.0.0.0", port=port)
