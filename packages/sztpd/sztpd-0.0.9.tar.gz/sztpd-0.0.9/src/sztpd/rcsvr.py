# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_C='/ds/ietf-datastores:operational'
_B='/ds/ietf-datastores:running'
_A=None
import os,ssl,json,base64,pyasn1,asyncio,yangson,datetime,tempfile,basicauth
from .  import utils
from aiohttp import web
from .handler import RouteHandler
from pyasn1.type import univ
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
async def set_server_header(request,response):response.headers['Server']='<redacted>'
class RestconfServer:
	root='/restconf';prefix_running=root+_B;prefix_operational=root+_C;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler,facade_yl=_A):
		AC='client-certs';AB='local-truststore-reference';AA='ca-certs';A9='client-authentication';A8='\n-----END CERTIFICATE-----\n';A7='-----BEGIN CERTIFICATE-----\n';A6='cert-data';A5='private-key-format';A4=':keystore/asymmetric-keys/asymmetric-key=';A3='reference';A2='server-identity';A1='local-port';A0='http';j='ASCII';i=':asymmetric-key';h='tcp-server-parameters';S='certificate';R='tls-server-parameters';Q='/ds/ietf-datastores:running{tail:.*}';P='/';G=dal;E='https';C=endpoint_config;B=view_handler;A.len_prefix_running=len(A.root+_B);A.len_prefix_operational=len(A.root+_C);A.loop=loop;A.dal=G;A.name=C['name'];A.view_handler=B;A.app=web.Application();A.app.on_response_prepare.append(set_server_header);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,B.handle_get_restconf_root);A.app.router.add_get(A.root+P,B.handle_get_restconf_root);A.app.router.add_get(A.root+'/yang-library-version',B.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',B.handle_get_opstate_request);A.app.router.add_get(A.root+Q,B.handle_get_config_request);A.app.router.add_put(A.root+Q,B.handle_put_config_request);A.app.router.add_post(A.root+Q,B.handle_post_config_request);A.app.router.add_delete(A.root+Q,B.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',B.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',B.handle_rpc_request)
		if A0 in C:F=A0
		else:assert E in C;F=E
		A.local_address=C[F][h]['local-address'];A.local_port=os.environ.get('SZTPD_DEFAULT_PORT',8080)
		if A1 in C[F][h]:A.local_port=C[F][h][A1]
		D=_A
		if F==E:
			T=C[E][R][A2][S][A3]['asymmetric-key'];J=A.dal.handle_get_config_request(P+A.dal.app_ns+A4+T);K=A.loop.run_until_complete(J);L=K[A.dal.app_ns+i][0]['cleartext-private-key'];U=base64.b64decode(L)
			if K[A.dal.app_ns+i][0][A5]=='ietf-crypto-types:ec-private-key-format':M,k=der_decoder(U,asn1Spec=rfc5915.ECPrivateKey());l=der_encoder(M);V=base64.b64encode(l).decode(j);assert L==V;W='-----BEGIN EC PRIVATE KEY-----\n'+V+'\n-----END EC PRIVATE KEY-----\n'
			elif K[A.dal.app_ns+i][0][A5]=='ietf-crypto-types:rsa-private-key-format':M,k=der_decoder(U,asn1Spec=rfc3447.RSAPrivateKey());m=der_encoder(M);X=base64.b64encode(m).decode(j);assert L==X;W='-----BEGIN RSA PRIVATE KEY-----\n'+X+'\n-----END RSA PRIVATE KEY-----\n'
			else:raise NotImplementedError('this line can never be reached')
			n=C[E][R][A2][S][A3][S];J=A.dal.handle_get_config_request(P+A.dal.app_ns+A4+T+'/certificates/certificate='+n);o=A.loop.run_until_complete(J);p=o[A.dal.app_ns+':certificate'][0][A6];q=base64.b64decode(p);r,Y=der_decoder(q,asn1Spec=rfc5652.ContentInfo());s=r.getComponentByName('content');t,Y=der_decoder(s,asn1Spec=rfc5652.SignedData());Z=t.getComponentByName('certificates');H=''
			for u in range(len(Z)):
				a=Z[u][0]
				for b in a['tbsCertificate']['extensions']:
					if b['extnID']==rfc5280.id_ce_basicConstraints:v,Y=der_decoder(b['extnValue'],asn1Spec=rfc5280.BasicConstraints())
				w=der_encoder(a);c=base64.b64encode(w).decode(j)
				if v['cA']==False:H=A7+c+A8+H
				else:H+=A7+c+A8
			D=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);D.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as d:
				e=d+'key.pem';f=d+'certs.pem'
				with open(e,'w')as x:x.write(W)
				with open(f,'w')as y:y.write(H)
				D.load_cert_chain(f,e)
			if A9 in C[E][R]:
				I=C[E][R][A9]
				def g(truststore_ref):
					C=G.handle_get_config_request(P+G.app_ns+':truststore/certificate-bags/certificate-bag='+truststore_ref);D=A.loop.run_until_complete(C);B=[]
					for E in D[G.app_ns+':certificate-bag'][0][S]:F=base64.b64decode(E[A6]);H,I=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not I;B+=utils.degenerate_cms_obj_to_ders(H)
					return B
				N=[]
				if AA in I:O=I[AA][AB];N+=g(O)
				if AC in I:O=I[AC][AB];N+=g(O)
				z=utils.der_dict_to_multipart_pem({'CERTIFICATE':N});D.load_verify_locations(cadata=z)
		if F==E:assert not D is _A
		else:assert D is _A
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=D,reuse_port=True);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A