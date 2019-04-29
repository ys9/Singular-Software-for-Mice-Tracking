from ctypes import POINTER, HRESULT
from ctypes import windll
from ctypes.wintypes import (DWORD, ULONG, HWND,
                             UINT, LPCOLESTR, LCID, LPVOID)

from comtypes import IUnknown, GUID

LPUNKNOWN = POINTER(IUnknown)
CLSID = GUID
LPCLSID = POINTER(CLSID)

WS_CHILD = 0x40000000
WS_CLIPSIBLINGS = 0x04000000

OleCreatePropertyFrame = windll.oleaut32.OleCreatePropertyFrame
OleCreatePropertyFrame.restype = HRESULT
OleCreatePropertyFrame.argtypes = (
    HWND,  # [in] hwndOwner
    UINT,  # [in] x
    UINT,  # [in] y
    LPCOLESTR,  # [in] lpszCaption
    ULONG,  # [in] cObjects
    POINTER(LPUNKNOWN),  # [in] ppUnk
    ULONG,  # [in] cPages
    LPCLSID,  # [in] pPageClsID
    LCID,  # [in] lcid
    DWORD,  # [in] dwReserved
    LPVOID,  # [in] pvReserved
)
