
"""
import json
from routing_agent import classify_complexity, select_model
from thinking_agent import allocate_thinking_budget
from embedding_agent import embedding_agent
from bedrock_client import invoke_nova
from dynamo_cache import save_to_cache
from utils import floats_to_decimal
from carbon_agent import predict_energy_cost, compute_actual_energy

def lambda_handler(event, context):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # USER ROUTES
    if path == "/users/me" and method == "GET":
        return handle_get_me(event)

    if path.startswith("/teams/") and method == "GET":
        team_id = path.split("/")[2]
        return handle_get_team(event, team_id)

    # ADMIN ROUTES
    if path == "/admin/overview" and method == "GET":
        return handle_admin_overview(event)

    if path == "/admin/leaderboard" and method == "GET":
        return handle_admin_leaderboard(event)

    # EXISTING PUBLIC ROUTE
    if path == "/ask":
        return handle_ask(event)

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Route not found"})
    }

    def require_admin(claims):
        groups = claims.get("cognito:groups", [])
        return "Admin" in groups

    def handle_get_me(event):
        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

        user_id = claims.get("sub")
        email = claims.get("email")

        # placeholder stats
        stats = {
            "messages_sent": 42,
            "total_energy_used_kwh": 1.2,
            "total_energy_saved_kwh": 0.4,
            "efficiency_score": 33.2,
        }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "user_id": user_id,
                "email": email,
                "stats": stats
            })
        }

    def handle_get_team(event, team_id):

        team_stats = {
            "team_id": team_id,
            "members": 14,
            "total_savings_kwh": 12.4,
            "ranking": 3,
        }

        return {
            "statusCode": 200,
            "body": json.dumps(team_stats)
        }

    def handle_admin_overview(event):
        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

        if not require_admin(claims):
            return {"statusCode": 403, "body": "Admins only"}

        org_stats = {
            "total_users": 120,
            "total_teams": 9,
            "total_carbon_saved_kg": 0.321,
            "top_team": "Team Alpha",
        }

        return {
            "statusCode": 200,
            "body": json.dumps(org_stats)
        }

    def handle_admin_leaderboard(event):
        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

        if not require_admin(claims):
            return {"statusCode": 403, "body": "Admins only"}

        leaderboard = [
            {"team": "Team Alpha", "kwh_saved": 52.3},
            {"team": "Team Beta", "kwh_saved": 41.2},
            {"team": "Team Gamma", "kwh_saved": 33.1},
        ]

        return {
            "statusCode": 200,
            "body": json.dumps(leaderboard)
        }

    # actual backend code block
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    prompt = body["prompt"]

    # 1. Embedding + cache
    emb_result = embedding_agent(prompt)

    if emb_result["cached"]:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "content-type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "response": emb_result["response"],
                "modelUsed": emb_result["modelUsed"],
                "cached": True,
                "energy_used_kwh": 0,
                "energy_saved_kwh": 0,
                "carbon_used_kg": 0,
                "carbon_saved_kg": 0,
                "carbon": {
                    "predicted_kwh": 0,
                    "predicted_co2": 0,
                    "actual_kwh": 0,
                    "actual_co2": 0
                }
            })
        }

    # 2. Classification
    complexity = classify_complexity(prompt)

    # 3. Select model
    model = select_model(complexity)

    # 4. Thinking budget
    max_tokens = allocate_thinking_budget(complexity)

    # 5. Carbon prediction
    predicted_carbon = predict_energy_cost(model, max_tokens)

    # 6. Invoke Bedrock
    response = invoke_nova(model, prompt, max_tokens)

    # 7. Compute actual carbon
    output_tokens = len(response.split())
    actual_carbon = compute_actual_energy(model, output_tokens)

    # 8. Save cache
    embedding_decimal = floats_to_decimal(emb_result["embedding"])
    save_to_cache(prompt, embedding_decimal, response, model)

    # 9. Return FULL PAYLOAD
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "content-type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps({
            "response": response,
            "modelUsed": model,
            "complexity": complexity,
            "cached": False,
           "energy_used_kwh": actual_carbon["predicted_kwh"],
            "energy_saved_kwh": max(0, predicted_carbon["predicted_kwh"] - actual_carbon["predicted_kwh"]),
            "carbon_used_kg": actual_carbon["predicted_co2"],
            "carbon_saved_kg": max(0, predicted_carbon["predicted_co2"] - actual_carbon["predicted_co2"]),

            "carbon": {
                "predicted_kwh": predicted_carbon["predicted_kwh"],
                "predicted_co2": predicted_carbon["predicted_co2"],
                "actual_kwh": actual_carbon["predicted_kwh"],
                "actual_co2": actual_carbon["predicted_co2"]
            }
        })
    }
"""

