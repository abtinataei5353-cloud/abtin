"""تجزیه کننده تصویر - تشخیص نمودار و استخراج داده های شمعی

این ماژول مسئول:
- بارگذاری و پردازش تصویر نمودار
- تشخیص نواحی شمعی
- استخراج قیمت بالا، پایین، باز، بسته
- شناسایی خطوط و سطوح کلیدی
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from src.config.logger_config import Logger

logger = Logger.get_logger(__name__)


@dataclass
class Candle:
    """یک شمع را نمایندگی می کند
    
    خصوصیات:
        open: قیمت باز
        high: قیمت بالاترین
        low: قیمت پایین ترین
        close: قیمت بستن
        volume: حجم معاملات (اختیاری)
        x_pos: موقعیت X در تصویر
    """
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    x_pos: int = 0


class ChartAnalyzer:
    """تجزیه کننده نمودار شمعی
    
    این کلاس نمودار تصویری را تجزیه می کند و اطلاعات شمعی را استخراج می کند.
    """

    def __init__(self):
        """مقداردهی اولیه تجزیه کننده نمودار"""
        self.image: Optional[np.ndarray] = None
        self.candles: List[Candle] = []
        self.price_scale: Optional[Tuple[float, float]] = None  # (min_price, max_price)
        self.time_scale: Optional[List[str]] = None
        logger.info("تجزیه کننده نمودار راه اندازی شد")

    def load_image(self, image_path: str) -> bool:
        """تصویر نمودار را بارگذاری کن
        
        آرگومان ها:
            image_path: مسیر فایل تصویر
            
        برگشت:
            True اگر موفق، False اگر ناموفق
        """
        try:
            # تصویر را با OpenCV بارگذاری کن
            self.image = cv2.imread(image_path)
            if self.image is None:
                logger.error(f"نمی توان تصویر را بارگذاری کنم: {image_path}")
                return False
            
            logger.info(f"تصویر بارگذاری شد: {image_path}")
            logger.info(f"ابعاد تصویر: {self.image.shape}")
            return True
        except Exception as e:
            logger.error(f"خطا در بارگذاری تصویر: {e}")
            return False

    def detect_candles(self) -> List[Candle]:
        """تشخیص شمع ها در تصویر
        
        این تابع:
        1. تصویر را به سطح خاکستری تبدیل می کند
        2. مرزهای شمع را تشخیص می کند
        3. قیمت هر شمع را استخراج می کند
        
        برگشت:
            فهرست شمع های تشخیص یافته
        """
        if self.image is None:
            logger.error("ابتدا تصویر را بارگذاری کنید")
            return []

        try:
            # تصویر را به خاکستری تبدیل کن
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            
            # تصویر را صاف کن (noise کم کن)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # مرزهای افقی را تشخیص کن (سط�� حمایتی و مقاومت)
            edges = cv2.Canny(blurred, 50, 150)
            
            # خطوط افقی را پیدا کن
            lines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi/180,
                threshold=50,
                minLineLength=50,
                maxLineGap=10
            )
            
            # شمع ها را تشخیص کن
            self._extract_candle_data(lines)
            
            logger.info(f"تعداد شمع تشخیص یافته: {len(self.candles)}")
            return self.candles
            
        except Exception as e:
            logger.error(f"خطا در تشخیص شمع ها: {e}")
            return []

    def _extract_candle_data(self, lines: Optional[np.ndarray]) -> None:
        """داده های شمعی را از خطوط استخراج کن
        
        آرگومان ها:
            lines: خطوط تشخیص یافته در تصویر
        """
        if lines is None or len(lines) == 0:
            logger.warning("هیچ خطی تشخیص داده نشد")
            return
        
        # خطوط را از راست به چپ مرتب کن (زمان های قدیم به جدید)
        self.candles = []
        
        # TODO: منطق استخراج داده شمعی
        # این قسمت باید:
        # 1. قله های محلی و دره های محلی را پیدا کند
        # 2. باز، بسته، بالا، پایین را برای هر شمع مشخص کند
        # 3. حجم را (اگر قابل مشاهده باشد) تخمین زند

    def set_price_scale(self, min_price: float, max_price: float) -> None:
        """مقیاس قیمت را تعریف کن
        
        آرگومان ها:
            min_price: حداقل قیمت قابل نمایش
            max_price: حداکثر قیمت قابل نمایش
        """
        self.price_scale = (min_price, max_price)
        logger.info(f"مقیاس قیمت تنظیم شد: {min_price} - {max_price}")

    def pixel_to_price(self, pixel_y: int) -> float:
        """موقعیت پیکسل را به قیمت تبدیل کن
        
        آرگومان ها:
            pixel_y: موقعیت Y در تصویر (پیکسل)
            
        برگشت:
            قیمت متناسب
        """
        if self.price_scale is None or self.image is None:
            return 0.0
        
        min_price, max_price = self.price_scale
        image_height = self.image.shape[0]
        
        # محاسبه قیمت بر اساس موقعیت Y
        # توجه: در تصویر، بالا = قیمت بالا، پایین = قیمت پایین
        price = max_price - (pixel_y / image_height) * (max_price - min_price)
        return price

    def price_to_pixel(self, price: float) -> int:
        """قیمت را به موقعیت پیکسل تبدیل کن
        
        آرگومان ها:
            price: قیمت
            
        برگشت:
            موقعیت Y در تصویر
        """
        if self.price_scale is None or self.image is None:
            return 0
        
        min_price, max_price = self.price_scale
        image_height = self.image.shape[0]
        
        # محاسبه معکوس: قیمت به پیکسل
        pixel_y = int(image_height - (price - min_price) / (max_price - min_price) * image_height)
        return pixel_y
