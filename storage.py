   data.get("customer")
    )


@app.post("/v1/reply")
async def reply(request: Request):
    data = await request.json()

    merchant_id = data.get("merchant_id", "unknown")
    msg = data.get("message", "").lower().strip()

    last = store.get_last_reply(merchant_id)

    # STOP / terminal
    if any(x in msg for x in [
        "stop", "no", "not interested",
        "unsubscribe", "leave me", "never"
    ]):
        return {"action": "end", "message": "Conversation ended."}

    # duplicate loop prevention
    if msg == last:
        return {"action": "end", "message": "Closing repeated thread."}

    # booking detection
    if any(x in msg for x in [
        "book", "schedule", "appointment",
        "wed", "mon", "tue", "thu", "fri",
        "am", "pm", ":"
    ]):
        store.remember_reply(merchant_id, msg)

        slot = re.findall(r'(\d.*)', msg)
        slot_text = slot[0] if slot else msg

        return {
            "action": "book",
            "message": f"Booked successfully for {slot_text}"
        }

    # positive intent
    if any(x in msg for x in [
        "yes", "sure", "ok", "okay",
        "launch", "start", "do it"
    ]):
        store.remember_reply(merchant_id, msg)
        return {
            "action": "launch",
            "message": "Great. Launching this now."
        }

    store.remember_reply(merchant_id, msg)

    return {
        "action": "ask",
        "message": "Would you like me to launch this now?"
    