import json
from routing_agent import classify_complexity, select_model
from thinking_agent import allocate_thinking_budget
from embedding_agent import embedding_agent
from bedrock_client import invoke_nova
from dynamo_cache import save_to_cache
from utils import floats_to_decimal
from carbon_agent import predict_energy_cost, compute_actual_energy
from eco_rewrite_agent import optimize_prompt
from coach_agent import analyze_prompt
from carbon_forecast_agent import compute_forecast
from eco_plan_agent import generate_plan


CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    # "Access-Control-Allow-Headers": "content-type,Authorization",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
}

# def handle_forecast(event):
#     body = json.loads(event["body"])

#     messages = body.get("messages", 0)
#     avg_tokens = body.get("avg_tokens", 0)
#     cache_hits = body.get("cache_hits", 0)

#     features = np.array([[messages, avg_tokens, cache_hits]], dtype=float)

#     prediction = float(forecast_model.predict(features)[0])

#     return {
#         "statusCode": 200,
#         "headers": CORS_HEADERS,
#         "body": json.dumps({
#             "predicted_kwh": prediction,
#             "predicted_co2": prediction * 0.475,  # rough emission factor
#         })
#     }


def handle_plan(event):
    body = json.loads(event["body"])
    prompt = body.get("prompt", "")

    if not prompt:
        return {
            "statusCode": 400,
            "headers": cors(),
            "body": json.dumps({"error": "Prompt required"})
        }

    plan = generate_plan(prompt)

    return {
        "statusCode": 200,
        "headers": cors(),
        "body": json.dumps({
            "plan": plan,
            "steps": len(plan)
        })
    }


def handle_optimize(event):
    body = json.loads(event["body"])
    prompt = body.get("prompt", "")

    if not prompt:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Prompt is required"})
        }

    optimized, savings_kwh, savings_co2 = optimize_prompt(prompt)

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "original": prompt,
            "optimized": optimized,
            "energy_savings_kwh": savings_kwh,
            "co2_savings_kg": savings_co2
        })
    }

# =========================
#   AUTH HELPERS
# =========================

def require_admin(claims):
    groups = claims.get("cognito:groups", [])
    return "Admin" in groups


# =========================
#   ROUTE HANDLERS
# =========================

def handle_get_me(event):
    claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

    user_id = claims.get("sub")
    email = claims.get("email")

    stats = {
        "messages_sent": 42,
        "total_energy_used_kwh": 1.2,
        "total_energy_saved_kwh": 0.4,
        "efficiency_score": 33.2,
    }

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "user_id": user_id,
            "email": email,
            "stats": stats
        })
    }


def handle_get_team(event, team_id):
    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "team_id": team_id,
            "members": 14,
            "total_savings_kwh": 12.4,
            "ranking": 3,
        })
    }


def handle_admin_overview(event):
    claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

    if not require_admin(claims):
        return {"statusCode": 403, "body": "Admins only"}

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "total_users": 120,
            "total_teams": 9,
            "total_carbon_saved_kg": 0.321,
            "top_team": "Team Alpha",
        })
    }


def handle_admin_leaderboard(event):
    claims = event["requestContext"]["authorizer"]["jwt"]["claims"]

    if not require_admin(claims):
        return {"statusCode": 403, "body": "Admins only"}

    leaderboard = [
        {"team": "Team Alpha", "kwh_saved": 52.3},
        {"team": "Team Beta", "kwh_saved": 41.2},
        {"team": "Team Gamma", "kwh_saved": 33.1},
    ]

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(leaderboard)
    }


# =========================
#   PUBLIC /ask ENDPOINT
# =========================

def handle_ask(event):
    body = json.loads(event["body"])
    prompt = body["prompt"]

    # Optional: Eco-Plan Mode support
    plan = body.get("plan")

    if plan:
        # Inject plan into the system prompt before routing
        plan_text = json.dumps(plan, indent=2)
        prompt = f"### Follow this plan before answering:\n{plan_text}\n\n### Final user request:\n{prompt}"


    emb_result = embedding_agent(prompt)


    # If cached, short-circuit
    if emb_result["cached"]:
        return {
            "statusCode": 200,
            "headers": cors(),
            "body": json.dumps({
                "response": emb_result["response"],
                "modelUsed": emb_result["modelUsed"],
                "cached": True,
                "energy_used_kwh": 0,
                "energy_saved_kwh": 0,
                "carbon_used_kg": 0,
                "carbon_saved_kg": 0,
            })
        }

    # Routing
    complexity = classify_complexity(prompt)
    model = select_model(complexity)
    max_tokens = allocate_thinking_budget(complexity)

    predicted_carbon = predict_energy_cost(model, max_tokens)
    response = invoke_nova(model, prompt, max_tokens)

    output_tokens = len(response.split())
    actual_carbon = compute_actual_energy(model, output_tokens)

    embedding_decimal = floats_to_decimal(emb_result["embedding"])
    save_to_cache(prompt, embedding_decimal, response, model)


    return {
        "statusCode": 200,
        "headers": cors(),
        "body": json.dumps({
            "response": response,
            "modelUsed": model,
            "complexity": complexity,
            "cached": False,
            "carbon": {
                "predicted_kwh": predicted_carbon["predicted_kwh"],
                "actual_kwh": actual_carbon["predicted_kwh"],
                "predicted_co2": predicted_carbon["predicted_co2"],
                "actual_co2": actual_carbon["predicted_co2"]
            },

            "energy_used_kwh": actual_carbon["predicted_kwh"],
            "energy_saved_kwh": max(0, predicted_carbon["predicted_kwh"] - actual_carbon["predicted_kwh"]),

            "carbon_used_kg": actual_carbon["predicted_co2"],
            "carbon_saved_kg": max(0, predicted_carbon["predicted_co2"] - actual_carbon["predicted_co2"]),

        })
    }

