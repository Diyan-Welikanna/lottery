from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import os

from database import get_db, LotteryResult, LotteryType, init_db
from scraper import run_scraper

# Initialize FastAPI app
app = FastAPI(
    title="Sri Lankan Lottery Results API",
    description="API for scraping and serving lottery results from NLB and DLB",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API responses
class LotteryTypeResponse(BaseModel):
    id: int
    name: str
    display_name: str
    board: str
    is_active: int
    
    class Config:
        from_attributes = True


class LotteryResultResponse(BaseModel):
    id: int
    lottery_name: str
    draw_number: Optional[str] = None  # Allow None values
    draw_date: datetime
    winning_numbers: List
    prize_amount: Optional[str] = None
    scraped_at: datetime
    
    class Config:
        from_attributes = True


class VerifyTicketRequest(BaseModel):
    lottery_name: str
    ticket_numbers: List[str]
    draw_number: Optional[str] = None
    draw_date: Optional[str] = None


class VerifyTicketResponse(BaseModel):
    is_winner: bool
    matched_numbers: List[str]
    lottery_name: str
    draw_number: str
    draw_date: datetime
    prize_info: Optional[str]


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized")


# API Endpoints

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "message": "Sri Lankan Lottery Results API",
        "version": "1.0.0",
        "endpoints": {
            "lotteries": "/api/lotteries",
            "latest_results": "/api/results/latest",
            "results_by_lottery": "/api/results/{lottery_name}",
            "verify_ticket": "/api/verify",
            "trigger_scrape": "/api/scrape"
        }
    }


@app.get("/api/lotteries", response_model=List[LotteryTypeResponse])
async def get_lotteries(db: Session = Depends(get_db)):
    """Get all available lottery types"""
    lotteries = db.query(LotteryType).filter(LotteryType.is_active == 1).all()
    return lotteries


@app.get("/api/results/latest", response_model=List[LotteryResultResponse])
async def get_latest_results(
    limit: int = Query(10, ge=1, le=100),
    board: Optional[str] = Query(None, description="Filter by board: DLB or NLB"),
    db: Session = Depends(get_db)
):
    """Get latest lottery results across all lotteries"""
    query = db.query(LotteryResult).order_by(LotteryResult.draw_date.desc())
    
    if board:
        # Join with lottery_types to filter by board
        lottery_types = db.query(LotteryType).filter(LotteryType.board == board.upper()).all()
        lottery_names = [lt.name for lt in lottery_types]
        query = query.filter(LotteryResult.lottery_name.in_(lottery_names))
    
    results = query.limit(limit).all()
    return results


@app.get("/api/results/{lottery_name}", response_model=List[LotteryResultResponse])
async def get_results_by_lottery(
    lottery_name: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get results for a specific lottery"""
    results = db.query(LotteryResult).filter(
        LotteryResult.lottery_name == lottery_name.lower()
    ).order_by(LotteryResult.draw_date.desc()).limit(limit).all()
    
    if not results:
        raise HTTPException(status_code=404, detail=f"No results found for lottery: {lottery_name}")
    
    return results


@app.get("/api/results/date/{date}", response_model=List[LotteryResultResponse])
async def get_results_by_date(
    date: str,
    db: Session = Depends(get_db)
):
    """Get results for a specific date (format: YYYY-MM-DD)"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        next_day = target_date + timedelta(days=1)
        
        results = db.query(LotteryResult).filter(
            LotteryResult.draw_date >= target_date,
            LotteryResult.draw_date < next_day
        ).all()
        
        return results
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


@app.post("/api/verify", response_model=VerifyTicketResponse)
async def verify_ticket(
    request: VerifyTicketRequest,
    db: Session = Depends(get_db)
):
    """Verify if ticket numbers match winning numbers"""
    
    # Find the appropriate draw result
    query = db.query(LotteryResult).filter(
        LotteryResult.lottery_name == request.lottery_name.lower()
    )
    
    if request.draw_number:
        query = query.filter(LotteryResult.draw_number == request.draw_number)
    elif request.draw_date:
        target_date = datetime.strptime(request.draw_date, "%Y-%m-%d")
        next_day = target_date + timedelta(days=1)
        query = query.filter(
            LotteryResult.draw_date >= target_date,
            LotteryResult.draw_date < next_day
        )
    else:
        # Use latest draw if no specific draw specified
        query = query.order_by(LotteryResult.draw_date.desc())
    
    result = query.first()
    
    if not result:
        raise HTTPException(status_code=404, detail="No matching lottery draw found")
    
    # Check for matching numbers
    winning_numbers = [str(num) for num in result.winning_numbers]
    ticket_numbers = [str(num) for num in request.ticket_numbers]
    matched_numbers = list(set(ticket_numbers) & set(winning_numbers))
    
    is_winner = len(matched_numbers) > 0
    
    return VerifyTicketResponse(
        is_winner=is_winner,
        matched_numbers=matched_numbers,
        lottery_name=result.lottery_name,
        draw_number=result.draw_number,
        draw_date=result.draw_date,
        prize_info=result.prize_amount if is_winner else None
    )


@app.post("/api/scrape")
async def trigger_scrape():
    """Manually trigger the scraper to fetch latest results"""
    try:
        saved_count = run_scraper()
        return {
            "status": "success",
            "message": f"Scraper completed. Saved {saved_count} new results.",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraper error: {str(e)}")


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    total_results = db.query(LotteryResult).count()
    total_lotteries = db.query(LotteryType).filter(LotteryType.is_active == 1).count()
    
    latest_scrape = db.query(LotteryResult).order_by(
        LotteryResult.scraped_at.desc()
    ).first()
    
    return {
        "total_results": total_results,
        "total_lotteries": total_lotteries,
        "latest_scrape": latest_scrape.scraped_at if latest_scrape else None,
        "database_url": os.getenv("DATABASE_URL", "sqlite:///./lottery_results.db")
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)
