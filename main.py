from fastapi import FastAPI, Request
from storage import ContextStore
from engine import VeraEngine

app = FastAPI(
    title="Vera Bot",
    version="1.0.0",
    description="Merchant growth automation bot for Vera Challenge"
)

store = ContextStore()
engine = VeraEngine(store)


# Root Route (optional but useful)
@app.get("/")
async def root():
    return {
        "message": "Vera Bot is live",
        "status": "running"
    }


# Required Health Route
@app.get("/v1/healthz")
async def healthz():
    return {
        "status": "healthy"
    }


# Required Metadata Route
@app.get("/v1/metadata")
async def metadata():
    return {
        "bot_name": "Vera Bot",
        "version": "1.0.0",
        "owner": "Pagidi Kondala Bhavani",
        "capabilities": [
            "merchant context processing",
            "trigger campaign generation",
            "reply automation"
        ],
        "status": "live"
    }


# Required Context Route
@app.post("/v1/context")
async def context(request: Request):
    try:
        data = await request.json()

        scope = data.get("scope")
        context_id = data.get("context_id")
        payload = data.get("payload", {})

        store.save(scope, context_id, payload)

        return {
            "accepted": True,
            "context_id": context_id
        }

    except Exception as e:
        return {
            "accepted": False,
            "error": str(e)
        }


# Required Tick Route
@app.post("/v1/tick")
async def tick(request: Request):
    try:
        data = await request.json()

        merchant_id = data.get("merchant_id")
        trigger = data.get("trigger", {})

        return engine.compose(merchant_id, trigger)

    except Exception:
        return {
            "message": "Hi, shall I help grow your sales today?",
            "cta": "Show me",
            "send_as": "VERA",
            "suppression_key": "safe_default"
        }


# Required Reply Route
@app.post("/v1/reply")
async def reply(request: Request):
    try:
        data = await request.json()

        msg = data.get("message", "").lower()

        if "yes" in msg or "do it" in msg or "launch" in msg:
            return {
                "message": "Great! Launching this campaign now.",
                "cta": "View Results"
            }

        elif "no" in msg:
            return {
                "message": "No problem. Shall I suggest another idea?",
                "cta": "Suggest Option"
            }

        return {
            "message": "Would you like me to improve today's sales?",
            "cta": "Show Ideas"
        }

    except Exception:
        return {
            "message": "Reply received.",
            "cta": "Continue"
        }