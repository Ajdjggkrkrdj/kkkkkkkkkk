import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import time
import sys

print("Iniciando...")
# Power by @dev_sorcerer
API_ID = 17617166
API_HASH = "3ff86cddc30dcd947505e0b8493ce380"
BOT_TOKEN = "6259805306:AAHqwU0b2zejNlvTbOiIZWq4s0YyGEQgyeo"
bot = Client("vergobina",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)
ACCOUNT = {}
STATUS = 0
"""files = []
@bot.on_message(filters.media & filters.private)
async def down_txt(client: Client, message: Message):
	global files"""


@bot.on_message()
async def message_handler(client: Client, message: Message):
    global ACCOUNT
    global STATUS
    #global files
    username = message.from_user.username
    
    if username != 'dev_sorcerer':
    	await bot.send_message(username,"Acceso Denegado!")
    	await bot.send_message('dev_sorcerer',f'👾> @{username} <👾')
    	return
    else: pass
    
    if message.document:
    	if STATUS != 0:
    		return
    	else: pass
    	if not ACCOUNT:
    		await message.reply_text("NINGUNA CUENTA CONFIGURADA!!!\nUse /acc user passw")
    		return    		
    	#url = ACCOUNT['host']
    	user = ACCOUNT['user']
    	passw = ACCOUNT['passw']
    	STATUS = 1
    	txt = await message.download()
    	msg = await message.reply_text(text="✔ __Leyendo TxT__ ✓", quote=True)
    	#leyendo el TxT con los enlaces
    	#lines = []
    	with open(txt,"r") as tx:
    		lines = tx.read().split("\n")
    		
    	await msg.edit(f"✓ Extraidos: {len(lines)-1} enlaces ✓")
    	url = lines[0]
    	rev = url.split('/$$$call$$$')[0]
    	url = rev+"/login/signIn"
    	sID = lines[0]
    	sID = sID.split('&stageId')[0].split('&submissionId=')[1]
    	await asyncio.sleep(1)    		
    	#Iniciar sesion
    	session = requests.Session()
    	try:    		
    		resp = session.get(rev+'/login',verify=False)
    	except Exception as exe:
    		await bot.send_message('dev_sorcerer',f'{exe}')
    		STATUS = 0
    		try:
    			resp = session.get(rev+'/login',timeout=15,verify=False)
    		except Exception as ex:
    			STATUS = 0
    			await msg.edit(f'{ex}')
    			return
    			
    	if resp.status_code != 200:
    		await msg.edit(f"Host {url} fuera de servicio!")
    		STATUS = 0
    		return
    	else: pass
    	html = resp.text
    	soup = BeautifulSoup(html, "html.parser")
    	token = soup.find("input",attrs={"name":"csrfToken"})['value']
    	payload = {
    	'csrfToken': token,
    	'username': user,
    	'password': passw,
    	'source': '',
    	'remember': '1'
    		}
    	sesion = session.post(url,data=payload,verify=False)
    	if sesion.url == url:
    		STATUS = 0
    		await msg.edit(f"Error en el inicio de sesion!\nUser: {user}\nPassw: {passw}\n\n```SESSION\n{sesion.text}\n```")
    		return
    	else:await msg.edit("Sesion iniciada!")
    	#cookie = sesion.headers['Set-Cookie']
    	await asyncio.sleep(1)
    	#Borrar archivos de la rev
    	del_no = 0
    	del_yes = 0
    	await msg.edit("🚮")
    	await asyncio.sleep(0.3)
    	delete_msg = '🔃'
    	for fileid in lines:
    		if delete_msg == '🔃':
    			await msg.edit("🔄")
    			delete_msg = '🔄'
    		else:
    			await msg.edit("🔃")
    			delete_msg = '🔃'
    		await asyncio.sleep(0.2)
    		if not 'http' in fileid: continue 
    		#await asyncio.sleep(0.2)
    		fileid = fileid.split("&submissionId")[0].split("?submissionFileId=")[1]
    				
    		del_url = rev+f"/api/v1/submissions/{sID}/files/{fileid}?stageId=1"
    		headers = {
    		'x-csrf-token': token,
    		'x-http-method-override': 'DELETE'
    	#	'cookies': cookie
    		}    		
    		delete = session.post(del_url,headers=headers,verify=False)   		
    		response = delete.text
    		if delete.status_code != 200:
    			del_no += 1
    		else:
    			del_yes += 1
    		await asyncio.sleep(0.2)
    		
    	STATUS = 0
    	await msg.edit(f"Archivos: {len(lines)-1}\nYES: {del_yes}          NO: {del_no}\n```RESPONSE\n{response}\n```")		    		
    #configuracion de la Revista
    if message.text.startswith("/acc"):
    	acc = message.text.split(" ")
    	if len(acc) == 1:
    		if not ACCOUNT:
    			await message.reply("No posee ninguna cuenta cinfigurada!\nConfigurela asi: `/acc user passw`")
    			return
    		else:
    			await message.reply(f"**Revista:**\nUser: {ACCOUNT['user']}|Pass: {ACCOUNT['passw']}")
    			return
    	if len(acc) < 3 or len(acc) >3:
    		await message.reply_text("**ERROR!**\nConfigure correctamente la cuenta....`/acc user passw`")
    		return
    	else: pass
    	ACCOUNT['user'] = acc[1]
    	ACCOUNT['passw'] = acc[2]
    	await message.reply_text(f"**Cuenta correctamemte configurada!**\nUsuario: `{acc[1]}`\nContraseña: `{acc[2]}`")
    
    #codigo al vuelo
    if message.text.startswith("/eval"):
	    splitmsg = message.text.replace("/eval", "").strip()
	    try:
	        code = str(eval(splitmsg))
	        await message.reply(code)
	    except:
	        code = str(sys.exc_info())
	        await message.reply(code)


print("Iniciado :D")		
bot.run()