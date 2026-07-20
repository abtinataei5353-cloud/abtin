"""تجزیه گر سطح حمایت و مقاومت

این ماژول مسئول:
- شناسایی سطح های حمایتی (پایین ترین نقاط)
- شناسایی سطح های مقاومتی (بالاترین نقاط)
- تشخیص منطقه های ترافیکی (zones)
- محاسبه قوت هر سطح
"""

import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
from src.config.logger_config import Logger

logger = Logger.get_logger(__name__)


@dataclass
class Level:
    """نمایندگی یک سطح حمایت یا مقاومت
    
    خصوصیات:
        price: قیمت سطح
        level_type: نوع سطح ('support' یا 'resistance')
        strength: قدرت سطح (0-100)
        touches: تعداد دفعاتی که قیمت این سطح را لمس کرده
    """
    price: float
    level_type: str  # 'support' یا 'resistance'
    strength: float
    touches: int


class SupportResistanceAnalyzer:
    """تجزیه کننده سطح های حمایت و مقاومت"""

    def __init__(self):
        """مقداردهی اولیه تجزیه کننده"""
        self.levels: List[Level] = []
        logger.info("تجزیه کننده حمایت/مقاومت راه اندازی شد")

    def find_levels(self, prices: np.ndarray, window: int = 5) -> List[Level]:
        """سطح های حمایت و مقاومت را پیدا کن
        
        آرگومان ها:
            prices: فهرست قیمت های بستن شمع ها
            window: اندازه پنجره برای تشخیص (تعداد شمع ها)
            
        برگشت:
            فهرست سطح های تشخیص یافته
        """
        self.levels = []
        
        if len(prices) < window * 2:
            logger.warning("داده های کافی برای تشخیص سطح وجود ندارد")
            return []
        
        try:
            # نقاط محلی (قله ها و دره ها) را پیدا کن
            highs_indices = self._find_local_maxima(prices, window)
            lows_indices = self._find_local_minima(prices, window)
            
            # سطح های مقاومت (قله ها)
            for idx in highs_indices:
                strength = self._calculate_level_strength(prices, prices[idx], 'resistance')
                level = Level(
                    price=prices[idx],
                    level_type='resistance',
                    strength=strength,
                    touches=self._count_touches(prices, prices[idx])
                )
                self.levels.append(level)
            
            # سطح های حمایت (دره ها)
            for idx in lows_indices:
                strength = self._calculate_level_strength(prices, prices[idx], 'support')
                level = Level(
                    price=prices[idx],
                    level_type='support',
                    strength=strength,
                    touches=self._count_touches(prices, prices[idx])
                )
                self.levels.append(level)
            
            # سطح ها را بر اساس قدرت مرتب کن
            self.levels.sort(key=lambda l: l.strength, reverse=True)
            
            logger.info(f"تعداد سطح های تشخیص یافته: {len(self.levels)}")
            return self.levels
            
        except Exception as e:
            logger.error(f"خطا در تشخیص سطح ها: {e}")
            return []
    
    def _find_local_maxima(self, data: np.ndarray, window: int) -> np.ndarray:
        """قله های محلی را پیدا کن
        
        آرگومان ها:
            data: داده های ورودی
            window: اندازه پنجره
            
        برگشت:
            شاخص های قله های محلی
        """
        maxima = []
        for i in range(window, len(data) - window):
            # اگر این نقطه از همه نقاط اطراف بالاتر باشد
            if all(data[i] >= data[i - j] for j in range(1, window + 1)) and \
               all(data[i] >= data[i + j] for j in range(1, window + 1)):
                maxima.append(i)
        return np.array(maxima)
    
    def _find_local_minima(self, data: np.ndarray, window: int) -> np.ndarray:
        """دره های محلی را پیدا کن
        
        آرگومان ها:
            data: داده های ورودی
            window: اندازه پنجره
            
        برگشت:
            شاخص های دره های محلی
        """
        minima = []
        for i in range(window, len(data) - window):
            # اگر این نقطه از همه نقاط اطراف پایین تر باشد
            if all(data[i] <= data[i - j] for j in range(1, window + 1)) and \
               all(data[i] <= data[i + j] for j in range(1, window + 1)):
                minima.append(i)
        return np.array(minima)
    
    def _calculate_level_strength(self, prices: np.ndarray, level_price: float, level_type: str) -> float:
        """قدرت یک سطح را محاسبه کن
        
        قدرت بر اساس:
        - تعداد دفعاتی که قیمت این سطح را لمس کرده
        - حجم معاملات
        - مدت زمان تشکیل
        
        آرگومان ها:
            prices: فهرست قیمت ها
            level_price: قیمت سطح
            level_type: نوع سطح
            
        برگشت:
            قدرت سطح (0-100)
        """
        # تعداد لمس کردن را بشمار
        tolerance = np.std(prices) * 0.01  # تلرانس 1% از انحراف معیار
        touches = np.sum(np.abs(prices - level_price) < tolerance)
        
        # قدرت را محاسبه کن
        strength = min(100, touches * 10)  # حداکثر 100
        return strength
    
    def _count_touches(self, prices: np.ndarray, level_price: float) -> int:
        """تعداد دفعاتی که قیمت یک سطح را لمس کرده را بشمار
        
        آرگومان ها:
            prices: فهرست قیمت ها
            level_price: قیمت سطح
            
        برگشت:
            تعداد لمس کردن
        """
        tolerance = np.std(prices) * 0.01
        touches = np.sum(np.abs(prices - level_price) < tolerance)
        return int(touches)
