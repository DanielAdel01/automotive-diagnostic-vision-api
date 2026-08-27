from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/diagnostics",
    tags=["diagnostics"]
)

class DiagnosticData(BaseModel):
    rpm: int
    coolant_temperature: float
    battery_voltage: float
    dtc: str

class DiagnosticReceipt(BaseModel):
    message: str
    dtc: str

class DiagnosticAnalysis(BaseModel):
    dtc: str
    severity: str
    recommendation: str


def get_ai_recommendation(dtc: str, data: DiagnosticData) -> dict:
    severity = "low"
    reasons = []

    if data.coolant_temperature > 104:
        severity = "high"
        reasons.append("coolant temperature critically high")

    if data.battery_voltage < 11.8:
        severity = "medium" if severity == "low" else severity
        reasons.append("battery voltage below safe threshold")

    if data.rpm > 6000:
        severity = "high"
        reasons.append("RPM exceeds safe operating range")

    if not reasons:
        recommendation = "No immediate concerns detected. Continue normal monitoring."
    else:
        recommendation = f"Inspect: {', '.join(reasons)}."

    return {
        "dtc": dtc,
        "severity": severity,
        "recommendation": recommendation
    }


@router.post("", response_model=DiagnosticReceipt)
def receive_diagnostic(data: DiagnosticData):
    return {"message": "Diagnostic data received", "dtc": data.dtc}


@router.get("/{dtc}")
def get_diagnostic(dtc: str):
    return {"dtc": dtc, "message": f"Diagnostic information for {dtc}"}


@router.post("/{dtc}/analysis", response_model=DiagnosticAnalysis)
def analyze_dtc(dtc: str, data: DiagnosticData):
    return get_ai_recommendation(dtc, data)
