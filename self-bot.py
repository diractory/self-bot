_J='broadcast'
_I='username'
_H='muted_users'
_G='banned_users'
_F='N/A'
_E='No'
_D='Yes'
_C=True
_B=False
_A=None
import base64,os
session_b64=os.environ.get('SESSION_STRING','')
if session_b64:
	with open('selfbot_radhey.session','wb')as f:f.write(base64.b64decode(session_b64))
import os,re,json,time,asyncio,random,requests,traceback
from uuid import uuid4
from telethon import TelegramClient,events,functions,types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.channels import GetFullChannelRequest,EditAdminRequest
try:import aiohttp;AIOHTTP_OK=_C
except ImportError:AIOHTTP_OK=_B
try:import sympy;SYMPY_OK=_C
except ImportError:SYMPY_OK=_B
try:import instaloader;INSTA_OK=_C
except ImportError:INSTA_OK=_B
API_ID=int(os.environ.get('API_ID','RADHEY ID'))
API_HASH=os.environ.get('API_HASH','RADHEY HASH')
PHONE=os.environ.get('PHONE','RDH NUMB')
OWNER_ID=8192070400
SESSION='selfbot_radhey'
DATA_FILE='selfbot_data.json'
def load_data():
	try:
		with open(DATA_FILE,'r')as f:return json.load(f)
	except(FileNotFoundError,json.JSONDecodeError):return{_H:[],_G:[]}
def save_data(d):
	with open(DATA_FILE,'w')as f:json.dump(d,f)
data=load_data()
muted_users=set(data.get(_H,[]))
banned_users=set(data.get(_G,[]))
auto_accept_active=_B
auto_fix_active=_C
ERROR_LOG_FILE='errors.log'
def log_error(cmd_text,exc):
	entry=f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CMD={cmd_text!r} ERROR={exc}\n{traceback.format_exc()}\n{'-'*60}\n"
	try:
		with open(ERROR_LOG_FILE,'a',encoding='utf-8')as f:f.write(entry)
	except Exception:pass
client=TelegramClient(SESSION,API_ID,API_HASH)
async def get_entity(val):
	try:
		if isinstance(val,int):return await client.get_entity(val)
		if val.startswith('@'):return await client.get_entity(val)
		try:return await client.get_entity(int(val))
		except Exception:return await client.get_entity(val)
	except Exception:return
async def get_admin_group_ids():
	'Only groups/channels where we are admin — safe for broadcast.';A='admin_rights';ids=[]
	async for d in client.iter_dialogs():
		if d.is_group or d.is_channel:
			try:
				perms=d.entity
				if hasattr(perms,A)and perms.admin_rights:ids.append(d.id);continue
				if hasattr(perms,'megagroup')or hasattr(perms,_J):
					full=await client(GetFullChannelRequest(d.id));chat=full.chats[0]
					if getattr(chat,A,_A):ids.append(d.id)
			except Exception:pass
	return ids
async def get_all_group_ids():
	'All groups/channels (for .gc).';ids=[]
	async for d in client.iter_dialogs():
		if d.is_group or d.is_channel:ids.append(d.id)
	return ids
async def get_dm_ids():
	ids=[]
	async for d in client.iter_dialogs():
		try:
			if d.is_user and not d.entity.bot:ids.append(d.id)
		except Exception:pass
	return ids
async def safe_sleep(count):
	'Randomised delay: 5–10s normally, 40s break every 15 messages.'
	if count>0 and count%15==0:await asyncio.sleep(40)
	else:await asyncio.sleep(random.uniform(5,10))
