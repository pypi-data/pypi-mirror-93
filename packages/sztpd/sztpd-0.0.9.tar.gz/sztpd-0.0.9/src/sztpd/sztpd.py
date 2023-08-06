# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

_G='tested?'
_F='$0$'
_E='wn-sztpd-0:device'
_D='device'
_C='activation-code'
_B='/'
_A=None
import gc,tracemalloc,os,re,json,base64,signal,asyncio,datetime,functools,pkg_resources
from passlib.hash import sha256_crypt
from .  import yl
from .  import utils
from .dal import DataAccessLayer,CreateCallbackFailed,CreateOrChangeCallbackFailed,ChangeCallbackFailed
from .rcsvr import RestconfServer
from .tenant import TenantViewHandler
from .rfc8572 import RFC8572ViewHandler
from .native import NativeViewHandler,Period,TimeUnit
from pyasn1.codec.der.decoder import decode as decode_der
from pyasn1.error import PyAsn1Error
from pyasn1_modules import rfc5652
from cryptography import x509
from cryptography.hazmat.primitives import serialization
loop=_A
sig=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def run(db_url,cacert_param=_A,cert_param=_A,key_param=_A):
	f=':tenants/tenant/bootstrap-servers/bootstrap-server/trust-anchor';e=':bootstrap-servers/bootstrap-server/trust-anchor';d=':transport';c='SIGHUP';b=True;V='use-for';U='1';Q='x';N=db_url;J=key_param;I=cert_param;H=cacert_param;global loop;global sig;A=_A;B=_A;R=False
	if H is not _A and N.startswith('sqlite:'):print('The "sqlite" dialect does not support the "cacert" parameter.');return 1
	if(I or J)and not H:print('The "cacert" parameter must be specified whenever the "key" and "cert" parameters are specified.');return 1
	if(I is _A)!=(J is _A):print('The "key" and "cert" parameters must be specified together.');return 1
	try:A=DataAccessLayer(N,H,I,J)
	except (SyntaxError,AssertionError)as K:print(str(K));return 1
	except NotImplementedError as K:R=b
	else:B=A.opaque()
	if R==b:
		L=os.environ.get('SZTPD_MODE')
		if L!=_A:
			assert type(L)==str
			if L not in[U,Q]:print("Unknown SZTPD_MODE value.  Must be '1' or 'x'.");return 1
			B=L
		else:
			print('');W=pkg_resources.resource_filename('sztpd','LICENSE.txt');S=open(W,'r');print(S.read());S.close();print('First time initialization.  Please accept the license terms.');print('');print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print('');X=input('Please enter "Yes" or "No": ')
			if X!='Yes':print('');print('Thank you for your consideration.');print('');return 1
			print('');print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print('');B=input('Please select mode: ')
			if B not in[U,Q]:print('Unknown mode selection.  Please try again.');return 1
			print('');print("Running SZTPD in mode '"+B+"'. (No more output expected)");print('')
		try:A=DataAccessLayer(N,H,I,J,json.loads(getattr(yl,'nbi_'+B)()),'wn-sztpd-'+B,B)
		except Exception as K:raise K;return 1
	assert B!=_A;assert A!=_A;tracemalloc.start(25);loop=asyncio.get_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=c));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		M=[];E=A.handle_get_config_request(_B+A.app_ns+d);O=loop.run_until_complete(E)
		for D in O[A.app_ns+d]['listen']['endpoint']:
			if D[V]=='native-interface':
				C=NativeViewHandler(A,B,loop)
				if B=='0':F=_B+A.app_ns+':device'
				elif B==U:F=_B+A.app_ns+':devices/device'
				elif B==Q:F=_B+A.app_ns+':tenants/tenant/devices/device'
				C.register_create_callback(F,_handle_device_created);Y=F+'/activation-code';C.register_change_callback(Y,_handle_device_act_code_changed);C.register_subtree_change_callback(F,_handle_device_subtree_changed);C.register_somehow_change_callback(F,_handle_device_somehow_changed);C.register_delete_callback(F,_handle_device_deleted);C.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations)
				if B!=Q:C.register_create_callback(_B+A.app_ns+e,_handle_bss_trust_anchor_cert_created_or_changed);C.register_change_callback(_B+A.app_ns+e,_handle_bss_trust_anchor_cert_created_or_changed)
				else:C.register_create_callback(_B+A.app_ns+f,_handle_bss_trust_anchor_cert_created_or_changed);C.register_change_callback(_B+A.app_ns+f,_handle_bss_trust_anchor_cert_created_or_changed)
				P=RestconfServer(loop,A,D,C)
			elif D[V]=='tenant-interface':Z=TenantViewHandler(C);P=RestconfServer(loop,A,D,Z)
			else:assert D[V]=='rfc8572-interface';T=json.loads(getattr(yl,'sbi_rfc8572')());a=RFC8572ViewHandler(A,B,T,C);P=RestconfServer(loop,A,D,a,T)
			M.append(P);del D;D=_A
		del O;O=_A;loop.run_forever()
		for G in M:E=G.app.shutdown();loop.run_until_complete(E);E=G.runner.cleanup();loop.run_until_complete(E);E=G.app.cleanup();loop.run_until_complete(E);del G;G=_A
		del M;M=_A
		if sig==c:sig=_A
	loop.close();del A;return 0
