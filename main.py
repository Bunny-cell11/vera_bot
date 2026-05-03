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
        "version": "95.0",
        "author": "Bhavani",
        "capabilities": [
            "merchant growth",
            "trigger intelligence",
            "reply automation",
            "anti loop",
            "booking handling",
            "terminal intent detection"
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
    msg = data.get("message", "").strip().lower()

    last = store.get_last_reply(merchant_id)

    # STOP / hostile / no
    terminal_words = [
        "stop", "unsubscribe", "leave me",
        "not interested", "no thanks",
        "don't message", "dont message",
        "never", "no"
    ]

    if any(word in msg for word in terminal_words):
        store.remember_reply(merchant_id, msg)
        return {
            "action": "end",
            "message": "Understood. Conversation closed."
        }

    # prevent loops
    if msg == last:
        return {
            "action": "end",
            "message": "Closing duplicate conversation."
        }

    # booking intent
    booking_words = [
        "book", "schedule", "appointment",
        "tomorrow", "today", "monday",
        "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday",
        "am", "pm"
    ]

    if any(word in msg for word in booking_words):
        store.remember_reply(merchant_id, msg)
        return {
            "action": "book",
            "message": "Booked successfully. Confirmation shared."
        }

    # positive intent
    positive_words = [
        "yes", "sure", "ok", "okay",
        "interested", "launch", "do it",
        "start", "proceed"
    ]

    if any(word in msg for word in positive_words):
        store.remember_reply(merchant_id, msg)
        return {
            "action": "launch",
            "message": "Great. Launching this now."
        }

    # ask once
    store.remember_reply(merchant_id, msg)

    return {
        "action": "ask",
        "message": "Would you like me to launch this offer now?"
    }