def _ig_info(username):
	E='en-US,en;q=0.9';D='Accept-Language';C='User-Agent';B='count';A='None';username=username.lstrip('@').strip()
	if INSTA_OK:
		try:L=instaloader.Instaloader();p=instaloader.Profile.from_username(L.context,username);return f"""📸 **Instagram — @{p.username}**
✓ **Name:** `{p.full_name or _F}`
✓ **Username:** @{p.username}
✓ **Followers:** `{p.followers:,}`
✓ **Following:** `{p.followees:,}`
✓ **Posts:** `{p.mediacount:,}`
✓ **Private:** `{_D if p.is_private else _E}`
✓ **Verified:** `{_D if p.is_verified else _E}`
✓ **Business:** `{_D if p.is_business_account else _E}`
✓ **Bio:** `{p.biography or A}`
✓ **Link:** https://instagram.com/{p.username}"""
		except Exception:pass
	try:
		session=requests.Session();session.get(f"https://www.instagram.com/{username}/",headers={C:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',D:E},timeout=10);csrf=session.cookies.get('csrftoken','');r=session.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",headers={C:'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36','x-ig-app-id':'936619743392459','x-csrftoken':csrf,'x-requested-with':'XMLHttpRequest','Accept':'*/*',D:E,'Referer':f"https://www.instagram.com/{username}/",'Origin':'https://www.instagram.com'},timeout=15)
		if r.status_code==200:u=r.json()['data']['user'];return f"""📸 **Instagram — @{u[_I]}**
✓ **Name:** `{u.get("full_name")or _F}`
✓ **IG ID:** `{u["id"]}`
✓ **Followers:** `{u["edge_followed_by"][B]:,}`
✓ **Following:** `{u["edge_follow"][B]:,}`
✓ **Posts:** `{u["edge_owner_to_timeline_media"][B]:,}`
✓ **Private:** `{_D if u["is_private"]else _E}`
✓ **Verified:** `{_D if u["is_verified"]else _E}`
✓ **Business:** `{_D if u.get("is_business_account")else _E}`
✓ **Bio:** `{u.get("biography")or A}`
✓ **External URL:** `{u.get("external_url")or A}`
✓ **Link:** https://instagram.com/{u[_I]}"""
		if r.status_code==404:return f"❌ @{username} doesn't exist or is banned."
		if r.status_code in(401,403):return f"❌ Instagram blocked the request (rate limited). Try again in a few minutes."
		return f"❌ Instagram API returned status {r.status_code}."
	except requests.exceptions.Timeout:return'❌ Request timed out. Instagram may be slow, try again.'
	except Exception as e:return f"❌ Failed to fetch info: {e}"
def _translate(text,target_lang):
	try:
		r=requests.get('https://api.mymemory.translated.net/get',params={'q':text,'langpair':f"auto|{target_lang}"},timeout=10);data=r.json()
		if data.get('responseStatus')==200:translated=data['responseData']['translatedText'];return f"🌐 **[{target_lang.upper()}]** {translated}"
		return f"❌ Translation failed: {data.get('responseDetails','unknown error')}"
	except Exception as e:return f"❌ Translation error: {e}"
async def _cmd_dispatch(event):
	N='.tr';M='⚠️ Reply to the message you want to broadcast.';L='⚠️ Reply to the message you want to forward.';K='.frwdall';J='.frwd';I='.unblock';H='.unban';G='.unmute';F='verified';E='dc_id';D='.info';C='No errors logged yet.';B='❌ User not found.';A='❌ Groups only.';global muted_users,banned_users,auto_accept_active;raw=event.raw_text.strip();text=raw.lower()
	if not text.startswith('.'):return
	if text=='.fix':global auto_fix_active;auto_fix_active=not auto_fix_active;state='ON ✅'if auto_fix_active else'OFF 🔕';await event.edit(f"**🛠 Auto-fix mode: {state}**\nWhen ON, any command error is caught, logged to `{ERROR_LOG_FILE}`, the command is retried once automatically, and you get a short error report here instead of a crash.")
	elif text=='.fixlog':
		try:
			with open(ERROR_LOG_FILE,'r',encoding='utf-8')as f:lines=f.readlines()
			tail=''.join(lines[-40:])or C
		except FileNotFoundError:tail=C
		await event.edit(f"**🧾 Last errors:**\n```\n{tail[-3500:]}\n```")
	elif text in('.help','.fux'):await event.edit("[𝗦𝗘𝗟𝗙𝗕𝗢𝗧 𝗕𝗬 #𝗥𝗔𝗗𝗛𝗘𝗬](https://t.me/xivasudev)\n\n**Channels : **\n**`.autoaccept`** — toggle auto-accept requests\n\n**User Controls : ** _(reply, @user, or user id)_\n**`.mute`** / **`.unmute`** — silence a user\n**`.unban`** — unban user\n**`.block`** / **`.unblock`** — Telegram block\n**`.kick`** — kick from group\n**`.admin`** — promote user to group admin\n**`.demote`** — remove user's admin rights\n\n**Broadcasting : **\n**`.frwd`** _(reply)_ — forward to all DMs\n**`.gc`** _(reply)_ — blast all your groups\n**`.broad`** _(reply)_ — text all users\n**`.frwdall`** _(reply)_ — DMs + groups combined\n**`.dm @user msg`** — single DM\n\n**Details : ** _(reply to get info)_\n**`.info`** — full user info\n**`.chatinfo`** — group/chat details\n**`.id`** — user or chat ID\n\n**`.count N`** — countdown (1–300s)\n**`.del`** — nuke private chat history\n**`.purge N`** — delete last N messages\n**`.close N`** — leave group after N sec\n**`.mm`** _(reply)_ — open middleman group\n**`.tag`** — tag all group members\n**`.say text`** — ghost-send a message\n\n**Reliability : **\n**`.fix`** — toggle auto-fix (retry + log errors)\n**`.fixlog`** — show last logged errors\n\n[𝗝𝗢𝗜𝗡](https://t.me/sunradhey) | by #𝗥𝗔𝗗𝗛𝗘𝗬")
	elif text=='.owner':
		lines=['**[𝗢𝘄𝗻𝗲𝗿 𝗜𝗻𝘁𝗿𝗼](tg://openmessage?user_id=8192070400)**','• Username: [@sayradhey](https://t.me/sayradhey)','• Selfbot script | Python Dev ~','• DEV ~ #𝗥𝗔𝗗𝗛𝗘𝗬','**Catch Me:** [𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠](https://t.me/sayradhey)'];msg=await event.edit('Typing...');out=''
		for line in lines:out+=line+'\n';await msg.edit(out);await asyncio.sleep(.8)
	elif text=='.autoaccept':auto_accept_active=not auto_accept_active;state='enabled ✅'if auto_accept_active else'disabled 🔕';await event.edit(f"Auto-accept chat requests {state}")
	elif text.startswith('.tinfo')or text.startswith(D):
		cmd_len=5 if text.startswith(D)else 7;target=raw[cmd_len:].strip()if len(raw)>cmd_len else _A
		try:
			if target:uf=await client(GetFullUserRequest(target))
			elif event.is_reply:reply=await event.get_reply_message();uf=await client(GetFullUserRequest(reply.sender_id))
			else:await event.edit('❌ Reply to a user or: `.info @username`');return
			u=uf.users[0]if hasattr(uf,'users')else uf.user;dc_map={1:'DC1 Miami',2:'DC2 Amsterdam',3:'DC3 Miami',4:'DC4 Amsterdam',5:'DC5 Singapore'};dc=dc_map.get(getattr(u,E,0),f"DC{getattr(u,E,'?')}");full_name=f"{u.first_name or''} {u.last_name or''}".strip();await event.edit(f"""**👤 Telegram Info**
✓ **Name:** `{full_name or _F}`
✓ **Username:** @{u.username or _F}
✓ **User ID:** `{u.id}`
✓ **Phone:** `{u.phone or _F}`
✓ **Bot:** `{_D if u.bot else _E}`
✓ **Verified:** `{_D if getattr(u,F,_B)else _E}`
✓ **Premium:** `{_D if getattr(u,"premium",_B)else _E}`
✓ **DC:** `{dc}`
✓ **Last Seen:** `{u.status.__class__.__name__ if u.status else"Hidden"}`""")
		except Exception as e:await event.edit(f"❌ Error: {e}")
	elif text=='.id':
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id);await event.edit(f"🆔 **User ID:** `{u.id}`")
		else:await event.edit(f"🆔 **Chat ID:** `{event.chat_id}`")
	elif text.startswith('.chatinfo'):
		try:
			chat=await event.get_chat()
			if hasattr(chat,'title'):members=getattr(chat,'participants_count',_F);ctype='Channel'if getattr(chat,_J,_B)else'Group/Supergroup';await event.edit(f"""**💬 Chat Info**
✓ **Title:** `{chat.title}`
✓ **ID:** `{chat.id}`
✓ **Type:** `{ctype}`
✓ **Username:** @{getattr(chat,_I,_F)or _F}
✓ **Members:** `{members}`
✓ **Verified:** `{_D if getattr(chat,F,_B)else _E}`""")
			else:me=await client.get_me();await event.edit(f"**💬 Chat Info**\n\n✓ **Type:** `Private Chat`\n✓ **Your ID:** `{me.id}`\n✓ **Chat ID:** `{event.chat_id}`")
		except Exception as e:await event.edit(f"❌ {e}")
	elif text.startswith('.insta')or text.startswith('.iginfo'):
		parts=raw.split(_A,1)
		if len(parts)<2:await event.edit('❌ Usage: `.insta @username`');return
		uname=parts[1].strip().lstrip('@');await event.edit(f"🔍 Fetching **@{uname}**...");loop=asyncio.get_event_loop();result=await loop.run_in_executor(_A,_ig_info,uname);await event.edit(result)
	elif text.startswith('.mute')and not text.startswith(G)or text.startswith('.ban')and not text.startswith(H):
		u=_A
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:u=await get_entity(parts[1].strip())
		if not u:await event.edit('❌ User not found. Reply to a user or provide @username.');return
		muted_users.add(u.id);banned_users.add(u.id);data[_H]=list(muted_users);data[_G]=list(banned_users);save_data(data);await event.edit(f"🚫 **{u.first_name or u.id}** blocked — messages will be deleted.")
	elif text.startswith(G):
		u=_A
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:u=await get_entity(parts[1].strip())
		if not u:await event.edit(B);return
		muted_users.discard(u.id);banned_users.discard(u.id);data[_H]=list(muted_users);data[_G]=list(banned_users);save_data(data);await event.edit(f"✅ **{u.first_name or u.id}** unblocked")
	elif text.startswith(H):
		u=_A
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:u=await get_entity(parts[1].strip())
		if not u:await event.edit(B);return
		banned_users.discard(u.id);data[_G]=list(banned_users);save_data(data);await event.edit(f"✅ Unbanned `{u.first_name or u.id}`")
	elif text.startswith('.block')and not text.startswith(I):
		target_id=_A
		if event.is_private:target_id=event.chat_id
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:
				u=await get_entity(parts[1].strip())
				if u:target_id=u.id
		if target_id:await client(functions.contacts.BlockRequest(id=target_id));await event.edit(f"🚫 Blocked `{target_id}`")
		else:await event.edit('❌ Use in a private chat, or: `.block @username`')
	elif text.startswith(I):
		target_id=_A
		if event.is_private:target_id=event.chat_id
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:
				u=await get_entity(parts[1].strip())
				if u:target_id=u.id
		if target_id:await client(functions.contacts.UnblockRequest(id=target_id));await event.edit(f"✅ Unblocked `{target_id}`")
		else:await event.edit('❌ Use in a private chat, or: `.unblock @username`')
	elif text.startswith('.kick'):
		if not event.is_group:await event.edit(A);return
		if not event.is_reply:await event.edit('❌ Reply to the user you want to kick.');return
		reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		try:await client.kick_participant(event.chat_id,u.id);await event.edit(f"🦵 Kicked `{u.first_name or u.id}`")
		except Exception as e:await event.edit(f"❌ {e}")
	elif text.startswith('.admin'):
		if not event.is_group:await event.edit(A);return
		u=_A
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:u=await get_entity(parts[1].strip())
		if not u:await event.edit('❌ Reply to a user, or: `.admin @username` / `.admin user_id`');return
		try:rights=types.ChatAdminRights(change_info=_C,post_messages=_C,edit_messages=_C,delete_messages=_C,ban_users=_C,invite_users=_C,pin_messages=_C,add_admins=_B,anonymous=_B,manage_call=_C,other=_C);await client(EditAdminRequest(event.chat_id,u.id,rights,'admin'));await event.edit(f"⭐ **{u.first_name or u.id}** promoted to admin.")
		except Exception as e:await event.edit(f"❌ {e}")
	elif text.startswith('.demote'):
		if not event.is_group:await event.edit(A);return
		u=_A
		if event.is_reply:reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		else:
			parts=raw.split(_A,1)
			if len(parts)>1:u=await get_entity(parts[1].strip())
		if not u:await event.edit('❌ Reply to a user, or: `.demote @username` / `.demote user_id`');return
		try:rights=types.ChatAdminRights(change_info=_B,post_messages=_B,edit_messages=_B,delete_messages=_B,ban_users=_B,invite_users=_B,pin_messages=_B,add_admins=_B,anonymous=_B,manage_call=_B,other=_B);await client(EditAdminRequest(event.chat_id,u.id,rights,''));await event.edit(f"⬇️ **{u.first_name or u.id}** demoted (admin rights removed).")
		except Exception as e:await event.edit(f"❌ {e}")
	elif text.startswith('.dm')and not text.startswith('.dmfrwd')and not text.startswith(J):
		content=raw[3:].strip()
		if event.is_reply:
			reply=await event.get_reply_message()
			if content:await client.send_message(reply.sender_id,content);await event.edit('✅ DM sent.')
			else:await event.edit('❌ Provide a message: `.dm message`')
		else:
			parts=content.split(_A,1)
			if len(parts)<2 or not parts[0].startswith('@'):await event.edit('❌ Usage: `.dm @username message`');return
			u=await get_entity(parts[0])
			if u:await client.send_message(u.id,parts[1]);await event.edit(f"✅ DM sent to @{u.username or u.id}")
			else:await event.edit(B)
	elif text.startswith(J)and not text.startswith(K):
		if not event.is_reply:await event.edit(L);return
		replied=await event.get_reply_message();dm_ids=await get_dm_ids();total=len(dm_ids);await event.edit(f"📨 Forwarding to {total} DMs... (anti-ban mode, be patient)");sent,failed=0,0
		for uid in dm_ids:
			try:await client.forward_messages(uid,replied);sent+=1
			except Exception:failed+=1
			await safe_sleep(sent)
		await event.edit(f"✅ Forwarded to **{sent}** DMs. Failed: {failed}")
	elif text.startswith('.gc'):
		if not event.is_reply:await event.edit(M);return
		replied=await event.get_reply_message();await event.edit("🔍 Finding groups where you're admin...");group_ids=await get_admin_group_ids()
		if not group_ids:group_ids=await get_all_group_ids()
		total=len(group_ids);await event.edit(f"📢 Broadcasting to {total} groups (admin mode, anti-ban)...");sent,failed=0,0
		for gid in group_ids:
			try:await client.forward_messages(gid,replied);sent+=1
			except Exception:failed+=1
			await safe_sleep(sent)
		await event.edit(f"✅ Broadcasted to **{sent}** groups. Failed: {failed}")
	elif text.startswith('.broad'):
		if not event.is_reply:await event.edit(M);return
		replied=await event.get_reply_message();dm_ids=await get_dm_ids();total=len(dm_ids);await event.edit(f"📣 Broadcasting to {total} users... (anti-ban mode)");sent,failed=0,0
		for uid in dm_ids:
			try:await client.send_message(uid,replied.text or'');sent+=1
			except Exception:failed+=1
			await safe_sleep(sent)
		await event.edit(f"✅ Broadcasted to **{sent}** users. Failed: {failed}")
	elif text.startswith(K):
		if not event.is_reply:await event.edit(L);return
		replied=await event.get_reply_message();await event.edit('🔍 Collecting targets...');dm_ids=await get_dm_ids();group_ids=await get_admin_group_ids();all_ids=dm_ids+group_ids;total=len(all_ids);await event.edit(f"🚀 Forwarding to {total} targets (anti-ban mode, takes time)...");sent,failed=0,0
		for target_id in all_ids:
			try:await client.forward_messages(target_id,replied);sent+=1
			except Exception:failed+=1
			await safe_sleep(sent)
		await event.edit(f"✅ Done! Forwarded to **{sent}** targets. Failed: {failed}")
	elif text.startswith('.mm'):
		if not event.is_reply:await event.edit('❌ Reply to a user with `.mm`');return
		reply=await event.get_reply_message();u=await client.get_entity(reply.sender_id)
		try:await client(functions.messages.CreateChatRequest(users=[u.id],title="#𝗥𝗔𝗗𝗛𝗘𝗬'S MIDDLEMAN SERVICE"));await event.edit(f"✅ **#𝗥𝗔𝗗𝗛𝗘𝗬'S MIDDLEMAN SERVICE**\nGroup created with `{u.first_name or u.id}`")
		except Exception as e:await event.edit(f"❌ {e}")
	elif text.startswith('.tag'):
		if not event.is_group:await event.edit(A);return
		custom_msg=raw[4:].strip()or'👋';await event.edit('🔍 Collecting members...')
		try:
			participants=await client.get_participants(event.chat_id,limit=50);tags=' '.join([f"[{p.first_name or'user'}](tg://user?id={p.id})"for p in participants if not p.bot and p.id!=(await client.get_me()).id])
			if tags:await client.send_message(event.chat_id,f"{custom_msg}\n{tags}");await event.delete()
			else:await event.edit('❌ No members found.')
		except Exception as e:await event.edit(f"❌ {e}")
	elif text=='.del':
		if not event.is_private:await event.edit('❌ Private chats only.');return
		try:await client(DeleteHistoryRequest(peer=event.chat_id,max_id=0,revoke=_C));msg=await event.respond('🧹 Chat history cleared.');await asyncio.sleep(3);await msg.delete()
		except Exception as e:await event.respond(f"❌ {e}")
	elif text.startswith('.purge'):
		parts=raw.split(_A,1)
		try:n=int(parts[1])
		except Exception:await event.edit('❌ Usage: `.purge N`');return
		msgs=await client.get_messages(event.chat_id,limit=n+1);ids=[m.id for m in msgs]
		try:await client.delete_messages(event.chat_id,ids);conf=await event.respond(f"✅ Purged {n} messages.");await asyncio.sleep(3);await conf.delete()
		except Exception as e:await event.respond(f"❌ {e}")
	elif text.startswith('.close'):
		if not event.is_group:await event.edit(A);return
		parts=raw.split(_A,1)
		try:sec=int(parts[1])
		except Exception:await event.edit('❌ Usage: `.close N`');return
		await event.edit(f"💣 Leaving group in {sec} seconds.");await asyncio.sleep(sec)
		try:await client.delete_dialog(event.chat_id)
		except Exception as e:await event.respond(f"❌ {e}")
	elif text.startswith('.count'):
		parts=raw.split(_A,2)
		try:sec=int(parts[1]);assert 1<=sec<=300
		except Exception:await event.edit('❌ Usage: `.count N` or `.count N message` (1–300)');return
		final_msg=parts[2]if len(parts)>2 else _A;m=await event.edit(f"⏳ **{sec}**s")
		for i in range(sec-1,-1,-1):
			await asyncio.sleep(1)
			try:await m.edit(f"⏳ **{i}**s")
			except Exception:pass
		if final_msg:await m.edit(f"**{final_msg}**")
		else:
			try:await m.delete()
			except Exception:pass
	elif text.startswith('.calc'):
		expr=raw[6:].strip()
		if not expr:await event.edit('❌ Usage: `.calc 2+2` or `.calc sqrt(144)`');return
		try:
			if SYMPY_OK:result=sympy.sympify(expr)
			else:result=eval(expr,{'__builtins__':{}},{})
			await event.edit(f"🧮 `{expr}` = `{result}`")
		except Exception:await event.edit('❌ Invalid expression.')
	elif text.startswith(N)or text.startswith('.translate'):
		cmd_end=3 if text.startswith(N)else 10;rest=raw[cmd_end:].strip()
		if not rest and event.is_reply:await event.edit('❌ Provide target language: `.tr hi` (while replying)');return
		parts=rest.split(_A,1)
		if len(parts)<1:await event.edit('❌ Usage: `.tr hi text` or reply + `.tr hi`');return
		lang=parts[0].lower()
		if len(parts)>=2:content=parts[1]
		elif event.is_reply:reply=await event.get_reply_message();content=reply.text or''
		else:await event.edit('❌ Provide text or reply to a message. Usage: `.tr hi Hello`');return
		if not content.strip():await event.edit('❌ No text to translate.');return
		await event.edit('🌐 Translating...');loop=asyncio.get_event_loop();result=await loop.run_in_executor(_A,_translate,content,lang);await event.edit(result)
	elif text.startswith('.say'):
		content=raw[4:].strip()
		if not content:await event.edit('❌ Usage: `.say hello world`');return
		await event.delete();await client.send_message(event.chat_id,content)
@client.on(events.NewMessage(outgoing=_C))
async def cmd_handler(event):
	if not event.raw_text.strip().startswith('.'):return
	try:await _cmd_dispatch(event)
	except Exception as e1:
		log_error(event.raw_text,e1)
		if auto_fix_active:
			await asyncio.sleep(1.5)
			try:await _cmd_dispatch(event);return
			except Exception as e2:
				log_error(event.raw_text+' [retry]',e2)
				try:await event.respond(f"⚠️ **Auto-fix**: `{event.raw_text}` failed twice.\n`{e2}`\nFull traceback → `.fixlog`")
				except Exception:pass
		else:
			try:await event.respond(f"❌ Error: `{e1}`\n(Enable `.fix` for auto-retry + logging)")
			except Exception:pass
@client.on(events.NewMessage(incoming=_C))
async def incoming_handler(event):
	global muted_users,banned_users;me=await client.get_me()
	if event.sender_id==me.id:return
	if event.sender_id in banned_users or event.sender_id in muted_users:
		try:await event.delete()
		except Exception:pass
async def web_server():
	if not AIOHTTP_OK:print('[WEB] aiohttp not installed — no health endpoint. Run: pip install aiohttp');return
	from aiohttp import web as aw;app=aw.Application();app.router.add_get('/',lambda r:aw.Response(text='✅ Selfbot @sayradhey running!'));app.router.add_get('/health',lambda r:aw.Response(text='OK'));runner=aw.AppRunner(app);await runner.setup();port=int(os.environ.get('PORT',8080));await aw.TCPSite(runner,'0.0.0.0',port).start();print(f"[WEB] Health server running on port {port}")
async def main():await client.start(phone=PHONE);me=await client.get_me();print(f"\n✅  Logged in as: {me.first_name} (@{me.username}) | ID: {me.id}");print('📡  Selfbot by #𝗥𝗔𝗗𝗛𝗘𝗬 — @sayradhey  |  v5.0');print('💬  Type .help in Telegram for full command list\n');await web_server();await client.run_until_disconnected()
if __name__=='__main__':asyncio.run(main())