async def _handle_device_created_post_sweep(watched_node_path,conn,opaque):
	k=':dynamic-callout';j='webhooks';i='verification-result';h='failure';g='=';f='tenant';e='function';d='functions';c='plugin';b='callback';a='ownership-authorization';W='verification-results';V='dynamic-callout';U='device-type';T='row_id';S='=[^/]*';J='wn-sztpd-rpcs:output';H=watched_node_path;B=conn;A=opaque;C=A.dal._get_row_data_for_list_path(H,B);D=re.sub(S,'',H);X=A.dal._get_jsob_for_row_id_in_table(D,C[T],B);K=_B+A.dal.app_ns+':device-types/device-type='+X[_D][U];C=A.dal._get_row_data_for_list_path(K,B);D=re.sub(S,'',K);L=A.dal._get_jsob_for_row_id_in_table(D,C[T],B)
	if a in L[U]:
		M=_B+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+L[U][a][V]['reference'];C=A.dal._get_row_data_for_list_path(M,B);D=re.sub(S,'',M);E=A.dal._get_jsob_for_row_id_in_table(D,C[T],B)
		if b in E[V]:
			F=E[V][b];assert F[c]in A.plugins;N=A.plugins[F[c]];assert d in N;O=N[d];assert F[e]in O;Y=O[F[e]];I=H.split(_B)
			if I[2]==f:P=I[1].split(g)[1]
			else:P='not-applicable'
			Q=I[-1].split(g)[1];Z={'wn-sztpd-rpcs:input':{f:P,'serial-number':[Q]}};G=Y(Z);R=h
			if J in G:
				if W in G[J]:
					if i in G[J][W]:R=G[J][W][i][0]['result']
			if R==h:raise CreateCallbackFailed('Unable to verify ownership for device: '+Q)
		else:assert j in E[A.dal.app_ns+k][0];l=E[A.dal.app_ns+k][0][j];raise NotImplementedError('webhooks for ownership verification not implemented yet')
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh):
	C=nvh;B=jsob;assert type(B)==dict
	if jsob_data_path==_B:assert _E in B;A=B[_E]
	else:assert _D in B;A=B[_D]
	if C.dal.post_dal_callbacks is _A:C.dal.post_dal_callbacks=[]
	C.dal.post_dal_callbacks.append((_handle_device_created_post_sweep,watched_node_path,C));A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={'log-entry':[]}
	if _C in A and A[_C].startswith(_F):A[_C]=sha256_crypt.using(rounds=1000).hash(A[_C][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_B:assert _E in A;B=A[_E]
	else:assert _D in A;B=A[_D]
	if _C in B and B[_C].startswith(_F):B[_C]=sha256_crypt.using(rounds=1000).hash(B[_C][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_deleted(data_path,nvh):0
async def _handle_bss_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	N='": ';B=watched_node_path;G=jsob['bootstrap-server']['trust-anchor'];H=base64.b64decode(G)
	try:I,O=decode_der(H,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as J:raise CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B+' ('+str(J)+')')
	K=utils.degenerate_cms_obj_to_ders(I);A=[]
	for L in K:M=x509.load_der_x509_certificate(L);A.append(M)
	D=[B for B in A if B.subject==B.issuer]
	if len(D)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) certificate: '+B)
	if len(D)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root (self-signed) certificate ('+str(len(D))+' found): '+B)
	F=D[0];A.remove(F);C=F
	while len(A):
		E=[B for B in A if B.issuer==C.subject]
		if len(E)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.  CMS encodes additional certs not issued by the certificate "'+str(C.subject)+N+B)
		if len(E)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+N+B)
		C=E[0];A.remove(C)
def _check_expirations(nvh):0