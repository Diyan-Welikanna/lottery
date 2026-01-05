from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lottery_results.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class LotteryResult(Base):
    __tablename__ = "lottery_results"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_name = Column(String, index=True)  # e.g., "sasiri", "kapruka"
    draw_number = Column(String, index=True)   # e.g., "867"
    draw_date = Column(DateTime, index=True)
    winning_numbers = Column(JSON)              # List of winning numbers
    prize_amount = Column(String)               # e.g., "Rs.200,000.00"
    additional_data = Column(JSON)              # Any extra data
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    class Config:
        from_attributes = True


class LotteryType(Base):
    __tablename__ = "lottery_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "sasiri"
    display_name = Column(String)                    # e.g., "SASIRI"
    board = Column(String)                           # "DLB" or "NLB"
    url = Column(String)                             # Scraping URL
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    
    # Add default lottery types for DLB and NLB
    db = SessionLocal()
    try:
        default_lotteries = [
            # DLB Lotteries
            {"name": "sasiri", "display_name": "SASIRI", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "kapruka", "display_name": "KAPRUKA", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "shanida", "display_name": "SHANIDA", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "super_ball", "display_name": "SUPER BALL", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "ada_kotipathi", "display_name": "ADA KOTIPATHI", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "jaya_sampatha", "display_name": "JAYA SAMPATHA", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "lagna_wasana", "display_name": "LAGNA WASANA", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            {"name": "supiri_dhana_sampatha", "display_name": "SUPIRI DHANA SAMPATHA", "board": "DLB", "url": "https://www.dlb.lk/result/en"},
            
            # NLB Lotteries
            {"name": "mahajana_sampatha", "display_name": "MAHAJANA SAMPATHA", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "vasana_sampatha", "display_name": "VASANA SAMPATHA", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "govisetha", "display_name": "GOVISETHA", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "supiri_wasana", "display_name": "SUPIRI WASANA", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "dhana_nidhanaya", "display_name": "DHANA NIDHANAYA", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "saturday_super_ball", "display_name": "SATURDAY SUPER BALL", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "sunday_mega_jackpot", "display_name": "SUNDAY MEGA JACKPOT", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "shanida_pattare", "display_name": "SHANIDA PATTARE", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
            {"name": "kotipathi_pattare", "display_name": "KOTIPATHI PATTARE", "board": "NLB", "url": "https://www.nlb.lk/English/results/"},
        ]
        
        for lottery in default_lotteries:
            exists = db.query(LotteryType).filter(LotteryType.name == lottery["name"]).first()
            if not exists:
                db.add(LotteryType(**lottery))
        
        db.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


def get_db():
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
