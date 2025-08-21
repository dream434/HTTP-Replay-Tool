M='POST'
L=print
K=None
J='protocol'
G='file_upload_object'
E='content'
D='headers'
C='url'
B='method'
import json as A
from flask import Flask,render_template as N,request as F
import requests as H,io
I=Flask(__name__)
I.jinja_env.filters['fromjson']=A.loads
def O(filename='requests.json'):
	B=filename
	try:
		with open(B,'r')as C:return A.load(C)
	except FileNotFoundError:L(f"Erreur: Le fichier '{B}' n'a pas été trouvé.");return[]
	except A.JSONDecodeError:L(f"Erreur: Le fichier '{B}' n'est pas un JSON valide.");return[]
def P(form_data,files_data):
	M='file_upload';F=files_data;A=form_data;H={};N=A.getlist('header_key[]');O=A.getlist('header_value[]')
	for(I,P)in zip(N,O):
		if I.strip():H[I.strip()]=P.strip()
	K={B:A.get(B),C:A.get(C),D:H,E:A.get(E),J:A.get(J,'HTTP/1.1')}
	if M in F:
		L=F[M]
		if L.filename!='':K[G]=L
	return K
def Q(req_data):
	N='Content-Type';A=req_data;O=A[B];P=A[C];Q=A[D];R=10;S=False;F={B:O,C:P,D:Q,'timeout':R,'allow_redirects':S};L=K;M=K
	if G in A and A[G]:
		I=A[G];T='file';L={T:(I.filename,I.stream,I.mimetype)};F['files']=L
		if N in F[D]:del F[D][N]
	elif A.get(E)and A[E].strip()!='':M=A[E];F['data']=M
	try:U=H.request(**F);return U
	except H.exceptions.RequestException as J:return f"Une erreur est survenue lors de la requête: {J}"
	except Exception as J:return f"Une erreur inattendue est survenue: {J}"
def R(req_data,resp):
	E=resp;D=req_data;A=f"Replayed {D[B]} {D[C]} with {D[J]} - Status: {E.status_code}\n";A+='--- Response Headers ---\n'
	for(F,G)in E.headers.items():A+=f"{F}: {G}\n"
	A+='--- Response Body ---\n';A+=E.text;return A
@I.route('/',methods=['GET',M])
def S():
	D=O();A=K
	if F.method==M:
		C=P(F.form,F.files);B=Q(C)
		if isinstance(B,H.Response):A=R(C,B)
		else:A=B
	return N('index.html',requests=D,output=A)
if __name__=='__main__':I.run(host='0.0.0.0',port=5000,debug=True)
