from comtypes import GUID
from comtypes import IPersist
from comtypes import IUnknown
from comtypes import COMMETHOD, HRESULT, POINTER, c_int, c_ulong
from ctypes.wintypes import _ULARGE_INTEGER


class IPersistStream(IPersist):
    _case_insensitive_ = True
    _iid_ = GUID('{00000109-0000-0000-C000-000000000046}')
    _idlflags_ = []


class ISequentialStream(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0C733A30-2A1C-11CE-ADE5-00AA0044773D}')
    _idlflags_ = []


class IStream(ISequentialStream):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000C-0000-0000-C000-000000000046}')
    _idlflags_ = []


IPersistStream._methods_ = [
    COMMETHOD([], HRESULT, 'IsDirty'),
    COMMETHOD([], HRESULT, 'Load',
              (['in'], POINTER(IStream), 'pstm')),
    COMMETHOD([], HRESULT, 'Save',
              (['in'], POINTER(IStream), 'pstm'),
              (['in'], c_int, 'fClearDirty')),
    COMMETHOD([], HRESULT, 'GetSizeMax',
              (['out'], POINTER(_ULARGE_INTEGER), 'pcbSize')),
]


class IEnumMoniker(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID("{00000102-0000-0000-C000-000000000046}")
    _idlflags_ = []


class IMoniker(IPersistStream):
    _case_insensitive_ = True
    _iid_ = GUID("{0000000F-0000-0000-C000-000000000046}")
    _idlflags_ = []


class IBindCtx(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID("{0000000E-0000-0000-C000-000000000046}")
    _idlflags_ = []


IEnumMoniker._methods_ = [
    COMMETHOD([], HRESULT, "Next",
              (['in'], c_ulong, 'celt'),
              (['out'], POINTER(POINTER(IMoniker)), 'rgelt'),
              (['out'], POINTER(c_ulong), 'pceltFetched')),

    COMMETHOD([], HRESULT, "Skip",
              (['in'], c_ulong, 'celt')),

    COMMETHOD([], HRESULT, "Reset"),
    COMMETHOD([], HRESULT, "Clone",
              (['out'], POINTER(POINTER(IMoniker)), 'ppenum'))
]

IMoniker._methods_ = [
    COMMETHOD([], HRESULT, "BindToObject",
              (['in'], POINTER(IBindCtx), "pbc"),
              (['in'], POINTER(IMoniker), "pmkToLeft"),
              (['in'], POINTER(GUID), "riidResult"),
              (['out'], POINTER(POINTER(IUnknown)), "ppvResult")
              ),
    COMMETHOD([], HRESULT, "BindToStorage",
              (['in'], POINTER(IBindCtx), "pbc"),
              (['in'], POINTER(IMoniker), "pmkToLeft"),
              (['in'], POINTER(GUID), "riid"),
              (['out'], POINTER(POINTER(IUnknown)), "ppvObj")
              )]

# IMoniker._methods_ = IPersistStream._methods_ + [
#    STDMETHOD(HRESULT, "BindToObject", POINTER(IBindCtx), POINTER(IMoniker), REFIID, c_void_p),
#    STDMETHOD(HRESULT, "BindToStorage", POINTER(IBindCtx), POINTER(IMoniker), REFIID, c_void_p),
#    STDMETHOD(HRESULT, "Reduce", POINTER(IBindCtx), DWORD,
#              POINTER(POINTER(IMoniker)), POINTER(POINTER(IMoniker))),
#    STDMETHOD(HRESULT, "ComposeWith", POINTER(IMoniker), BOOL, POINTER(POINTER(IMoniker))),
#    STDMETHOD(HRESULT, "Enum", BOOL, POINTER(IEnumMoniker)),
#    STDMETHOD(HRESULT, "IsEqual", POINTER(IMoniker)),
#    STDMETHOD(HRESULT, "Hash", POINTER(DWORD)),
#    STDMETHOD(HRESULT, "IsRunning", POINTER(IBindCtx), POINTER(IMoniker), POINTER(IMoniker)),
#    STDMETHOD(HRESULT, "GetTimeOfLastChange", POINTER(IBindCtx), POINTER(IMoniker),
#              POINTER(FILETIME)),
#    STDMETHOD(HRESULT, "Inverse", POINTER(IMoniker)),
#    STDMETHOD(HRESULT, "CommonPrefixWith", POINTER(IMoniker), POINTER(POINTER(IMoniker))),
#    STDMETHOD(HRESULT, "RelativePathTo", POINTER(IMoniker), POINTER(POINTER(IMoniker))),
#    STDMETHOD(HRESULT, "GetDisplayName", POINTER(IBindCtx), POINTER(IMoniker), POINTER(LPOLESTR)),
#    STDMETHOD(HRESULT, "ParseDisplayName", POINTER(IBindCtx), POINTER(IMoniker),
#              LPOLESTR, POINTER(ULONG), POINTER(POINTER(IMoniker))),
#    STDMETHOD([], HRESULT, "IsSystemMoniker", POINTER(DWORD))]