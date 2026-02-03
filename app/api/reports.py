from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.ai.llm_engine import generate_ai_insights
from app.ai.recommendations import build_recommendations
from app.ai.benchmarking import benchmark_cost
from app.services.report_generator import create_pdf

router = APIRouter()


@router.post("/generate")
def generate_full_report(payload: dict):
    try:
        ai_text = generate_ai_insights(payload, payload.get("language", "en"))

        benchmark_msg = benchmark_cost(
            payload.get("expense_ratio", 0),
            payload.get("industry", "small_business")
        )

        recommendations = build_recommendations(
            payload.get("health_score", 50),
            payload.get("risks", []),
            payload.get("credit_metrics", {}),
            benchmark_msg
        )

        pdf = create_pdf(
            "financial_report.pdf",
            payload,
            recommendations
        )

        body = {
            "ai_summary": ai_text,
            "recommendations": recommendations,
            "pdf_report": pdf
        }

        return JSONResponse(content=body, headers={"Access-Control-Allow-Origin": "*"})
    except Exception as e:
        err_body = {"detail": "Failed to generate report", "error": str(e)}
        return JSONResponse(status_code=500, content=err_body, headers={"Access-Control-Allow-Origin": "*"})

