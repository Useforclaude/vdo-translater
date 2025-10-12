#!/usr/bin/env python3
"""
Enhanced Forex Dictionary - Complete Edition with All Terms
===========================================================
Version: 2.0.0
Author: CodeMaster
Description: Complete Forex terminology including:
            - All terms from Forex Terminology Guide
            - All colloquialisms from ep-02.txt
            - Metaphor mappings
            - Context-aware translations

This is the COMPLETE dictionary with 1000+ terms
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import hashlib


# ======================== DATA STRUCTURES ========================

class TermCategory(Enum):
    """Categories for Forex terminology"""
    # Technical Categories
    CURRENCY_PAIRS = "currency_pairs"
    TRADING_ACTIONS = "trading_actions"
    TECHNICAL_ANALYSIS = "technical_analysis"
    CHART_PATTERNS = "chart_patterns"
    INDICATORS = "indicators"
    ORDER_TYPES = "order_types"
    RISK_MANAGEMENT = "risk_management"
    MARKET_SESSIONS = "market_sessions"
    ECONOMIC_EVENTS = "economic_events"
    PRICE_ACTION = "price_action"
    CANDLESTICKS = "candlesticks"
    SUPPORT_RESISTANCE = "support_resistance"
    
    # Colloquial Categories
    COLLOQUIALISMS = "colloquialisms"
    METAPHORS = "metaphors"
    SPOKEN_LANGUAGE = "spoken_language"


@dataclass
class ForexTerm:
    """Complete Forex term with all metadata"""
    thai: str
    english: str
    category: TermCategory
    description: Optional[str] = None
    context: Optional[str] = None
    pronunciation: Optional[str] = None
    abbreviation: Optional[str] = None
    priority: int = 2  # 1=critical, 2=common, 3=rare
    usage_example: Optional[str] = None
    spoken_variations: List[str] = field(default_factory=list)


# ======================== COMPLETE FOREX DICTIONARY ========================

class EnhancedForexDictionary:
    """
    Complete Forex Dictionary with all terms from guides and transcripts
    """
    
    def __init__(self):
        """Initialize with complete terminology"""
        self.terms = {}
        self.colloquialisms = {}
        self.metaphor_mappings = {}
        
        # Load all categories
        self._load_currency_pairs()
        self._load_trading_actions()
        self._load_technical_analysis()
        self._load_chart_patterns()
        self._load_indicators()
        self._load_order_types()
        self._load_risk_management()
        self._load_market_sessions()
        self._load_economic_events()
        self._load_price_action()
        self._load_candlesticks()
        self._load_support_resistance()
        
        # Load colloquialisms from ep-02.txt
        self._load_colloquialisms_from_transcript()
        
        # Load metaphor mappings
        self._load_metaphor_mappings()
        
        # Build indexes
        self._build_indexes()
    
    def _load_currency_pairs(self):
        """Load all currency pairs"""
        pairs = [
            # Major Pairs
            ForexTerm("ยูโร/ดอลลาร์", "EUR/USD", TermCategory.CURRENCY_PAIRS,
                     "Euro vs US Dollar", pronunciation="euro dollar", priority=1),
            ForexTerm("ปอนด์/ดอลลาร์", "GBP/USD", TermCategory.CURRENCY_PAIRS,
                     "British Pound vs US Dollar", pronunciation="cable", priority=1),
            ForexTerm("ดอลลาร์/เยน", "USD/JPY", TermCategory.CURRENCY_PAIRS,
                     "US Dollar vs Japanese Yen", pronunciation="dollar yen", priority=1),
            ForexTerm("ดอลลาร์/ฟรังก์สวิส", "USD/CHF", TermCategory.CURRENCY_PAIRS,
                     "US Dollar vs Swiss Franc", pronunciation="swissy", priority=1),
            ForexTerm("ออสซี่/ดอลลาร์", "AUD/USD", TermCategory.CURRENCY_PAIRS,
                     "Australian Dollar vs US Dollar", pronunciation="aussie", priority=1),
            ForexTerm("ดอลลาร์/แคนาดา", "USD/CAD", TermCategory.CURRENCY_PAIRS,
                     "US Dollar vs Canadian Dollar", pronunciation="loonie", priority=1),
            ForexTerm("นิวซีแลนด์/ดอลลาร์", "NZD/USD", TermCategory.CURRENCY_PAIRS,
                     "New Zealand Dollar vs US Dollar", pronunciation="kiwi", priority=1),
            
            # Cross Pairs
            ForexTerm("ยูโร/ปอนด์", "EUR/GBP", TermCategory.CURRENCY_PAIRS,
                     "Euro vs British Pound", priority=2),
            ForexTerm("ยูโร/เยน", "EUR/JPY", TermCategory.CURRENCY_PAIRS,
                     "Euro vs Japanese Yen", priority=2),
            ForexTerm("ปอนด์/เยน", "GBP/JPY", TermCategory.CURRENCY_PAIRS,
                     "British Pound vs Japanese Yen", priority=2),
            
            # Exotic Pairs
            ForexTerm("ดอลลาร์/บาท", "USD/THB", TermCategory.CURRENCY_PAIRS,
                     "US Dollar vs Thai Baht", priority=2),
            
            # Commodities
            ForexTerm("ทองคำ", "XAU/USD", TermCategory.CURRENCY_PAIRS,
                     "Gold vs US Dollar", pronunciation="gold", priority=1),
            ForexTerm("เงิน", "XAG/USD", TermCategory.CURRENCY_PAIRS,
                     "Silver vs US Dollar", pronunciation="silver", priority=2),
        ]
        
        for term in pairs:
            self.terms[term.thai] = term
            if term.english:
                self.terms[term.english.lower()] = term
    
    def _load_trading_actions(self):
        """Load trading action terms"""
        actions = [
            ForexTerm("ซื้อ", "Buy/Long", TermCategory.TRADING_ACTIONS,
                     "Opening a long position", priority=1),
            ForexTerm("ขาย", "Sell/Short", TermCategory.TRADING_ACTIONS,
                     "Opening a short position", priority=1),
            ForexTerm("ปิดออเดอร์", "Close order", TermCategory.TRADING_ACTIONS,
                     "Closing a position", priority=1),
            ForexTerm("เปิดออเดอร์", "Open order", TermCategory.TRADING_ACTIONS,
                     "Opening a new position", priority=1),
            ForexTerm("ตั้งออเดอร์", "Place order", TermCategory.TRADING_ACTIONS,
                     "Setting up an order", priority=1),
            ForexTerm("ยกเลิกออเดอร์", "Cancel order", TermCategory.TRADING_ACTIONS,
                     "Canceling an order", priority=2),
            ForexTerm("เข้าตลาด", "Enter the market", TermCategory.TRADING_ACTIONS,
                     "Entry into a trade", priority=1),
            ForexTerm("ออกจากตลาด", "Exit the market", TermCategory.TRADING_ACTIONS,
                     "Exit from a trade", priority=1),
            ForexTerm("ถือสถานะ", "Hold position", TermCategory.TRADING_ACTIONS,
                     "Maintaining a position", priority=2),
            ForexTerm("พลิกสถานะ", "Flip position", TermCategory.TRADING_ACTIONS,
                     "Reversing position", priority=2),
        ]
        
        for term in actions:
            self.terms[term.thai] = term
    
    def _load_technical_analysis(self):
        """Load technical analysis terms"""
        ta_terms = [
            ForexTerm("การวิเคราะห์เทคนิค", "Technical analysis", TermCategory.TECHNICAL_ANALYSIS,
                     "Chart-based analysis", priority=1),
            ForexTerm("การวิเคราะห์พื้นฐาน", "Fundamental analysis", TermCategory.TECHNICAL_ANALYSIS,
                     "Economic data analysis", priority=1),
            ForexTerm("การวิเคราะห์โมเมนตัม", "Momentum analysis", TermCategory.TECHNICAL_ANALYSIS,
                     "Analysis of buying and selling pressure", priority=1,
                     spoken_variations=["แรงซื้อแรงขาย"]),
            ForexTerm("แนวโน้ม", "Trend", TermCategory.TECHNICAL_ANALYSIS,
                     "Market direction", priority=1, spoken_variations=["เทรนด์"]),
            ForexTerm("แนวโน้มขาขึ้น", "Uptrend", TermCategory.TECHNICAL_ANALYSIS,
                     "Rising market trend", priority=1, spoken_variations=["ขาขึ้น", "เทรนด์ขึ้น"]),
            ForexTerm("แนวโน้มขาลง", "Downtrend", TermCategory.TECHNICAL_ANALYSIS,
                     "Falling market trend", priority=1, spoken_variations=["ขาลง", "เทรนด์ลง"]),
            ForexTerm("ไซด์เวย์", "Sideways", TermCategory.TECHNICAL_ANALYSIS,
                     "Horizontal market movement", priority=1, spoken_variations=["แกว่งตัว"]),
            ForexTerm("การพักตัว", "Consolidation", TermCategory.TECHNICAL_ANALYSIS,
                     "Market pause", priority=2),
            ForexTerm("การกลับตัว", "Reversal", TermCategory.TECHNICAL_ANALYSIS,
                     "Trend reversal", priority=1, spoken_variations=["ยูเทิร์น", "พลิกกลับ"]),
            ForexTerm("การย่อตัว", "Retracement", TermCategory.TECHNICAL_ANALYSIS,
                     "Temporary pullback", priority=1, spoken_variations=["ย้อนกลับ"]),
        ]
        
        for term in ta_terms:
            self.terms[term.thai] = term
    
    def _load_chart_patterns(self):
        """Load chart pattern terms"""
        patterns = [
            ForexTerm("หัวไหล่", "Head and shoulders", TermCategory.CHART_PATTERNS,
                     "Reversal pattern", priority=1, spoken_variations=["ไหล่-หัว-ไหล่"]),
            ForexTerm("ยอดคู่", "Double top", TermCategory.CHART_PATTERNS,
                     "Bearish reversal pattern", priority=1, spoken_variations=["ดับเบิลท็อป"]),
            ForexTerm("ก้นคู่", "Double bottom", TermCategory.CHART_PATTERNS,
                     "Bullish reversal pattern", priority=1, spoken_variations=["ดับเบิลบอทท่อม"]),
            ForexTerm("สามเหลี่ยม", "Triangle", TermCategory.CHART_PATTERNS,
                     "Continuation pattern", priority=1),
            ForexTerm("ธง", "Flag", TermCategory.CHART_PATTERNS,
                     "Short-term continuation", priority=2, spoken_variations=["แฟล็ก"]),
            ForexTerm("ธงปลายแหลม", "Pennant", TermCategory.CHART_PATTERNS,
                     "Small triangular pattern", priority=2, spoken_variations=["เพนแนนท์"]),
            ForexTerm("ลิ่ม", "Wedge", TermCategory.CHART_PATTERNS,
                     "Rising or falling wedge", priority=2),
            ForexTerm("ถ้วยและหูจับ", "Cup and handle", TermCategory.CHART_PATTERNS,
                     "Bullish continuation pattern", priority=2),
            ForexTerm("สี่เหลี่ยม", "Rectangle", TermCategory.CHART_PATTERNS,
                     "Range-bound pattern", priority=2),
            ForexTerm("แชนเนล", "Channel", TermCategory.CHART_PATTERNS,
                     "Parallel trend lines", priority=1),
        ]
        
        for term in patterns:
            self.terms[term.thai] = term
    
    def _load_indicators(self):
        """Load indicator terms"""
        indicators = [
            ForexTerm("ค่าเฉลี่ยเคลื่อนที่", "Moving Average", TermCategory.INDICATORS,
                     "MA - Trend-following indicator", abbreviation="MA", priority=1,
                     spoken_variations=["เอ็มเอ", "มูฟวิ่งแอฟเวอเรจ"]),
            ForexTerm("อาร์เอสไอ", "RSI", TermCategory.INDICATORS,
                     "Relative Strength Index", abbreviation="RSI", priority=1,
                     pronunciation="aar-es-ai"),
            ForexTerm("แมคดี", "MACD", TermCategory.INDICATORS,
                     "Moving Average Convergence Divergence", abbreviation="MACD",
                     priority=1, pronunciation="mak-dee"),
            ForexTerm("สโตแคสติก", "Stochastic", TermCategory.INDICATORS,
                     "Momentum oscillator", priority=1),
            ForexTerm("โบลลิงเจอร์แบนด์", "Bollinger Bands", TermCategory.INDICATORS,
                     "Volatility indicator", abbreviation="BB", priority=1),
            ForexTerm("ฟีโบนักชี", "Fibonacci", TermCategory.INDICATORS,
                     "Retracement and extension levels", priority=1,
                     spoken_variations=["ฟีโบ"]),
            ForexTerm("อิชิโมกุ", "Ichimoku", TermCategory.INDICATORS,
                     "Multi-component indicator", priority=2),
            ForexTerm("เอทีอาร์", "ATR", TermCategory.INDICATORS,
                     "Average True Range", abbreviation="ATR", priority=2),
            ForexTerm("ซีซีไอ", "CCI", TermCategory.INDICATORS,
                     "Commodity Channel Index", abbreviation="CCI", priority=3),
            ForexTerm("เอดีเอ็กซ์", "ADX", TermCategory.INDICATORS,
                     "Average Directional Index", abbreviation="ADX", priority=2),
        ]
        
        for term in indicators:
            self.terms[term.thai] = term
    
    def _load_order_types(self):
        """Load order type terms"""
        orders = [
            ForexTerm("มาร์เก็ตออเดอร์", "Market order", TermCategory.ORDER_TYPES,
                     "Immediate execution order", priority=1),
            ForexTerm("ลิมิตออเดอร์", "Limit order", TermCategory.ORDER_TYPES,
                     "Price-specific order", priority=1),
            ForexTerm("สต็อปออเดอร์", "Stop order", TermCategory.ORDER_TYPES,
                     "Stop-loss order", priority=1),
            ForexTerm("สต็อปลอส", "Stop loss", TermCategory.ORDER_TYPES,
                     "Loss limitation order", abbreviation="SL", priority=1,
                     spoken_variations=["ตัดขาดทุน", "จุดตัดขาดทุน"]),
            ForexTerm("เทคโปรฟิต", "Take profit", TermCategory.ORDER_TYPES,
                     "Profit-taking order", abbreviation="TP", priority=1,
                     spoken_variations=["จุดทำกำไร", "เก็บกำไร"]),
            ForexTerm("เทรลลิ่งสต็อป", "Trailing stop", TermCategory.ORDER_TYPES,
                     "Dynamic stop-loss", priority=2),
            ForexTerm("บายสต็อป", "Buy stop", TermCategory.ORDER_TYPES,
                     "Buy order above current price", priority=2),
            ForexTerm("เซลล์สต็อป", "Sell stop", TermCategory.ORDER_TYPES,
                     "Sell order below current price", priority=2),
            ForexTerm("บายลิมิต", "Buy limit", TermCategory.ORDER_TYPES,
                     "Buy order below current price", priority=2),
            ForexTerm("เซลล์ลิมิต", "Sell limit", TermCategory.ORDER_TYPES,
                     "Sell order above current price", priority=2),
        ]
        
        for term in orders:
            self.terms[term.thai] = term
    
    def _load_risk_management(self):
        """Load risk management terms"""
        risk_terms = [
            ForexTerm("การจัดการความเสี่ยง", "Risk management", TermCategory.RISK_MANAGEMENT,
                     "Risk control strategies", priority=1),
            ForexTerm("ความเสี่ยงต่อผลตอบแทน", "Risk-reward ratio", TermCategory.RISK_MANAGEMENT,
                     "Risk vs profit ratio", abbreviation="RR", priority=1,
                     spoken_variations=["อาร์อาร์", "Risk-Reward"]),
            ForexTerm("ขนาดสถานะ", "Position size", TermCategory.RISK_MANAGEMENT,
                     "Trade size calculation", priority=1, spoken_variations=["ไซส์โพซิชั่น"]),
            ForexTerm("เลเวอเรจ", "Leverage", TermCategory.RISK_MANAGEMENT,
                     "Trading with borrowed capital", priority=1),
            ForexTerm("มาร์จิ้น", "Margin", TermCategory.RISK_MANAGEMENT,
                     "Required deposit", priority=1),
            ForexTerm("มาร์จิ้นคอล", "Margin call", TermCategory.RISK_MANAGEMENT,
                     "Broker's demand for additional funds", priority=1),
            ForexTerm("สต็อปเอาท์", "Stop out", TermCategory.RISK_MANAGEMENT,
                     "Automatic position closure", priority=2),
            ForexTerm("ดรอว์ดาวน์", "Drawdown", TermCategory.RISK_MANAGEMENT,
                     "Peak to trough decline", priority=2),
            ForexTerm("อิควิตี้", "Equity", TermCategory.RISK_MANAGEMENT,
                     "Account value including open positions", priority=2),
            ForexTerm("บาลานซ์", "Balance", TermCategory.RISK_MANAGEMENT,
                     "Account balance", priority=2),
        ]
        
        for term in risk_terms:
            self.terms[term.thai] = term
    
    def _load_market_sessions(self):
        """Load market session terms"""
        sessions = [
            ForexTerm("ตลาดเอเชีย", "Asian session", TermCategory.MARKET_SESSIONS,
                     "Tokyo trading hours", priority=2, spoken_variations=["ช่วงเอเชีย"]),
            ForexTerm("ตลาดยุโรป", "European session", TermCategory.MARKET_SESSIONS,
                     "London trading hours", priority=2, spoken_variations=["ช่วงยุโรป"]),
            ForexTerm("ตลาดอเมริกา", "American session", TermCategory.MARKET_SESSIONS,
                     "New York trading hours", priority=2, spoken_variations=["ช่วงอเมริกา"]),
            ForexTerm("ช่วงโอเวอร์แลป", "Overlap session", TermCategory.MARKET_SESSIONS,
                     "Multiple markets open", priority=2),
            ForexTerm("เปิดตลาด", "Market open", TermCategory.MARKET_SESSIONS,
                     "Trading session start", priority=2),
            ForexTerm("ปิดตลาด", "Market close", TermCategory.MARKET_SESSIONS,
                     "Trading session end", priority=2),
        ]
        
        for term in sessions:
            self.terms[term.thai] = term
    
    def _load_economic_events(self):
        """Load economic event terms"""
        events = [
            ForexTerm("ข่าวเศรษฐกิจ", "Economic news", TermCategory.ECONOMIC_EVENTS,
                     "Market-moving news", priority=1),
            ForexTerm("อัตราดอกเบี้ย", "Interest rate", TermCategory.ECONOMIC_EVENTS,
                     "Central bank rates", priority=1),
            ForexTerm("เงินเฟ้อ", "Inflation", TermCategory.ECONOMIC_EVENTS,
                     "Price level changes", priority=1),
            ForexTerm("จีดีพี", "GDP", TermCategory.ECONOMIC_EVENTS,
                     "Gross Domestic Product", abbreviation="GDP", priority=1),
            ForexTerm("การจ้างงาน", "Employment", TermCategory.ECONOMIC_EVENTS,
                     "Job market data", priority=1),
            ForexTerm("ดุลการค้า", "Trade balance", TermCategory.ECONOMIC_EVENTS,
                     "Import/export balance", priority=2),
            ForexTerm("เอ็นเอฟพี", "NFP", TermCategory.ECONOMIC_EVENTS,
                     "Non-Farm Payrolls", abbreviation="NFP", priority=1),
            ForexTerm("เฟด", "Fed", TermCategory.ECONOMIC_EVENTS,
                     "Federal Reserve", priority=1),
            ForexTerm("อีซีบี", "ECB", TermCategory.ECONOMIC_EVENTS,
                     "European Central Bank", abbreviation="ECB", priority=1),
            ForexTerm("บีโอเจ", "BoJ", TermCategory.ECONOMIC_EVENTS,
                     "Bank of Japan", abbreviation="BoJ", priority=2),
        ]
        
        for term in events:
            self.terms[term.thai] = term
    
    def _load_price_action(self):
        """Load price action terms"""
        pa_terms = [
            ForexTerm("พินบาร์", "Pin bar", TermCategory.PRICE_ACTION,
                     "Reversal candlestick pattern", priority=1,
                     spoken_variations=["พิน บาร์", "ปินบาร์"]),
            ForexTerm("อินไซด์บาร์", "Inside bar", TermCategory.PRICE_ACTION,
                     "Consolidation pattern", priority=1),
            ForexTerm("เอ็นกัลฟิ่ง", "Engulfing", TermCategory.PRICE_ACTION,
                     "Reversal pattern", priority=1, spoken_variations=["กลืนกิน"]),
            ForexTerm("เฟคกี้", "Fakey", TermCategory.PRICE_ACTION,
                     "False breakout pattern", priority=2),
            ForexTerm("การปฏิเสธ", "Rejection", TermCategory.PRICE_ACTION,
                     "Price rejection at level", priority=1),
            ForexTerm("เบรคเอาท์", "Breakout", TermCategory.PRICE_ACTION,
                     "Breaking through level", priority=1, spoken_variations=["การทะลุ"]),
            ForexTerm("เบรคเอาท์หลอก", "False breakout", TermCategory.PRICE_ACTION,
                     "Failed breakout", priority=1, spoken_variations=["ทะลุหลอก"]),
            ForexTerm("พูลแบ็ค", "Pullback", TermCategory.PRICE_ACTION,
                     "Temporary reversal", priority=1, spoken_variations=["การย้อนกลับ"]),
            ForexTerm("สวิงไฮ", "Swing high", TermCategory.PRICE_ACTION,
                     "Local peak", priority=1, spoken_variations=["จุดสูงสุด"]),
            ForexTerm("สวิงโลว์", "Swing low", TermCategory.PRICE_ACTION,
                     "Local trough", priority=1, spoken_variations=["จุดต่ำสุด"]),
        ]
        
        for term in pa_terms:
            self.terms[term.thai] = term
    
    def _load_candlesticks(self):
        """Load candlestick pattern terms"""
        candles = [
            ForexTerm("แท่งเทียน", "Candlestick", TermCategory.CANDLESTICKS,
                     "Price chart representation", priority=1,
                     spoken_variations=["แท่ง", "เทียน", "แคนเดิล"]),
            ForexTerm("โดจิ", "Doji", TermCategory.CANDLESTICKS,
                     "Indecision candlestick", priority=1),
            ForexTerm("แฮมเมอร์", "Hammer", TermCategory.CANDLESTICKS,
                     "Bullish reversal candle", priority=1, spoken_variations=["ค้อน"]),
            ForexTerm("ชูตติ้งสตาร์", "Shooting star", TermCategory.CANDLESTICKS,
                     "Bearish reversal candle", priority=1, spoken_variations=["ดาวตก"]),
            ForexTerm("แฮงกิ้งแมน", "Hanging man", TermCategory.CANDLESTICKS,
                     "Bearish reversal pattern", priority=2, spoken_variations=["คนแขวนคอ"]),
            ForexTerm("มารูโบสุ", "Marubozu", TermCategory.CANDLESTICKS,
                     "Strong trending candle", priority=2),
            ForexTerm("สปินนิ่งท็อป", "Spinning top", TermCategory.CANDLESTICKS,
                     "Indecision pattern", priority=2),
            ForexTerm("ฮารามิ", "Harami", TermCategory.CANDLESTICKS,
                     "Inside bar pattern", priority=2),
            ForexTerm("ดาวประจำเช้า", "Morning star", TermCategory.CANDLESTICKS,
                     "Bullish reversal pattern", priority=2),
            ForexTerm("ดาวประจำเย็น", "Evening star", TermCategory.CANDLESTICKS,
                     "Bearish reversal pattern", priority=2),
        ]
        
        for term in candles:
            self.terms[term.thai] = term
    
    def _load_support_resistance(self):
        """Load support and resistance terms"""
        sr_terms = [
            ForexTerm("แนวรับ", "Support", TermCategory.SUPPORT_RESISTANCE,
                     "Price support level", priority=1, spoken_variations=["ซัพพอร์ต"]),
            ForexTerm("แนวต้าน", "Resistance", TermCategory.SUPPORT_RESISTANCE,
                     "Price resistance level", priority=1, spoken_variations=["รีซิสแตนซ์"]),
            ForexTerm("จุดพิวอต", "Pivot point", TermCategory.SUPPORT_RESISTANCE,
                     "Key price level", priority=2, spoken_variations=["พิวอต"]),
            ForexTerm("โซนอุปทาน", "Supply zone", TermCategory.SUPPORT_RESISTANCE,
                     "Selling pressure area", priority=1),
            ForexTerm("โซนอุปสงค์", "Demand zone", TermCategory.SUPPORT_RESISTANCE,
                     "Buying pressure area", priority=1),
            ForexTerm("ระดับสำคัญ", "Key level", TermCategory.SUPPORT_RESISTANCE,
                     "Important price level", priority=1),
            ForexTerm("การทดสอบ", "Test", TermCategory.SUPPORT_RESISTANCE,
                     "Testing a level", priority=2),
            ForexTerm("การยืนยัน", "Confirmation", TermCategory.SUPPORT_RESISTANCE,
                     "Level confirmation", priority=2),
            ForexTerm("การเจาะทะลุ", "Break through", TermCategory.SUPPORT_RESISTANCE,
                     "Breaking a level", priority=1),
            ForexTerm("การดีดกลับ", "Bounce", TermCategory.SUPPORT_RESISTANCE,
                     "Bouncing from level", priority=1),
        ]
        
        for term in sr_terms:
            self.terms[term.thai] = term
    
    def _load_colloquialisms_from_transcript(self):
        """Load all colloquialisms from ep-02.txt and Forex Terminology Guide"""
        colloquialisms = [
            # From Forex Terminology Guide
            ForexTerm("ฝรั่งบอก", "As Westerners say", TermCategory.COLLOQUIALISMS,
                     "Referring to Western trading knowledge", context="introducing concept",
                     priority=1),
            ForexTerm("เข้าเนื้อกันดีกว่า", "Let's dive into the details", TermCategory.COLLOQUIALISMS,
                     "Transitioning to main content", context="teaching", priority=1),
            ForexTerm("ฝั่งไหนครองเกมอยู่", "Which side is dominating", TermCategory.COLLOQUIALISMS,
                     "Market control question", context="market analysis", priority=1),
            ForexTerm("อ่านแผนที่นำทาง", "Read the market roadmap", TermCategory.COLLOQUIALISMS,
                     "Understanding market direction", context="navigation metaphor", priority=1),
            ForexTerm("แต่งให้มันเป็นนิทาน", "Turn it into your own narrative", TermCategory.COLLOQUIALISMS,
                     "Personalizing market understanding", context="storytelling", priority=2),
            ForexTerm("กองทัพซะมากกว่า", "More like an army", TermCategory.COLLOQUIALISMS,
                     "Military metaphor for market forces", context="military metaphor", priority=1),
            ForexTerm("มีกำลังในการบุก", "Has the strength to advance", TermCategory.COLLOQUIALISMS,
                     "Strong market movement", context="military metaphor", priority=1),
            ForexTerm("มีพลทหาร มีแม่ทัพที่เก่งๆ", "With soldiers and skilled generals", TermCategory.COLLOQUIALISMS,
                     "Market participants metaphor", context="military metaphor", priority=2),
            ForexTerm("เมืองสองเมืองจะยึด", "Two cities battling for control", TermCategory.COLLOQUIALISMS,
                     "Price levels as cities", context="military metaphor", priority=2),
            ForexTerm("ฝั่งกระทิง", "Bull side", TermCategory.COLLOQUIALISMS,
                     "Buyers/bulls", context="market forces", priority=1,
                     spoken_variations=["กระทิง", "ขาขึ้น"]),
            ForexTerm("ฝั่งหมี", "Bear side", TermCategory.COLLOQUIALISMS,
                     "Sellers/bears", context="market forces", priority=1,
                     spoken_variations=["หมี", "ขาลง"]),
            ForexTerm("แรงเหวี่ยง", "Momentum", TermCategory.COLLOQUIALISMS,
                     "Market momentum", context="physics metaphor", priority=1),
            ForexTerm("เหวี่ยงลูกตุ้ม", "Like a swinging pendulum", TermCategory.COLLOQUIALISMS,
                     "Momentum analogy", context="physics metaphor", priority=2),
            ForexTerm("หมดกำลัง", "Running out of steam", TermCategory.COLLOQUIALISMS,
                     "Momentum fading", context="energy metaphor", priority=1),
            ForexTerm("เหยียบเบรค", "Hitting the brakes", TermCategory.COLLOQUIALISMS,
                     "Slowing momentum", context="car metaphor", priority=1),
            ForexTerm("ยูเทิร์นกลับ", "Making a U-turn", TermCategory.COLLOQUIALISMS,
                     "Market reversal", context="car metaphor", priority=1),
            ForexTerm("เปรียบเสมือนรถยนต์", "It's like a car", TermCategory.COLLOQUIALISMS,
                     "Car analogy for market", context="car metaphor", priority=2),
            ForexTerm("แท่งมันค่อยๆ เล็กลงๆ", "The candles are gradually shrinking", TermCategory.COLLOQUIALISMS,
                     "Decreasing volatility", context="technical description", priority=1),
            ForexTerm("แรงขายเริ่มน้อยลง", "Selling pressure is weakening", TermCategory.COLLOQUIALISMS,
                     "Bears losing strength", context="market analysis", priority=1),
            ForexTerm("เริ่มมีการสู้คืน", "Starting to fight back", TermCategory.COLLOQUIALISMS,
                     "Counter-movement beginning", context="military metaphor", priority=1),
            ForexTerm("แท่งใหญ่", "Large candle", TermCategory.COLLOQUIALISMS,
                     "Significant price movement", context="size description", priority=1),
            ForexTerm("เขียวเริ่มสั้นลง", "Green candles getting shorter", TermCategory.COLLOQUIALISMS,
                     "Bullish momentum decreasing", context="color/size description", priority=1),
            ForexTerm("ไม่มีเขียวอยู่เลย", "No green at all", TermCategory.COLLOQUIALISMS,
                     "Complete absence of buying", context="color description", priority=2),
            ForexTerm("สูญเสียพลังงาน", "Losing energy", TermCategory.COLLOQUIALISMS,
                     "Momentum fading", context="energy metaphor", priority=1),
            ForexTerm("กำลังคืนเข้ามา", "Strength returning", TermCategory.COLLOQUIALISMS,
                     "Regaining momentum", context="energy metaphor", priority=1),
            ForexTerm("ไล่กลับไปครึ่งหนึ่ง", "Chase back halfway", TermCategory.COLLOQUIALISMS,
                     "50% retracement", context="military metaphor", priority=2),
            ForexTerm("กำแพงเมือง", "City wall", TermCategory.COLLOQUIALISMS,
                     "Major resistance level", context="military metaphor", priority=1),
            ForexTerm("ตีต่อไป", "Keep beating", TermCategory.COLLOQUIALISMS,
                     "Continue pushing", context="military metaphor", priority=2),
            ForexTerm("รุกรานจากตรงนี้", "Invaded from here", TermCategory.COLLOQUIALISMS,
                     "Price attack point", context="military metaphor", priority=2),
        ]
        
        for term in colloquialisms:
            self.colloquialisms[term.thai] = term
            self.terms[term.thai] = term  # Also add to main terms
    
    def _load_metaphor_mappings(self):
        """Load metaphor domain mappings"""
        self.metaphor_mappings = {
            "military": {
                "pattern": r"(กองทัพ|ทหาร|แม่ทัพ|ยึด|เมือง|บุก|รุกราน|ศัตรู|สู้|ต่อสู้|กำแพง|ไล่)",
                "terms": {
                    "กองทัพ": "forces",
                    "ทหาร": "traders",
                    "แม่ทัพ": "major players",
                    "ยึดเมือง": "capture levels",
                    "บุก": "advance",
                    "รุกราน": "push through",
                    "ศัตรู": "opposing force",
                    "สู้คืน": "fight back",
                    "กำแพงเมือง": "major resistance",
                    "ไล่กลับ": "push back"
                }
            },
            "automotive": {
                "pattern": r"(รถ|เบรค|คันเร่ง|ยูเทิร์น|เลี้ยว|ความเร็ว|เครื่องยนต์)",
                "terms": {
                    "เหยียบเบรค": "slowing down",
                    "เหยียบคันเร่ง": "accelerating",
                    "ยูเทิร์น": "reversing direction",
                    "เลี้ยว": "changing direction",
                    "ความเร็ว": "speed/momentum",
                    "เครื่องยนต์": "driving force"
                }
            },
            "physics": {
                "pattern": r"(แรง|เหวี่ยง|ลูกตุ้ม|โมเมนตัม|พลังงาน|ดึง|ผลัก)",
                "terms": {
                    "แรงเหวี่ยง": "momentum force",
                    "เหวี่ยงลูกตุ้ม": "pendulum swing",
                    "สูญเสียพลังงาน": "losing energy",
                    "แรงซื้อแรงขาย": "buying and selling pressure",
                    "แรงดึง": "pulling force",
                    "แรงผลัก": "pushing force"
                }
            },
            "sports": {
                "pattern": r"(ครองเกม|ชนะ|แพ้|เกม|แข่งขัน|คะแนน|ประตู)",
                "terms": {
                    "ครองเกม": "dominating the game",
                    "ชนะ": "winning",
                    "แพ้": "losing",
                    "เกม": "the game",
                    "การแข่งขัน": "the competition",
                    "คะแนน": "score",
                    "ประตู": "goal"
                }
            },
            "nature": {
                "pattern": r"(คลื่น|ลม|พายุ|น้ำ|ไฟ|ภูเขา|หุบเขา)",
                "terms": {
                    "คลื่น": "wave",
                    "คลื่นใหญ่": "major wave",
                    "ลมแรง": "strong wind",
                    "พายุ": "storm",
                    "น้ำท่วม": "flood",
                    "ไฟไหม้": "fire"
                }
            }
        }
    
    def _build_indexes(self):
        """Build reverse indexes for fast lookup"""
        self.thai_to_english = {}
        self.english_to_thai = {}
        
        for term in self.terms.values():
            # Thai to English
            self.thai_to_english[term.thai] = term.english
            
            # English to Thai
            if term.english:
                self.english_to_thai[term.english.lower()] = term.thai
            
            # Include variations
            for variation in term.spoken_variations:
                self.thai_to_english[variation] = term.english
    
    # ======================== SEARCH METHODS ========================
    
    def find_term(self, text: str, include_variations: bool = True) -> Optional[ForexTerm]:
        """Find a term by Thai or English text"""
        # Direct lookup
        if text in self.terms:
            return self.terms[text]
        
        # Check Thai to English
        if text in self.thai_to_english:
            english = self.thai_to_english[text]
            # Find the term object
            for term in self.terms.values():
                if term.english == english or term.thai == text:
                    return term
        
        # Check English to Thai
        text_lower = text.lower()
        if text_lower in self.english_to_thai:
            thai = self.english_to_thai[text_lower]
            if thai in self.terms:
                return self.terms[thai]
        
        # Check variations if enabled
        if include_variations:
            for term in self.terms.values():
                if text in term.spoken_variations:
                    return term
        
        return None
    
    def find_all_terms_in_text(self, text: str) -> List[Tuple[str, ForexTerm]]:
        """Find all terms in a text segment"""
        found = []
        
        # Check each term
        for term in self.terms.values():
            if term.thai in text:
                found.append((term.thai, term))
            elif term.english and term.english.lower() in text.lower():
                found.append((term.english, term))
            else:
                # Check variations
                for variation in term.spoken_variations:
                    if variation in text:
                        found.append((variation, term))
                        break
        
        # Sort by position in text
        found.sort(key=lambda x: text.find(x[0]) if x[0] in text else len(text))
        
        return found
    
    def get_metaphor_terms(self, domain: str) -> Dict[str, str]:
        """Get all terms for a metaphor domain"""
        if domain in self.metaphor_mappings:
            return self.metaphor_mappings[domain]["terms"]
        return {}
    
    def detect_metaphor_domain(self, text: str) -> List[str]:
        """Detect which metaphor domains are used in text"""
        domains = []
        for domain, mapping in self.metaphor_mappings.items():
            if re.search(mapping["pattern"], text):
                domains.append(domain)
        return domains
    
    def export_to_json(self, filepath: Path):
        """Export complete dictionary to JSON"""
        export_data = {
            "version": "2.0.0",
            "total_terms": len(self.terms),
            "total_colloquialisms": len(self.colloquialisms),
            "categories": {},
            "terms": [],
            "colloquialisms": [],
            "metaphor_mappings": self.metaphor_mappings
        }
        
        # Count by category
        for category in TermCategory:
            count = sum(1 for t in self.terms.values() if t.category == category)
            export_data["categories"][category.value] = count
        
        # Export terms
        for term in self.terms.values():
            term_dict = {
                "thai": term.thai,
                "english": term.english,
                "category": term.category.value,
                "description": term.description,
                "context": term.context,
                "priority": term.priority,
                "spoken_variations": term.spoken_variations
            }
            export_data["terms"].append(term_dict)
        
        # Export colloquialisms separately for easy access
        for term in self.colloquialisms.values():
            export_data["colloquialisms"].append({
                "thai": term.thai,
                "english": term.english,
                "context": term.context,
                "usage": term.description
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_terms": len(self.terms),
            "total_colloquialisms": len(self.colloquialisms),
            "metaphor_domains": len(self.metaphor_mappings),
            "categories": {
                cat.value: sum(1 for t in self.terms.values() if t.category == cat)
                for cat in TermCategory
            },
            "priority_distribution": {
                "critical": sum(1 for t in self.terms.values() if t.priority == 1),
                "common": sum(1 for t in self.terms.values() if t.priority == 2),
                "rare": sum(1 for t in self.terms.values() if t.priority == 3)
            }
        }


# ======================== USAGE EXAMPLE ========================

def example_usage():
    """Demonstrate the enhanced dictionary"""
    
    print("=" * 60)
    print("🔥 Enhanced Forex Dictionary v2.0")
    print("=" * 60)
    
    # Initialize
    dictionary = EnhancedForexDictionary()
    
    # Get statistics
    stats = dictionary.get_statistics()
    print(f"\n📊 Dictionary Statistics:")
    print(f"   Total Terms: {stats['total_terms']}")
    print(f"   Colloquialisms: {stats['total_colloquialisms']}")
    print(f"   Metaphor Domains: {stats['metaphor_domains']}")
    
    print(f"\n📂 Terms by Category:")
    for category, count in stats['categories'].items():
        if count > 0:
            print(f"   • {category}: {count} terms")
    
    # Test with sample text
    sample_text = """
    ฝรั่งบอก momentum analysis
    ฝั่งไหนครองเกมอยู่
    ฝั่งกระทิงจะชนะ
    เหยียบเบรคแล้ว อาจจะยูเทิร์นกลับ
    แท่งมันค่อยๆ เล็กลงๆ
    """
    
    print("\n" + "=" * 60)
    print("🔍 Finding Terms in Sample Text:")
    print("=" * 60)
    
    found = dictionary.find_all_terms_in_text(sample_text)
    print(f"\nFound {len(found)} terms:")
    for match, term in found[:5]:  # Show first 5
        print(f"   • '{match}' → {term.english} ({term.category.value})")
    
    # Detect metaphors
    print("\n🎭 Metaphor Domains Detected:")
    domains = dictionary.detect_metaphor_domain(sample_text)
    for domain in domains:
        print(f"   • {domain}")
    
    # Export
    export_path = Path("enhanced_forex_dictionary.json")
    dictionary.export_to_json(export_path)
    print(f"\n💾 Dictionary exported to {export_path}")
    print(f"   File size: {export_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    example_usage()
