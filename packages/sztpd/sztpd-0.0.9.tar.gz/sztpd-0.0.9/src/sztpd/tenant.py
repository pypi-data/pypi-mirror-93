# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_Z='wn-sztpd-x:'
_Y='Unable to parse "input" JSON document: '
_X='malformed-message'
_W='wn-sztpd-x'
_V='application/yang-data+json'
_U='/wn-sztpd-x:tenants/tenant=[^ ]*'
_T='/wn-sztpd-x:tenants/tenant=[^/]*/'
_S='Top node names must begin with the "wn-sztpd-1" prefix.'
_R='application'
_Q='wn-sztpd-1'
_P=False
_O='name'
_N='wn-sztpd-1:'
_M=True
_L='/wn-sztpd-x:tenants/tenant/0/'
_K='Non-root data_paths must begin with "/wn-sztpd-1:".'
_J='wn-sztpd-x:tenant'
_I='+'
_H='invalid-value'
_G='text/plain'
_F='protocol'
_E=None
_D=':'
_C='/wn-sztpd-x:tenants/tenant='
_B='/wn-sztpd-1:'
_A='/'
import re,json,datetime,basicauth
from aiohttp import web
from passlib.hash import sha256_crypt
from .  import yl
from .  import dal
from .  import utils
from .rcsvr import RestconfServer
from .handler import RouteHandler
class TenantViewHandler(RouteHandler):
	supported_media_types=_V,
	def __init__(A,native):A.native=native
	async def _check_auth(C,request,data_path):
		K='access-denied';J='comment';I='failure';H='outcome';E=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A['method']=E.method;A['path']=E.path;L=E.headers.get('AUTHORIZATION')
		if L is _E:A[H]=I;A[J]='No authorization specified in the HTTP header.';await C.native._insert_audit_log_entry(_E,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D,indent=2);return B
		G,N=basicauth.decode(L);F=_E
		try:F=await C.native.dal.get_tenant_name_for_admin(G)
		except dal.NodeNotFound as Q:A[H]=I;A[J]='Unknown admin: '+G;await C.native._insert_audit_log_entry(_E,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D,indent=2);return B
		if F==_E:A[H]=I;A[J]='Host-level admins cannot use tenant interface ('+G+').';await C.native._insert_audit_log_entry(_E,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D,indent=2);return B
		O=_A+C.native.dal.app_ns+':tenants/tenant='+F+'/admin-accounts/admin-account='+G+'/password';P=await C.native.dal.handle_get_config_request(O);M=P[C.native.dal.app_ns+':password'];assert M.startswith('$5$')
		if not sha256_crypt.verify(N,M):A[H]=I;A[J]='Password mismatch for admin '+G;await C.native._insert_audit_log_entry(F,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D,indent=2);return B
		A[H]='success';await C.native._insert_audit_log_entry(F,A);return F
	async def handle_get_restconf_root(E,request):
		F=request;H=_A;C=await E._check_auth(F,H)
		if type(C)is web.Response:A=C;return A
		else:I=C
		B,J=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;D=B;assert D!=_G;G=utils.Encoding[D.rsplit(_I,1)[1]]
		A=web.Response(status=200);A.content_type=D
		if G==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert G==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		return A
	async def handle_get_yang_library_version(E,request):
		F=request;H=_A;C=await E._check_auth(F,H)
		if type(C)is web.Response:A=C;return A
		else:I=C
		B,J=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;D=B;assert D!=_G;G=utils.Encoding[D.rsplit(_I,1)[1]]
		A=web.Response(status=200);A.content_type=D
		if G==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert G==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		return A
	async def handle_get_opstate_request(E,request):
		F=request;B,M=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_operational:]);G=await E._check_auth(F,B)
		if type(G)is web.Response:A=G;return A
		else:H=G
		D,V=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(D)is web.Response:A=D;return A
		else:assert type(D)==str;N=D;assert N!=_G;W=utils.Encoding[N.rsplit(_I,1)[1]]
		if B=='/ietf-yang-library:yang-library':A=web.Response(status=200);A.content_type=_V;A.text=getattr(yl,'nbi_x_tenant')();return A
		assert B==_A or B.startswith(_B)
		if B==_A:O=_C+H
		else:
			if not B.startswith(_B):A=web.Response(status=400);S=utils.gen_rc_errors(_F,_H,error_message=_K);A.text=json.dumps(S,indent=2);return A
			X,P=B.split(_D,1);assert P!=_E;O=_C+H+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_B,_C+H+_A,M[R])
		I,C=await E.native.handle_get_opstate_request_lower_half(O,Q)
		if C!=_E:
			assert I.status==200;J={}
			if B==_A:
				for K in C[_J][0].keys():
					if K==_O:continue
					J[_N+K]=C[_J][0][K]
			else:L=next(iter(C));assert L.count(_D)==1;T,U=L.split(_D);assert T==_W;assert type(C)==dict;assert len(C)==1;J[_N+U]=C[L]
			I.text=json.dumps(J,indent=2)
		return I
	async def handle_get_config_request(E,request):
		F=request;A,M=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_running:]);G=await E._check_auth(F,A)
		if type(G)is web.Response:C=G;return C
		else:H=G
		D,V=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(D)is web.Response:C=D;return C
		else:assert type(D)==str;N=D;assert N!=_G;W=utils.Encoding[N.rsplit(_I,1)[1]]
		assert A==_A or A.startswith(_B)
		if A==_A:O=_C+H
		else:
			if not A.startswith(_B):C=web.Response(status=400);S=utils.gen_rc_errors(_F,_H,error_message=_K);C.text=json.dumps(S,indent=2);return C
			X,P=A.split(_D,1);assert P!=_E;O=_C+H+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_B,_C+H+_A,M[R])
		I,B=await E.native.handle_get_config_request_lower_half(O,Q)
		if B!=_E:
			assert I.status==200;J={}
			if A==_A:
				for K in B[_J][0].keys():
					if K==_O:continue
					J[_N+K]=B[_J][0][K]
			else:L=next(iter(B));assert L.count(_D)==1;T,U=L.split(_D);assert T==_W;assert type(B)==dict;assert len(B)==1;J[_N+U]=B[L]
			I.text=json.dumps(J,indent=2)
		return I
	async def handle_post_config_request(G,request):
		C=request;D,K=utils.parse_raw_path(C._message.path[RestconfServer.len_prefix_running:]);H=await G._check_auth(C,D)
		if type(H)is web.Response:A=H;return A
		else:I=H
		E,U=utils.check_http_headers(C,G.supported_media_types,accept_required=_P)
		if type(E)is web.Response:A=E;return A
		else:assert type(E)==str;L=E;assert L!=_G;V=utils.Encoding[L.rsplit(_I,1)[1]]
		if D==_A:M=_C+I
		else:
			if not D.startswith(_B):A=web.Response(status=400);B=utils.gen_rc_errors(_F,_H,error_message=_K);A.text=json.dumps(B,indent=2);return A
			W,N=D.split(_D,1);assert N!=_E;M=_C+I+_A+N
		O=dict()
		for P in K.keys():O[P]=re.sub(_B,_C+I+_A,K[P])
		try:F=await C.json()
		except json.decoder.JSONDecodeError as Q:A=web.Response(status=400);B=utils.gen_rc_errors(_F,_X,error_message=_Y+str(Q));A.text=json.dumps(B,indent=2);return A
		assert type(F)==dict;assert len(F)==1;J=next(iter(F));assert J.count(_D)==1;R,S=J.split(_D)
		if R!=_Q:A=web.Response(status=400);B=utils.gen_rc_errors(_R,_H,error_message=_S);A.text=json.dumps(B,indent=2);return A
		T={_Z+S:F[J]};A=await G.native.handle_post_config_request_lower_half(M,O,T)
		if A.status!=201:
			if'/wn-sztpdex:tenants/tenant/0/'in A.text:A.text=A.text.replace(_L,_B)
			elif _C in A.text:A.text=re.sub(_T,_B,A.text);A.text=re.sub(_U,_B,A.text)
		return A
	async def handle_put_config_request(H,request):
		E=request;D,M=utils.parse_raw_path(E._message.path[RestconfServer.len_prefix_running:]);I=await H._check_auth(E,D)
		if type(I)is web.Response:A=I;return A
		else:F=I
		G,X=utils.check_http_headers(E,H.supported_media_types,accept_required=_P)
		if type(G)is web.Response:A=G;return A
		else:assert type(G)==str;N=G;assert N!=_G;Y=utils.Encoding[N.rsplit(_I,1)[1]]
		if D==_A:O=_C+F
		else:
			if not D.startswith(_B):A=web.Response(status=400);B=utils.gen_rc_errors(_F,_H,error_message=_K);A.text=json.dumps(B,indent=2);return A
			Z,P=D.split(_D,1);assert P!=_E;O=_C+F+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_B,_C+F+_A,M[R])
		try:C=await E.json()
		except json.decoder.JSONDecodeError as S:A=web.Response(status=400);B=utils.gen_rc_errors(_F,_X,error_message=_Y+str(S));A.text=json.dumps(B,indent=2);return A
		if D==_A:
			J={_J:[{_O:F}]}
			for K in C.keys():
				assert K.count(_D)==1;T,U=K.split(_D)
				if T!=_Q:A=web.Response(status=400);B=utils.gen_rc_errors(_R,_H,error_message=_S);A.text=json.dumps(B,indent=2);return A
				J[_J][0][U]=C[K]
		else:
			assert type(C)==dict;assert len(C)==1;L=next(iter(C));assert L.count(_D)==1;V,W=L.split(_D)
			if V!=_Q:A=web.Response(status=400);B=utils.gen_rc_errors(_R,_H,error_message=_S);A.text=json.dumps(B,indent=2);return A
			J={_Z+W:C[L]}
		A=await H.native.handle_put_config_request_lower_half(O,Q,J)
		if A.status!=201 and A.status!=204:
			if _L in A.text:A.text=A.text.replace(_L,_B)
			elif _C in A.text:A.text=re.sub(_T,_B,A.text);A.text=re.sub(_U,_B,A.text)
		return A
	async def handle_delete_config_request(E,request):
		F=request;B,N=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_running:]);G=await E._check_auth(F,B)
		if type(G)is web.Response:A=G;return A
		else:H=G
		C,O=utils.check_http_headers(F,E.supported_media_types,accept_required=_P)
		if type(C)is web.Response:A=C;return A
		else:
			assert type(C)==str;D=C
			if D==_G:L=_E
			else:L=utils.Encoding[D.rsplit(_I,1)[1]]
		if B==_A:I=_C+H
		else:
			if not B.startswith(_B):
				J=_K;A=web.Response(status=400);A.content_type=D
				if D==_G:A.text=J
				else:M=utils.gen_rc_errors(_F,_H,error_message=J);A.text=json.dumps(M,indent=2)
				return A
			P,K=B.split(_D,1);assert K!=_E;I=_C+H+_A+K
		A=await E.native.handle_delete_config_request_lower_half(I)
		if A.status!=204:
			if _L in A.text:A.text=A.text.replace(_L,_B)
			elif _C in A.text:A.text=re.sub(_T,_B,A.text);A.text=re.sub(_U,_B,A.text)
		return A
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):0