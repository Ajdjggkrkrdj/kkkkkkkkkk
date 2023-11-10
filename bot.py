import asyncio
from pyrogram.types import Message
from pyrogram import Client
import requests
from bs4 import BeautifulSoup
import time
import sys

print("Iniciando...")

API_ID = 17617166
API_HASH = "3ff86cddc30dcd947505e0b8493ce380"
BOT_TOKEN = "6259805306:AAHqwU0b2zejNlvTbOiIZWq4s0YyGEQgyeo"
bot = Client("vergobina",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)
ACCOUNT = {}
STATUS = 0

def start_message(client: Client, message: Message):
    bot.send_message("dev_sorcerer", "Reiniciado y listo para funcionar de nuevo! 🚀")
    
@bot.on_message()
async def message_handler(client: Client, message: Message):
    global ACCOUNT
    global STATUS
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
    	files = []
    	lines = []
    	for document in message.document:
    		await files.append(bot.download_media(document))
    		
    	#url = ACCOUNT['host']
    	user = ACCOUNT['user']
    	passw = ACCOUNT['passw']
    	STATUS = 1
    	#txt = await message.download()
    	msg = await message.reply_text(text="✔ __Leyendo TxT__ ✓", quote=True)
    	#leyendo el TxT con los enlaces
    	for txt in files:
    		with open(txt,"r") as tx:
    			lines += tx.read().split("\n")
    		
    	await msg.edit(f"✓ Extraidos: {len(lines)-1} enlaces ✓")
    	url = lines[0]
    	rev = url.split('/$$$call$$$')[0]
    	url = rev+"/login/signIn"
    	sID = lines[0]
    	sID = sID.split('&stageId')[0].split('&submissionId=')[1]
    	time.sleep(1)    		
    	#Iniciar sesion
    	session = requests.Session()
    	resp = session.get(url)
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
    	sesion = session.post(url,data=payload)
    	#cookie = sesion.headers['Set-Cookie']
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
    	for fileid in lines:
    		if not 'http' in fileid: continue 
    		#await asyncio.sleep(0.2)
    		fileid = fileid.split("&submissionId")[0].split("?submissionFileId=")[1]
    				
    		del_url = rev+f"/api/v1/submissions/{sID}/files/{fileid}?stageId=1"
    		headers = {
    		'x-csrf-token': token,
    		'x-http-method-override': 'DELETE'
    #		'cookies': cookie
    		}
    		await asyncio.sleep(0.3)
    		delete = session.post(del_url,headers=headers)
    		response = delete.text
    		if delete.status_code != 200:
    			del_no += 1
    		else:
    			del_yes += 1
    	STATUS = 0
    	await msg.edit(f"Archivos: {len(lines)-len(files)}\nYES: {del_yes}          NO: {del_no}\n```RESPONSE\n{response}\n```")
    		#https://apye.esceg.cu/index.php/apye/$$$call$$$/api/file/file-api/download-file?submissionFileId=242505&submissionId=35216&stageId=1
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

if __name__ == '__main__':
	start_message()
	print("Iniciado :D")		
	bot.run()