from enum import Enum

from .base import Province, VietNamDivisionType


class ProvinceEnum(Province, Enum):
    P_1 = ("Thành phố Hà Nội", 1, VietNamDivisionType.THANH_PHO_TRUNG_UONG, "thanh_pho_ha_noi", 24)
    P_2 = ("Tỉnh Hà Giang", 2, VietNamDivisionType.TINH, "tinh_ha_giang", 219)
