from fastapi import FastAPI, Request
from storage import ContextStore
from engine import VeraEngine
import re

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
        "version": "100.0",
        "author": "Bhavani",
        "capabilities": [
            "merchant growth",
            "trigger intelligence",
            "reply automation",
            "slot booking",
            "anti loop",
            "terminal intent detection"
        ]
    }


@app.post("/v1/context")
async def context(request: Request):
    data = await request.json()

    store.save(
        data.get("scope"),
        data.get("context_id"),
        data.get("payload", {}),
        data.get("version", 1)
    )

    return {"accepted": True}


@app.post("/v1/tick")
async def tick(request: Request):
    data = await request.json()

    return engine.compose(
        data.get("merchant_id"),
        data.get("trigger", {}),
        data.get("customer")
    )


@app.post("/v1/reply")
async def reply(request: Request):
    data = await request.json()

    merchant_id = data.get("merchant_id", "unknown")
    msg = data.get("message", "").lower().strip()

    last = store.get_last_reply(merchant_id)

    # duplicate protection
    if msg == last:
        return {
            "action": "end",
            "message": "Closing repeated thread."
        }

    # booking first
    booking_words = [
        "book", "schedule", "appointment",
        "wed", "mon", "tue", "thu", "fri",
        "sat", "sun", "am", "pm", ":"
    ]

    if any(word in msg for word in booking_words):
        store.remember_reply(merchant_id, msg)

        slot = re.findall(r'(\d.*)', msg)
        slot_text = slot[0] if slot else msg

        return {
            "action": "book",
            "message": f"Booked successfully for {slot_text}"
        }

    # stop / terminal
    terminal_words = [
        "stop",
        "unsubscribe",
        "not interested",
        "leave me",
        "never"
    ]

    if msg == "no" or any(word in msg for word in terminal_words):
        return {
            "action": "end",
            "message": "Conversation ended."
        }

    # positive
    positive_words = [
        "yes", "sure", "ok", "okay",
        "launch", "start", "do it"
    ]

    if any(word in msg for word in positive_words):
        store.remember_reply(merchant_id, msg)

        return {
            "action": "launch",
            "message": "Great. Launching this now."
        }

    store.remember_reply(merchant_id, msg)

    return {
        "action": "ask",
        "message": "Would you like me to launch this now?"
    }