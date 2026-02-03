from fastapi import FastAPI
from app.core.logging import setup_logging
from app.api import auth, upload, analytics, forecast, recommendations, reports, risk, credit, tax, working_capital, bookkeeping, payments
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models import user  # Import models to register them

def create_app():
    app = FastAPI(
        title="Financial Health Assessment AI",
        description="AI-powered financial health platform for SMEs",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_logging()

    @app.on_event("startup")
    def startup():
        # Create all database tables
        Base.metadata.create_all(bind=engine)

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
    app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
    app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
    app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
    app.include_router(reports.router, prefix="/reports", tags=["Reports"])
    app.include_router(risk.router, prefix="/risk", tags=["Risk"])
    app.include_router(credit.router, prefix="/credit", tags=["Credit Scoring"])
    app.include_router(tax.router, prefix="/tax", tags=["Tax Compliance"])
    app.include_router(working_capital.router, prefix="/working-capital", tags=["Working Capital"])
    app.include_router(bookkeeping.router, prefix="/bookkeeping", tags=["Bookkeeping"])
    app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])

    @app.get("/")
    def health():
        return {
            "status": "Backend running",
            "version": "1.0.0",
            "features": [
                "Authentication",
                "Financial Health Scoring",
                "Risk Detection",
                "Cashflow Forecasting",
                "Credit Scoring with Loan Products",
                "Tax Compliance Analysis",
                "Working Capital Optimization",
                "Bookkeeping & Accounting",
                "Multilingual Support"
            ]
        }

    return app

app = create_app()
