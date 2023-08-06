# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_Ag='Returning an RPC-error provided by callback (NOTE: RPC-error != exception, hence a normal exit).'
_Af='Unrecognized error-tag: '
_Ae='partial-operation'
_Ad='operation-failed'
_Ac='rollback-failed'
_Ab='data-exists'
_Aa='resource-denied'
_AZ='lock-denied'
_AY='in-use'
_AX='unknown-namespace'
_AW='bad-element'
_AV='unknown-attribute'
_AU='bad-attribute'
_AT='missing-attribute'
_AS='too-big'
_AR='exception-thrown'
_AQ='functions'
_AP='callback-details'
_AO='from-device'
_AN='identity-certificate'
_AM='source-ip-address'
_AL='mode-0 == no-sn'
_AK='"ietf-sztp-bootstrap-server:input" is missing.'
_AJ='/ietf-sztp-bootstrap-server:report-progress'
_AI='Resource does not exist.'
_AH='Requested resource does not exist.'
_AG=':log-entry'
_AF='/devices/device='
_AE=':devices/device='
_AD='2021-02-04'
_AC='2019-04-30'
_AB='urn:ietf:params:xml:ns:yang:ietf-yang-types'
_AA='ietf-yang-types'
_A9='module'
_A8='module-set-id'
_A7='ietf-yang-library:modules-state'
_A6='application/yang-data+xml'
_A5='webhooks'
_A4='callout-type'
_A3='passed-input'
_A2='ssl_object'
_A1='access-denied'
_A0='/ietf-sztp-bootstrap-server:get-bootstrapping-data'
_z='Parent node does not exist.'
_y='Resource can not be modified.'
_x='2013-07-15'
_w='webhook'
_v='exited-normally'
_u='opaque'
_t='function'
_s='plugin'
_r='serial-number'
_q='rpc-supported'
_p='data-missing'
_o='Unable to parse "input" document: '
_n='import'
_m='application/yang-data+json'
_l='operation-not-supported'
_k=':device'
_j='Content-Type'
_i='1'
_h='malformed-message'
_g=False
_f=':tenants/tenant='
_e='x'
_d='implement'
_c='callback-results'
_b='callback'
_a='invalid-value'
_Z='unknown-element'
_Y=True
_X='application'
_W='path'
_V='method'
_U='source-ip'
_T='timestamp'
_S='0'
_R='conformance-type'
_Q='namespace'
_P='revision'
_O='ietf-sztp-bootstrap-server:input'
_N='error-tag'
_M='error'
_L='protocol'
_K='text/plain'
_J='ietf-restconf:errors'
_I='name'
_H=':dynamic-callout'
_G='+'
_F='return-code'
_E='dynamic-callout'
_D='error-returned'
_C=None
_B='event-details'
_A='/'
import os,json,base64,pprint,asyncio,aiohttp,yangson,datetime,basicauth,urllib.parse,pkg_resources
from .  import yl
from .  import dal
from .  import utils
from aiohttp import web
from .native import Read
from pyasn1.type import univ
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43);supported_media_types=_m,_A6;yl4errors={_A7:{_A8:'TBD',_A9:[{_I:_AA,_P:_x,_Q:_AB,_R:_n},{_I:'ietf-restconf',_P:'2017-01-26',_Q:'urn:ietf:params:xml:ns:yang:ietf-restconf',_R:_d},{_I:'ietf-netconf-acm',_P:'2018-02-14',_Q:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_R:_n},{_I:'ietf-sztp-bootstrap-server',_P:_AC,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_R:_d},{_I:'ietf-yang-structure-ext',_P:'2020-06-22',_Q:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_R:_d},{_I:'ietf-sztp-csr',_P:_AD,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_R:_d},{_I:'ietf-crypto-types',_P:_AD,_Q:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_R:_d}]}};yl4conveyedinfo={_A7:{_A8:'TBD',_A9:[{_I:_AA,_P:_x,_Q:_AB,_R:_n},{_I:'ietf-inet-types',_P:_x,_Q:'urn:ietf:params:xml:ns:yang:ietf-inet-types',_R:_n},{_I:'ietf-sztp-conveyed-info',_P:_AC,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-conveyed-info',_R:_d}]}}
	def __init__(A,dal,mode,yl,nvh):D='sztpd';A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename(D,'yang');A.dm=yangson.DataModel(json.dumps(yl),[B]);A.dm4conveyedinfo=yangson.DataModel(json.dumps(A.yl4conveyedinfo),[B]);C=pkg_resources.resource_filename(D,'yang4errors');A.dm4errors=yangson.DataModel(json.dumps(A.yl4errors),[C,B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_S:C=_A+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode==_i:C=_A+A.dal.app_ns+_AE+B[0]+E
		elif A.mode==_e:C=_A+A.dal.app_ns+_f+B[1]+_AF+B[0]+E
		D={};D[A.dal.app_ns+_AG]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_S or A.mode==_i or B==_C:C=_A+A.dal.app_ns+':audit-log'
		elif A.mode==_e:C=_A+A.dal.app_ns+_f+B+'/audit-log'
		D={};D[A.dal.app_ns+_AG]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_restconf_root(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B[_V]=C.method;B[_W]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_G,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert I==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_yang_library_version(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B[_V]=C.method;B[_W]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_G,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert I==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_opstate_request(C,request):
		D=request;E=D.path[C.len_prefix_operational:];E=_A;G=await C._check_auth(D,E)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;F,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_Y)
		if type(F)is web.Response:A=F;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(F)==str;H=F;assert H!=_K;J=utils.Encoding[H.rsplit(_G,1)[1]]
		if E=='/ietf-yang-library:yang-library'or E==_A or E=='':A=web.Response(status=200);A.content_type=_m;A.text=getattr(yl,'sbi_rfc8572')()
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_G,1)[1]];K=utils.gen_rc_errors(_L,_Z,error_message=_AH);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_get_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;J=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=204)
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_G,1)[1]];K=utils.gen_rc_errors(_L,_Z,error_message=_AH);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_post_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_g)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message=_y)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_z)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_put_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_g)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message=_y)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_z)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_delete_config_request(C,request):
		D=request;G=D.path[C.len_prefix_running:];H=await C._check_auth(D,G)
		if type(H)is web.Response:A=H;return A
		else:L=H
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_g)
		if type(E)is web.Response:A=E;N=M;B[_F]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(L,B);return A
		else:
			assert type(E)==str;I=E
			if I==_K:J=_C
			else:J=utils.Encoding[I.rsplit(_G,1)[1]]
		if G==_A or G=='':A=web.Response(status=400);F=_y;K=utils.gen_rc_errors(_X,_a,error_message=F)
		else:A=web.Response(status=404);F=_z;K=utils.gen_rc_errors(_L,_Z,error_message=F)
		A.content_type=I
		if J is _C:A.text=F
		else:O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,O)
		B[_F]=A.status;B[_D]=K;await C._insert_bootstrapping_log_entry(L,B);return A
	async def handle_action_request(C,request):
		D=request;F=D.path[C.len_prefix_operational:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_g)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message='Resource does not support action.')
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_AI)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_rpc_request(C,request):
		P='sleep';D=request;F=D.path[C.len_prefix_operations:];J=await C._check_auth(D,F)
		if type(J)is web.Response:A=J;return A
		else:E=J
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;H,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_g)
		if type(H)is web.Response:A=H;N=M;B[_F]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(E,B);return A
		else:
			assert type(H)==str;K=H
			if K==_K:L=_C
			else:L=utils.Encoding[K.rsplit(_G,1)[1]]
		if F==_A0:
			async with C.nvh.fifolock(Read):
				if os.environ.get('SZTPD_MODE')and P in D.query:await asyncio.sleep(int(D.query[P]))
				A=await C._handle_get_bootstrapping_data_rpc(E,D,B);B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_AJ:
			try:A=await C._handle_report_progress_rpc(E,D,B)
			except NotImplementedError as Q:raise NotImplementedError('is this ever called?')
			B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_A or F=='':A=web.Response(status=400);G=_AI;I=utils.gen_rc_errors(_X,_a,error_message=G)
		else:A=web.Response(status=404);G='Unrecognized RPC.';I=utils.gen_rc_errors(_L,_Z,error_message=G)
		A.content_type=K
		if A.content_type==_K:A.text=G
		else:I=utils.gen_rc_errors(_L,_a,error_message=G);O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,L,C.dm4errors,O)
		B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(E,B);return A
	async def _check_auth(A,request,data_path):
		z='num-times-accessed';y='local-truststore-reference';x=':device-type';w='identity-certificates';v='activation-code';u='" not found for any tenant.';t='Device "';s='X-Client-Cert';e='verification';d='device-type';T='sbi-access-stats';P='lifecycle-statistics';J='comment';I='failure';H='outcome';C=request
		def F(request,supported_media_types):
			E='Accept';D=supported_media_types;C=request;B=web.Response(status=401)
			if E in C.headers and any((C.headers[E]==A for A in D)):B.content_type=C.headers[E]
			elif _j in C.headers and any((C.headers[_j]==A for A in D)):B.content_type=C.headers[_j]
			else:B.content_type=_K
			if B.content_type!=_K:F=utils.Encoding[B.content_type.rsplit(_G,1)[1]];G=utils.gen_rc_errors(_L,_A1);H=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(G,F,A.dm4errors,H)
			return B
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B['source-proxies']=list(C.forwarded);B['host']=C.host;B[_V]=C.method;B[_W]=C.path;K=set();M=_C;N=C.transport.get_extra_info('peercert')
		if N is not _C:O=N['subject'][-1][0][1];K.add(O)
		elif C.headers.get(s)!=_C:f=C.headers.get(s);U=bytes(urllib.parse.unquote(f),'utf-8');M=x509.load_pem_x509_certificate(U,default_backend());g=M.subject;O=g.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;K.add(O)
		Q=_C;V=_C;R=C.headers.get('AUTHORIZATION')
		if R!=_C:Q,V=basicauth.decode(R);K.add(Q)
		if len(K)==0:B[H]=I;B[J]='Device provided no identification credentials.';await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
		if len(K)!=1:B[H]=I;B[J]='Device provided mismatched authentication credentials ('+O+' != '+Q+').';await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
		E=K.pop();D=_C
		if A.mode==_S:L=_A+A.dal.app_ns+_k
		elif A.mode==_i:L=_A+A.dal.app_ns+_AE+E
		if A.mode!=_e:
			try:D=await A.dal.handle_get_opstate_request(L)
			except dal.NodeNotFound as W:B[H]=I;B[J]=t+E+u;await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
			G=_C
		else:
			try:G=await A.dal.get_tenant_name_for_global_key(_A+A.dal.app_ns+':tenants/tenant/devices/device',E)
			except dal.NodeNotFound as W:B[H]=I;B[J]=t+E+u;await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
			L=_A+A.dal.app_ns+_f+G+_AF+E;D=await A.dal.handle_get_opstate_request(L)
		assert D!=_C;assert A.dal.app_ns+_k in D;D=D[A.dal.app_ns+_k]
		if A.mode!=_S:D=D[0]
		if v in D:
			if R==_C:B[H]=I;B[J]='Activation code required but none passed for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
			X=D[v];assert X.startswith('$5$')
			if not sha256_crypt.verify(V,X):B[H]=I;B[J]='Activation code mismatch for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
		else:0
		assert d in D;h=_A+A.dal.app_ns+':device-types/device-type='+D[d];Y=await A.dal.handle_get_opstate_request(h)
		if w in Y[A.dal.app_ns+x][0]:
			if N is _C and M is _C:B[H]=I;B[J]='Client cert required but none passed for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
			if N:Z=C.transport.get_extra_info(_A2);assert Z is not _C;a=Z.getpeercert(_Y)
			else:assert M is not _C;a=U
			S=Y[A.dal.app_ns+x][0][w];assert e in S;assert y in S[e];b=S[e][y];i=_A+A.dal.app_ns+':truststore/certificate-bags/certificate-bag='+b['certificate-bag']+'/certificate='+b['certificate'];j=await A.dal.handle_get_config_request(i);k=j[A.dal.app_ns+':certificate'][0]['cert-data'];l=base64.b64decode(k);m,n=der_decoder(l,asn1Spec=rfc5652.ContentInfo());assert not n;o=utils.degenerate_cms_obj_to_ders(m);p=ValidationContext(trust_roots=o);q=CertificateValidator(a,validation_context=p)
			try:q._validate_path()
			except PathBuildingError as W:B[H]=I;B[J]="Client cert for serial number '"+E+"' does not validate using trust anchors specified by device-type '"+D[d]+"'";await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
		B[H]='success';await A._insert_audit_log_entry(G,B);r=L+'/lifecycle-statistics';c=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if D[P][T][z]==0:D[P][T]['first-accessed']=c
		D[P][T]['last-accessed']=c;D[P][T][z]+=1;await A.dal.handle_put_opstate_request(r,D[P]);return E,G
	async def _handle_get_bootstrapping_data_rpc(A,device_id,request,bootstrapping_log_entry):
		Aj='ietf-sztp-bootstrap-server:output';Ai='ASCII';Ah='content';Ag='contentType';Af=':configuration';Ae='configuration-handling';Ad='script';Ac='hash-value';Ab='hash-algorithm';Aa='address';AZ='referenced-definition';AY='not';AX='match-criteria';AW='matched-response';AE='post-configuration-script';AD='configuration';AC='pre-configuration-script';AB='os-version';AA='os-name';A9='trust-anchor';A8='port';A7='bootstrap-server';A6='ietf-sztp-conveyed-info:redirect-information';A5='value';A4='response-manager';v='image-verification';u='download-uri';t='boot-image';s='selected-response';l=device_id;k='onboarding-information';j='key';f='reference';c='ietf-sztp-conveyed-info:onboarding-information';b='redirect-information';X=request;N='response';J='managed-response';I='response-details';E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_entry;g,AF=utils.check_http_headers(X,A.supported_media_types,accept_required=_Y)
		if type(g)is web.Response:B=g;AG=AF;C[_F]=B.status;C[_D]=AG;return B
		else:assert type(g)==str;O=g;assert O!=_K;T=utils.Encoding[O.rsplit(_G,1)[1]]
		L=_C
		if X.body_exists:
			AH=await X.text();AI=utils.Encoding[X.headers[_j].rsplit(_G,1)[1]]
			try:G=A.dm.get_schema_node(_A0);L=utils.encoded_str_to_obj(AH,AI,A.dm,G)
			except Exception as Y:B=web.Response(status=400);m=_o+str(Y);B.content_type=O;H=utils.gen_rc_errors(_L,_h,error_message=m);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
			if not _O in L:
				B=web.Response(status=400)
				if not _O in L:m=_o+_AK
				B.content_type=O;H=utils.gen_rc_errors(_L,_h,error_message=m);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
		C[_B]={};C[_B][E]={}
		if L is _C:C[_B][E][_A3]={'no-input-passed':[_C]}
		else:C[_B][E][_A3]=L[_O]
		if A.mode!=_e:P=_A+A.dal.app_ns+':'
		else:P=_A+A.dal.app_ns+_f+l[1]+_A
		if A.mode==_S:w=P+'device'
		else:w=P+'devices/device='+l[0]
		try:R=await A.dal.handle_get_config_request(w)
		except Exception as Y:B=web.Response(status=501);B.content_type=_m;H=utils.gen_rc_errors(_X,_l,error_message='Unhandled exception: '+str(Y));B.text=utils.enc_rc_errors('json',H);return B
		assert R!=_C;assert A.dal.app_ns+_k in R;R=R[A.dal.app_ns+_k]
		if A.mode!=_S:R=R[0]
		if A4 not in R or AW not in R[A4]:B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_X,_p,error_message='No responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;C[_B][E][s]='no-responses-configured';return B
		F=_C
		for h in R[A4][AW]:
			if not AX in h:F=h;break
			if L is _C:continue
			for Q in h[AX]['match']:
				if Q[j]not in L[_O]:break
				if'present'in Q:
					if AY in Q:
						if Q[j]in L[_O]:break
					elif Q[j]not in L[_O]:break
				elif A5 in Q:
					if AY in Q:
						if Q[A5]==L[_O][Q[j]]:break
					elif Q[A5]!=L[_O][Q[j]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:F=h;break
		if F is _C or'none'in F[N]:
			if F is _C:C[_B][E][s]='no-match-found'
			else:C[_B][E][s]=F[_I]+" (explicit 'none')"
			B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_X,_p,error_message='No matching responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
		C[_B][E][s]=F[_I];C[_B][E][I]={J:{}}
		if D in F[N]:
			C[_B][E][I][J]={D:{}};M={}
			if _E in F[N][D]:
				C[_B][E][I][J][D]={_E:{}};assert f in F[N][D][_E];n=F[N][D][_E][f];C[_B][E][I][J][D][_E][_I]=n;S=await A.dal.handle_get_config_request(P+'dynamic-callouts/dynamic-callout='+n);assert n==S[A.dal.app_ns+_H][0][_I];C[_B][E][I][J][D][_E][_q]=S[A.dal.app_ns+_H][0][_q];Z={}
				if A.mode!=_S:Z[_r]=l[0]
				else:Z[_r]=_AL
				Z[_AM]=X.remote;x=X.transport.get_extra_info(_A2)
				if x:
					y=x.getpeercert(_Y)
					if y:Z[_AN]=y
				if L:Z[_AO]=L
				if _b in S[A.dal.app_ns+_H][0]:
					C[_B][E][I][J][D][_E][_A4]=_b;z=S[A.dal.app_ns+_H][0][_b][_s];A0=S[A.dal.app_ns+_H][0][_b][_t];C[_B][E][I][J][D][_E][_AP]={_s:z,_t:A0};C[_B][E][I][J][D][_E][_c]={}
					if _u in S[A.dal.app_ns+_H][0]:A1=S[A.dal.app_ns+_H][0][_u]
					else:A1=_C
					K=_C
					try:K=A.nvh.plugins[z][_AQ][A0](Z,A1)
					except Exception as Y:C[_B][E][I][J][D][_E][_c][_AR]=str(Y);B=web.Response(status=500);B.content_type=O;H=utils.gen_rc_errors(_X,_l,error_message='Server encountered an error while trying to generate a response: '+str(Y));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
					assert K and type(K)==dict
					if _J in K:
						assert len(K[_J][_M])==1
						if any((A==K[_J][_M][0][_N]for A in(_a,_AS,_AT,_AU,_AV,_AW,_Z,_AX,_h))):B=web.Response(status=400)
						elif any((A==K[_J][_M][0][_N]for A in _A1)):B=web.Response(status=403)
						elif any((A==K[_J][_M][0][_N]for A in(_AY,_AZ,_Aa,_Ab,_p))):B=web.Response(status=409)
						elif any((A==K[_J][_M][0][_N]for A in(_Ac,_Ad,_Ae))):B=web.Response(status=500)
						elif any((A==K[_J][_M][0][_N]for A in _l)):B=web.Response(status=501)
						else:raise NotImplementedError(_Af+K[_J][_M][0][_N])
						B.content_type=O;H=K;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=K;C[_B][E][I][J][D][_E][_c][_v]=_Ag;return B
					else:C[_B][E][I][J][D][_E][_c][_v]='Returning conveyed information provided by callback.'
				elif _A5 in S[A.dal.app_ns+_H][0]:C[_B][E][I][J][D][_E][_A4]=_w;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(S[A.dal.app_ns+_H][0]))
				M=K
			elif b in F[N][D]:
				C[_B][E][I][J][D]={b:{}};M[A6]={};M[A6][A7]=[]
				if f in F[N][D][b]:
					d=F[N][D][b][f];C[_B][E][I][J][D][b]={AZ:d};o=await A.dal.handle_get_config_request(P+'conveyed-information-responses/redirect-information-response='+d)
					for AJ in o[A.dal.app_ns+':redirect-information-response'][0][b][A7]:
						W=await A.dal.handle_get_config_request(P+'bootstrap-servers/bootstrap-server='+AJ);W=W[A.dal.app_ns+':bootstrap-server'][0];i={};i[Aa]=W[Aa]
						if A8 in W:i[A8]=W[A8]
						if A9 in W:i[A9]=W[A9]
						M[A6][A7].append(i)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(F[N][D][b]))
			elif k in F[N][D]:
				C[_B][E][I][J][D]={};M[c]={}
				if f in F[N][D][k]:
					d=F[N][D][k][f];C[_B][E][I][J][D][k]={AZ:d};o=await A.dal.handle_get_config_request(P+'conveyed-information-responses/onboarding-information-response='+d);U=o[A.dal.app_ns+':onboarding-information-response'][0][k]
					if t in U:
						AK=U[t];AL=await A.dal.handle_get_config_request(P+'boot-images/boot-image='+AK);V=AL[A.dal.app_ns+':boot-image'][0];M[c][t]={};a=M[c][t]
						if AA in V:a[AA]=V[AA]
						if AB in V:a[AB]=V[AB]
						if u in V:
							a[u]=list()
							for AM in V[u]:a[u].append(AM)
						if v in V:
							a[v]=list()
							for A2 in V[v]:p={};p[Ab]=A2[Ab];p[Ac]=A2[Ac];a[v].append(p)
					if AC in U:AN=U[AC];AO=await A.dal.handle_get_config_request(P+'scripts/pre-configuration-script='+AN);M[c][AC]=AO[A.dal.app_ns+':pre-configuration-script'][0][Ad]
					if AD in U:AP=U[AD];A3=await A.dal.handle_get_config_request(P+'configurations/configuration='+AP);M[c][Ae]=A3[A.dal.app_ns+Af][0][Ae];M[c][AD]=A3[A.dal.app_ns+Af][0]['config']
					if AE in U:AQ=U[AE];AR=await A.dal.handle_get_config_request(P+'scripts/post-configuration-script='+AQ);M[c][AE]=AR[A.dal.app_ns+':post-configuration-script'][0][Ad]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(F[N][D]))
		else:raise NotImplementedError('unhandled response type: '+str(F[N]))
		e=rfc5652.ContentInfo()
		if O==_m:e[Ag]=A.id_ct_sztpConveyedInfoJSON;e[Ah]=encode_der(json.dumps(M,indent=2),asn1Spec=univ.OctetString())
		else:assert O==_A6;e[Ag]=A.id_ct_sztpConveyedInfoXML;G=A.dm4conveyedinfo.get_schema_node(_A);assert G;AS=utils.obj_to_encoded_str(M,T,A.dm4conveyedinfo,G,strip_wrapper=_Y);e[Ah]=encode_der(AS,asn1Spec=univ.OctetString())
		AT=encode_der(e,rfc5652.ContentInfo());q=base64.b64encode(AT).decode(Ai);AU=base64.b64decode(q);AV=base64.b64encode(AU).decode(Ai);assert q==AV;r={};r[Aj]={};r[Aj][D]=q;B=web.Response(status=200);B.content_type=O;G=A.dm.get_schema_node(_A0);B.text=utils.obj_to_encoded_str(r,T,A.dm,G);return B
	async def _handle_report_progress_rpc(A,device_id,request,bootstrapping_log_entry):
		m='remote-port';l='webhook-results';e='tcp-client-parameters';d='encoding';W='http';V=device_id;L=request;E='report-progress-event';C=bootstrapping_log_entry;S,f=utils.check_http_headers(L,A.supported_media_types,accept_required=_g)
		if type(S)is web.Response:B=S;g=f;C[_F]=B.status;C[_D]=g;return B
		else:assert type(S)==str;J=S
		if J!=_K:O=utils.Encoding[J.rsplit(_G,1)[1]]
		if not L.body_exists:
			M='RPC "input" node missing (required for "report-progress").';B=web.Response(status=400);B.content_type=J
			if B.content_type==_K:B.text=M
			else:F=utils.gen_rc_errors(_L,_a,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G)
			C[_D]=B.text;return B
		h=utils.Encoding[L.headers[_j].rsplit(_G,1)[1]];i=await L.text()
		try:G=A.dm.get_schema_node(_AJ);P=utils.encoded_str_to_obj(i,h,A.dm,G)
		except Exception as K:B=web.Response(status=400);M=_o+str(K);B.content_type=J;F=utils.gen_rc_errors(_L,_h,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
		if not _O in P:
			B=web.Response(status=400)
			if not _O in P:M=_o+_AK
			B.content_type=J;F=utils.gen_rc_errors(_L,_h,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
		C[_B]={};C[_B][E]={};C[_B][E][_A3]=P[_O];C[_B][E][_E]={}
		if A.mode==_S or A.mode==_i:Q=_A+A.dal.app_ns+':preferences/outbound-interactions/relay-progress-report-callout'
		elif A.mode==_e:Q=_A+A.dal.app_ns+_f+V[1]+'/preferences/outbound-interactions/relay-progress-report-callout'
		try:j=await A.dal.handle_get_config_request(Q)
		except Exception as K:C[_B][E][_E]['no-callout-configured']=[_C]
		else:
			T=j[A.dal.app_ns+':relay-progress-report-callout'];C[_B][E][_E][_I]=T
			if A.mode==_S or A.mode==_i:Q=_A+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+T
			elif A.mode==_e:Q=_A+A.dal.app_ns+_f+V[1]+'/dynamic-callouts/dynamic-callout='+T
			H=await A.dal.handle_get_config_request(Q);assert T==H[A.dal.app_ns+_H][0][_I];C[_B][E][_E][_q]=H[A.dal.app_ns+_H][0][_q];N={}
			if A.mode!=_S:N[_r]=V[0]
			else:N[_r]=_AL
			N[_AM]=L.remote;X=L.transport.get_extra_info(_A2)
			if X:
				Y=X.getpeercert(_Y)
				if Y:N[_AN]=Y
			if P:N[_AO]=P
			if _b in H[A.dal.app_ns+_H][0]:
				C[_B][E][_E][_A4]=_b;Z=H[A.dal.app_ns+_H][0][_b][_s];a=H[A.dal.app_ns+_H][0][_b][_t];C[_B][E][_E][_AP]={_s:Z,_t:a};C[_B][E][_E][_c]={}
				if _u in H[A.dal.app_ns+_H][0]:b=H[A.dal.app_ns+_H][0][_u]
				else:b=_C
				D=_C
				try:D=A.nvh.plugins[Z][_AQ][a](N,b)
				except Exception as K:C[_B][E][_E][_c][_AR]=str(K);B=web.Response(status=500);B.content_type=J;F=utils.gen_rc_errors(_X,_l,error_message='Server encountered an error while trying to process the progress report: '+str(K));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
				if D:
					assert type(D)==dict;assert len(D)==1;assert _J in D;assert len(D[_J][_M])==1
					if any((A==D[_J][_M][0][_N]for A in(_a,_AS,_AT,_AU,_AV,_AW,_Z,_AX,_h))):B=web.Response(status=400)
					elif any((A==D[_J][_M][0][_N]for A in _A1)):B=web.Response(status=403)
					elif any((A==D[_J][_M][0][_N]for A in(_AY,_AZ,_Aa,_Ab,_p))):B=web.Response(status=409)
					elif any((A==D[_J][_M][0][_N]for A in(_Ac,_Ad,_Ae))):B=web.Response(status=500)
					elif any((A==D[_J][_M][0][_N]for A in _l)):B=web.Response(status=501)
					else:raise NotImplementedError(_Af+D[_J][_M][0][_N])
					B.content_type=J;F=D;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=D;C[_B][E][_E][_c][_v]=_Ag;return B
				else:C[_B][E][_E][_c][_v]='Callback returned no output (normal)'
			elif _A5 in H[A.dal.app_ns+_H][0]:
				C[_B][E][_E][l]={_w:[]}
				for I in H[A.dal.app_ns+_H][0][_A5][_w]:
					R={};R[_I]=I[_I]
					if d not in I or I[d]=='json':c=rpc_input_json
					elif I[d]=='xml':c=rpc_input_xml
					if W in I:
						U='http://'+I[W][e]['remote-address']
						if m in I[W][e]:U+=':'+str(I[W][e][m])
						U+='/relay-notification';R['uri']=U
						try:
							async with aiohttp.ClientSession()as k:B=await k.post(U,data=c)
						except aiohttp.client_exceptions.ClientConnectorError as K:R['connection-error']=str(K)
						else:
							R['http-status-code']=B.status
							if B.status==200:break
					else:assert'https'in I;raise NotImplementedError('https-based webhook is not supported yet.')
					C[_B][E][_E][l][_w].append(R)
			else:raise NotImplementedError('unrecognized callout type '+str(H[A.dal.app_ns+_H][0]))
		B=web.Response(status=204);return B