# def handle_ask(event):
#     body = json.loads(event.get("body") or "{}")

#     prompt = body.get("prompt")
#     plan = body.get("plan")

#     if not prompt:
#         return {
#             "statusCode": 400,
#             "headers": cors(),
#             "body": json.dumps({"error": "Missing prompt"})
#         }

#     # 🧠 Inject Eco-Plan if present
#     if plan:
#         plan_text = json.dumps(plan, indent=2)
#         prompt = (
#             "### Follow this plan step-by-step before answering:\n"
#             f"{plan_text}\n\n"
#             "### Final user request:\n"
#             f"{prompt}"
#         )

#     # 🔍 1️⃣ Check cache FIRST (no embedding yet)
#     emb_result = embedding_agent(prompt)

#     if emb_result["cached"]:   # whatever your cache lookup function is

#         return {
#             "statusCode": 200,
#             "headers": cors(),
#             "body": json.dumps({
#                 "response": cached["response"],
#                 "modelUsed": cached["model"],
#                 "cached": True,
#                 "energy_used_kwh": 0,
#                 "energy_saved_kwh": cached.get("energy_saved_kwh", 0),
#                 "carbon_used_kg": 0,
#                 "carbon_saved_kg": cached.get("carbon_saved_kg", 0),
#             })
#         }

#     # 🔢 2️⃣ Only now compute embedding
#     emb_result = embedding_agent(prompt)

#     # 🧭 3️⃣ Route model
#     complexity = classify_complexity(prompt)
#     model = select_model(complexity)
#     max_tokens = allocate_thinking_budget(complexity)


#     # 🌱 4️⃣ Predict energy
#     predicted_carbon = predict_energy_cost(model, max_tokens)

#     # 🤖 5️⃣ Generate response
#     response = invoke_nova(model, prompt, max_tokens)

#     output_tokens = len(response.split())
#     actual_carbon = compute_actual_energy(model, output_tokens)

#     # 💾 6️⃣ Save to cache
#     save_to_cache(
#         prompt,
#         floats_to_decimal(emb_result["embedding"]),
#         response,
#         model
#     )

#     return {
#         "statusCode": 200,
#         "headers": cors(),
#         "body": json.dumps({
#             "response": response,
#             "modelUsed": model,
#             "complexity": complexity,
#             "cached": False,
#             "carbon": {
#                 "predicted_kwh": predicted_carbon["predicted_kwh"],
#                 "actual_kwh": actual_carbon["predicted_kwh"],
#                 "predicted_co2": predicted_carbon["predicted_co2"],
#                 "actual_co2": actual_carbon["predicted_co2"]
#             },
#             "energy_used_kwh": actual_carbon["predicted_kwh"],
#             "energy_saved_kwh": max(
#                 0,
#                 predicted_carbon["predicted_kwh"] - actual_carbon["predicted_kwh"]
#             ),
#             "carbon_used_kg": actual_carbon["predicted_co2"],
#             "carbon_saved_kg": max(
#                 0,
#                 predicted_carbon["predicted_co2"] - actual_carbon["predicted_co2"]
#             )
#         })
#     }

# =========================
#   MAIN ROUTER
# =========================

def lambda_handler(event, context):

    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
            },
            "body": ""
        }
    
    # Authenticated routes
    if path == "/users/me" and method == "GET":
        return handle_get_me(event)

    if path.startswith("/teams/") and method == "GET":
        team_id = path.split("/")[2]
        return handle_get_team(event, team_id)

    if path == "/admin/overview" and method == "GET":
        return handle_admin_overview(event)

    if path == "/admin/leaderboard" and method == "GET":
        return handle_admin_leaderboard(event)

    if path == "/optimize" and method == "POST":
        return handle_optimize(event)

    if path == "/forecast" and method == "POST":
        return handle_forecast(event)

    if path == "/plan" and method == "POST":
        return handle_plan(event)


    if path == "/coach" and method == "POST":
        body = json.loads(event["body"])
        prompt = body.get("prompt", "")

        result = analyze_prompt(prompt)

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(result)
        }

    # Public
    if path == "/ask":
        return handle_ask(event)

    # 404
    return {
        "statusCode": 404,
        "body": json.dumps({"error": f"Route not found: {path}"})
    }


# Utility
def cors():
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    }



