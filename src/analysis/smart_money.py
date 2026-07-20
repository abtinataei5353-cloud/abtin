"""تجزیه کننده مفاهیم هوشمند پول (Smart Money Concepts)

این ماژول مسئول:
- تشخیص Fair Value Gaps (FVG) - شکاف های بدون معامله
- تشخیص Order Blocks - نواحی سفارش
- تشخیص Break of Structure (BOS) - شکست ساختار
- تشخیص Change of Character (CHoCH) - تغییر رفتار بازار
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from src.config.logger_config import Logger

logger = Logger.get_logger(__name__)


class SMCType(Enum):
    """انواع مفاهیم هوشمند پول"""
    FVG = "fvg"  # Fair Value Gap
    ORDER_BLOCK = "order_block"  # Order Block
    BOS = "bos"  # Break of Structure
    CHOCH = "choch"  # Change of Character


@dataclass
class SMCSignal:
    """نمایندگی یک سیگنال Smart Money
    
    خصوصیات:
        signal_type: نوع سیگنال (FVG، Order Block، BOS، CHoCH)
        price_low: قیمت پایین منطقه
        price_high: قیمت بالای منطقه
        strength: قدرت سیگنال (0-100)
        direction: جهت ('buy' یا 'sell')
        description: توضیح سیگنال
    """
    signal_type: SMCType
    price_low: float
    price_high: float
    strength: float
    direction: str
    description: str


class SmartMoneyAnalyzer:
    """تجزیه کننده مفاهیم هوشمند پول"""

    def __init__(self):
        """مقداردهی اولیه تجزیه کننده Smart Money"""
        self.signals: List[SMCSignal] = []
        logger.info("تجزیه کننده Smart Money راه اندازی شد")

    def analyze(self, candles: List) -> List[SMCSignal]:
        """تجزیه شمع ها برای سیگنال های Smart Money
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های تشخیص یافته
        """
        self.signals = []
        
        if len(candles) < 3:
            logger.warning("داده های کافی برای تجزیه Smart Money وجود ندارد")
            return []
        
        try:
            # تشخیص FVG
            fvg_signals = self._find_fvg(candles)
            self.signals.extend(fvg_signals)
            
            # تشخیص Order Blocks
            ob_signals = self._find_order_blocks(candles)
            self.signals.extend(ob_signals)
            
            # تشخیص BOS
            bos_signals = self._find_bos(candles)
            self.signals.extend(bos_signals)
            
            # تشخیص CHoCH
            choch_signals = self._find_choch(candles)
            self.signals.extend(choch_signals)
            
            logger.info(f"تعداد سیگنال های Smart Money: {len(self.signals)}")
            return self.signals
            
        except Exception as e:
            logger.error(f"خطا در تجزیه Smart Money: {e}")
            return []

    def _find_fvg(self, candles: List) -> List[SMCSignal]:
        """Fair Value Gaps را تشخیص دهید
        
        Fair Value Gap: شکاف بدون معامله که قیمت آن را ندیده است
        
        وقتی یک شمع بازمانده:
        - قبلی: بالا می رود
        - فعلی: با شکاف پایین می رود
        آن شکاف یک FVG Down است
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های FVG
        """
        signals = []
        
        # حداقل 3 شمع نیاز است (قبلی، فعلی، بعدی)
        for i in range(1, len(candles) - 1):
            prev_candle = candles[i - 1]
            curr_candle = candles[i]
            
            # FVG Up: قبلی پایین می رود، فعلی با شکاف بالا می رود
            if prev_candle.close < prev_candle.open and curr_candle.open > prev_candle.high:
                # FVG منطقه از low قبلی تا open فعلی
                signal = SMCSignal(
                    signal_type=SMCType.FVG,
                    price_low=prev_candle.high,
                    price_high=curr_candle.open,
                    strength=75,  # قدرت فیکس برای اکنون
                    direction='buy',  # FVG up معمولا برای خریداری است
                    description=f"Fair Value Gap (Up): شکاف بدون معامله بین {prev_candle.high:.2f} و {curr_candle.open:.2f}"
                )
                signals.append(signal)
            
            # FVG Down: قبلی بالا می رود، فعلی با شکاف پایین می رود
            elif prev_candle.close > prev_candle.open and curr_candle.open < prev_candle.low:
                signal = SMCSignal(
                    signal_type=SMCType.FVG,
                    price_low=curr_candle.open,
                    price_high=prev_candle.low,
                    strength=75,
                    direction='sell',  # FVG down معمولا برای فروش است
                    description=f"Fair Value Gap (Down): شکاف بدون معامله بین {curr_candle.open:.2f} و {prev_candle.low:.2f}"
                )
                signals.append(signal)
        
        logger.info(f"تعداد FVG تشخیص یافته: {len(signals)}")
        return signals

    def _find_order_blocks(self, candles: List) -> List[SMCSignal]:
        """Order Blocks را تشخیص دهید
        
        Order Block: منطقه ای که حد بندان آنجا خریدند و حالا برای فروش منتظرند
        معمولا قبل از یک حرکت قوی تشکیل می شود
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های Order Block
        """
        signals = []
        
        for i in range(2, len(candles)):
            prev_candle = candles[i - 2]
            curr_candle = candles[i]
            
            # Bullish Order Block: بعد از یک قطع پایین
            if prev_candle.close < prev_candle.open:  # شم�� قرمز (پایین)
                # اگر شمع بعدی بالا برود
                if curr_candle.close > curr_candle.open:  # شمع سبز (بالا)
                    signal = SMCSignal(
                        signal_type=SMCType.ORDER_BLOCK,
                        price_low=prev_candle.low,
                        price_high=prev_candle.high,
                        strength=60,
                        direction='buy',
                        description=f"Bullish Order Block: حد بندان در {prev_candle.low:.2f} - {prev_candle.high:.2f}"
                    )
                    signals.append(signal)
        
        logger.info(f"تعداد Order Block تشخیص یافته: {len(signals)}")
        return signals

    def _find_bos(self, candles: List) -> List[SMCSignal]:
        """Break of Structure را تشخیص دهید
        
        BOS: شکست یک سطح حمایتی یا مقاومتی
        نشان می دهد که ساختار بازار تغییر کرده
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های BOS
        """
        signals = []
        
        # حداقل 5 شمع نیاز است
        if len(candles) < 5:
            return signals
        
        for i in range(3, len(candles)):
            # بررسی سه شمع آخر
            candle3 = candles[i - 2]
            candle2 = candles[i - 1]
            candle1 = candles[i]
            
            # Bearish BOS: هر شمع جدید low پایین تری نسبت به قبل
            # نشان می دهد ساختار نزولی است
            if candle3.low > candle2.low > candle1.low:
                signal = SMCSignal(
                    signal_type=SMCType.BOS,
                    price_low=candle1.low,
                    price_high=candle2.high,
                    strength=70,
                    direction='sell',
                    description=f"Bearish BOS: شکست ساختار، low جدید در {candle1.low:.2f}"
                )
                signals.append(signal)
        
        logger.info(f"تعداد BOS تشخیص یافته: {len(signals)}")
        return signals

    def _find_choch(self, candles: List) -> List[SMCSignal]:
        """Change of Character را تشخیص دهید
        
        CHoCH: تغییر در رفتار بازار
        هنگامی که بالا ترین نقطه (high) یا پایین ترین نقطه (low) شکسته شود
        
        آرگومان ها:
            candles: فهرست شمع ها
            
        برگشت:
            فهرست سیگنال های CHoCH
        """
        signals = []
        
        if len(candles) < 4:
            return signals
        
        # آخرین 4 شمع را بررسی کن
        for i in range(2, len(candles)):
            candle_old = candles[i - 2]
            candle_old2 = candles[i - 1]
            candle_new = candles[i]
            
            # Bullish CHoCH: High جدید بالاتر از High قدیم
            if candle_new.high > candle_old.high and candle_old2.high <= candle_old.high:
                signal = SMCSignal(
                    signal_type=SMCType.CHOCH,
                    price_low=candle_old.high,
                    price_high=candle_new.high,
                    strength=65,
                    direction='buy',
                    description=f"Bullish CHoCH: تغییر رفتار، High جدید در {candle_new.high:.2f}"
                )
                signals.append(signal)
        
        logger.info(f"تعداد CHoCH تشخیص یافته: {len(signals)}")
        return signals
