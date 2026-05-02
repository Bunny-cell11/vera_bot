from fastapi import FastAPI, Request
from storage import ContextStore
from engine import VeraEngine

app = FastAPI()

store = ContextStore()
engine = VeraEngine(store)


@app.get("/")
async def root():
    return {"message": "Vera Bot Live"}


@app.get("/v1/healthz")
async def healthz():
    return {"status": "healthy"}


@app.get("/v1/metadata")
async def metadata():
    return {
        "bot_name": "Vera Bot",
        "version": "10.0",
        "author": "Bhavani",
        "capabilities": [
            "merchant growth",
            "deterministic decisions",
            "category intelligence",
            "reply automation"
        ]
    }


@app.post("/v1/context")
async def context(request: Request):
    data = await request.json()

    scope = data.get("scope")
    context_id = data.get("context_id")
    payload = data.get("payload", {})
    version = data.get("version", 1)

    store.save(scope, context_id, payload, version)

    return {
        "accepted": True,
        "ack_id": f"ack_{context_id}_{version}"
    }


@app.post("/v1/tick")
async def tick(request: Request):
    data = await request.json()

    merchant_id = data.get("merchant_id")
    trigger = data.get("trigger", {})
    customer = data.get("customer")

    return engine.compose(merchant_id, trigger, customer)


@app.post("/v1/reply")
async def reply(request: Request):
    data = await request.json()

    merchant_id = data.get("merchant_id", "unknown")
    msg = data.get("message", "").lower()

    store.remember_reply(merchant_id, msg)

    if "yes" in msg or "do it" in msg or "launch" in msg:
        return {
            "message": "Great. Launching this now.",
            "cta": "View Results"
        }

    if "no" in msg:
        return {
            "message": "No problem. Want a better offer instead?",
            "cta": "Show Better Option"
        }

    if "later" in msg:
        return {
            "message": "Understood. I'll remind you at a better time.",
            "cta": "Okay"
        }

    return {
        "message": "Would you like a better campaign idea?",
        "cta": "Show Ideas"
    }