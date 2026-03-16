from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from dotenv import load_dotenv

# ==============================
# LOAD ENV
# ==============================


app = FastAPI(title="Electricity Bill Predictor")

# ==============================
# CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# GLOBALS
# ==============================
MODEL = None
SCALER = None
Y_SCALER = None

# ==============================
# LOAD MODEL
# ==============================
@app.on_event("startup")
def load_ai():
    global MODEL, SCALER, Y_SCALER
    try:
        MODEL = load_model("model.h5", compile=False)
        SCALER = joblib.load("scaler.save")
        Y_SCALER = joblib.load("y_scaler.save")

        print("✅ Model Loaded")
    except Exception as e:
        print("❌ Model load error:", e)

# ==============================
# INPUT SCHEMA
# ==============================
class Appliance(BaseModel):
    watt: float
    quantity: int
    hours: float

class PredictionInput(BaseModel):
    appliances: list[Appliance]
    bhk: int
    usage_change_percent: float = 0   # ⭐ NEXT MONTH FACTOR

class ChatInput(BaseModel):
    message: str

# ==============================
# FEATURE CREATION
# ==============================
def create_features(appliances):
    total_energy = 0

    for a in appliances:
        total_energy += (a.watt * a.quantity * a.hours) / 1000

    kitchen = total_energy * 0.35
    laundry = total_energy * 0.30
    heavy = total_energy * 0.35
    usage_hours = min(total_energy, 24)

    return np.array([[kitchen, laundry, heavy, usage_hours]])

# ==============================
# TNEB BILL CALCULATION
# ==============================
def tneb_bill(units):

    units = max(units, 0)

    if units <= 100:
        return 0

    bill = 0
    remaining = units - 100

    slab = min(remaining, 100)
    bill += slab * 2.25
    remaining -= slab
    if remaining <= 0:
        return bill

    slab = min(remaining, 200)
    bill += slab * 4.5
    remaining -= slab
    if remaining <= 0:
        return bill

    slab = min(remaining, 100)
    bill += slab * 6
    remaining -= slab
    if remaining <= 0:
        return bill

    slab = min(remaining, 100)
    bill += slab * 8
    remaining -= slab
    if remaining <= 0:
        return bill

    slab = min(remaining, 200)
    bill += slab * 9
    remaining -= slab
    if remaining <= 0:
        return bill

    slab = min(remaining, 200)
    bill += slab * 10
    remaining -= slab
    if remaining <= 0:
        return bill

    bill += remaining * 11
    return bill

# ==============================
# HEALTH
# ==============================
@app.get("/health")
def health():
    return {"status": "Backend Running ✅"}

# ==============================
# PREDICTION API
# ==============================
@app.post("/predict")
def predict(data: PredictionInput):

    if MODEL is None or SCALER is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # --------------------------
        # Feature creation
        # --------------------------
        X = create_features(data.appliances)
        kitchen, laundry, heavy, _ = X[0]

        manual_daily = kitchen + laundry + heavy

        if manual_daily <= 0:
            return {
                "daily_units": 0,
                "monthly_units": 0,
                "estimated_bill": 0,
                "next_month_bill": 0
            }

        # --------------------------
        # Scale
        # --------------------------
        X_scaled = SCALER.transform(X)

        # --------------------------
        # AI Prediction
        # --------------------------
        raw_ai = float(
            MODEL.predict(X_scaled, verbose=0)[0][0]
        )

        ai_correction = np.tanh(raw_ai) * 0.15

        # --------------------------
        # Hybrid Energy
        # --------------------------
        daily_units = manual_daily * (1 + ai_correction)

        daily_units = np.clip(
            daily_units,
            manual_daily * 0.7,
            manual_daily * 1.5
        )

        monthly_units = max(daily_units * 30, 120)

        bill = tneb_bill(monthly_units)

        if bill <= 0:
            bill = monthly_units * 2.25

        # --------------------------
        # Next month forecast using usage_change_percent
        # --------------------------
        # usage_change_percent = +15  -> 15% increase
        # usage_change_percent = -10 -> 10% decrease
        next_month_units = monthly_units * (1 + data.usage_change_percent / 100.0)
        next_month_bill = tneb_bill(next_month_units)

        # --------------------------
        # Response for current frontend
        # --------------------------
        return {
            "manual_daily_units": round(manual_daily, 2),
            "daily_units": round(daily_units, 2),
            "monthly_units": round(monthly_units, 2),
            "estimated_bill": round(bill, 2),

            "next_month_units": round(next_month_units, 2),
            "next_month_bill": round(next_month_bill, 2),

            "ai_adjustment_%": round(ai_correction * 100, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =====================================
# CHAT API
# =====================================
@app.post("/chat")
async def chat(data: ChatInput):
    if not data.message or not data.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    msg = data.message.lower().strip()

    if "save electricity" in msg or "save energy" in msg:
        reply = (
            "⚡ Turn off unused appliances, use LED bulbs, and unplug chargers when not in use. "
            "Using 5-star appliances can reduce electricity usage a lot."
        )
    elif "ac" in msg:
        reply = (
            "❄️ Set your AC to 24–26°C, clean the filter regularly, and keep doors closed. "
            "This can help reduce power consumption."
        )
    elif "fan" in msg:
        reply = (
            "💨 BLDC fans consume much less electricity than regular fans. "
            "Using them can save a good amount every month."
        )
    elif "fridge" in msg or "refrigerator" in msg:
        reply = (
            "🧊 Keep the fridge door closed properly, avoid frequent opening, "
            "and set medium cooling for better efficiency."
        )
    elif "light" in msg or "bulb" in msg:
        reply = (
            "💡 Use LED bulbs instead of incandescent bulbs. "
            "LED bulbs use much less electricity and last longer."
        )
    else:
        reply = (
            "🤖 Try using LED lights, BLDC fans, inverter ACs, and 5-star appliances. "
            "Also switch off devices when not needed to save electricity."
        )

    return {"reply": reply}

# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)