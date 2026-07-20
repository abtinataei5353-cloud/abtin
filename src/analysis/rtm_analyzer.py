"""تجزیه کننده مفاهیم RTM (Read The Market)

RTM یک روش تجزیه بازار است که بر اساس:
- Base: تجمع قیمت در یک منطقه
- Decision: تصمیم بازار برای حرکت
- Rally: حرکت بالا
- Drop: حرکت پایین
- Flag Limit: تلفات محدود
- Quasimodo: بازگشت سریع
- و... مفاهیم دیگر
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from src.config.logger_config import Logger

logger = Logger.get_logger(__name__)


class RTMPhase(Enum):
    """مراحل RTM"""
    BASE = "base"  # تجمع
    DECISION = "decision"  # تصمیم
    RALLY = "rally"  # حرکت بالا
    DROP = "drop"  # حرکت پایین
    COMPRESSION = "compression"  # فشرده سازی
    QUASIMODO = "quasimodo"  # بازگشت سریع


@dataclass
class RTMSignal:
    """نمایندگی یک سیگنال RTM
    
    خصوصیات:
        phase: فاز RTM (Base، Decision، Rally، Drop، ...)
        price_level: سطح قیمت
        strength: قدرت سیگنال (0-100)
        description: توضیح سیگنال
    """
    phase: RTMPhase
    price_level: float
    strength: float
    description: str


class RTMAnalyzer:
    """تجزیه کننده مفاهیم RTM"""

    def __init__(self):
        """مقداردهی اولیه تجزیه کننده RTM"""
        self.signals: List[RTMSignal] = []
        logger.info("تجزیه کننده RTM راه اندازی شد")

    def analyze(self, candles: List) -> List[RTMSignal]:
        """تجزیه شمع ها برای مفاهیم RTM
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های RTM
        """
        self.signals = []
        
        if len(candles) < 5:
            logger.warning("داده های کافی برای تجزیه RTM وجود ندارد")
            return []
        
        try:
            # Base تجمع را تشخیص دهید
            base_signals = self._find_base(candles)
            self.signals.extend(base_signals)
            
            # Decision و Rally را تشخیص دهید
            decision_signals = self._find_decision_rally(candles)
            self.signals.extend(decision_signals)
            
            # Drop را تشخیص دهید
            drop_signals = self._find_drop(candles)
            self.signals.extend(drop_signals)
            
            # Quasimodo را تشخیص دهید
            quasimodo_signals = self._find_quasimodo(candles)
            self.signals.extend(quasimodo_signals)
            
            logger.info(f"تعداد سیگنال های RTM: {len(self.signals)}")
            return self.signals
            
        except Exception as e:
            logger.error(f"خطا در تجزیه RTM: {e}")
            return []

    def _find_base(self, candles: List) -> List[RTMSignal]:
        """Base (تجمع) را تشخیص دهید
        
        Base: زمانی که قیمت در یک محدوده محدود نوسان می کند
        معمولا قبل از یک حرکت بزرگ تشکیل می شود
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های Base
        """
        signals = []
        
        # Base 5-15 شمع است
        for base_size in range(5, min(16, len(candles) - 1)):
            for i in range(base_size, len(candles)):
                # آخرین base_size شمع را بررسی کن
                recent_candles = candles[i - base_size:i]
                
                # تمام قیمت های high و low را استخراج کن
                highs = [c.high for c in recent_candles]
                lows = [c.low for c in recent_candles]
                
                # محدوده نوسان را محاسبه کن
                price_range = max(highs) - min(lows)
                avg_price = np.mean([c.close for c in recent_candles])
                
                # اگر نوسان کم باشد (کمتر از 2% از متوسط)
                if price_range < avg_price * 0.02:
                    signal = RTMSignal(
                        phase=RTMPhase.BASE,
                        price_level=np.mean(highs),
                        strength=70,
                        description=f"Base تجمع: قیمت در محدوده {min(lows):.2f} - {max(highs):.2f} جمع شده"
                    )
                    signals.append(signal)
                    break  # بعدی را بررسی کن
        
        logger.info(f"تعداد Base تشخیص یافته: {len(signals)}")
        return signals

    def _find_decision_rally(self, candles: List) -> List[RTMSignal]:
        """Decision و Rally را تشخیص دهید
        
        Decision: لحظه ای که قیمت Base را ترک می کند
        Rally: حرکت بالا بعد از Decision
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های Decision/Rally
        """
        signals = []
        
        for i in range(5, len(candles) - 1):
            # آخرین 5 شمع را بررسی کن
            recent = candles[i - 5:i]
            next_candle = candles[i]
            
            closes = [c.close for c in recent]
            
            # میانگین close آخرین 5 شمع
            avg_close = np.mean(closes)
            
            # اگر close جدید بسیار بالاتر باشد (> 1.5%)
            if next_candle.close > avg_close * 1.015:
                signal = RTMSignal(
                    phase=RTMPhase.RALLY,
                    price_level=next_candle.high,
                    strength=75,
                    description=f"Rally حرکت بالا: قیمت از {avg_close:.2f} به {next_candle.close:.2f} برخاست"
                )
                signals.append(signal)
        
        logger.info(f"تعداد Rally تشخیص یافته: {len(signals)}")
        return signals

    def _find_drop(self, candles: List) -> List[RTMSignal]:
        """Drop (حرکت پایین) را تشخیص دهید
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های Drop
        """
        signals = []
        
        for i in range(5, len(candles) - 1):
            # آخرین 5 شمع را بررسی کن
            recent = candles[i - 5:i]
            next_candle = candles[i]
            
            closes = [c.close for c in recent]
            avg_close = np.mean(closes)
            
            # اگر close جدید خیلی پایین تر باشد (< 1.5%)
            if next_candle.close < avg_close * 0.985:
                signal = RTMSignal(
                    phase=RTMPhase.DROP,
                    price_level=next_candle.low,
                    strength=75,
                    description=f"Drop حرکت پایین: قیمت از {avg_close:.2f} به {next_candle.close:.2f} افتاد"
                )
                signals.append(signal)
        
        logger.info(f"تعداد Drop تشخیص یافته: {len(signals)}")
        return signals

    def _find_quasimodo(self, candles: List) -> List[RTMSignal]:
        """Quasimodo (بازگشت سریع) را تشخیص دهید
        
        Quasimodo: بالا یا پایین که به سرعت به قبل برگردد
        معمولا یک فرصت خریدوفروش خوب است
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های Quasimodo
        """
        signals = []
        
        for i in range(2, len(candles) - 1):
            prev = candles[i - 1]
            curr = candles[i]
            
            # Bullish Quasimodo: low جدید بسیار کم، اما close بالا
            if curr.low < prev.low * 0.98 and curr.close > prev.close:
                signal = RTMSignal(
                    phase=RTMPhase.QUASIMODO,
                    price_level=curr.low,
                    strength=60,
                    description=f"Bullish Quasimodo: low سریع در {curr.low:.2f} و بازگشت به {curr.close:.2f}"
                )
                signals.append(signal)
        
        logger.info(f"تعداد Quasimodo تشخیص یافته: {len(signals)}")
        return signals
